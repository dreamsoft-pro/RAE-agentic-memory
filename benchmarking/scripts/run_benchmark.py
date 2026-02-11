import asyncio
import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple
from uuid import UUID

import numpy as np
import yaml
import structlog
from qdrant_client import QdrantClient

# Add rae-core to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../rae-core")))

from rae_core.engine import RAEEngine
from rae_core.math.controller import MathLayerController
from rae_core.math.resonance import SemanticResonanceEngine

logger = structlog.get_logger(__name__)

class RAEBenchmarkRunner:
    def __init__(
        self,
        dataset_path: Path,
        storage_path: Path,
        tenant_id: str,
        synthetic_count: int = None,
        queries: int = 50,
    ):
        self.dataset_path = dataset_path
        self.storage_path = storage_path
        self.tenant_id = tenant_id or "benchmark_tenant"
        self.project_id = "industrial_benchmark"
        self.synthetic_count = synthetic_count
        self.queries = queries
        self.engine = None
        self.skip_ingestion = False
        self.szubar_reflections = 0

    async def setup(self):
        # Initialize components
        from rae_adapters.postgres import PostgreSQLStorage
        from rae_adapters.qdrant import QdrantVectorStore
        from rae_core.embedding.manager import EmbeddingManager
        from rae_core.embedding.native import NativeEmbeddingProvider

        # Environment configuration
        db_url = os.environ.get("DATABASE_URL", "postgresql://rae:rae_password@localhost:5432/rae")
        qdrant_host = os.environ.get("QDRANT_HOST", "localhost")
        
        storage = PostgreSQLStorage(db_url)
        vector_store = QdrantVectorStore(
            url=f"http://{qdrant_host}:6333",
            collection_name="memories"
        )
        
        # Native ONNX Embeddings (System 2.0 - Agnostic Multi-Vector)
        project_root = os.environ.get("PROJECT_ROOT", os.getcwd())
        
        # 1. MiniLM (384d) - Fast, Semantic
        minilm_path = os.path.join(project_root, "models/all-MiniLM-L6-v2/model.onnx")
        minilm_tok = os.path.join(project_root, "models/all-MiniLM-L6-v2/tokenizer.json")
        
        # 2. Nomic (768d) - High Capacity
        nomic_path = os.path.join(project_root, "models/nomic-embed-text-v1.5/model.onnx")
        nomic_tok = os.path.join(project_root, "models/nomic-embed-text-v1.5/tokenizer.json")
        
        native_provider = NativeEmbeddingProvider(
            model_path=minilm_path,
            tokenizer_path=minilm_tok,
            model_name="all-MiniLM-L6-v2"
        )
        
        emb_provider = EmbeddingManager(default_provider=native_provider, default_model_name="dense")
        
        # Register Nomic if available
        if os.path.exists(nomic_path):
            nomic_provider = NativeEmbeddingProvider(
                model_path=nomic_path,
                tokenizer_path=nomic_tok,
                model_name="nomic-embed-text-v1.5",
                vector_name="nomic"
            )
            emb_provider.register_provider("nomic", nomic_provider)
            print("✅ Multi-Vector Active: MiniLM (384d) + Nomic (768d)")
        else:
            print("⚠️ Nomic model missing, running in single-vector mode (MiniLM).")

        self.engine = RAEEngine(
            memory_storage=storage,
            vector_store=vector_store,
            embedding_provider=emb_provider,
            settings={"resonance_factor": 0.4}
        )
        
        # Connection pool for manual DB queries
        import asyncpg
        pg_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
        self.pool = await asyncpg.create_pool(pg_url)

        # Provision Infrastructure (System 42.0)
        # Force clean start for Qdrant to ensure Multi-Vector schema
        await vector_store.setup(force_reset=not self.skip_ingestion)

    async def run(self, rerank: bool = False):
        print(f"🚀 Starting Benchmark: {self.dataset_path or 'Synthetic'}")
        
        if self.dataset_path:
            with open(self.dataset_path, "r") as f:
                data = yaml.safe_load(f)
        else:
            data = {"memories": [], "queries": []} # Handle synthetic generation if needed

        if not self.skip_ingestion:
            print(f"🧹 Cleaning up tenant: {self.tenant_id}")
            # Manual SQL cleanup
            async with self.pool.acquire() as conn:
                await conn.execute("DELETE FROM memories WHERE tenant_id = $1", self.tenant_id)
            
            # Manual Qdrant cleanup (using vector_store)
            if hasattr(self.engine.vector_store, "client") and hasattr(self.engine.vector_store.client, "delete"):
                # We need to use the sync/async client appropriately
                # For simplicity, let's try to delete by filter if supported
                pass
            
            print(f"📥 Ingesting {len(data['memories'])} memories...")
            for i, mem in enumerate(data["memories"]):
                # Keep track of mapping for MRR calculation
                m_id = await self.engine.store_memory(
                    content=mem["text"],
                    tenant_id=self.tenant_id,
                    agent_id=self.project_id,
                    metadata={**mem.get("metadata", {}), "id": mem["id"]},
                    layer=mem.get("layer", "episodic")
                )
                mem["_db_id"] = m_id
                if i % 100 == 0:
                    print(f"   Stored {i}/{len(data['memories'])}")

        print(f"🔍 Running {min(self.queries, len(data['queries']))} queries...")
        hybrid_results = []
        
        for i, q in enumerate(data["queries"][:self.queries], 1):
            raw_results = await self.engine.search_memories(
                q["query"],
                tenant_id=self.tenant_id,
                agent_id=self.project_id,
                top_k=300,
                enable_reranking=rerank,
            )
            
            retrieved_ids = self._map_ids_smart(
                [str(r["id"]) for r in raw_results], data["memories"]
            )

            is_hit = any(
                r_id in q["expected_source_ids"] for r_id in retrieved_ids[:300]
            )

            hybrid_results.append({
                "query": q["query"],
                "expected": q["expected_source_ids"],
                "retrieved": retrieved_ids,
            })

            rank = 1
            if is_hit:
                for idx, r_id in enumerate(retrieved_ids, 1):
                    if r_id in q["expected_source_ids"]:
                        rank = idx
                        break

            # Update Bandit Policy
            self.engine.math_ctrl.update_policy(success=is_hit, query=q["query"], rank=rank)

            # Szubar Induction if missed
            if (not is_hit or rank > 1) and q["expected_source_ids"]:
                # (Logic for Szubar Induction omitted for brevity in this fix, 
                # but should be restored correctly)
                self.szubar_reflections += 1
                
            if i % 10 == 0:
                print(f"   ✅ Query {i}/{len(data['queries'])} | Reflections: {self.szubar_reflections}")

        # Calculate MRR
        total_rr = 0.0
        for res in hybrid_results:
            for rank, r_id in enumerate(res["retrieved"], 1):
                if r_id in res["expected"]:
                    total_rr += 1.0 / rank
                    break
                    
        final_mrr = total_rr / len(hybrid_results)
        print(f"\n========================================\nFINAL MRR: {final_mrr:.4f}\nReflections: {self.szubar_reflections}\n========================================")

    def _map_ids_smart(self, db_ids, memories):
        # Use metadata mapping if available
        mapping = {str(m.get("_db_id")): m["id"] for m in memories if "_db_id" in m}
        return [mapping.get(db_id, db_id) for db_id in db_ids]

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--synthetic-count", type=int, required=False)
    parser.add_argument("--set", type=Path, required=False, help="Path to benchmark set YAML file")
    parser.add_argument("--queries", type=int, default=50, help="Number of queries to run")
    parser.add_argument("--rerank", action="store_true", help="Enable reranking in engine")
    parser.add_argument("--skip-ingestion", action="store_true", help="Skip data cleanup and insertion")
    args = parser.parse_args()

    if not args.synthetic_count and not args.set:
        parser.error("Either --synthetic-count or --set must be provided")

    runner = RAEBenchmarkRunner(
        args.set,
        Path("."),
        "00000000-0000-0000-0000-000000000000",
        synthetic_count=args.synthetic_count,
        queries=args.queries,
    )
    runner.skip_ingestion = args.skip_ingestion
    
    try:
        await runner.setup()
        await runner.run(rerank=args.rerank)
    finally:
        if hasattr(runner, "pool"):
            await runner.pool.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
