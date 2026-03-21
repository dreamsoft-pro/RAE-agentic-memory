import json
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
import asyncpg

from rae_core.adapters.postgres import PostgreSQLStorage

@pytest.fixture
def mock_conn():
    conn = AsyncMock()
    return conn

@pytest.fixture
def mock_pool(mock_conn):
    pool = MagicMock()
    pool.acquire.return_value.__aenter__.return_value = mock_conn
    pool.close = AsyncMock()
    return pool

class TestPostgreSQLStorageCoverage:
    @pytest.mark.asyncio
    async def test_get_pool_value_error(self):
        """Test that _get_pool raises ValueError if dsn and pool are missing."""
        storage = PostgreSQLStorage()
        with pytest.raises(ValueError, match="Either dsn or pool must be provided"):
            await storage._get_pool()

    @pytest.mark.asyncio
    async def test_get_pool_create_pool(self):
        """Test that _get_pool creates a pool if dsn is provided."""
        storage = PostgreSQLStorage(dsn="postgresql://localhost/db")
        with patch("asyncpg.create_pool", new_callable=AsyncMock) as mock_create:
            mock_create.return_value = MagicMock()
            pool = await storage._get_pool()
            assert pool == mock_create.return_value
            mock_create.assert_called_once_with("postgresql://localhost/db")

    @pytest.mark.asyncio
    async def test_store_reflection_audit(self, mock_pool, mock_conn):
        """Test store_reflection_audit."""
        storage = PostgreSQLStorage(pool=mock_pool)
        
        audit_id = await storage.store_reflection_audit(
            query_id="q1",
            tenant_id="t1",
            fsi_score=0.9,
            final_decision="keep",
            l1_report={"l1": "ok"},
            l2_report={"l2": "ok"},
            l3_report={"l3": "ok"},
            agent_id="a1",
            metadata={"meta": "data"}
        )
        
        assert isinstance(audit_id, uuid4().__class__)
        assert mock_conn.execute.called
        args = mock_conn.execute.call_args[0]
        assert "INSERT INTO reflection_audits" in args[0]
        assert args[2] == "q1"
        assert args[3] == "t1"
        assert args[4] == "a1"
        assert args[5] == 0.9
        assert args[6] == "keep"
        assert json.loads(args[7]) == {"l1": "ok"}
        assert json.loads(args[10]) == {"meta": "data"}

    def test_row_to_dict_json_parsing(self):
        """Test _row_to_dict with JSON string metadata."""
        storage = PostgreSQLStorage()
        
        # Case: metadata is a JSON string
        row = {"id": "uuid", "metadata": json.dumps({"key": "value"})}
        result = storage._row_to_dict(row)
        assert result["metadata"] == {"key": "value"}
        
        # Case: metadata is already a dict
        row = {"id": "uuid", "metadata": {"key": "value"}}
        result = storage._row_to_dict(row)
        assert result["metadata"] == {"key": "value"}
        
        # Case: metadata is None
        row = {"id": "uuid", "metadata": None}
        result = storage._row_to_dict(row)
        assert result["metadata"] == {}

        # Case: invalid JSON string
        row = {"id": "uuid", "metadata": "{invalid"}
        result = storage._row_to_dict(row)
        assert result["metadata"] == {}

        # Case: row is None
        assert storage._row_to_dict(None) is None

    @pytest.mark.asyncio
    async def test_search_memories_with_project(self, mock_pool, mock_conn):
        """Test search_memories with project kwarg."""
        storage = PostgreSQLStorage(pool=mock_pool)
        mock_conn.fetch.return_value = []
        
        await storage.search_memories(
            query="test", tenant_id="t1", agent_id="a1", layer="working", project="p1"
        )
        
        args = mock_conn.fetch.call_args[0]
        assert "AND project = $6" in args[0]
        assert args[6] == "p1"

    @pytest.mark.asyncio
    async def test_close(self, mock_pool):
        """Test close method."""
        storage = PostgreSQLStorage(pool=mock_pool)
        await storage.close()
        mock_pool.close.assert_called_once()

    def test_get_stem(self):
        """Test _get_stem method."""
        storage = PostgreSQLStorage()
        assert storage._get_stem("cats") == "cat"
        assert storage._get_stem("parties") == "part"
        assert storage._get_stem("miss") == "miss"
        assert storage._get_stem("a") == "a"
        assert storage._get_stem("running") == "running"
