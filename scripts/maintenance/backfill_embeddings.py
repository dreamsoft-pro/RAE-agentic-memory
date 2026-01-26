"""
Backfill memory_embeddings table from legacy memories.embedding column.

Usage:
    python3 scripts/maintenance/backfill_embeddings.py
"""
import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

import asyncpg  # noqa: E402
import structlog  # noqa: E402

from apps.memory_api.config import settings  # noqa: E402

logger = structlog.get_logger(__name__)

async def main():
    logger.info("Starting embedding backfill...")

    # Connect to DB
    dsn = settings.DATABASE_URL
    if not dsn:
        # Construct DSN from components
        dsn = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB}"
        logger.info(f"Constructed DSN from settings: {dsn.split('@')[-1]}")

    try:
        pool = await asyncpg.create_pool(dsn)
    except Exception as e:
        logger.error(f"Failed to connect to DB: {e}")
        return

    async with pool.acquire() as conn:
        # Get count
        count = await conn.fetchval("SELECT COUNT(*) FROM memories WHERE embedding IS NOT NULL")
        logger.info(f"Found {count} memories with legacy embeddings")

        # Fetch in batches
        limit = 1000
        offset = 0
        total_migrated = 0
        total_skipped = 0

        while True:
            rows = await conn.fetch(
                """
                SELECT id, embedding
                FROM memories
                WHERE embedding IS NOT NULL
                ORDER BY created_at DESC
                LIMIT $1 OFFSET $2
                """,
                limit, offset
            )

            if not rows:
                break

            for row in rows:
                memory_id = row['id']
                embedding_str = row['embedding']

                # Parse embedding
                # asyncpg returns vector as string like "[0.1, 0.2, ...]" usually,
                # but might be different depending on codec.
                # If it's pgvector, it might be a list.
                embedding = []
                if isinstance(embedding_str, str):
                    try:
                        embedding = [float(x) for x in embedding_str.strip("[]").split(",")]
                    except ValueError:
                        logger.warning(f"Failed to parse embedding for {memory_id}")
                        continue
                elif isinstance(embedding_str, list):
                    embedding = embedding_str
                else:
                    logger.warning(f"Unknown embedding format {type(embedding_str)} for {memory_id}")
                    continue

                # Determine model name by dimension
                dim = len(embedding)
                model_name = "unknown"
                if dim == 1536:
                    model_name = "openai"
                elif dim == 768:
                    model_name = "ollama"
                elif dim == 384:
                    model_name = "dense"
                elif dim == 1024:
                    model_name = "cohere"

                # Insert
                try:
                    # Convert list to string for SQL if needed, or pass list if pgvector codec is registered.
                    # Standard asyncpg without register_vector needs string.
                    emb_val = str(embedding)

                    cmd = """
                    INSERT INTO memory_embeddings (memory_id, model_name, embedding, created_at)
                    VALUES ($1, $2, $3, NOW())
                    ON CONFLICT (memory_id, model_name) DO NOTHING
                    """
                    result = await conn.execute(cmd, memory_id, model_name, emb_val)
                    if result == "INSERT 0 1":
                        total_migrated += 1
                    else:
                        total_skipped += 1 # Conflict

                except Exception as e:
                    logger.error(f"Failed to insert embedding for {memory_id}: {e}")

            offset += limit
            logger.info(f"Processed {offset}/{count}...")

    await pool.close()
    logger.info(f"Backfill complete. Migrated: {total_migrated}, Skipped: {total_skipped}")

if __name__ == "__main__":
    asyncio.run(main())
