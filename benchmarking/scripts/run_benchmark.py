#!/usr/bin/env python3
import argparse
import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

import asyncpg
import yaml
from qdrant_client import AsyncQdrantClient
from qdrant_client import models as q_models

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "rae-core"))

class RAEBenchmarkRunner:
    def __init__(self, benchmark_file: Path, output_dir: Path):
        self.benchmark_file = benchmark_file
        self.output_dir = output_dir
        self.tenant_id = "00000000-0000-0000-0000-000000000000"
        self.id_map = {}

    async def setup(self):
        print(f"🔌 Initializing System 36.0 (Ascension)...")
        self.pool = await asyncpg.create_pool(
            host=os.getenv("POSTGRES_HOST", "127.0.0.1"),
            port=int(os.getenv("POSTGRES_PORT", 5432)),
            database=os.getenv("POSTGRES_DB", "rae"),
            user=os.getenv("POSTGRES_USER", "rae"),
            password=os.getenv("POSTGRES_PASSWORD", "rae_password"),
        )
        self.qdrant = AsyncQdrantClient(host=os.getenv("QDRANT_HOST", "127.0.0.1"), port=6333)
        
        from rae_core.engine import RAEEngine
        from rae_core.math.controller import MathLayerController
        from rae_adapters.postgres import PostgreSQLStorage
        from rae_core.adapters.qdrant import QdrantVectorStore
        from rae_core.embedding.manager import EmbeddingManager
        from rae_core.embedding.native import NativeEmbeddingProvider

        nomic_path = "/app/models/nomic-embed-text-v1.5/model.onnx"
        nomic_provider = NativeEmbeddingProvider(model_path=nomic_path, tokenizer_path=nomic_path.replace("model.onnx", "tokenizer.json"), model_name="nomic")
        self.manager = EmbeddingManager(default_provider=nomic_provider, default_model_name="nomic")
        
        self.engine = RAEEngine(
            memory_storage=PostgreSQLStorage(pool=self.pool),
            vector_store=QdrantVectorStore(client=self.qdrant),
            embedding_provider=self.manager,
            math_controller=MathLayerController()
        )

    async def sync_ids(self, project_id):
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT id, metadata->>'id' as source_id FROM memories WHERE agent_id = $1", project_id)
            self.id_map = {str(row['id']): row['source_id'] for row in rows if row['source_id']}
            print(f"🔄 Synchronized {len(self.id_map)} IDs for {project_id}")

    async def run(self, rerank: bool = False):
        with open(self.benchmark_file, "r") as f:
            data = yaml.safe_load(f)
        
        project_id = data.get("name", "RAE-agentic-memory")
        print(f"🎯 Project: {project_id}")
        
        # FULL INGESTION
        await self.qdrant.delete_collection("memories")
        await self.qdrant.create_collection("memories", vectors_config={"nomic": q_models.VectorParams(size=768, distance=q_models.Distance.COSINE)})
        await self.pool.execute("DELETE FROM memories WHERE agent_id = $1", project_id)
        
        print("📥 Ingesting...")
        for m in data['memories']:
            m_id = await self.engine.store_memory(tenant_id=self.tenant_id, agent_id=project_id, content=m['text'], metadata=m.get('metadata', {}), layer="longterm")
            # Force technical ID into metadata for syncing with explicit casting
            await self.pool.execute("UPDATE memories SET metadata = metadata || jsonb_build_object('id', $1::text) WHERE id = $2::uuid", m['id'], m_id)

        await self.sync_ids(project_id)

        print("🔍 Querying...")
        total_rr = 0.0
        for q in data['queries']:
            raw = await self.engine.search_memories(query=q['query'], tenant_id=self.tenant_id, agent_id=project_id, top_k=300, enable_reranking=rerank)
            retrieved = [self.id_map.get(str(r['id']), str(r['id'])) for r in raw]
            for rank, r_id in enumerate(retrieved, 1):
                if r_id in q['expected_source_ids']:
                    total_rr += 1.0 / rank
                    break
        
        print(f"\n========================================\nFINAL MRR: {total_rr / len(data['queries']):.4f}\n========================================")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", type=Path, required=True)
    parser.add_argument("--rerank", action="store_true")
    args = parser.parse_args()
    runner = RAEBenchmarkRunner(args.set, Path("."))
    try:
        await runner.setup()
        await runner.run(rerank=args.rerank)
    finally:
        await runner.pool.close()

if __name__ == "__main__":
    asyncio.run(main())