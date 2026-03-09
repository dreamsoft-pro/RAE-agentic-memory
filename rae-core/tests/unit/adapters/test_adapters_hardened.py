import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from rae_core.adapters.postgres import PostgreSQLStorage
from rae_core.adapters.qdrant import QdrantVectorStore

class TestAdaptersHardened:
    @pytest.fixture
    def mock_pool(self):
        pool = MagicMock()
        pool.acquire = MagicMock()
        conn = AsyncMock()
        pool.acquire.return_value.__aenter__.return_value = conn
        return pool, conn

    @pytest.mark.asyncio
    async def test_postgres_get_memory_error(self, mock_pool):
        pool, conn = mock_pool
        storage = PostgreSQLStorage(pool=pool)
        conn.fetchrow.side_effect = Exception("SQL Error")
        with pytest.raises(Exception, match="SQL Error"):
            await storage.get_memory(uuid4(), "t1")

    @pytest.mark.asyncio
    async def test_qdrant_search_error_propagation(self):
        mock_client = MagicMock()
        mock_client.query_points = AsyncMock(side_effect=RuntimeError("Qdrant Down"))
        store = QdrantVectorStore(client=mock_client)
        store._initialized = True
        with pytest.raises(RuntimeError, match="Qdrant Down"):
            await store.search_similar([0.1]*384, tenant_id="t1")

    @pytest.mark.asyncio
    async def test_qdrant_batch_store_error(self):
        mock_client = MagicMock()
        # Full async chain for Qdrant config
        mock_client.get_collection = AsyncMock()
        mock_client.get_collections = AsyncMock(return_value=MagicMock(collections=[MagicMock(name="memories")]))
        mock_client.update_collection = AsyncMock()
        
        # The target failure
        mock_client.upsert = AsyncMock(side_effect=Exception("Upsert Failed"))
        
        store = QdrantVectorStore(client=mock_client)
        store._initialized = True
        
        with pytest.raises(Exception, match="Upsert Failed"):
            await store.batch_store_vectors([(uuid4(), [0.1], {})], "t1")
