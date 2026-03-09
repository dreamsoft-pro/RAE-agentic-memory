"""Hardened unit tests for QdrantVectorStore adapter."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4, UUID
from qdrant_client.http import models
from rae_core.adapters.qdrant import QdrantVectorStore

class TestQdrantVectorStore:
    @pytest.fixture
    def mock_client(self):
        client = MagicMock()
        client.get_collections = AsyncMock()
        client.get_collection = AsyncMock()
        client.create_collection = AsyncMock()
        client.delete_collection = AsyncMock()
        client.update_collection = AsyncMock()
        client.upsert = AsyncMock()
        client.retrieve = AsyncMock()
        client.delete = AsyncMock()
        client.query_points = AsyncMock()
        client.count = AsyncMock()
        client.close = AsyncMock()
        return client

    @pytest.mark.asyncio
    async def test_init_default(self):
        with patch("rae_core.adapters.qdrant.AsyncQdrantClient") as mock_init:
            store = QdrantVectorStore(url="http://test:6333")
            mock_init.assert_called_once_with(url="http://test:6333", api_key=None)
            assert store.collection_name == "memories"

    @pytest.mark.asyncio
    async def test_ensure_collection_new(self, mock_client):
        store = QdrantVectorStore(client=mock_client)
        
        # Mock: No collections exist
        mock_client.get_collections.return_value = MagicMock(collections=[])
        
        await store._ensure_collection()
        
        mock_client.create_collection.assert_called_once()
        assert store._initialized is True

    @pytest.mark.asyncio
    async def test_ensure_collection_exists_valid(self, mock_client):
        store = QdrantVectorStore(client=mock_client, embedding_dim=128)
        
        # Mock: Collection exists with correct dim
        # Using objects that mimic Qdrant models
        mock_coll = MagicMock()
        mock_coll.name = "memories"
        mock_client.get_collections.return_value = MagicMock(collections=[mock_coll])
        
        coll_info = MagicMock()
        coll_info.config.params.vectors = {"dense": MagicMock(size=128)}
        mock_client.get_collection.return_value = coll_info
        
        await store._ensure_collection()
        
        mock_client.create_collection.assert_not_called()
        assert store._initialized is True

    @pytest.mark.asyncio
    async def test_ensure_collection_schema_mismatch(self, mock_client):
        store = QdrantVectorStore(client=mock_client, embedding_dim=128)
        
        # Mock: Collection exists but with WRONG dim (384)
        mock_coll = MagicMock()
        mock_coll.name = "memories"
        mock_client.get_collections.return_value = MagicMock(collections=[mock_coll])
        
        coll_info = MagicMock()
        coll_info.config.params.vectors = {"dense": MagicMock(size=384)}
        mock_client.get_collection.return_value = coll_info
        
        await store._ensure_collection()
        
        # Should delete and recreate
        mock_client.delete_collection.assert_called_with("memories")
        mock_client.create_collection.assert_called_once()

    @pytest.mark.asyncio
    async def test_batch_store_vectors_success(self, mock_client):
        store = QdrantVectorStore(client=mock_client)
        store._initialized = True # Skip ensure_collection logic
        
        mem_id = uuid4()
        vectors = [(mem_id, [0.1] * 384, {"tag": "test"})]
        
        res = await store.batch_store_vectors(vectors, tenant_id="t1")
        
        assert res == 1
        mock_client.upsert.assert_called_once()
        args, kwargs = mock_client.upsert.call_args
        point = kwargs["points"][0]
        assert point.id == str(mem_id)
        assert point.payload["tenant_id"] == "t1"
        assert point.payload["tag"] == "test"

    @pytest.mark.asyncio
    async def test_batch_store_named_vectors(self, mock_client):
        store = QdrantVectorStore(client=mock_client)
        store._initialized = True
        store._known_vectors = {"dense"}
        
        mem_id = uuid4()
        # Custom named vector "extra" not known yet
        vectors = [(mem_id, {"dense": [0.1]*384, "extra": [0.2]*128}, {})]
        
        # Mock get_collection for ensure_vector_config
        coll_info = MagicMock()
        coll_info.config.params.vectors = {"dense": MagicMock(size=384)}
        mock_client.get_collection.return_value = coll_info

        await store.batch_store_vectors(vectors, tenant_id="t1")
        
        # Should call update_collection for "extra"
        mock_client.update_collection.assert_called_once()
        assert "extra" in store._known_vectors

    @pytest.mark.asyncio
    async def test_get_vector_success(self, mock_client):
        store = QdrantVectorStore(client=mock_client)
        store._initialized = True
        
        mem_id = uuid4()
        mock_client.retrieve.return_value = [
            MagicMock(id=str(mem_id), payload={"tenant_id": "t1"}, vector={"dense": [0.1, 0.2]})
        ]
        
        res = await store.get_vector(mem_id, tenant_id="t1")
        assert res == [0.1, 0.2]

    @pytest.mark.asyncio
    async def test_get_vector_wrong_tenant(self, mock_client):
        store = QdrantVectorStore(client=mock_client)
        store._initialized = True
        
        mem_id = uuid4()
        mock_client.retrieve.return_value = [
            MagicMock(id=str(mem_id), payload={"tenant_id": "other"}, vector=[0.1])
        ]
        
        res = await store.get_vector(mem_id, tenant_id="t1")
        assert res is None

    @pytest.mark.asyncio
    async def test_delete_vector_tenant_safe(self, mock_client):
        store = QdrantVectorStore(client=mock_client)
        store._initialized = True
        
        mem_id = uuid4()
        # Mock: Point exists but belongs to OTHER tenant
        mock_client.retrieve.return_value = [MagicMock(payload={"tenant_id": "other"})]
        
        res = await store.delete_vector(mem_id, tenant_id="t1")
        assert res is False
        mock_client.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_search_similar_success(self, mock_client):
        store = QdrantVectorStore(client=mock_client)
        store._initialized = True
        
        mem_id = uuid4()
        mock_response = MagicMock()
        mock_response.points = [
            MagicMock(id=str(mem_id), score=0.95, payload={"memory_id": str(mem_id)})
        ]
        mock_client.query_points.return_value = mock_response
        
        res = await store.search_similar([0.1]*384, tenant_id="t1")
        
        assert len(res) == 1
        assert res[0][0] == mem_id
        assert res[0][1] == 0.95

    @pytest.mark.asyncio
    async def test_count_vectors(self, mock_client):
        store = QdrantVectorStore(client=mock_client)
        store._initialized = True
        
        mock_client.count.return_value = MagicMock(count=42)
        
        res = await store.count_vectors(tenant_id="t1")
        assert res == 42

    @pytest.mark.asyncio
    async def test_search_with_contradiction_penalty(self, mock_client):
        store = QdrantVectorStore(client=mock_client)
        store._initialized = True
        
        id1 = uuid4()
        # Mock search result
        mock_search = MagicMock()
        mock_search.points = [MagicMock(score=0.9, payload={"memory_id": str(id1)})]
        mock_client.query_points.return_value = mock_search
        
        # Mock get_vector (retrieve) for penalty calculation
        # Vector [1, 0] vs Query [1, 0] -> similarity 1.0 (no penalty)
        mock_client.retrieve.return_value = [
            MagicMock(payload={"tenant_id": "t1"}, vector={"dense": [1.0, 0.0]})
        ]
        
        results = await store.search_with_contradiction_penalty([1.0, 0.0], "t1")
        assert results[0][1] == 0.9 # Unchanged
        
        # Now mock vector [0, 1] vs Query [1, 0] -> similarity 0.0 (penalty!)
        mock_client.retrieve.return_value = [
            MagicMock(payload={"tenant_id": "t1"}, vector={"dense": [0.0, 1.0]})
        ]
        results = await store.search_with_contradiction_penalty([1.0, 0.0], "t1", penalty_factor=0.5)
        assert results[0][1] == 0.45 # 0.9 * 0.5
