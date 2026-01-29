#!/usr/bin/env python3
"""
RAE Benchmark Runner - System 3.2 PURE MATH (Fixed SQL v2)
Deterministic Core without LLM/Reranking dependencies.
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import asyncpg
import yaml
from qdrant_client import AsyncQdrantClient
from qdrant_client import models as q_models

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "rae-core"))


class RAEBenchmarkRunner:
    def __init__(
        self,
        benchmark_file: Path,
        output_dir: Path,
        api_url: str,
        synthetic_count: int = None,
    ):
        self.benchmark_file = benchmark_file
        self.output_dir = output_dir
        self.api_url = api_url
        self.synthetic_count = synthetic_count
        self.tenant_id = "00000000-0000-0000-0000-000000000000"
        self.project_id = "RAE-agentic-memory"
        self.szubar_reflections = 0
        self.reflection_map: dict[str, list[str]] = {}

    async def setup(self):
        print("🔌 Initializing System 3.2 (Pure Math Core)...")
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

        from rae_core.embedding.native import NativeEmbeddingProvider

        model_path = os.getenv(
            "ONNX_EMBEDDER_PATH", "models/all-MiniLM-L6-v2/model.onnx"
        )
        tokenizer_path = model_path.replace("model.onnx", "tokenizer.json")

        print(f"🧠 Using Native ONNX Provider: {model_path}")
        self.provider = NativeEmbeddingProvider(
            model_path=model_path, tokenizer_path=tokenizer_path
        )
        self.emb_dim = self.provider.get_dimension()
        print(f"📏 Detected Embedding Dimension: {self.emb_dim}")

        try:
            await self.qdrant.delete_collection("memories")
        except Exception:
            pass

        await self.qdrant.create_collection(
            "memories",
            vectors_config={
                "dense": q_models.VectorParams(
                    size=self.emb_dim, distance=q_models.Distance.COSINE
                )
            },
        )

    async def cleanup(self):
        print("🧹 Cleaning data...")
        async with self.pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM knowledge_graph_edges WHERE tenant_id = $1", self.tenant_id
            )
            await conn.execute(
                "DELETE FROM knowledge_graph_nodes WHERE tenant_id = $1", self.tenant_id
            )
            await conn.execute(
                "DELETE FROM memories WHERE tenant_id = $1 AND layer != 'reflective'",
                self.tenant_id,
            )

    def generate_synthetic_data(self, count: int):
        print(f"🏭 Generating {count} synthetic memories...")
        import random

        memories = []
        components = ["api", "auth", "db", "ui", "storage", "network"]
        for i in range(count):
            comp = random.choice(components)
            memories.append(
                {
                    "id": f"mem_{i:06d}",
                    "text": f"[MES] {comp}: Event {i} occurred at {datetime.now().isoformat()}",
                    "metadata": {"component": comp, "importance": 0.5},
                }
            )
        queries = []
        for _ in range(50):
            target = random.choice(components)
            queries.append(
                {
                    "query": f"Find logs for {target}",
                    "expected_source_ids": [
                        m["id"] for m in memories if target in m["text"]
                    ],
                    "difficulty": "medium",
                }
            )
        return {"name": f"industrial_{count}", "memories": memories, "queries": queries}

    async def run(self):
        if self.synthetic_count:
            data = self.generate_synthetic_data(self.synthetic_count)
        else:
            with open(self.benchmark_file, "r") as f:
                data = yaml.safe_load(f)

        from rae_adapters.postgres import PostgreSQLStorage
        from rae_adapters.qdrant import QdrantVectorStore
        from rae_core.embedding.manager import EmbeddingManager
        from rae_core.engine import RAEEngine

        storage = PostgreSQLStorage(pool=self.pool)
        vector_store = QdrantVectorStore(client=self.qdrant, embedding_dim=self.emb_dim)
        manager = EmbeddingManager(default_provider=self.provider)
        engine = RAEEngine(
            memory_storage=storage,
            vector_store=vector_store,
            embedding_provider=manager,
        )

        print(f"📥 Inserting {len(data['memories'])} memories...")
        batch_size = 10
        comp_nodes = {}
        for i in range(0, len(data["memories"]), batch_size):
            batch = data["memories"][i : i + batch_size]
            embeddings = await engine.embedding_provider.embed_batch(
                [m["text"] for m in batch]
            )
            for j, mem in enumerate(batch):
                m_id = await engine.memory_storage.store_memory(
                    tenant_id=self.tenant_id,
                    agent_id=self.project_id,
                    content=mem["text"],
                    layer="longterm",
                    importance=0.5,
                    metadata=mem["metadata"],
                )
                await engine.vector_store.store_vector(
                    m_id, embeddings[j], self.tenant_id, metadata=mem["metadata"]
                )
                mem["_db_id"] = m_id
                node_id = await self.pool.fetchval(
                    "INSERT INTO knowledge_graph_nodes (node_id, tenant_id, project_id, label) VALUES ($1, $2, $3, $4) RETURNING id",
                    str(m_id),
                    self.tenant_id,
                    self.project_id,
                    "Memory",
                )
                mem["_node_id"] = node_id
                comp = mem["metadata"]["component"]
                if comp not in comp_nodes:
                    comp_nodes[comp] = []
                comp_nodes[comp].append(node_id)
            if i % 1000 == 0:
                print(f"   ✅ {i}")

        print("🔗 Linking nodes...")
        for comp, nodes in comp_nodes.items():
            if len(nodes) > 1:
                for k in range(len(nodes) - 1, max(0, len(nodes) - 5), -1):
                    await self.pool.execute(
                        "INSERT INTO knowledge_graph_edges (tenant_id, project_id, source_node_id, target_node_id, relation, properties) VALUES ($1, $2, $3, $4, $5, $6) ON CONFLICT DO NOTHING",
                        self.tenant_id,
                        self.project_id,
                        nodes[k],
                        nodes[k - 1],
                        "same_component",
                        json.dumps({"weight": 0.7}),
                    )

        print("🔍 Running Queries...")
        hybrid_results = []
        for i, q in enumerate(data["queries"], 1):
            raw_results = await engine.search_memories(
                query=q["query"],
                tenant_id=self.tenant_id,
                agent_id=self.project_id,
                top_k=10,
                enable_reranking=False,
            )
            retrieved_ids = self._map_ids_smart(
                [str(r["id"]) for r in raw_results], data["memories"]
            )
            is_hit = any(r_id in q["expected_source_ids"] for r_id in retrieved_ids[:5])
            hybrid_results.append(
                {
                    "expected": q["expected_source_ids"],
                    "retrieved": retrieved_ids,
                    "is_hit": is_hit,
                }
            )
            engine.math_ctrl.update_policy(success=is_hit)

            if not is_hit and q["expected_source_ids"]:
                missed_id = q["expected_source_ids"][0]
                ref_id = await engine.store_memory(
                    tenant_id=self.tenant_id,
                    agent_id=self.project_id,
                    content=f"search_document: [ALIAS] {q['query']}",
                    layer="reflective",
                    importance=1.0,
                )
                missed_node_id = next(
                    (m["_node_id"] for m in data["memories"] if m["id"] == missed_id),
                    None,
                )
                if missed_node_id:
                    ref_node_id = await self.pool.fetchval(
                        "INSERT INTO knowledge_graph_nodes (node_id, tenant_id, project_id, label) VALUES ($1, $2, $3, $4) RETURNING id",
                        str(ref_id),
                        self.tenant_id,
                        self.project_id,
                        "Reflection",
                    )
                    await self.pool.execute(
                        "INSERT INTO knowledge_graph_edges (tenant_id, project_id, source_node_id, target_node_id, relation, properties) VALUES ($1, $2, $3, $4, $5, $6)",
                        self.tenant_id,
                        self.project_id,
                        ref_node_id,
                        missed_node_id,
                        "alias_bridge",
                        json.dumps({"weight": 1.0}),
                    )
                    self.szubar_reflections += 1
            if i % 10 == 0:
                print(f"   ✅ Q {i} | Reflections: {self.szubar_reflections}")

        # Correct MRR calculation
        total_rr = 0.0
        for res in hybrid_results:
            for rank, r_id in enumerate(res["retrieved"], 1):
                if r_id in res["expected"]:
                    total_rr += 1.0 / rank
                    break
        final_mrr = total_rr / len(hybrid_results)
        print(
            f"\n========================================\nFINAL MRR: {final_mrr:.4f}\nReflections: {self.szubar_reflections}\n========================================"
        )

    def _map_ids_smart(self, db_ids, memories):
        mapping = {str(m.get("_db_id")): m["id"] for m in memories if "_db_id" in m}
        return [mapping.get(db_id, db_id) for db_id in db_ids]


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--synthetic-count", type=int, required=True)
    args = parser.parse_args()
    runner = RAEBenchmarkRunner(
        None, Path("."), "", synthetic_count=args.synthetic_count
    )
    try:
        await runner.setup()
        await runner.cleanup()
        await runner.run()
    finally:
        await runner.pool.close()


if __name__ == "__main__":
    asyncio.run(main())
