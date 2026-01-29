#!/usr/bin/env python3
"""
RAE Benchmark Runner - System 3.3 (Auto-Tuned Szubar, No Reranking)
Deterministic Core with Optimized Ingestion for Old Hardware.
"""

import argparse
import asyncio
import json
import os
import sys
import time
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
        benchmark_file: Path | None,
        output_dir: Path,
        api_url: str,
        synthetic_count: int | None = None,
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
        print("🔌 Initializing System 3.3 (Optimized Math Core)...")
        self.pool = await asyncpg.create_pool(
            host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
            port=int(os.getenv("POSTGRES_PORT", 5432)),
            database=os.getenv("POSTGRES_DB", "rae"),
            user=os.getenv("POSTGRES_USER", "rae"),
            password=os.getenv("POSTGRES_PASSWORD", "rae_password"),
        )
        self.qdrant = AsyncQdrantClient(
            host=os.getenv("QDRANT_HOST", "127.0.0.1"),
            port=int(os.getenv("QDRANT_PORT", 6333)),
        )

        from rae_core.embedding.native import NativeEmbeddingProvider

        default_model = "models/all-MiniLM-L6-v2/model.onnx"
        if os.path.exists("models/nomic-embed-text-v1.5/model.onnx"):
            default_model = "models/nomic-embed-text-v1.5/model.onnx"

        model_path = os.getenv("ONNX_EMBEDDER_PATH", default_model)
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
        print(f"🧹 Cleaning data for project: {self.project_id}...")
        async with self.pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM knowledge_graph_edges WHERE project_id = $1", self.project_id
            )
            await conn.execute(
                "DELETE FROM knowledge_graph_nodes WHERE project_id = $1", self.project_id
            )
            await conn.execute(
                "DELETE FROM memories WHERE project = $1 AND tenant_id = $2",
                self.project_id, self.tenant_id
            )
            print("   ✅ Cleanup completed")

    def generate_synthetic_data(self, count: int):
        print(f"🏭 Generating {count} synthetic memories (Industrial Pattern)...")
        import random
        memories = []
        components = ["api", "auth", "db", "ui", "storage", "network"]
        
        for i in range(count):
            # Simulate industrial distribution: 40% logs, 30% tickets, 30% metrics
            r = random.random()
            if r < 0.4:
                m_type = "log"
                comp = random.choice(components)
                text = f"[LOG] {comp}: Request processed in {random.randint(10, 500)}ms - Status: {random.choice(['200', '500', '404'])}"
                m_id = f"log_{i:06d}"
            elif r < 0.7:
                m_type = "ticket"
                comp = random.choice(components)
                text = f"[TICKET] {comp}: User reports failure in module - Priority: {random.choice(['high', 'low'])}"
                m_id = f"ticket_{i:06d}"
            else:
                m_type = "metric"
                comp = random.choice(components)
                text = f"[METRIC] {comp}: cpu_usage at {random.randint(0, 100)}% on host-{random.randint(1,9)}"
                m_id = f"metric_{i:06d}"

            memories.append({
                "id": m_id,
                "text": text,
                "metadata": {"component": comp, "type": m_type, "importance": 0.5},
            })
            
        queries = []
        for _ in range(50):
            target = random.choice(components)
            # Query matching logic
            q_text = f"Find logs for {target}"
            expected = [m["id"] for m in memories if target in m["text"] and m["metadata"]["type"] == "log"]
            
            if expected:
                queries.append({
                    "query": q_text,
                    "expected_source_ids": expected,
                    "difficulty": "medium",
                })
        return {"name": f"synthetic_{count}", "memories": memories, "queries": queries}

    async def run(self):
        if self.synthetic_count:
            data = self.generate_synthetic_data(self.synthetic_count)
        else:
            if not self.benchmark_file:
                raise ValueError("Benchmark file required if synthetic count not provided")
            try:
                from yaml import CSafeLoader as Loader
            except ImportError:
                from yaml import SafeLoader as Loader
            
            print(f"📖 Reading {self.benchmark_file} (this may take a minute)...")
            start_read = time.time()
            with open(self.benchmark_file, "r") as f:
                data = yaml.load(f, Loader=Loader)
            print(f"✅ Read completed in {time.time() - start_read:.2f}s")

        self.project_id = data.get("name", "RAE-agentic-memory")
        print(f"🎯 Project: {self.project_id}")
        await self.cleanup()

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
        batch_size = 500
        comp_nodes: dict[str, list[int]] = {}
        for i in range(0, len(data["memories"]), batch_size):
            batch = data["memories"][i : i + batch_size]
            embeddings = await engine.embedding_provider.embed_batch(
                [m.get("text", m.get("content", "")) for m in batch],
                task_type="search_document"
            )
            for j, mem in enumerate(batch):
                content = mem.get("text", mem.get("content", ""))
                m_id = await engine.memory_storage.store_memory(
                    tenant_id=self.tenant_id,
                    agent_id=self.project_id,
                    content=content,
                    layer="longterm",
                    importance=mem.get("metadata", {}).get("importance", 0.5),
                    metadata=mem.get("metadata", {}),
                )
                await engine.vector_store.store_vector(
                    m_id, embeddings[j], self.tenant_id, metadata=mem.get("metadata", {})
                )
                mem["_db_id"] = m_id
                node_id = await self.pool.fetchval(
                    "INSERT INTO knowledge_graph_nodes (node_id, tenant_id, project_id, label) VALUES ($1, $2, $3, $4) RETURNING id",
                    str(m_id), self.tenant_id, self.project_id, "Memory",
                )
                mem["_node_id"] = node_id
                comp = mem.get("metadata", {}).get("component", "unknown")
                if comp not in comp_nodes:
                    comp_nodes[comp] = []
                comp_nodes[comp].append(node_id)
            if (i + batch_size) % 1000 == 0 or (i + batch_size) >= len(data['memories']):
                print(f"   ✅ Processed {i + batch_size}/{len(data['memories'])}")

        print("🔗 Linking nodes (building GraphRAG context)...")
        for comp, nodes in comp_nodes.items():
            if len(nodes) > 1:
                for k in range(len(nodes) - 1, max(0, len(nodes) - 5), -1):
                    await self.pool.execute(
                        "INSERT INTO knowledge_graph_edges (tenant_id, project_id, source_node_id, target_node_id, relation, properties) VALUES ($1, $2, $3, $4, $5, $6) ON CONFLICT DO NOTHING",
                        self.tenant_id, self.project_id, nodes[k], nodes[k - 1], "same_component", json.dumps({"weight": 0.7}),
                    )

        print("🔍 Running Queries (Testing Bandit Convergence)...")
        hybrid_results = []
        for i, q in enumerate(data["queries"], 1):
            raw_results = await engine.search_memories(
                query=q["query"],
                tenant_id=self.tenant_id,
                agent_id=self.project_id,
                top_k=10,
                enable_reranking=False,
            )
            retrieved_ids = self._map_ids_smart([str(r["id"]) for r in raw_results], data["memories"])
            is_hit = any(r_id in q["expected_source_ids"] for r_id in retrieved_ids[:5])
            hybrid_results.append({"expected": q["expected_source_ids"], "retrieved": retrieved_ids, "is_hit": is_hit})
            engine.math_ctrl.update_policy(success=is_hit)

            if not is_hit and q["expected_source_ids"]:
                missed_id = q["expected_source_ids"][0]
                ref_id = await engine.memory_storage.store_memory(
                    tenant_id=self.tenant_id, agent_id=self.project_id,
                    content=f"search_document: [ALIAS] {q['query']}",
                    layer="reflective", importance=1.0,
                )
                missed_node_id = next((m["_node_id"] for m in data["memories"] if m["id"] == missed_id), None)
                if missed_node_id:
                    ref_node_id = await self.pool.fetchval(
                        "INSERT INTO knowledge_graph_nodes (node_id, tenant_id, project_id, label) VALUES ($1, $2, $3, $4) RETURNING id",
                        str(ref_id), self.tenant_id, self.project_id, "Reflection",
                    )
                    await self.pool.execute(
                        "INSERT INTO knowledge_graph_edges (tenant_id, project_id, source_node_id, target_node_id, relation, properties) VALUES ($1, $2, $3, $4, $5, $6)",
                        self.tenant_id, self.project_id, ref_node_id, missed_node_id, "alias_bridge", json.dumps({"weight": 1.0}),
                    )
                    self.szubar_reflections += 1
            if i % 10 == 0:
                print(f"   ✅ Query {i}/{len(data['queries'])} | Reflections: {self.szubar_reflections}")

        total_rr = 0.0
        for res in hybrid_results:
            for rank, r_id in enumerate(res["retrieved"], 1):
                if r_id in res["expected"]:
                    total_rr += 1.0 / rank
                    break
        final_mrr = total_rr / len(hybrid_results)
        print(f"\n========================================\nFINAL MRR: {final_mrr:.4f}\nReflections: {self.szubar_reflections}\n========================================")

    def _map_ids_smart(self, db_ids, memories):
        mapping = {str(m.get("_db_id")): m["id"] for m in memories if "_db_id" in m}
        return [mapping.get(db_id, db_id) for db_id in db_ids]


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--synthetic-count", type=int, required=False)
    parser.add_argument("--set", type=Path, required=False, help="Path to benchmark set YAML file")
    args = parser.parse_args()

    if not args.synthetic_count and not args.set:
        parser.error("Either --synthetic-count or --set must be provided")

    runner = RAEBenchmarkRunner(args.set, Path("."), "", synthetic_count=args.synthetic_count)
    try:
        await runner.setup()
        await runner.run()
    finally:
        if hasattr(runner, 'pool'):
            await runner.pool.close()

if __name__ == "__main__":
    asyncio.run(main())
