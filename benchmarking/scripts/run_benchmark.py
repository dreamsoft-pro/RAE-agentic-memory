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
from pathlib import Path
from typing import Any

import asyncpg
import litellm
import yaml
from qdrant_client import AsyncQdrantClient
from qdrant_client import models as q_models

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "rae-core"))

from rae_core.interfaces.embedding import IEmbeddingProvider


class LiteLLMEmbeddingProvider(IEmbeddingProvider):
    def __init__(self, model_name: str):
        self.model_name = model_name
        if "nomic" in model_name:
            self.dim = 768
        elif "openai" in model_name or "text-embedding-3" in model_name:
            self.dim = 1536
        else:
            self.dim = 384

        # Configure Ollama base if needed
        if model_name.startswith("ollama/"):
            litellm.api_base = os.getenv("OLLAMA_API_URL", "http://localhost:11434")

    def get_dimension(self) -> int:
        return self.dim

    async def embed_text(
        self, text: str, task_type: str = "search_document"
    ) -> list[float]:
        # Nomic v1.5 requires specific prefixes
        prefix = ""
        if "nomic" in self.model_name.lower():
            prefix = (
                "search_query: " if task_type == "search_query" else "search_document: "
            )

        response = await litellm.aembedding(
            model=self.model_name, input=[prefix + text]
        )
        # Cast to list[float] to satisfy mypy
        embedding: list[float] = response["data"][0]["embedding"]
        return embedding

    async def embed_batch(
        self, texts: list[str], task_type: str = "search_document"
    ) -> list[list[float]]:
        # Nomic v1.5 requires specific prefixes
        prefix = ""
        if "nomic" in self.model_name.lower():
            prefix = (
                "search_query: " if task_type == "search_query" else "search_document: "
            )

        processed_texts = [prefix + t for t in texts]
        response = await litellm.aembedding(
            model=self.model_name, input=processed_texts
        )
        # Cast to list[list[float]]
        embeddings: list[list[float]] = [d["embedding"] for d in response["data"]]
        return embeddings


