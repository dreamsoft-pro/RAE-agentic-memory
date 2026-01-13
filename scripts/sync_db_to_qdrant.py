import asyncio
import asyncpg
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import PointStruct
import json
from uuid import UUID

# Configuration
PG_DSN = "postgresql://rae:rae_password@localhost:5432/rae"
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "memories"
BATCH_SIZE = 1000

async def sync():
    print(f"🚀 Starting sync of memories from Postgres to Qdrant...")
    
    # 1. Connect to services
    pg_conn = await asyncpg.connect(PG_DSN)
    qdrant_client = AsyncQdrantClient(url=QDRANT_URL)
    
    try:
        # 2. Fetch total count
        total = await pg_conn.fetchval("SELECT count(*) FROM memories WHERE embedding IS NOT NULL")
        print(f"📦 Found {total} memories with embeddings in Postgres.")
        
        # 3. Process in batches
        processed = 0
        async with pg_conn.transaction():
            # Use a cursor for memory efficiency with large datasets
            query = """
                SELECT id, tenant_id, agent_id, session_id, layer, content, importance, tags, metadata, embedding
                FROM memories 
                WHERE embedding IS NOT NULL
            """
            
            rows = await pg_conn.fetch(query) # Fetching all since 20k is manageable in RAM, but cursor is safer for 100k+
            
            points = []
            for row in rows:
                memory_id = row['id']
                raw_embedding = row['embedding']
                
                if not raw_embedding:
                    continue
                
                # Parse pgvector string "[0.1, 0.2, ...]" to list of floats
                if isinstance(raw_embedding, str):
                    embedding = [float(x) for x in raw_embedding.strip('[]').split(',')]
                else:
                    embedding = list(raw_embedding)
                
                # Determine vector name by dimension
                dim = len(embedding)
                vector_data = {}
                if dim == 1536:
                    vector_data["openai"] = embedding
                elif dim == 768:
                    vector_data["ollama"] = embedding
                elif dim == 384:
                    vector_data["dense"] = embedding
                else:
                    vector_data["dense"] = embedding # Fallback
                
                # Prepare payload (matching rae-core schema)
                payload = {
                    "memory_id": str(memory_id),
                    "tenant_id": row['tenant_id'],
                    "agent_id": row['agent_id'] or "default",
                    "session_id": row['session_id'] or "default",
                    "layer": row['layer'],
                    "content": row['content'],
                    "importance": row['importance'] or 0.5,
                    "tags": row['tags'] or [],
                }
                # Merge metadata if exists
                if row['metadata']:
                    meta = row['metadata']
                    if isinstance(meta, str):
                        try:
                            meta = json.loads(meta)
                        except:
                            pass
                    if isinstance(meta, dict):
                        payload.update(meta)

                points.append(PointStruct(
                    id=str(memory_id),
                    vector=vector_data,
                    payload=payload
                ))
                
                # Push batch to Qdrant
                if len(points) >= BATCH_SIZE:
                    await qdrant_client.upsert(
                        collection_name=COLLECTION_NAME,
                        points=points,
                        wait=False
                    )
                    processed += len(points)
                    print(f"✅ Synced {processed}/{total}...")
                    points = []
            
            # Final batch
            if points:
                await qdrant_client.upsert(
                    collection_name=COLLECTION_NAME,
                    points=points,
                    wait=True
                )
                processed += len(points)
                print(f"✅ Synced {processed}/{total} (final batch).")

        print(f"✨ Successfully synchronized {processed} memories to Qdrant.")
        
    finally:
        await pg_conn.close()
        await qdrant_client.close()

if __name__ == "__main__":
    asyncio.run(sync())
