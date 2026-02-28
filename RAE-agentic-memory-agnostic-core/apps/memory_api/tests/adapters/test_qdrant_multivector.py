"""
Tests for Qdrant Multi-Vector (Named Vectors) Support.

Verifies the 'RAE Stores embeddings from different models in separate, named vector spaces'
requirement. This ensures RAE can handle agents using different embedding models
(e.g., OpenAI 1536d vs Ollama 768d vs Local 384d) without dimension mismatch errors.
"""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from apps.memory_api.models import MemoryRecord
from apps.memory_api.services.vector_store.qdrant_store import QdrantStore


@pytest.fixture
def mock_qdrant_client():
    client = MagicMock()
    client.get_collections.return_value.collections = []
    client.upsert = MagicMock()
    client.query_points.return_value.points = []
    return client


@pytest.fixture
def qdrant_store(mock_qdrant_client):
    return QdrantStore(client=mock_qdrant_client)


@pytest.mark.asyncio
async def test_ensure_collection_multivector(qdrant_store, mock_qdrant_client):
    """Verify collection is created with multiple named vectors configuration."""
    await qdrant_store.ainit()

    mock_qdrant_client.create_collection.assert_called_once()
    config = mock_qdrant_client.create_collection.call_args[1]["vectors_config"]

    # Must support standard named vectors defined in RAE specs
    assert "dense" in config
    assert "openai" in config  # 1536d
    assert "ollama" in config  # 768d

    assert config["openai"].size == 1536
    assert config["ollama"].size == 768


@pytest.mark.asyncio
async def test_add_vector_determines_name(qdrant_store, mock_qdrant_client):
    """
    Test that upsert handles explicit dictionary embeddings (Named Vectors).
    This mimics the behavior when RAE detects a specific model is being used.
    """
    memory = MemoryRecord(
        id=str(uuid4()),
        content="Multi-vector content",
        layer="episodic",
        tenant_id="t1",
        project_id="p1",
    )

    # Embedding passed as a dictionary mapping name -> vector
    # This is how RAE Core passes multi-model embeddings
    embeddings = [
        {
            "dense": [0.1] * 384,
            "openai": [0.2] * 1536,
        }
    ]

    await qdrant_store.upsert([memory], embeddings)

    # Verify upsert payload
    mock_qdrant_client.upsert.assert_called_once()
    points = mock_qdrant_client.upsert.call_args[1]["points"]
    point = points[0]

    # Check vector payload structure
    assert isinstance(point.vector, dict)
    assert "dense" in point.vector
    assert "openai" in point.vector
    assert "text" in point.vector  # Sparse vector automatically added

    assert len(point.vector["dense"]) == 384
    assert len(point.vector["openai"]) == 1536


@pytest.mark.asyncio
async def test_search_uses_correct_vector(qdrant_store, mock_qdrant_client):
    """
    Test querying a specific named vector space.
    If an agent uses OpenAI, we should query the 'openai' vector space.
    """
    query_vec = [0.9] * 1536  # OpenAI dimension

    await qdrant_store.query(
        query_embedding=query_vec,
        top_k=5,
        filters=None,
        vector_name="openai",  # Explicitly targeting openai space
    )

    mock_qdrant_client.query_points.assert_called_once()
    call_kwargs = mock_qdrant_client.query_points.call_args[1]

    assert call_kwargs["using"] == "openai"
    assert call_kwargs["query"] == query_vec
