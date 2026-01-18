import asyncio
import json
import os
from uuid import uuid4

import asyncpg
import httpx
import yaml
from qdrant_client import AsyncQdrantClient, models

# Configuration
YAML_PATH = "benchmarking/sets/industrial_ultra.yaml"
CHECKPOINT_PATH = "benchmarking/results/ultra_backfill_checkpoint.json"
TENANT_ID = "00000000-0000-0000-0000-000000000999"
PROJECT_ID = "ultra_v2"
BATCH_SIZE = 500
EMBED_BATCH_SIZE = 16
OLLAMA_URL = "http://ollama-dev:11434/api/embed"
MODEL = "nomic-embed-text"

# DB Config (Internal Docker Network)
DB_CONFIG = {
    "host": "postgres",
    "user": "rae",
    "password": "rae_password",
    "database": "rae",
}


async def get_embeddings_batch(client, texts, retries=3):
    """Get multiple embeddings with retry logic."""
    prefixed_texts = [f"search_document: {t}" for t in texts]
    for attempt in range(retries):
        try:
            resp = await client.post(
                OLLAMA_URL,
                json={"model": MODEL, "input": prefixed_texts},
                timeout=120.0,
            )
            if resp.status_code == 200:
                return resp.json().get("embeddings")
            await asyncio.sleep(5 * (attempt + 1))
        except Exception:
            await asyncio.sleep(10 * (attempt + 1))
    return None


def save_checkpoint(index):
    os.makedirs(os.path.dirname(CHECKPOINT_PATH), exist_ok=True)
    with open(CHECKPOINT_PATH, "w") as f:
        json.dump({"last_index": index}, f)


def load_checkpoint():
    if os.path.exists(CHECKPOINT_PATH):
        try:
            with open(CHECKPOINT_PATH, "r") as f:
                return json.load(f).get("last_index", 0)
        except:
            return 0
    return 0


async def backfill_ultra():
    print("🚀 Starting PRODUCTION Backfill for Industrial Ultra (100k)")
    print(f"📂 Loading {YAML_PATH}...")
    with open(YAML_PATH, "r") as f:
        data = yaml.safe_load(f)
    memories = data.get("memories", [])
    total_memories = len(memories)
    print(f"Loaded {total_memories} memory definitions.")

    conn = await asyncpg.connect(**DB_CONFIG)
    qdrant = AsyncQdrantClient(host="qdrant", port=6333)
    start_from = load_checkpoint()
    print(f"📍 Resuming from index {start_from}")

    async with httpx.AsyncClient(timeout=180.0) as client:
        for i in range(start_from, total_memories, BATCH_SIZE):
            batch = memories[i : i + BATCH_SIZE]
            all_embeddings = []
            batch_texts = [m["text"] for m in batch]

            success = True
            for j in range(0, len(batch_texts), EMBED_BATCH_SIZE):
                sub_batch = batch_texts[j : j + EMBED_BATCH_SIZE]
                embs = await get_embeddings_batch(client, sub_batch)
                if embs:
                    all_embeddings.extend(embs)
                else:
                    success = False
                    break

            if not success:
                print(f"❌ Failed to get embeddings at {i}. Checkpointing.")
                save_checkpoint(i)
                break

            db_rows = []
            qdrant_points = []
            for memory, emb in zip(batch, all_embeddings):
                m_id = str(uuid4())
                db_rows.append(
                    (
                        m_id,
                        TENANT_ID,
                        memory["text"],
                        memory["id"],
                        memory.get("metadata", {}).get("importance", 0.5),
                        1.0,
                        "semantic",
                        memory.get("tags", []),
                        PROJECT_ID,
                    )
                )
                qdrant_points.append(
                    models.PointStruct(
                        id=m_id,
                        vector={"dense": emb},
                        payload={
                            "id": m_id,
                            "tenant_id": TENANT_ID,
                            "content": memory["text"],
                            "source": memory["id"],
                            "project": PROJECT_ID,
                        },
                    )
                )

            try:
                await conn.executemany(
                    "INSERT INTO memories (id, tenant_id, content, source, importance, strength, layer, tags, project) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)",
                    db_rows,
                )
                await qdrant.upsert(
                    collection_name="memories", points=qdrant_points, wait=False
                )
                save_checkpoint(i + len(batch))
                if (i + len(batch)) % 1000 == 0:
                    print(f"✅ Progress: {((i+len(batch))/total_memories)*100:.1f}%")
            except Exception as e:
                print(f"🔥 DB Error: {e}")
                break

    await conn.close()
    await qdrant.close()
    print("✨ Ultra Backfill Operation Ended.")


if __name__ == "__main__":
    asyncio.run(backfill_ultra())
