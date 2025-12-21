"""Unit tests for extended PostgreSQLStorage adapter methods."""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from rae_core.adapters.postgres import PostgreSQLStorage


class TestPostgreSQLStorageExtended:
    """Test suite for extended PostgreSQLStorage methods."""

    @pytest.fixture
    def mock_pool(self):
        """Create a mock asyncpg pool."""
        pool = AsyncMock()
        # acquire is not async, it returns a context manager
        pool.acquire = MagicMock()
        return pool

    @pytest.fixture
    def mock_conn(self, mock_pool):
        """Create a mock connection."""
        conn = AsyncMock()
        # Setup acquire context manager
        mock_pool.acquire.return_value.__aenter__.return_value = conn
        return conn

    @pytest.fixture
    def pg_storage(self, mock_pool):
        """Create PostgreSQLStorage instance with mock pool."""
        # Patch asyncpg to avoid import errors
        with patch("rae_core.adapters.postgres.asyncpg") as mock_asyncpg:
            mock_asyncpg.create_pool.return_value = mock_pool

            storage = PostgreSQLStorage(
                dsn="postgresql://localhost/test", pool=mock_pool
            )
            return storage

    @pytest.mark.asyncio
    async def test_get_metric_aggregate(self, pg_storage, mock_conn):
        """Test calculating metric aggregate."""
        mock_conn.fetchval.return_value = 0.75

        result = await pg_storage.get_metric_aggregate(
            tenant_id="tenant1",
            metric="importance",
            func="avg",
            filters={"agent_id": "agent1", "layer": "working"}
        )

        assert result == 0.75
        mock_conn.fetchval.assert_called_once()
        query_arg = mock_conn.fetchval.call_args[0][0]
        assert "SELECT avg(importance)" in query_arg
        assert "WHERE tenant_id = $1" in query_arg
        assert "agent_id = $2" in query_arg
        assert "layer = $3" in query_arg

    @pytest.mark.asyncio
    async def test_get_metric_aggregate_validation(self, pg_storage):
        """Test validation of metrics and functions."""
        with pytest.raises(ValueError, match="Invalid metric"):
            await pg_storage.get_metric_aggregate("tenant1", "bad_metric", "avg")

        with pytest.raises(ValueError, match="Invalid function"):
            await pg_storage.get_metric_aggregate("tenant1", "importance", "bad_func")

    @pytest.mark.asyncio
    async def test_update_memory_access_batch(self, pg_storage, mock_conn):
        """Test batch update of memory access."""
        mock_conn.execute.return_value = "UPDATE 2"
        memory_ids = [uuid4(), uuid4()]

        result = await pg_storage.update_memory_access_batch(
            memory_ids=memory_ids,
            tenant_id="tenant1"
        )

        assert result is True
        mock_conn.execute.assert_called_once()
        query_arg = mock_conn.execute.call_args[0][0]
        assert "UPDATE memories" in query_arg
        assert "WHERE id = ANY($2)" in query_arg

    @pytest.mark.asyncio
    async def test_adjust_importance(self, pg_storage, mock_conn):
        """Test adjusting importance."""
        mock_conn.fetchval.return_value = 0.8
        memory_id = uuid4()

        new_importance = await pg_storage.adjust_importance(
            memory_id=memory_id,
            delta=0.1,
            tenant_id="tenant1"
        )

        assert new_importance == 0.8
        mock_conn.fetchval.assert_called_once()
        query_arg = mock_conn.fetchval.call_args[0][0]
        assert "UPDATE memories" in query_arg
        assert "importance = GREATEST(0.0, LEAST(1.0, importance + $1))" in query_arg

    @pytest.mark.asyncio
    async def test_adjust_importance_not_found(self, pg_storage, mock_conn):
        """Test adjusting importance for missing memory."""
        mock_conn.fetchval.return_value = None

        with pytest.raises(ValueError, match="Memory not found"):
            await pg_storage.adjust_importance(
                memory_id=uuid4(),
                delta=0.1,
                tenant_id="tenant1"
            )
