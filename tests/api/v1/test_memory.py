from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from apps.memory_api.main import app
from apps.memory_api.models import ScoredMemoryRecord
from apps.memory_api.models.hybrid_search_models import (
    HybridSearchResult, 
    QueryAnalysis, 
    QueryIntent,
    SearchResultItem
)
from apps.memory_api.api.v1.memory import get_vector_store, get_embedding_service, get_hybrid_search_service
from apps.memory_api.security.dependencies import get_and_verify_tenant_id


# Define fixtures for mocks
@pytest.fixture
def mock_vector_store():
    return AsyncMock()

@pytest.fixture
def mock_embedding_service():
    return MagicMock()

@pytest.fixture
def mock_hybrid_search_service():
    return AsyncMock()

@pytest.fixture
async def mock_get_tenant_id():
    return "test-tenant"

@pytest.fixture(autouse=True)
def mock_pii_scrubber():
    with patch("apps.memory_api.api.v1.memory.pii_scrubber") as mock_scrubber:
        mock_scrubber.scrub_text.side_effect = lambda x: x
        yield mock_scrubber

@pytest.fixture(autouse=True)
def mock_memory_repo():
    with patch("apps.memory_api.api.v1.memory.MemoryRepository") as MockRepo:
        mock_repo_instance = AsyncMock()
        MockRepo.return_value = mock_repo_instance
        yield mock_repo_instance

@pytest.fixture(autouse=True)
def override_api_dependencies(mock_vector_store, mock_embedding_service, mock_hybrid_search_service):
    # Override core services
    app.dependency_overrides[get_vector_store] = lambda: mock_vector_store
    app.dependency_overrides[get_embedding_service] = lambda: mock_embedding_service
    app.dependency_overrides[get_hybrid_search_service] = lambda: mock_hybrid_search_service
    
    # Override auth to avoid 401
    async def _mock_tenant():
        return "test-tenant"
    app.dependency_overrides[get_and_verify_tenant_id] = _mock_tenant
    
    yield
    
    app.dependency_overrides = {}


@pytest.fixture
def client_with_overrides(mock_app_state_pool):
    app.state.pool = MagicMock()
    with TestClient(app) as client_instance:
        yield client_instance
    if hasattr(app.state, "pool"):
        del app.state.pool


