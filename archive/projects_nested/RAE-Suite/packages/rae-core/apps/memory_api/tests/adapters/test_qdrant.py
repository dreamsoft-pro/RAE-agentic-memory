"""
Unit tests for QdrantVectorStore adapter.

Tests the QdrantStore implementation including:
- Initialization and collection check
- Upsert logic (dense + sparse generation)
- Query logic (dense + sparse + filters)
- Deletion
"""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from qdrant_client import models

from apps.memory_api.models import MemoryRecord
from apps.memory_api.services.vector_store.qdrant_store import QdrantStore


@pytest.fixture
def mock_qdrant_client():
    """Mock QdrantClient."""
    client = MagicMock()
    # Mock collections
    client.get_collections.return_value.collections = []
    # Mock upsert
    client.upsert = MagicMock()
    # Mock search
    client.search.return_value = []
    # Mock query_points (new API)
    client.query_points.return_value.points = []
    # Mock delete
    client.delete = MagicMock()
    return client


@pytest.fixture
def qdrant_store(mock_qdrant_client):
    """QdrantStore instance with mock client."""
    return QdrantStore(client=mock_qdrant_client)


@pytest.mark.asyncio
class TestQdrantVectorStore:
    """Tests for QdrantStore."""

    async def test_ensure_collection(self, qdrant_store, mock_qdrant_client):
        """Test collection creation if not exists."""
        # Setup: Collection does not exist
        mock_qdrant_client.get_collections.return_value.collections = []

        await qdrant_store.ainit()

        # Verify creation was called with named vectors
        mock_qdrant_client.create_collection.assert_called_once()
        call_kwargs = mock_qdrant_client.create_collection.call_args[1]
        assert call_kwargs["collection_name"] == "memories"
        assert "vectors_config" in call_kwargs
        # Default config includes dense, openai, ollama
        assert "dense" in call_kwargs["vectors_config"]
        assert "text" in call_kwargs["sparse_vectors_config"]

    async def test_store_vector(self, qdrant_store, mock_qdrant_client):
        """Test storing a single memory with vector."""
        memory = MemoryRecord(
            id=str(uuid4()),
            content="Test content for sparse vector generation",
            layer="episodic",
            tenant_id="tenant1",
            project_id="proj1",
        )
        embedding = [0.1, 0.2, 0.3]  # Dummy 3D vector

        await qdrant_store.upsert([memory], [embedding])

        # Verify upsert call
        mock_qdrant_client.upsert.assert_called_once()
        call_args = mock_qdrant_client.upsert.call_args
        assert call_args[1]["collection_name"] == "memories"
        points = call_args[1]["points"]
        assert len(points) == 1
        point = points[0]

        # Verify payload matches memory
        assert point.payload["id"] == str(memory.id)
        assert point.payload["content"] == memory.content

        # Verify vector structure (dense + sparse)
        assert "dense" in point.vector
        assert point.vector["dense"] == embedding
        assert "text" in point.vector
        # Sparse vector should be generated from content
        assert isinstance(point.vector["text"], models.SparseVector)
        assert len(point.vector["text"].indices) > 0

    async def test_batch_store_vectors(self, qdrant_store, mock_qdrant_client):
        """Test storing multiple vectors."""
        memories = [
            MemoryRecord(
                id=str(uuid4()),
                content="A",
                layer="episodic",
                tenant_id="t",
                project_id="p",
            ),
            MemoryRecord(
                id=str(uuid4()),
                content="B",
                layer="episodic",
                tenant_id="t",
                project_id="p",
            ),
        ]
        embeddings = [[0.1], [0.2]]

        await qdrant_store.upsert(memories, embeddings)

        mock_qdrant_client.upsert.assert_called_once()
        points = mock_qdrant_client.upsert.call_args[1]["points"]
        assert len(points) == 2

    async def test_search_similar(self, qdrant_store, mock_qdrant_client):
        """Test searching for similar vectors."""
        # Mock query response
        mock_point = MagicMock()
        mock_point.score = 0.95
        mock_point.payload = {
            "id": str(uuid4()),
            "content": "Match",
            "layer": "episodic",
            "tenant_id": "t",
            "project_id": "p",
        }
        mock_qdrant_client.query_points.return_value.points = [mock_point]

        query_vec = [0.1, 0.2, 0.3]

        # Qdrant filters must be structured (must/should/must_not), not flat KV pairs
        qdrant_filter = {
            "must": [
                models.FieldCondition(
                    key="tenant_id", match=models.MatchValue(value="t")
                )
            ]
        }

        results = await qdrant_store.query(
            query_embedding=query_vec, top_k=5, filters=qdrant_filter
        )

        assert len(results) == 1
        assert results[0].score == 0.95
        assert results[0].content == "Match"

        # Verify query call uses correct vector name
        mock_qdrant_client.query_points.assert_called_once()
        call_kwargs = mock_qdrant_client.query_points.call_args[1]
        assert call_kwargs["collection_name"] == "memories"
        assert call_kwargs["query"] == query_vec
        assert call_kwargs["using"] == "dense"
        assert call_kwargs["limit"] == 5

    async def test_get_vector(self):
        """Placeholder for get_vector (not implemented in base QdrantStore yet)."""
        pass

    async def test_delete_vector(self, qdrant_store, mock_qdrant_client):
        """Test deleting a vector."""
        mem_id = str(uuid4())
        await qdrant_store.delete(mem_id)

        mock_qdrant_client.delete.assert_called_once()
        call_kwargs = mock_qdrant_client.delete.call_args[1]
        assert call_kwargs["collection_name"] == "memories"
        # Verify point selector
        selector = call_kwargs["points_selector"]
        assert isinstance(selector, models.PointIdsList)
        assert selector.points == [mem_id]

    async def test_close(self):
        """Test resource cleanup (no-op for sync client wrapper but good to test)."""
        pass

    async def test_search_with_contradiction_penalty(self):
        """Test search with contradiction logic (mocked)."""
        # Logic resides in RAE Engine, not Store, but Store provides raw results.
        pass
