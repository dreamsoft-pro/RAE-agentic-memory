from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch, MagicMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from apps.memory_api.dependencies import get_rae_core_service, get_qdrant_client
from apps.memory_api.main import app
from apps.memory_api.models import (
    MemoryRecord,
    QueryMemoryRequest,
    StoreMemoryRequest,
    ScoredMemoryRecord,
)
from apps.memory_api.services.rae_core_service import RAECoreService
from apps.memory_api.security.dependencies import get_and_verify_tenant_id
from apps.memory_api.services.embedding import get_embedding_service
from apps.memory_api.services.vector_store import get_vector_store
from apps.memory_api.tests.conftest import mock_pool


@pytest.fixture
def mock_rae_service():
    """Mock for RAECoreService."""
    service = AsyncMock(spec=RAECoreService)
    
    # Setup store_memory return
    service.store_memory.return_value = "test-memory-id"
    
    # Setup delete_memory return
    service.delete_memory.return_value = True
    
    # Setup list_memories return
    service.list_memories.return_value = []
    
    # Setup count_memories return
    service.count_memories.return_value = 10
    
    # Setup get_metric_aggregate return
    service.get_metric_aggregate.return_value = 0.7
    
    # Setup update_memory_access_batch
    service.update_memory_access_batch.return_value = 1
    
    return service


@pytest.fixture
def mock_embedding_service():
    """Mock for EmbeddingService."""
    service = MagicMock()
    service.generate_embeddings.return_value = [[0.1] * 384]
    return service


@pytest.fixture
def mock_vector_store():
    """Mock for VectorStore."""
    store = AsyncMock()
    store.upsert.return_value = None
    store.delete.return_value = None
    store.query.return_value = []
    return store


@pytest.fixture
def client_with_overrides(mock_pool, mock_rae_service, mock_embedding_service, mock_vector_store):
    """
    Test client with all necessary overrides for memory endpoints.
    """
    # Setup mock pool
    app.state.pool = mock_pool
    
    # Override auth
    async def _mock_tenant():
        return "test-tenant"
    
    # Setup dependency overrides
    app.dependency_overrides[get_and_verify_tenant_id] = _mock_tenant
    app.dependency_overrides[get_rae_core_service] = lambda: mock_rae_service
    
    # Mock Qdrant client
    mock_qdrant = AsyncMock()
    mock_health = MagicMock()
    mock_health.status = "ok"
    mock_qdrant.health_check = AsyncMock(return_value=mock_health)
    app.dependency_overrides[get_qdrant_client] = lambda: mock_qdrant

    # Patch services obtained via functions (not DI in older parts)
    with patch(
        "apps.memory_api.api.v1.memory.get_embedding_service",
        return_value=mock_embedding_service
    ), patch(
        "apps.memory_api.api.v1.memory.get_vector_store",
        return_value=mock_vector_store
    ), patch(
        "apps.memory_api.main.asyncpg.create_pool",
        new=AsyncMock(return_value=mock_pool)
    ), patch(
        "apps.memory_api.main.rebuild_full_cache", new=AsyncMock()
    ):
        with TestClient(app) as client:
            yield client
            
    # Cleanup
    app.dependency_overrides = {}
    if hasattr(app.state, "pool"):
        del app.state.pool


