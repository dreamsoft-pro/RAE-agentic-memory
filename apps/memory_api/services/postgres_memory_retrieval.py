from typing import List, Dict
import asyncpg

async def get_semantic_memories(pool: asyncpg.Pool, tenant_id: str, project: str) -> List[Dict]:
    """
    Retrieves all semantic memories for a given tenant and project from Postgres.
    """
    async with pool.acquire() as conn:
        records = await conn.fetch("""
            SELECT id, content, tags, metadata, layer, created_at
            FROM memories
            WHERE tenant_id = $1 AND project = $2 AND layer = 'sm'
            ORDER BY created_at DESC
        """, tenant_id, project)
        return [dict(r) for r in records]

async def get_reflective_memories(pool: asyncpg.Pool, tenant_id: str, project: str) -> List[Dict]:
    """
    Retrieves all reflective memories for a given tenant and project from Postgres.
    """
    async with pool.acquire() as conn:
        records = await conn.fetch("""
            SELECT id, content, tags, metadata, layer, created_at
            FROM memories
            WHERE tenant_id = $1 AND project = $2 AND layer = 'rm'
            ORDER BY created_at DESC
        """, tenant_id, project)
        return [dict(r) for r in records]
