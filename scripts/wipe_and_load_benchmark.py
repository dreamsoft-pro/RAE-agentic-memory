"""
RAE Gold Standard Loader.
Loads data from a benchmark YAML through the UICTC Pipeline.
"""

import asyncio
import os
import sys
import yaml
from pathlib import Path
import structlog

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "rae-core"))

from rae_core.engine import RAEEngine
from rae_adapters.postgres import PostgreSQLStorage
from rae_adapters.qdrant import QdrantVectorStore
from rae_core.embedding.native import NativeEmbeddingProvider

async def wipe_databases(db_url: str, qdrant_url: str):
    import asyncpg
    from qdrant_client import AsyncQdrantClient
    print("🧹 Wiping Databases...")
    conn = await asyncpg.connect(db_url)
    await conn.execute("TRUNCATE memories CASCADE;")
    await conn.close()
    qc = AsyncQdrantClient(url=qdrant_url)
    try: await qc.delete_collection("memories")
    except: pass
    await qc.close()

async def load_benchmark_file(file_path: str):
    db_url = os.getenv("DATABASE_URL", "postgresql://rae:rae_password@postgres/rae")
    qdrant_host = os.getenv("QDRANT_HOST", "qdrant")
    qdrant_url = f"http://{qdrant_host}:6333"
    
    await wipe_databases(db_url, qdrant_url)
    
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    
    # Setup Engine
    model_dir = "/app/models/all-MiniLM-L6-v2"
    embedding_provider = NativeEmbeddingProvider(
        model_path=f"{model_dir}/model.onnx",
        tokenizer_path=f"{model_dir}/tokenizer.json"
    )
    storage = PostgreSQLStorage(db_url)
    vector_store = QdrantVectorStore(url=qdrant_url)
    engine = RAEEngine(memory_storage=storage, vector_store=vector_store, embedding_provider=embedding_provider)
    
    print(f"📥 Loading {len(data['memories'])} memories from {file_path}...")
    
    tenant_id = "00000000-0000-0000-0000-000000000000"
    agent_id = "ffffffff-ffff-ffff-ffff-ffffffffffff"
    
    count = 0
    for mem in data["memories"]:
        # Store metadata including the original doc ID for lineage testing
        meta = mem.get("metadata", {})
        meta["external_id"] = mem["id"] # Important for Ground Truth matching
        
        await engine.store_memory(
            content=mem["content"],
            source="gold_standard_load",
            project="GOLD_STANDARD",
            tenant_id=tenant_id,
            agent_id=agent_id,
            importance=mem.get("importance", 0.5),
            metadata=meta
        )
        count += 1
        if count % 100 == 0:
            print(f"  Ingested {count}/{len(data['memories'])}...")

    print(f"✨ Load complete. Baza danych gotowa do testów retrievalu.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True)
    args = parser.parse_args()
    asyncio.run(load_benchmark_file(args.file))
