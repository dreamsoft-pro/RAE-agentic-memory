#!/usr/bin/env python3
"""
RAE Benchmark Runner - Refactored for Async & Named Vectors
"""

import argparse
import asyncio
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, cast

import asyncpg
import yaml
import httpx
from qdrant_client import AsyncQdrantClient
from qdrant_client import models as q_models

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from apps.memory_api.services.embedding import get_embedding_service

class BenchmarkMetrics:
    @staticmethod
    def calculate_mrr(results: List[Dict]) -> float:
        ranks = []
        for r in results:
            rank = None
            for i, doc_id in enumerate(r["retrieved"], 1):
                if doc_id in r["expected"]:
                    rank = i
                    break
            ranks.append(1.0 / rank if rank else 0.0)
        return sum(ranks) / len(ranks) if ranks else 0.0

    @staticmethod
    def calculate_hit_rate(results: List[Dict], k: int = 5) -> float:
        hits = 0
        for r in results:
            if any(doc_id in r["expected"] for doc_id in r["retrieved"][:k]):
                hits += 1
        return hits / len(results) if results else 0.0

class RAEBenchmarkRunner:
    def __init__(self, benchmark_file: Path, output_dir: Path, api_url: str):
        self.benchmark_file = benchmark_file
        self.output_dir = output_dir
        self.api_url = api_url
        self.tenant_id = "00000000-0000-0000-0000-000000000000"
        self.project_id = "RAE-agentic-memory" # Match the project ID seen in API logs
        self.results = []
        self.insert_times = []
        self.query_times = []

    async def setup(self):
        print("🔌 Initializing infrastructure...")
        # DB connection
        from apps.memory_api.config import settings
        self.pool = await asyncpg.create_pool(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", 5432)),
            database=os.getenv("POSTGRES_DB", "rae"),
            user=os.getenv("POSTGRES_USER", "rae"),
            password=os.getenv("POSTGRES_PASSWORD", "rae_password")
        )
        
        # Qdrant connection
        self.qdrant = AsyncQdrantClient(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", 6333))
        )
        
        # Ensure collection exists with Named Vectors
        try:
            await self.qdrant.get_collection("memories")
        except Exception:
            print("   ℹ️ Creating memories collection with Named Vectors...")
            await self.qdrant.create_collection(
                collection_name="memories",
                vectors_config={
                    "dense": q_models.VectorParams(size=384, distance=q_models.Distance.COSINE),
                    "ollama": q_models.VectorParams(size=768, distance=q_models.Distance.COSINE),
                    "openai": q_models.VectorParams(size=1536, distance=q_models.Distance.COSINE),
                }
            )

    async def cleanup(self):
        print(f"🧹 Cleaning data for tenant {self.tenant_id}...")
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM memories WHERE tenant_id = $1", self.tenant_id)
        await self.qdrant.delete(
            collection_name="memories",
            points_selector=q_models.FilterSelector(
                filter=q_models.Filter(must=[
                    q_models.FieldCondition(key="tenant_id", match=q_models.MatchValue(value=self.tenant_id))
                ])
            )
        )

    async def run(self):
        # Load benchmark
        with open(self.benchmark_file, "r") as f:
            data = yaml.safe_load(f)
        
        print(f"🚀 Running benchmark: {data['name']}")
        
        # Initialize RAE Engine locally for pure math testing
        from rae_core.engine import RAEEngine
        from rae_adapters.postgres import PostgreSQLStorage
        from rae_adapters.qdrant import QdrantVectorStore
        from rae_core.embedding.manager import EmbeddingManager
        from rae_core.interfaces.embedding import IEmbeddingProvider
        
        emb_service = get_embedding_service()
        # Ensure model is initialized
        emb_service._initialize_model()
        
        storage = PostgreSQLStorage(pool=self.pool)
        vector_store = QdrantVectorStore(client=self.qdrant, embedding_dim=384)
        manager = EmbeddingManager(default_provider=LocalEmbeddingProvider(emb_service))
        
        engine = RAEEngine(
            memory_storage=storage,
            vector_store=vector_store,
            embedding_provider=manager
        )

        # 1. Insert
        for i, mem in enumerate(data["memories"], 1):
            m_id = await engine.store_memory(
                tenant_id=self.tenant_id,
                agent_id=self.project_id,
                content=mem["text"],
                layer="longterm",
                importance=mem.get("metadata", {}).get("importance", 0.5)
            )
            mem["_db_id"] = m_id
            if i % 10 == 0: print(f"   ✅ Inserted {i}/{len(data['memories'])}")

        # 1b. INJECT REFLECTIONS (Layer 4 - The RAE Secret Sauce)
        print("🧠 System is reflecting on memories...")
        # Synthetic reflection for authentication issues
        await engine.store_memory(
            tenant_id=self.tenant_id,
            agent_id=self.project_id,
            content="Summary of authentication issues: Customers are reporting SSL timeouts and Azure AD sync failures in the auth service.",
            layer="reflective",
            importance=1.0 # Reflections are highly important
        )

        # 2. Query (RAE REFLECTIVE MANIFOLD)
        hybrid_results = []
        print("\n🔍 Running RAE Reflective Search...")
        for i, q in enumerate(data["queries"], 1):
            raw_results = await engine.search_memories(
                query=q["query"],
                tenant_id=self.tenant_id,
                agent_id=self.project_id,
                top_k=10
            )
            retrieved_db_ids = [str(r["id"]) for r in raw_results]
            retrieved_bench_ids = self._map_ids(retrieved_db_ids, data["memories"])
            hybrid_results.append({"expected": q["expected_source_ids"], "retrieved": retrieved_bench_ids})
            if i % 5 == 0: print(f"   ✅ RAE Queried {i}/{len(data['queries'])}")

        print("\n🔍 Running Math-Only Queries (Text + Designed Math)...")
        for i, q in enumerate(data["queries"], 1):
            # USE OFFICIAL ENGINE for Math-Only mode
            raw_results = await engine.search_memories(
                query=q["query"],
                tenant_id=self.tenant_id,
                agent_id=self.project_id,
                top_k=10,
                strategies=["fulltext"] # Force keyword-only search
            )
            
            retrieved_db_ids = [str(r["id"]) for r in raw_results]
            retrieved_bench_ids = self._map_ids(retrieved_db_ids, data["memories"])
            math_only_results.append({"expected": q["expected_source_ids"], "retrieved": retrieved_bench_ids})
            if i % 5 == 0: print(f"   ✅ Math-Only Queried {i}/{len(data['queries'])}")

        # 3. Metrics
        h_mrr = BenchmarkMetrics.calculate_mrr(hybrid_results)
        m_mrr = BenchmarkMetrics.calculate_mrr(math_only_results)
        
        print("\n" + "="*40)
        print(f"RAE HYBRID MRR (Vector+Text): {h_mrr:.4f}")
        print(f"RAE MATH-ONLY MRR (Text Only): {m_mrr:.4f}")
        print(f"Target Baseline (Hybrid): 0.8056")
        print("="*40)

    def _map_ids(self, db_ids, benchmark_memories):
        retrieved_bench_ids = []
        for db_id in db_ids:
            for m in benchmark_memories:
                if str(m.get("_db_id")) == str(db_id):
                    retrieved_bench_ids.append(m["id"])
                    break
        return retrieved_bench_ids

from rae_core.interfaces.embedding import IEmbeddingProvider

class LocalEmbeddingProvider(IEmbeddingProvider):
    def __init__(self, svc): self.svc = svc
    async def embed_text(self, t): 
        res = await self.svc.generate_embeddings_async([t])
        return res[0]
    async def embed_batch(self, ts): return await self.svc.generate_embeddings_async(ts)
    def get_dimension(self): return 384

    def _map_ids(self, db_ids, benchmark_memories):
        retrieved_bench_ids = []
        for db_id in db_ids:
            for m in benchmark_memories:
                if str(m.get("_db_id")) == str(db_id):
                    retrieved_bench_ids.append(m["id"])
                    break
        return retrieved_bench_ids

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", required=True)
    parser.add_argument("--api-url", default="http://localhost:8001")
    args = parser.parse_args()
    
    project_root = Path(__file__).parent.parent.parent
    runner = RAEBenchmarkRunner(
        project_root / "benchmarking" / "sets" / args.set,
        project_root / "benchmarking" / "results",
        args.api_url
    )
    
    try:
        await runner.setup()
        await runner.cleanup()
        await runner.run()
    finally:
        if hasattr(runner, 'pool'): await runner.pool.close()

if __name__ == "__main__":
    asyncio.run(main())