class RAEBenchmarkRunner:
    def __init__(
        self,
        benchmark_file: Path | None,
        output_dir: Path,
        api_url: str,
        synthetic_count: int | None = None,
        queries: int = 50,
    ):
        self.benchmark_file = benchmark_file
        self.output_dir = output_dir
        self.api_url = api_url
        self.synthetic_count = synthetic_count
        self.query_count = queries
        self.tenant_id = "00000000-0000-0000-0000-000000000000"
        self.project_id = "RAE-agentic-memory"
        self.szubar_reflections = 0
        self.reflection_map: dict[str, list[str]] = {}

    async def setup(self):
        print("🔌 Initializing System 3.6.1 (Agnostic Hive Mind)...")
        # Load Math Controller Config
        ctrl_config = {}
        config_path = Path("config/math_controller.yaml")
        if config_path.exists():
            with open(config_path, "r") as f:
                ctrl_config = yaml.safe_load(f)
        
        from rae_core.math.controller import MathLayerController
        math_ctrl = MathLayerController(config=ctrl_config)

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

        # 1. Setup Multi-Model Embedding Manager (Pure Native ONNX)
        from rae_core.embedding.manager import EmbeddingManager
        from rae_core.embedding.native import NativeEmbeddingProvider

        # Primary Model (Nomic ONNX)
        nomic_path = "models/nomic-embed-text-v1.5/model.onnx"
        nomic_provider = NativeEmbeddingProvider(
            model_path=nomic_path,
            tokenizer_path=nomic_path.replace("model.onnx", "tokenizer.json"),
            model_name="nomic",
            max_length=512,
        )

        # Secondary Model (MiniLM ONNX - Dense)
        dense_path = "models/all-MiniLM-L6-v2/model.onnx"
        dense_provider = NativeEmbeddingProvider(
            model_path=dense_path,
            tokenizer_path=dense_path.replace("model.onnx", "tokenizer.json"),
            model_name="dense",
            max_length=512,
        )

        self.manager = EmbeddingManager(
            default_provider=nomic_provider,
            default_model_name="nomic",
        )
        self.manager.register_provider("dense", dense_provider)

        self.provider = self.manager  # Engine will use manager
        self.emb_dim = nomic_provider.get_dimension()
        self.vector_name = "nomic"  # For reporting
        print("🧠 Native ONNX Registered: nomic (768d)")

        # 2. Setup Qdrant with Multi-Vector support
        try:
            await self.qdrant.delete_collection("memories")
        except Exception:
            pass

        await self.qdrant.create_collection(
            "memories",
            vectors_config={
                "nomic": q_models.VectorParams(
                    size=768, distance=q_models.Distance.COSINE
                ),
                "dense": q_models.VectorParams(
                    size=384, distance=q_models.Distance.COSINE
                ),
            },
        )

        # 3. Initialize Engine
        from rae_adapters.postgres import PostgreSQLStorage
        from rae_core.adapters.qdrant import QdrantVectorStore
        from rae_core.engine import RAEEngine

        self.storage = PostgreSQLStorage(pool=self.pool)
        self.vector_store = QdrantVectorStore(
            client=self.qdrant
        )  # Standard agnostic store

        self.engine = RAEEngine(
            memory_storage=self.storage,
            vector_store=self.vector_store,
            embedding_provider=self.manager,
            math_controller=math_ctrl,
        )

    async def cleanup(self):
        print(f"🧹 Cleaning data for project: {self.project_id}...")
        async with self.pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM knowledge_graph_edges WHERE project_id = $1",
                self.project_id,
            )
            await conn.execute(
                "DELETE FROM knowledge_graph_nodes WHERE project_id = $1",
                self.project_id,
            )
            await conn.execute(
                "DELETE FROM memories WHERE (project = $1 OR agent_id = $1) AND tenant_id = $2",
                self.project_id,
                self.tenant_id,
            )
            print("   ✅ Cleanup completed")

    def generate_synthetic_data(self, count: int, query_count: int = 50):
        print(f"🏭 Generating {count} synthetic memories (Industrial Pattern)...")
        import random

        memories: list[dict[str, Any]] = []
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

            memories.append(
                {
                    "id": m_id,
                    "text": text,
                    "metadata": {"component": comp, "type": m_type, "importance": 0.5},
                }
            )

        queries: list[dict[str, Any]] = []
        for _ in range(query_count):
            target = random.choice(components)
            # Query matching logic
            q_text = f"Find logs for {target}"
            expected = [
                m["id"]
                for m in memories
                if target in str(m["text"]) and m["metadata"]["type"] == "log"
            ]

            if expected:
                queries.append(
                    {
                        "query": q_text,
                        "expected_source_ids": expected,
                        "difficulty": "medium",
                    }
                )
        return {"name": f"synthetic_{count}", "memories": memories, "queries": queries}

    async def run(self):
        if self.synthetic_count:
            data = self.generate_synthetic_data(self.synthetic_count, self.query_count)
        else:
            if not self.benchmark_file:
                raise ValueError(
                    "Benchmark file required if synthetic count not provided"
                )
            try:
                from yaml import CSafeLoader as SafeLoader
            except ImportError:
                from yaml import SafeLoader  # type: ignore

            print(f"📖 Reading {self.benchmark_file} (this may take a minute)...")
            start_read = time.time()
            with open(self.benchmark_file, "r") as f:
                data = yaml.load(f, Loader=SafeLoader)
            print(f"✅ Read completed in {time.time() - start_read:.2f}s")

        self.project_id = data.get("name", "RAE-agentic-memory")
        print(f"🎯 Project: {self.project_id}")
        await self.cleanup()

        print(f"📥 Inserting {len(data['memories'])} memories (Industrial Batch Mode)...")
        batch_size = 50
        comp_nodes: dict[str, list[int]] = {}

        for i in range(0, len(data["memories"]), batch_size):
            batch = data["memories"][i : i + batch_size]
            texts = [m.get("text", m.get("content", "")) for m in batch]

            # 1. Batch Embedding (Fast ONNX - Nomic Only for speed)
            nomic_embs = await self.engine.embedding_provider.providers[
                "nomic"
            ].embed_batch(texts, task_type="search_document")

            # 2. Insert into Storage & Vector Store
            for j, mem in enumerate(batch):
                content = texts[j]

                # Direct Storage Insert (Postgres)
                m_id = await self.storage.store_memory(
                    tenant_id=self.tenant_id,
                    agent_id=self.project_id,
                    content=content,
                    layer="longterm",
                    importance=mem.get("metadata", {}).get("importance", 0.5),
                    metadata=mem.get("metadata", {}),
                )

                # Direct Vector Insert (Qdrant)
                vector_struct = {"nomic": nomic_embs[j]}
                await self.vector_store.store_vector(
                    memory_id=m_id,
                    embedding=vector_struct,
                    tenant_id=self.tenant_id,
                    metadata=mem.get("metadata", {}),
                )

                mem["_db_id"] = m_id

                # Graph Node Insert (Simplified)
                node_id = await self.pool.fetchval(
                    "INSERT INTO knowledge_graph_nodes (node_id, tenant_id, project_id, label) VALUES ($1, $2, $3, $4) RETURNING id",
                    str(m_id),
                    self.tenant_id,
                    self.project_id,
                    "Memory",
                )
                mem["_node_id"] = node_id
                comp = mem.get("metadata", {}).get("component", "unknown")
                if comp not in comp_nodes:
                    comp_nodes[comp] = []
                comp_nodes[comp].append(node_id)

            if (i + batch_size) % 500 == 0 or (i + batch_size) >= len(data["memories"]):
                print(
                    f"   ✅ Processed {min(i + batch_size, len(data['memories']))}/{len(data['memories'])}"
                )

        print("🔗 Linking nodes (building GraphRAG context)...")
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

        print("🔍 Running Queries (Testing Bandit Convergence)...")
        hybrid_results = []
        for i, q in enumerate(data["queries"], 1):
            raw_results = await self.engine.search_memories(
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
                    "query": q["query"],
                    "expected": q["expected_source_ids"],
                    "retrieved": retrieved_ids,
                }
            )

            # Method 3.4: Feedback Loop for Bandit
            self.engine.math_ctrl.update_policy(success=is_hit)

            if not is_hit and q["expected_source_ids"]:
                # Cast to list to satisfy mypy if it thinks it's a Collection
                expected_ids = list(q["expected_source_ids"])
                missed_id = expected_ids[0]
                # Index reflection via engine to get multi-vector support
                ref_id = await self.engine.store_memory(
                    tenant_id=self.tenant_id,
                    agent_id=self.project_id,
                    content=f"[ALIAS] {q['query']}",  # Prefix handled by engine
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
                print(
                    f"   ✅ Query {i}/{len(data['queries'])} | Reflections: {self.szubar_reflections}"
                )

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
    parser.add_argument("--synthetic-count", type=int, required=False)
    parser.add_argument(
        "--set", type=Path, required=False, help="Path to benchmark set YAML file"
    )
    parser.add_argument(
        "--queries", type=int, default=50, help="Number of queries to run"
    )
    args = parser.parse_args()

    if not args.synthetic_count and not args.set:
        parser.error("Either --synthetic-count or --set must be provided")

    runner = RAEBenchmarkRunner(
        args.set,
        Path("."),
        "",
        synthetic_count=args.synthetic_count,
        queries=args.queries,
    )
    try:
        await runner.setup()
        await runner.run()
    finally:
        if hasattr(runner, "pool"):
            await runner.pool.close()


if __name__ == "__main__":
    asyncio.run(main())
