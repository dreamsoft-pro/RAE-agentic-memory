import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from apps.memory_api.main import app
from apps.memory_api.models import ScoredMemoryRecord
from datetime import datetime

client = TestClient(app)

@pytest.fixture
def mock_vector_store():
    with patch("apps.memory_api.api.v1.memory.get_vector_store") as mock:
        instance = AsyncMock()
        instance.upsert = AsyncMock()
        instance.query = AsyncMock(return_value=[])
        instance.delete = AsyncMock()
        
        mock.return_value = instance
        yield instance

@pytest.fixture
def mock_embedding_service():
    with patch("apps.memory_api.api.v1.memory.get_embedding_service") as mock:
        instance = MagicMock()
        instance.generate_embeddings.return_value = [[0.1] * 384]
        mock.return_value = instance
        yield instance

@pytest.mark.asyncio
async def test_store_memory_success(mock_app_state_pool, mock_vector_store, mock_embedding_service):
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value
    
    mock_conn.fetchrow.return_value = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "created_at": datetime.now(),
        "last_accessed_at": datetime.now(),
        "usage_count": 0
    }

    # POPRAWKA: Dodano 'importance', aby uniknąć błędu walidacji w API
    payload = {
        "content": "Test content",
        "source": "cli",
        "layer": "ltm",
        "tags": ["test"],
        "project": "default",
        "importance": 0.5 
    }
    
    response = client.post(
        "/v1/memory/store", 
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"}
    )
    
    if response.status_code != 200:
        print("STORE ERROR:", response.json())

    assert response.status_code == 200
    assert response.json()["id"] == "123e4567-e89b-12d3-a456-426614174000"

@pytest.mark.asyncio
async def test_query_memory_success(mock_app_state_pool, mock_vector_store, mock_embedding_service):
    record = ScoredMemoryRecord(
        id="mem-1",
        content="Found",
        score=0.95,
        importance=0.5,
        layer="ltm",
        tags=[],
        source="src",
        project="proj",
        timestamp=datetime.now(),
        last_accessed_at=datetime.now(),
        usage_count=10
    )

    mock_vector_store.query.return_value = [record]

    payload = {"query_text": "test query", "k": 1}

    response = client.post(
        "/v1/memory/query",
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    assert len(response.json()["results"]) == 1

@pytest.mark.asyncio
async def test_delete_memory_success(mock_app_state_pool, mock_vector_store):
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value
    mock_conn.execute.return_value = "DELETE 1"

    response = client.delete(
        "/v1/memory/delete?memory_id=mem-1",
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200

@pytest.mark.asyncio
async def test_rebuild_reflections_success(mock_app_state_pool):
    """Test POST /v1/memory/rebuild-reflections endpoint"""
    with patch("apps.memory_api.api.v1.memory.generate_reflection_for_project") as mock_task:
        mock_task.delay = MagicMock(return_value=MagicMock(id="task-123"))

        payload = {
            "tenant_id": "test-tenant",
            "project": "test-project"
        }

        response = client.post(
            "/v1/memory/rebuild-reflections",
            json=payload,
            headers={"X-Tenant-Id": "test-tenant"}
        )

        assert response.status_code == 202
        assert "dispatched" in response.json()["message"].lower()

@pytest.mark.asyncio
async def test_reflection_stats_success(mock_app_state_pool):
    """Test GET /v1/memory/reflection-stats endpoint"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    # Mock database response
    mock_conn.fetchrow.return_value = {
        "reflective_memory_count": 42,
        "average_strength": 0.75
    }

    response = client.get(
        "/v1/memory/reflection-stats?project=test-project",
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["reflective_memory_count"] == 42
    assert data["average_strength"] == 0.75

@pytest.mark.asyncio
async def test_store_memory_missing_tenant_header(mock_app_state_pool, mock_vector_store, mock_embedding_service):
    """Test store memory without tenant header returns 400"""
    payload = {
        "content": "Test content",
        "source": "cli",
        "layer": "em",
        "importance": 0.5
    }

    response = client.post("/v1/memory/store", json=payload)

    assert response.status_code == 400
    assert "X-Tenant-Id" in response.json()["detail"]

@pytest.mark.asyncio
async def test_query_memory_with_filters(mock_app_state_pool, mock_vector_store, mock_embedding_service):
    """Test query memory with tag filters"""
    record = ScoredMemoryRecord(
        id="mem-1",
        content="Filtered result",
        score=0.90,
        importance=0.7,
        layer="em",
        tags=["filtered", "test"],
        source="src",
        project="proj",
        timestamp=datetime.now(),
        last_accessed_at=datetime.now(),
        usage_count=5
    )

    mock_vector_store.query.return_value = [record]

    payload = {
        "query_text": "test query",
        "k": 5,
        "filters": {"tags": ["filtered"]}
    }

    response = client.post(
        "/v1/memory/query",
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) == 1
    assert "filtered" in results[0]["tags"]

@pytest.mark.asyncio
async def test_query_memory_with_graph_traversal(mock_app_state_pool, mock_vector_store, mock_embedding_service):
    """Test query memory with GraphRAG (use_graph=true)"""
    with patch("apps.memory_api.api.v1.memory.get_hybrid_search_service") as mock_hybrid:
        mock_service = AsyncMock()
        mock_service.hybrid_search = AsyncMock(return_value={
            "results": [],
            "synthesized_context": "Graph context",
            "graph_statistics": {"nodes_traversed": 10}
        })
        mock_hybrid.return_value = mock_service

        payload = {
            "query_text": "test query",
            "k": 5,
            "use_graph": True,
            "graph_depth": 2,
            "project": "test-project"
        }

        response = client.post(
            "/v1/memory/query",
            json=payload,
            headers={"X-Tenant-Id": "test-tenant"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "synthesized_context" in data
        assert "graph_statistics" in data

@pytest.mark.asyncio
async def test_delete_memory_not_found(mock_app_state_pool, mock_vector_store):
    """Test delete memory that doesn't exist"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value
    mock_conn.execute.return_value = "DELETE 0"

    response = client.delete(
        "/v1/memory/delete?memory_id=nonexistent",
        headers={"X-Tenant-Id": "test-tenant"}
    )

    # Should still return 200 even if memory doesn't exist (idempotent)
    assert response.status_code == 200