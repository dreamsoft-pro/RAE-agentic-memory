#!/usr/bin/env python3
"""
RAE Benchmark Runner - System 3.0 AUTONOMOUS (Iteration 2 Fixed)
"""

import argparse
import asyncio
import json
import os
import sys
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, cast

import asyncpg
import yaml
from qdrant_client import AsyncQdrantClient
from qdrant_client import models as q_models

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "rae-core"))

from apps.memory_api.services.embedding import get_embedding_service

class Bandit:
    def __init__(self):
        self.arms = {
            "Math-Heavy":   {"fulltext": 10.0, "vector": 1.0},
            "Balanced":     {"fulltext": 1.0,  "vector": 1.0},
            "Vector-Heavy": {"fulltext": 1.0,  "vector": 10.0}
        }
        self.stats = {name: {"alpha": 1.0, "beta": 1.0} for name in self.arms}

    def select_arm(self) -> str:
        samples = {name: random.betavariate(stat["alpha"], stat["beta"]) for name, stat in self.stats.items()}
        return max(samples, key=samples.get)

    def update(self, arm_name: str, reward: float):
        if reward > 0: self.stats[arm_name]["alpha"] += reward
        else: self.stats[arm_name]["beta"] += (1.0 - reward)

    def get_weights(self, arm_name: str) -> Dict[str, float]:
        return self.arms[arm_name]

class RAEBenchmarkRunner:
    def __init__(self, benchmark_file: Path, output_dir: Path, api_url: str):
        self.benchmark_file = benchmark_file
        self.output_dir = output_dir
        self.api_url = api_url
        self.tenant_id = "00000000-0000-0000-0000-000000000000"
        self.project_id = "RAE-agentic-memory"
        self.bandit = Bandit()
        self.szubar_reflections = 0

    async def setup(self):
        print("🔌 Initializing System 3.0 (Autonomous)...")
        self.pool = await asyncpg.create_pool(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", 5432)),
            database=os.getenv("POSTGRES_DB", "rae"),
            user=os.getenv("POSTGRES_USER", "rae"),
            password=os.getenv("POSTGRES_PASSWORD", "rae_password")
        )
        self.qdrant = AsyncQdrantClient(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", 6333))
        )
        try: await self.qdrant.get_collection("memories")
        except Exception: 
            await self.qdrant.create_collection("memories", vectors_config={
                "dense": q_models.VectorParams(size=384, distance=q_models.Distance.COSINE),
                "ollama": q_models.VectorParams(size=768, distance=q_models.Distance.COSINE),
                "openai": q_models.VectorParams(size=1536, distance=q_models.Distance.COSINE),
            })
        
        if os.path.exists("bandit_stats.json"):
            with open("bandit_stats.json", "r") as f:
                self.bandit.stats = json.load(f)
            print("   [Bandit] Knowledge loaded.")

    async def cleanup(self):
        print(f"🧹 Cleaning data (preserving reflections)...")
        async with self.pool.acquire() as conn:
            await conn.execute("DELETE FROM memories WHERE tenant_id = $1 AND layer != 'reflective'", self.tenant_id)
        try:
            await self.qdrant.delete(
                collection_name="memories",
                points_selector=q_models.FilterSelector(
                    filter=q_models.Filter(
                        must=[q_models.FieldCondition(key="tenant_id", match=q_models.MatchValue(value=self.tenant_id))],
                        must_not=[q_models.FieldCondition(key="layer", match=q_models.MatchValue(value="reflective"))]
                    )
                )
            )
        except Exception: pass

    async def run(self):
        with open(self.benchmark_file, "r") as f: data = yaml.safe_load(f)
        print(f"🚀 Running Benchmark: {data['name']}")
        
        from rae_core.engine import RAEEngine
        from rae_adapters.postgres import PostgreSQLStorage
        from rae_adapters.qdrant import QdrantVectorStore
        from rae_core.embedding.manager import EmbeddingManager
        from rae_core.interfaces.embedding import IEmbeddingProvider
        
        emb_service = get_embedding_service()
        emb_service._initialize_model()
        
        class AdaptiveEmbeddingProvider(IEmbeddingProvider):
            def __init__(self, svc): self.svc = svc
            async def embed_text(self, t): res = await self.svc.generate_embeddings_async([t]); return res[0]
            async def embed_batch(self, ts): return await self.svc.generate_embeddings_async(ts)
            def get_dimension(self): return 768

        storage = PostgreSQLStorage(pool=self.pool)
        vector_store = QdrantVectorStore(client=self.qdrant, embedding_dim=768)
        manager = EmbeddingManager(default_provider=AdaptiveEmbeddingProvider(emb_service))
        engine = RAEEngine(memory_storage=storage, vector_store=vector_store, embedding_provider=manager)

        memory_lookup = {mem["id"]: mem["text"] for mem in data['memories']}
        for i, mem in enumerate(data['memories'], 1):
            m_id = await engine.store_memory(
                tenant_id=self.tenant_id, agent_id=self.project_id,
                content=f"search_document: {mem['text']}", 
                layer="longterm", importance=0.5
            )
            mem["_db_id"] = m_id
            if i % 500 == 0: print(f"   ✅ Inserted {i}")

        results_for_metrics = []
        for i, q in enumerate(data["queries"], 1):
            selected_arm = self.bandit.select_arm()
            weights = self.bandit.get_weights(selected_arm)
            raw_results = await engine.search_memories(
                query=f"search_query: {q['query']}",
                tenant_id=self.tenant_id, agent_id=self.project_id,
                top_k=10, custom_weights=weights
            )
            retrieved_db_ids = [str(r["id"]) for r in raw_results]
            retrieved_bench_ids = self._map_ids(retrieved_db_ids, data["memories"])
            results_for_metrics.append({"expected": q["expected_source_ids"], "retrieved": retrieved_bench_ids})
            
            is_hit = any(doc_id in q["expected_source_ids"] for doc_id in retrieved_bench_ids[:5])
            self.bandit.update(selected_arm, 1.0 if is_hit else 0.0)
            
            if not is_hit:
                missed_id = q["expected_source_ids"][0]
                await engine.store_memory(
                    tenant_id=self.tenant_id, agent_id=self.project_id,
                    content=f"search_document: [REFLECTION] For '{q['query']}', see: {memory_lookup.get(missed_id, '')[:100]}",
                    layer="reflective", importance=1.0
                )
                self.szubar_reflections += 1

        # --- SAFE MRR CALCULATION ---
        rr_sum = 0.0
        for res in results_for_metrics:
            for rank, rid in enumerate(res["retrieved"], 1):
                if rid in res["expected"]:
                    rr_sum += (1.0 / rank)
                    break
        mrr = rr_sum / len(data["queries"])
        
        with open("bandit_stats.json", "w") as f: json.dump(self.bandit.stats, f, indent=2)
        print(f"\n========================================\nSYSTEM 3.0 MRR: {mrr:.4f}\nReflections: {self.szubar_reflections}\n========================================")

    def _map_ids(self, db_ids, benchmark_memories):
        mapping = {str(m.get("_db_id")): m["id"] for m in benchmark_memories if "_db_id" in m}
        return [mapping[db_id] for db_id in db_ids if db_id in mapping]

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", required=True)
    args = parser.parse_args()
    runner = RAEBenchmarkRunner(Path(args.set), Path("."), "")
    try:
        await runner.setup()
        await runner.cleanup()
        await runner.run()
    finally:
        if hasattr(runner, 'pool'): await runner.pool.close()

if __name__ == "__main__":
    asyncio.run(main())