@pytest.mark.asyncio
async def test_store_memory_success(client_with_overrides, mock_rae_service):
    """Test successful memory storage via RAECoreService."""
    payload = {
        "content": "Test content",
        "source": "cli",
        "layer": "em",
        "tags": ["test"],
        "project": "default",
        "importance": 0.5,
    }

    response = client_with_overrides.post(
        "/v1/memory/store", json=payload, headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    assert response.json()["id"] == "test-memory-id"

    # Verify RAECoreService was called correctly
    mock_rae_service.store_memory.assert_called_once()
    call_args = mock_rae_service.store_memory.call_args[1]
    assert call_args["content"] == "Test content"
    assert call_args["source"] == "cli"
    assert call_args["project"] == "default"


@pytest.mark.asyncio
async def test_store_memory_failure(client_with_overrides, mock_rae_service):
    """Test handling of storage failure."""
    mock_rae_service.store_memory.side_effect = Exception("Storage Error")

    payload = {
        "content": "Test content",
        "source": "cli",
        "project": "default",
        "importance": 0.5,
    }

    response = client_with_overrides.post(
        "/v1/memory/store", json=payload, headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 500
    assert "Storage error" in response.json()["error"]["message"]


@pytest.mark.asyncio
async def test_query_memory_vector_only(client_with_overrides, mock_vector_store, mock_rae_service):
    """Test memory query using vector search."""
    # Mock vector store results
    record = ScoredMemoryRecord(
        id="mem-1",
        tenant_id="test-tenant",
        project="proj",
        content="Found content",
        score=0.95,
        importance=0.5,
        layer="em",
        tags=[],
        source="src",
        created_at=datetime.now(timezone.utc),
        last_accessed_at=datetime.now(timezone.utc),
        usage_count=5,
    )
    mock_vector_store.query.return_value = [record]

    payload = {"query_text": "test query", "k": 1}

    response = client_with_overrides.post(
        "/v1/memory/query", json=payload, headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data["results"]) == 1
    assert data["results"][0]["id"] == "mem-1"

    # Verify stats update called on RAECoreService
    mock_rae_service.update_memory_access_batch.assert_called_once()


@pytest.mark.asyncio
async def test_delete_memory_success(client_with_overrides, mock_rae_service, mock_vector_store):
    """Test successful memory deletion."""
    mock_rae_service.delete_memory.return_value = True

    response = client_with_overrides.delete(
        "/v1/memory/delete?memory_id=mem-1", headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
    
    mock_rae_service.delete_memory.assert_called_once_with("mem-1", "test-tenant")
    mock_vector_store.delete.assert_called_once_with("mem-1")


@pytest.mark.asyncio
async def test_delete_memory_not_found(client_with_overrides, mock_rae_service):
    """Test delete memory that doesn't exist."""
    mock_rae_service.delete_memory.return_value = False

    response = client_with_overrides.delete(
        "/v1/memory/delete?memory_id=nonexistent",
        headers={"X-Tenant-Id": "test-tenant"},
    )

    assert response.status_code == 404
    assert "not found" in response.json()["error"]["message"].lower()


@pytest.mark.asyncio
async def test_reflection_stats(client_with_overrides, mock_rae_service):
    """Test retrieval of reflection statistics."""
    mock_rae_service.count_memories.return_value = 42
    mock_rae_service.get_metric_aggregate.return_value = 0.75

    response = client_with_overrides.get(
        "/v1/memory/reflection-stats?project=test-project",
        headers={"X-Tenant-Id": "test-tenant"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["reflective_memory_count"] == 42
    assert data["average_strength"] == 0.75
    
    mock_rae_service.count_memories.assert_called_once()
    mock_rae_service.get_metric_aggregate.assert_called_once()


@pytest.mark.asyncio
async def test_hierarchical_reflection_deprecated(client_with_overrides, mock_rae_service):
    """Test deprecated hierarchical reflection endpoint."""
    with patch(
        "apps.memory_api.services.reflection_engine.ReflectionEngine"
    ) as MockEngine:
        mock_engine_instance = AsyncMock()
        MockEngine.return_value = mock_engine_instance
        mock_engine_instance.generate_hierarchical_reflection.return_value = "Summary"

        # Mock stats
        mock_rae_service.count_memories.return_value = 10

        response = client_with_overrides.post(
            "/v1/memory/reflection/hierarchical?project=my-project&bucket_size=15",
            headers={"X-Tenant-Id": "test-tenant"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["summary"] == "Summary"
        assert data["statistics"]["episode_count"] == 10