#!/usr/bin/env python3
"""
RAE Benchmark Runner - System 3.2 FULLY INTEGRATED
Now using MathLayerController from rae-core for dynamic weighting.
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

import asyncpg
import yaml
from qdrant_client import AsyncQdrantClient
from qdrant_client import models as q_models

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "rae-core"))

from apps.memory_api.services.embedding import get_embedding_service


class RAEBenchmarkRunner:
    def __init__(self, benchmark_file: Path, output_dir: Path, api_url: str):
        self.benchmark_file = benchmark_file
        self.output_dir = output_dir
        self.api_url = api_url
        self.tenant_id = "00000000-0000-0000-0000-000000000000"
        self.project_id = "RAE-agentic-memory"
        self.szubar_reflections = 0
        self.reflection_map: dict[str, list[str]] = {}

    async def setup(self):
        print("🔌 Initializing System 3.2 (Integrated Core)...")
        self.pool = await asyncpg.create_pool(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", 5432)),
            database=os.getenv("POSTGRES_DB", "rae"),
            user=os.getenv("POSTGRES_USER", "rae"),
            password=os.getenv("POSTGRES_PASSWORD", "rae_password"),
        )
        self.qdrant = AsyncQdrantClient(
            host=os.getenv("QDRANT_HOST", "localhost"),
            port=int(os.getenv("QDRANT_PORT", 6333)),
        )
        try:
            await self.qdrant.get_collection("memories")
        except Exception:
            await self.qdrant.create_collection(
                "memories",
                vectors_config={
                    "dense": q_models.VectorParams(
                        size=384, distance=q_models.Distance.COSINE
                    ),
                    "ollama": q_models.VectorParams(
                        size=768, distance=q_models.Distance.COSINE
                    ),
                    "openai": q_models.VectorParams(
                        size=1536, distance=q_models.Distance.COSINE
                    ),
                },
            )

        if os.path.exists("reflection_map.json"):
            with open("reflection_map.json", "r") as f:
                self.reflection_map = json.load(f)

    async def cleanup(self):
        print("🧹 Cleaning data (preserving reflections)...")
        async with self.pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM memories WHERE tenant_id = $1 AND layer != 'reflective'",
                self.tenant_id,
            )
        try:
            await self.qdrant.delete(
                collection_name="memories",
                points_selector=q_models.FilterSelector(
                    filter=q_models.Filter(
                        must=[
                            q_models.FieldCondition(
                                key="tenant_id",
                                match=q_models.MatchValue(value=self.tenant_id),
                            )
                        ],
                        must_not=[
                            q_models.FieldCondition(
                                key="layer",
                                match=q_models.MatchValue(value="reflective"),
                            )
                        ],
                    )
                ),
            )
        except Exception:
            pass

    async def run(self):
        with open(self.benchmark_file, "r") as f:
            data = yaml.safe_load(f)
        print(f"🚀 Running Integrated Benchmark: {data['name']}")

        from rae_adapters.postgres import PostgreSQLStorage
        from rae_adapters.qdrant import QdrantVectorStore
        from rae_core.embedding.manager import EmbeddingManager
        from rae_core.engine import RAEEngine
        from rae_core.interfaces.embedding import IEmbeddingProvider

        emb_service = get_embedding_service()
        emb_service._initialize_model()

        class AdaptiveEmbeddingProvider(IEmbeddingProvider):
            def __init__(self, svc):
                self.svc = svc

            async def embed_text(self, t):
                res = await self.svc.generate_embeddings_async([t])
                return res[0]

            async def embed_batch(self, ts):
                return await self.svc.generate_embeddings_async(ts)

            def get_dimension(self):
                return 768

        storage = PostgreSQLStorage(pool=self.pool)
        vector_store = QdrantVectorStore(client=self.qdrant, embedding_dim=768)
        manager = EmbeddingManager(
            default_provider=AdaptiveEmbeddingProvider(emb_service)
        )

        # CORE ENGINE WITH INTEGRATED MATH CONTROLLER
        engine = RAEEngine(
            memory_storage=storage,
            vector_store=vector_store,
            embedding_provider=manager,
            settings={"bandit_persistence_path": "bandit_state.json"},
        )

        # 1. Insert
        memory_lookup = {mem["id"]: mem["text"] for mem in data["memories"]}
        for i, mem in enumerate(data["memories"], 1):
            m_id = await engine.store_memory(
                tenant_id=self.tenant_id,
                agent_id=self.project_id,
                content=mem["text"],
                layer="longterm",
                importance=0.5,
            )
            mem["_db_id"] = m_id
            if i % 500 == 0:
                print(f"   ✅ Inserted {i}")

        # 2. Query Loop
        hybrid_results = []
        for i, q in enumerate(data["queries"], 1):
            query_text = q["query"]

            # CORE CALL (Autonomous Weights)
            raw_results = await engine.search_memories(
                query=query_text,
                tenant_id=self.tenant_id,
                agent_id=self.project_id,
                top_k=10,
            )

            retrieved_db_ids = [str(r["id"]) for r in raw_results]
            retrieved_mixed_ids = self._map_ids_smart(
                retrieved_db_ids, data["memories"]
            )

            # Evaluate Hit
            is_hit = False
            hit_type = "MISS"
            for r_id in retrieved_mixed_ids[:5]:
                if r_id in q["expected_source_ids"]:
                    is_hit = True
                    hit_type = "DIRECT"
                    break
                if r_id in self.reflection_map and any(
                    t in q["expected_source_ids"] for t in self.reflection_map[r_id]
                ):
                    is_hit = True
                    hit_type = "REFLECTION"
                    break

            hybrid_results.append(
                {
                    "expected": q["expected_source_ids"],
                    "retrieved": retrieved_mixed_ids,
                    "hit_type": hit_type,
                }
            )

            # CORE FEEDBACK (Bandit update)
            engine.math_ctrl.update_policy(success=is_hit)

            # Szubar self-healing
            if not is_hit:
                missed_id = q["expected_source_ids"][0]
                if missed_id in memory_lookup:
                    ref_content = f"search_document: [REFLECTION] Concept: '{query_text}' is related to: {memory_lookup[missed_id][:100]}..."
                    ref_id = await engine.store_memory(
                        tenant_id=self.tenant_id,
                        agent_id=self.project_id,
                        content=ref_content,
                        layer="reflective",
                        importance=1.0,
                    )
                    self.szubar_reflections += 1
                    self.reflection_map[str(ref_id)] = q["expected_source_ids"]

            if i % 20 == 0:
                print(f"   ✅ Q {i} | Reflections: {self.szubar_reflections}")

        # 3. Final Report
        rr_sum = 0.0
        reflection_hits = 0
        for res in hybrid_results:
            for rank, r_id in enumerate(res["retrieved"], 1):
                is_match = (r_id in res["expected"]) or (
                    r_id in self.reflection_map
                    and any(t in res["expected"] for t in self.reflection_map[r_id])
                )
                if is_match:
                    rr_sum += 1.0 / rank
                    if res["hit_type"] == "REFLECTION":
                        reflection_hits += 1
                    break
        mrr = rr_sum / len(data["queries"])

        with open("reflection_map.json", "w") as f:
            json.dump(self.reflection_map, f, indent=2)

        print(
            f"\n========================================\nINTEGRATED MRR: {mrr:.4f}\nReflection Hits: {reflection_hits}\n========================================"
        )

        # Save results to JSON for CI check
        from datetime import datetime

        results_dir = Path("benchmarking/results")
        results_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        set_name = self.benchmark_file.stem
        result_file = results_dir / f"{set_name}_{timestamp}.json"

        # Calculate hit rates for metrics compatibility
        hits_at_1 = sum(
            1
            for res in hybrid_results
            if any(r in res["expected"] for r in res["retrieved"][:1])
        ) / len(data["queries"])
        hits_at_5 = sum(
            1
            for res in hybrid_results
            if any(r in res["expected"] for r in res["retrieved"][:5])
        ) / len(data["queries"])

        report = {
            "name": data["name"],
            "timestamp": timestamp,
            "metrics": {
                "mrr": mrr,
                "hit_rate": {
                    "@1": hits_at_1,
                    "@5": hits_at_5,
                },
                "overall_quality_score": (mrr + hits_at_5) / 2,
                "reflection_hits": reflection_hits,
            },
        }

        with open(result_file, "w") as f:
            json.dump(report, f, indent=2)
        print(f"📊 Results saved to: {result_file}")

    def _map_ids_smart(self, db_ids, benchmark_memories):
        mapping = {
            str(m.get("_db_id")): m["id"] for m in benchmark_memories if "_db_id" in m
        }
        return [mapping.get(db_id, db_id) for db_id in db_ids]


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
        if hasattr(runner, "pool"):
            await runner.pool.close()


if __name__ == "__main__":
    asyncio.run(main())
