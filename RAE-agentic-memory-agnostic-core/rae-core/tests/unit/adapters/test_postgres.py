from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from rae_core.adapters.postgres import PostgreSQLStorage


@pytest.fixture
def mock_conn():
    conn = AsyncMock()
    return conn


@pytest.fixture
def mock_pool(mock_conn):
    pool = MagicMock()
    pool.acquire.return_value.__aenter__.return_value = mock_conn
    return pool


@pytest.fixture
def pg_storage(mock_pool):
    storage = PostgreSQLStorage(dsn="postgresql://localhost/db")
    storage._pool = mock_pool
    return storage


class TestPostgreSQLStorage:
    @pytest.mark.asyncio
    async def test_store_memory(self, pg_storage, mock_conn):
        """Test storing a memory."""
        mock_conn.execute.return_value = "INSERT 0 1"
        content = "test content"

        memory_id = await pg_storage.store_memory(
            content=content,
            layer="working",
            tenant_id="tenant1",
            agent_id="agent1",
            project="p1",
        )

        assert isinstance(memory_id, uuid4().__class__)
        assert mock_conn.execute.called

    @pytest.mark.asyncio
    async def test_get_memory(self, pg_storage, mock_conn):
        """Test retrieving a memory."""
        now = datetime.now(timezone.utc)
        memory_id = uuid4()
        mock_conn.fetchrow.return_value = {
            "id": memory_id,
            "content": "test",
            "layer": "working",
            "usage_count": 5,
            "created_at": now,
            "importance": 0.8,
        }

        result = await pg_storage.get_memory(memory_id, "tenant1")
        assert result["id"] == memory_id
        assert result["content"] == "test"

    @pytest.mark.asyncio
    async def test_search_memories(self, pg_storage, mock_conn):
        """Test searching memories."""
        memory_id = uuid4()

        mock_conn.fetch.return_value = [
            {
                "id": memory_id,
                "content": "test",
                "score": 1.0,
            }
        ]

        results = await pg_storage.search_memories(
            query="test", tenant_id="tenant1", agent_id="agent1", layer="working"
        )

        assert len(results) == 1
        assert results[0]["id"] == memory_id
        assert results[0]["score"] == 1.0

    @pytest.mark.asyncio
    async def test_update_memory(self, pg_storage, mock_conn):
        """Test updating memory."""
        result = await pg_storage.update_memory(
            memory_id=uuid4(), tenant_id="tenant1", updates={"content": "new"}
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_memory(self, pg_storage, mock_conn):
        """Test deleting memory."""
        result = await pg_storage.delete_memory(uuid4(), "tenant1")
        assert result is True

    @pytest.mark.asyncio
    async def test_update_memory_expiration(self, pg_storage, mock_conn):
        """Test updating memory expiration."""
        result = await pg_storage.update_memory_expiration(uuid4(), "tenant1", None)
        assert result is True
