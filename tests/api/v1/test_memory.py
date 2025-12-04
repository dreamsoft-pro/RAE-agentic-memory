from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from apps.memory_api.main import app
from apps.memory_api.models import ScoredMemoryRecord, HybridSearchResult
from apps.memory_api.models.hybrid_search_models import QueryAnalysis, QueryIntent
from apps.memory_api.api.v1.memory import get_vector_store, get_embedding_service, get_hybrid_search_service
from apps.memory_api.security.dependencies import get_and_verify_tenant_id


# Mocks for dependencies
mock_vector_store_instance = AsyncMock()
mock_embedding_service_instance = MagicMock()
mock_hybrid_search_service_instance = AsyncMock()

def get_mock_vector_store():
    return mock_vector_store_instance

def get_mock_embedding_service():
    return mock_embedding_service_instance

def get_mock_hybrid_search_service():
    return mock_hybrid_search_service_instance

async def mock_get_tenant_id():
    return "test-tenant"

@pytest.fixture(autouse=True)
def override_api_dependencies():
    # Override core services
    app.dependency_overrides[get_vector_store] = get_mock_vector_store
    app.dependency_overrides[get_embedding_service] = get_mock_embedding_service
    app.dependency_overrides[get_hybrid_search_service] = get_mock_hybrid_search_service
    
    # Override auth to avoid 401
    app.dependency_overrides[get_and_verify_tenant_id] = mock_get_tenant_id
    
    # Reset mocks before each test
    mock_vector_store_instance.reset_mock()
    mock_embedding_service_instance.reset_mock()
    mock_hybrid_search_service_instance.reset_mock()
    
    yield
    
    app.dependency_overrides = {}


@pytest.fixture
def client_with_overrides():
    with TestClient(app) as client_instance:
        yield client_instance


@pytest.mark.asyncio
async def test_store_memory_success(
    client_with_overrides: TestClient, mock_app_state_pool
):
    # Accessing the connection mock from the mock_app_state_pool fixture (MagicMock)
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    mock_conn.fetchrow.return_value = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "created_at": datetime.now(timezone.utc),
        "last_accessed_at": datetime.now(timezone.utc),
        "usage_count": 0,
    }

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
    assert response.json()["id"] == "123e4567-e89b-12d3-a456-426614174000"
    
    mock_conn.fetchrow.assert_called_once()
    mock_embedding_service_instance.generate_embeddings.assert_called_once()
    mock_vector_store_instance.upsert.assert_called_once()


