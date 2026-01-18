import asyncio
from uuid import uuid4

import asyncpg
import httpx
from qdrant_client import AsyncQdrantClient, models

# Configuration
YAML_PATH = "benchmarking/sets/industrial_ultra.yaml"
TENANT_ID = "00000000-0000-0000-0000-000000000999"
PROJECT_ID = "ultra_v2"
BATCH_SIZE = 500
EMBED_BATCH_SIZE = 16
OLLAMA_URL = "http://ollama-dev:11434/api/embed"
MODEL = "nomic-embed-text"

DB_CONFIG = {
    "host": "postgres",
    "user": "rae",
    "password": "rae_password",
    "database": "rae",
}


async def get_embeddings_batch(client, texts):
    prefixed_texts = [f"search_document: {t}" for t in texts]
    try:
        resp = await client.post(
            OLLAMA_URL, json={"model": MODEL, "input": prefixed_texts}, timeout=120.0
        )
        return resp.json().get("embeddings") if resp.status_code == 200 else None
    except:
        return None


def stream_memories(path):
    """Extremely lightweight YAML parser for this specific file format."""
    memories = []
    current_mem = {}
    in_memories = False

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line == "memories:":
                in_memories = True
                continue
            if line == "queries:":
                break
            if not in_memories:
                continue

            if line.startswith("- id:"):
                if current_mem:
                    yield current_mem
                current_mem = {"id": line.split(":")[1].strip().strip('"')}
            elif line.startswith("text:"):
                current_mem["text"] = line.split("text:")[1].strip().strip('"')
            elif line.startswith("importance:"):
                # Handle nested metadata if needed, but here simplified
                pass
        if current_mem:
            yield current_mem


async def backfill():
    print("🚀 Starting STREAMING Backfill for Ultra (100k)")
    conn = await asyncpg.connect(**DB_CONFIG)
    qdrant = AsyncQdrantClient(host="qdrant", port=6333)

    batch = []
    count = 0

    async with httpx.AsyncClient(timeout=180.0) as client:
        for memory in stream_memories(YAML_PATH):
            batch.append(memory)

            if len(batch) >= BATCH_SIZE:
                # Process Batch
                texts = [m["text"] for m in batch]
                embeddings = await get_embeddings_batch(client, texts)

                if embeddings:
                    db_rows = []
                    points = []
                    for m, emb in zip(batch, embeddings):
                        m_id = str(uuid4())
                        db_rows.append(
                            (
                                m_id,
                                TENANT_ID,
                                m["text"],
                                m["id"],
                                0.5,
                                1.0,
                                "semantic",
                                [],
                                PROJECT_ID,
                            )
                        )
                        points.append(
                            models.PointStruct(
                                id=m_id,
                                vector={"dense": emb},
                                payload={
                                    "id": m_id,
                                    "tenant_id": TENANT_ID,
                                    "content": m["text"],
                                    "source": m["id"],
                                    "project": PROJECT_ID,
                                },
                            )
                        )

                    await conn.executemany(
                        "INSERT INTO memories (id, tenant_id, content, source, importance, strength, layer, tags, project) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)",
                        db_rows,
                    )
                    await qdrant.upsert(
                        collection_name="memories", points=points, wait=False
                    )

                    count += len(batch)
                    print(f"✅ Progress: {count}/100000")

                batch = []

    await conn.close()
    await qdrant.close()
    print("✨ Finished.")


if __name__ == "__main__":
    asyncio.run(backfill())
