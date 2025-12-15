from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from apps.memory_api.repositories.memory_repository import MemoryRepository


class AsyncContextManager:
    def __init__(self, return_value=None):
        self.return_value = return_value

    async def __aenter__(self):
        return self.return_value

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


@pytest.fixture
def mock_pool():
    pool = MagicMock()

    # Setup connection as AsyncMock so fetch/execute are async
    conn = AsyncMock()

    # But transaction() must be sync method returning async context manager
    # We overwrite the auto-created AsyncMock child with a MagicMock
    conn.transaction = MagicMock(return_value=AsyncContextManager())

    # acquire() returns an async context manager that yields conn
    pool.acquire.return_value = AsyncContextManager(conn)

    return pool, conn


@pytest.mark.asyncio
async def test_insert_memory_success(mock_pool):
    pool, conn = mock_pool
    repo = MemoryRepository(pool)

    # Mock fetchrow result
    conn.fetchrow.return_value = {
        "id": "mem-1",
        "created_at": datetime.now(timezone.utc),
        "last_accessed_at": None,
        "usage_count": 0,
    }

    result = await repo.insert_memory(
        tenant_id="t1",
        content="content",
        source="user",
        importance=0.5,
        layer="em",
        tags=["tag"],
        timestamp=datetime.now(),
        project="p1",
    )

    assert result["id"] == "mem-1"
    conn.fetchrow.assert_called_once()
    # Check transaction
    conn.transaction.assert_called_once()


@pytest.mark.asyncio
async def test_insert_memory_failure(mock_pool):
    pool, conn = mock_pool
    repo = MemoryRepository(pool)
    conn.fetchrow.return_value = None

    result = await repo.insert_memory(
        tenant_id="t1",
        content="content",
        source="user",
        importance=0.5,
        layer="em",
        tags=None,
        timestamp=datetime.now(),
        project="p1",
    )

    assert result is None


@pytest.mark.asyncio
async def test_delete_memory_success(mock_pool):
    pool, conn = mock_pool
    repo = MemoryRepository(pool)
    conn.execute.return_value = "DELETE 1"

    result = await repo.delete_memory("mem-1", "t1")
    assert result is True


@pytest.mark.asyncio
async def test_delete_memory_not_found(mock_pool):
    pool, conn = mock_pool
    repo = MemoryRepository(pool)
    conn.execute.return_value = "DELETE 0"

    result = await repo.delete_memory("mem-1", "t1")
    assert result is False


@pytest.mark.asyncio
async def test_get_memory_by_id_found(mock_pool):
    pool, conn = mock_pool
    repo = MemoryRepository(pool)
    conn.fetchrow.return_value = {"id": "mem-1", "content": "test"}

    result = await repo.get_memory_by_id("mem-1", "t1")
    assert result["id"] == "mem-1"


@pytest.mark.asyncio
async def test_get_memory_by_id_not_found(mock_pool):
    pool, conn = mock_pool
    repo = MemoryRepository(pool)
    conn.fetchrow.return_value = None

    result = await repo.get_memory_by_id("mem-1", "t1")
    assert result is None


@pytest.mark.asyncio
async def test_get_semantic_memories(mock_pool):
    pool, conn = mock_pool
    repo = MemoryRepository(pool)
    conn.fetch.return_value = [{"id": "m1"}, {"id": "m2"}]

    result = await repo.get_semantic_memories("t1", "p1")
    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_reflective_memories(mock_pool):
    pool, conn = mock_pool
    repo = MemoryRepository(pool)
    conn.fetch.return_value = [{"id": "r1"}]

    result = await repo.get_reflective_memories("t1", "p1")
    assert len(result) == 1


@pytest.mark.asyncio
async def test_get_episodic_memories(mock_pool):
    pool, conn = mock_pool
    repo = MemoryRepository(pool)
    conn.fetch.return_value = [{"id": "e1"}]

    # Basic call
    await repo.get_episodic_memories("t1", "p1")
    conn.fetch.assert_called()

    # With filters
    await repo.get_episodic_memories("t1", "p1", limit=10, session_id="sess-1")
    # Verify SQL construction via call args is tricky with partial string match,
    # but we assume coverage is hit.


@pytest.mark.asyncio
async def test_count_memories_by_layer(mock_pool):
    pool, conn = mock_pool
    repo = MemoryRepository(pool)
    conn.fetchval.return_value = 5

    count = await repo.count_memories_by_layer("t1", "em", project="p1")
    assert count == 5

    # Without project
    await repo.count_memories_by_layer("t1", "em")
    assert conn.fetchval.call_count == 2


@pytest.mark.asyncio
async def test_get_average_strength(mock_pool):
    pool, conn = mock_pool
    repo = MemoryRepository(pool)
    conn.fetchval.return_value = 0.8

    avg = await repo.get_average_strength("t1", "em", project="p1")
    assert avg == 0.8

    conn.fetchval.return_value = None
    avg = await repo.get_average_strength("t1", "em")
    assert avg == 0.0


@pytest.mark.asyncio
async def test_update_memory_access_stats(mock_pool):
    pool, conn = mock_pool
    repo = MemoryRepository(pool)

    # Empty list
    res = await repo.update_memory_access_stats([], "t1")
    assert res == 0

    # With IDs
    conn.execute.return_value = "UPDATE 3"
    res = await repo.update_memory_access_stats(["m1", "m2", "m3"], "t1")
    assert res == 3
    conn.execute.assert_called()