@pytest.mark.asyncio
async def test_store_memory_success(
    client_with_overrides: TestClient, 
    mock_memory_repo, 
    mock_embedding_service, 
    mock_vector_store
):
    mock_memory_repo.insert_memory.return_value = {
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
    
    mock_memory_repo.insert_memory.assert_called_once()
    mock_embedding_service.generate_embeddings.assert_called_once()
    mock_vector_store.upsert.assert_called_once()


@pytest.mark.asyncio
async def test_store_memory_db_failure(client_with_overrides: TestClient, mock_memory_repo):
    mock_memory_repo.insert_memory.side_effect = Exception("DB Error")

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
    data = response.json()
    error_msg = data.get("detail", str(data))
    assert "Database error" in error_msg


@pytest.mark.asyncio
async def test_query_memory_vector_only(
    client_with_overrides: TestClient, 
    mock_memory_repo,
    mock_vector_store,
    mock_embedding_service
):
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

    mock_vector_store.query.return_value = [record]
    mock_embedding_service.generate_embeddings.return_value = [[0.1] * 384]

    payload = {"query_text": "test query", "k": 1}

    response = client_with_overrides.post(
        "/v1/memory/query", json=payload, headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    assert len(response.json()["results"]) == 1
    
    mock_memory_repo.update_memory_access_stats.assert_called()


@pytest.mark.asyncio
async def test_query_memory_hybrid(
    client_with_overrides: TestClient, 
    mock_memory_repo,
    mock_hybrid_search_service
):
    # Create a valid QueryAnalysis object
    analysis = QueryAnalysis(
        intent=QueryIntent.FACTUAL,
        confidence=0.9,
        original_query="test query"
    )

    hybrid_result = HybridSearchResult(
        results=[
            SearchResultItem(
                memory_id=uuid4(),
                content="Hybrid Found",
                final_score=0.95,
                hybrid_score=0.95,
                rank=1,
                created_at=datetime.now(timezone.utc),
                metadata={
                    "importance": 0.5,
                    "layer": "em",
                    "source": "src",
                    "project": "proj",
                    "last_accessed_at": datetime.now(timezone.utc),
                    "usage_count": 10
                }
            )
        ],
        query_analysis=analysis,
        vector_results_count=1,
        semantic_results_count=0,
        graph_results_count=0,
        fulltext_results_count=0,
        total_results=1,
        total_time_ms=100
    )
    mock_hybrid_search_service.search.return_value = hybrid_result

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
    # synthesized_context removed from API logic so it should be null
    assert data.get("synthesized_context") is None 
    assert len(data["results"]) == 1
    assert data["results"][0]["content"] == "Hybrid Found"
    assert data["graph_statistics"]["total_results"] == 1
    
    mock_hybrid_search_service.search.assert_called_once()
    mock_memory_repo.update_memory_access_stats.assert_called()


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
    data = response.json()
    error_msg = data.get("detail", str(data))
    assert "project parameter is required" in error_msg


@pytest.mark.asyncio
async def test_delete_memory_success(
    client_with_overrides: TestClient, 
    mock_memory_repo,
    mock_vector_store
):
    mock_memory_repo.delete_memory.return_value = True

    response = client_with_overrides.delete(
        "/v1/memory/delete?memory_id=mem-1", headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
    mock_vector_store.delete.assert_called_once_with("mem-1")


@pytest.mark.asyncio
async def test_delete_memory_not_found(client_with_overrides: TestClient, mock_memory_repo):
    """Test delete memory that doesn't exist"""
    mock_memory_repo.delete_memory.return_value = False

    response = client_with_overrides.delete(
        "/v1/memory/delete?memory_id=nonexistent",
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 404
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
async def test_reflection_stats_success(client_with_overrides: TestClient, mock_memory_repo):
    # Mock repository response
    mock_memory_repo.count_memories_by_layer.return_value = 42
    mock_memory_repo.get_average_strength.return_value = 0.75

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
    # Override the tenant id dependency to simulate missing header
    async def _mock_missing():
        raise Exception("Missing") # Actually HTTPException in real code but here we just need fail
    
    # Actually let's rely on default behavior if we don't override
    # But we autouse override.
    # So we need to override locally
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
        data = response.json()
        error_msg = data.get("detail", str(data))
        assert "X-Tenant-Id" in error_msg
    finally:
        # Restore mock (actually fixture handles cleanup, but for safety)
        pass


@pytest.mark.asyncio
async def test_query_memory_with_filters(
    client_with_overrides: TestClient, 
    mock_memory_repo,
    mock_vector_store
):
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

    mock_vector_store.query.return_value = [record]

    payload = {"query_text": "test query", "k": 5, "filters": {"tags": ["filtered"]}}

    response = client_with_overrides.post(
        "/v1/memory/query", json=payload, headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) == 1
    assert "filtered" in results[0]["tags"]
    mock_memory_repo.update_memory_access_stats.assert_called()


@pytest.mark.asyncio
async def test_query_memory_with_graph_traversal(
    client_with_overrides: TestClient, 
    mock_memory_repo,
    mock_hybrid_search_service
):
    analysis = QueryAnalysis(
        intent=QueryIntent.EXPLORATORY,
        confidence=0.8,
        original_query="test query"
    )

    hybrid_result = HybridSearchResult(
        results=[
            SearchResultItem(
                memory_id=uuid4(),
                content="Hybrid Found",
                final_score=0.95,
                hybrid_score=0.95,
                rank=1,
                created_at=datetime.now(timezone.utc),
                metadata={
                    "importance": 0.5,
                    "layer": "em",
                    "source": "src",
                    "project": "proj",
                    "last_accessed_at": datetime.now(timezone.utc),
                    "usage_count": 10
                }
            )
        ],
        query_analysis=analysis,
        vector_results_count=1,
        semantic_results_count=0,
        graph_results_count=0,
        fulltext_results_count=0,
        total_results=1,
        total_time_ms=100
    )
    mock_hybrid_search_service.search.return_value = hybrid_result

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
    assert data.get("synthesized_context") is None
    assert data["graph_statistics"]["total_results"] == 1
    
    mock_hybrid_search_service.search.assert_called_once()
    mock_memory_repo.update_memory_access_stats.assert_called()


@pytest.mark.asyncio
async def test_generate_hierarchical_reflection_deprecated(client_with_overrides: TestClient, mock_memory_repo):
    with patch("apps.memory_api.services.reflection_engine.ReflectionEngine") as MockEngine:
        mock_engine_instance = AsyncMock()
        MockEngine.return_value = mock_engine_instance
        mock_engine_instance.generate_hierarchical_reflection.return_value = "Summary"
        
        # Mock episode count query
        mock_memory_repo.count_memories_by_layer.return_value = 10

        response = client_with_overrides.post(
            "/v1/memory/reflection/hierarchical?project=my-project&bucket_size=15",
            headers={"X-Tenant-Id": "test-tenant"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["summary"] == "Summary"
        assert data["statistics"]["episode_count"] == 10