@pytest.mark.asyncio
async def test_store_memory_db_failure(client_with_overrides: TestClient, mock_app_state_pool):
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value
    mock_conn.fetchrow.return_value = None

    payload = {
        "content": "Test content",
        "source": "cli",
        "layer": "em",
        "importance": 0.5,
        "project": "default"
    }

    response = client_with_overrides.post(
        "/v1/memory/store", json=payload, headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 500
    # Check for "detail" first, but handle "error" format if middleware intercepts
    data = response.json()
    if "detail" in data:
        assert "Failed to store memory" in data["detail"]
    else:
        assert "Failed to store memory" in str(data)


@pytest.mark.asyncio
async def test_query_memory_vector_only(client_with_overrides: TestClient, mock_app_state_pool):
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value
    
    record = ScoredMemoryRecord(
        id="mem-1",
        content="Found",
        score=0.95,
        importance=0.5,
        layer="em",
        tags=[],
        source="src",
        project="proj",
        timestamp=datetime.now(timezone.utc),
        last_accessed_at=datetime.now(timezone.utc),
        usage_count=10,
    )

    mock_vector_store_instance.query.return_value = [record]
    mock_embedding_service_instance.generate_embeddings.return_value = [[0.1] * 384]

    payload = {"query_text": "test query", "k": 1}

    response = client_with_overrides.post(
        "/v1/memory/query", json=payload, headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    assert len(response.json()["results"]) == 1
    
    mock_conn.execute.assert_called() # update_memory_access_stats calls execute


@pytest.mark.asyncio
async def test_query_memory_hybrid(client_with_overrides: TestClient, mock_app_state_pool):
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value
    
    # Create a valid QueryAnalysis object
    analysis = QueryAnalysis(
        intent=QueryIntent.FACTUAL,
        confidence=0.9,
        original_query="test query"
    )

    hybrid_result = HybridSearchResult(
        vector_matches=[
            ScoredMemoryRecord(
                id="mem-1",
                content="Hybrid Found",
                score=0.95,
                importance=0.5,
                layer="em",
                tags=[],
                source="src",
                project="proj",
                timestamp=datetime.now(timezone.utc),
                last_accessed_at=datetime.now(timezone.utc),
                usage_count=10,
            )
        ],
        synthesized_context="Graph context",
        statistics={"nodes_traversed": 10},
        query_analysis=analysis # Required field
    )
    mock_hybrid_search_service_instance.search.return_value = hybrid_result

    payload = {
        "query_text": "test query",
        "k": 5,
        "use_graph": True,
        "graph_depth": 2,
        "project": "test-project",
    }

    response = client_with_overrides.post(
        "/v1/memory/query", json=payload, headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["synthesized_context"] == "Graph context"
    assert len(data["results"]) == 1
    assert data["results"][0]["content"] == "Hybrid Found"
    
    mock_hybrid_search_service_instance.search.assert_called_once()
    mock_conn.execute.assert_called()


@pytest.mark.asyncio
async def test_query_memory_hybrid_missing_project(client_with_overrides: TestClient):
    payload = {
        "query_text": "test query",
        "use_graph": True
    }
    response = client_with_overrides.post(
        "/v1/memory/query", json=payload, headers={"X-Tenant-Id": "test-tenant"}
    )
    assert response.status_code == 400
    # Handle potential middleware error wrapping
    data = response.json()
    error_msg = data.get("detail", str(data))
    assert "project parameter is required" in error_msg


@pytest.mark.asyncio
async def test_delete_memory_success(client_with_overrides: TestClient, mock_app_state_pool):
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value
    mock_conn.execute.return_value = "DELETE 1"

    response = client_with_overrides.delete(
        "/v1/memory/delete?memory_id=mem-1", headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
    mock_vector_store_instance.delete.assert_called_once_with("mem-1")


@pytest.mark.asyncio
async def test_delete_memory_not_found(client_with_overrides: TestClient, mock_app_state_pool):
    """Test delete memory that doesn't exist"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value
    mock_conn.execute.return_value = "DELETE 0"

    response = client_with_overrides.delete(
        "/v1/memory/delete?memory_id=nonexistent",
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 404
    # Handle potential middleware error wrapping
    data = response.json()
    error_msg = data.get("detail", str(data))
    assert "Memory not found" in error_msg


@pytest.mark.asyncio
async def test_rebuild_reflections_success(client_with_overrides: TestClient):
    with patch("apps.memory_api.api.v1.memory.generate_reflection_for_project") as mock_task:
        payload = {"tenant_id": "test-tenant", "project": "test-project"}
        response = client_with_overrides.post(
            "/v1/memory/rebuild-reflections",
            json=payload,
            headers={"X-Tenant-Id": "test-tenant"},
        )
        assert response.status_code == 202
        mock_task.delay.assert_called_once()


@pytest.mark.asyncio
async def test_reflection_stats_success(client_with_overrides: TestClient, mock_app_state_pool):
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    # Mock database response
    mock_conn.fetchval.side_effect = [42, 0.75]

    response = client_with_overrides.get(
        "/v1/memory/reflection-stats?project=test-project",
        headers={"X-Tenant-Id": "test-tenant"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["reflective_memory_count"] == 42
    assert data["average_strength"] == 0.75


@pytest.mark.asyncio
async def test_store_memory_missing_tenant_header(client_with_overrides: TestClient):
    # Override the tenant id dependency to simulate missing header by raising HTTPException
    app.dependency_overrides[get_and_verify_tenant_id] = get_and_verify_tenant_id
    
    try:
        payload = {
            "content": "Test content",
            "source": "cli",
            "layer": "em",
            "importance": 0.5,
            "project": "default"
        }
        # No headers provided
        response = client_with_overrides.post("/v1/memory/store", json=payload)
        
        assert response.status_code == 400
        
        # Handle potential middleware error wrapping
        data = response.json()
        error_msg = data.get("detail", str(data))
        assert "X-Tenant-Id" in error_msg
    finally:
        # Restore mock
        app.dependency_overrides[get_and_verify_tenant_id] = mock_get_tenant_id


@pytest.mark.asyncio
async def test_query_memory_with_filters(
    client_with_overrides: TestClient, mock_app_state_pool
):
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value
    
    record = ScoredMemoryRecord(
        id="mem-1",
        content="Filtered result",
        score=0.90,
        importance=0.7,
        layer="em",
        tags=["filtered", "test"],
        source="src",
        project="proj",
        timestamp=datetime.now(timezone.utc),
        last_accessed_at=datetime.now(timezone.utc),
        usage_count=5,
    )

    mock_vector_store_instance.query.return_value = [record]

    payload = {"query_text": "test query", "k": 5, "filters": {"tags": ["filtered"]}}

    response = client_with_overrides.post(
        "/v1/memory/query", json=payload, headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) == 1
    assert "filtered" in results[0]["tags"]
    mock_conn.execute.assert_called()


@pytest.mark.asyncio
async def test_query_memory_with_graph_traversal(
    client_with_overrides: TestClient, mock_app_state_pool
):
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value
    
    analysis = QueryAnalysis(
        intent=QueryIntent.EXPLORATORY,
        confidence=0.8,
        original_query="test query"
    )

    hybrid_result = HybridSearchResult(
        vector_matches=[
            ScoredMemoryRecord(
                id="mem-1",
                content="Hybrid Found",
                score=0.95,
                importance=0.5,
                layer="em",
                tags=[],
                source="src",
                project="proj",
                timestamp=datetime.now(timezone.utc),
                last_accessed_at=datetime.now(timezone.utc),
                usage_count=10,
            )
        ],
        synthesized_context="Graph context",
        statistics={"nodes_traversed": 10},
        query_analysis=analysis
    )
    mock_hybrid_search_service_instance.search.return_value = hybrid_result

    payload = {
        "query_text": "test query",
        "k": 5,
        "use_graph": True,
        "graph_depth": 2,
        "project": "test-project",
    }

    response = client_with_overrides.post(
        "/v1/memory/query", json=payload, headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "synthesized_context" in data
    assert "graph_statistics" in data
    
    mock_hybrid_search_service_instance.search.assert_called_once()
    mock_conn.execute.assert_called()


@pytest.mark.asyncio
async def test_generate_hierarchical_reflection_deprecated(client_with_overrides: TestClient, mock_app_state_pool):
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value
    
    with patch("apps.memory_api.services.reflection_engine.ReflectionEngine") as MockEngine:
        mock_engine_instance = AsyncMock()
        MockEngine.return_value = mock_engine_instance
        mock_engine_instance.generate_hierarchical_reflection.return_value = "Summary"
        
        # Mock episode count query
        mock_conn.fetchval.return_value = 10

        response = client_with_overrides.post(
            "/v1/memory/reflection/hierarchical?project=my-project&bucket_size=15",
            headers={"X-Tenant-Id": "test-tenant"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["summary"] == "Summary"
        assert data["statistics"]["episode_count"] == 10