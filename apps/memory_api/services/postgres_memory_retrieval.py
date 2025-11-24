from typing import Dict, List

import asyncpg

from apps.memory_api.repositories.memory_repository import MemoryRepository


async def get_semantic_memories(
    pool: asyncpg.Pool, tenant_id: str, project: str
) -> List[Dict]:
    """
    Retrieves all semantic memories for a given tenant and project from Postgres.

    Uses MemoryRepository for data access.
    """
    repository = MemoryRepository(pool)
    return await repository.get_semantic_memories(tenant_id, project)


async def get_reflective_memories(
    pool: asyncpg.Pool, tenant_id: str, project: str
) -> List[Dict]:
    """
    Retrieves all reflective memories for a given tenant and project from Postgres.

    Uses MemoryRepository for data access.
    """
    repository = MemoryRepository(pool)
    return await repository.get_reflective_memories(tenant_id, project)
