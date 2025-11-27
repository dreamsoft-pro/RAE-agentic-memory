import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from apps.memory_api.main import app
from datetime import datetime

client = TestClient(app)


@pytest.fixture
def mock_hybrid_search_service():
    with patch("apps.memory_api.routes.hybrid_search.HybridSearchService") as mock:
        instance = MagicMock()
        instance.search = AsyncMock()
        mock.return_value = instance
        yield instance


@pytest.mark.asyncio
async def test_hybrid_search_success(mock_app_state_pool, mock_hybrid_search_service):
    """Test POST /v1/search/hybrid with successful search"""
    mock_result = MagicMock()
    mock_result.total_results = 5
    mock_result.total_time_ms = 123.45
    mock_result.results = []
    mock_result.weights_used = {"vector": 0.4, "semantic": 0.3, "graph": 0.2, "fulltext": 0.1}
    mock_result.query_analysis = {"intent": "factual_lookup"}

    mock_hybrid_search_service.search.return_value = mock_result

    payload = {
        "tenant_id": "test-tenant",
        "project_id": "test-project",
        "query": "authentication system",
        "k": 10,
        "enable_vector_search": True,
        "enable_semantic_search": True,
        "enable_graph_search": True,
        "enable_fulltext_search": True
    }

    response = client.post(
        "/v1/search/hybrid",
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "search_result" in data
    assert "message" in data


@pytest.mark.asyncio
async def test_hybrid_search_with_reranking(mock_app_state_pool, mock_hybrid_search_service):
    """Test hybrid search with LLM re-ranking enabled"""
    mock_result = MagicMock()
    mock_result.total_results = 3
    mock_result.total_time_ms = 250.0
    mock_result.results = []
    mock_result.weights_used = {"vector": 0.5, "semantic": 0.3, "graph": 0.2}
    mock_result.query_analysis = {"intent": "exploratory"}

    mock_hybrid_search_service.search.return_value = mock_result

    payload = {
        "tenant_id": "test-tenant",
        "project_id": "test-project",
        "query": "explain the authentication flow",
        "k": 5,
        "enable_vector_search": True,
        "enable_semantic_search": True,
        "enable_graph_search": True,
        "enable_fulltext_search": False,
        "enable_reranking": True,
        "reranking_model": "claude-3-5-sonnet-20241022"
    }

    response = client.post(
        "/v1/search/hybrid",
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "search_result" in data


@pytest.mark.asyncio
async def test_hybrid_search_with_filters(mock_app_state_pool, mock_hybrid_search_service):
    """Test hybrid search with temporal and tag filters"""
    mock_result = MagicMock()
    mock_result.total_results = 2
    mock_result.total_time_ms = 89.5
    mock_result.results = []
    mock_result.weights_used = {"vector": 0.6, "semantic": 0.4}
    mock_result.query_analysis = {"intent": "temporal_query"}

    mock_hybrid_search_service.search.return_value = mock_result

    payload = {
        "tenant_id": "test-tenant",
        "project_id": "test-project",
        "query": "recent security updates",
        "k": 10,
        "enable_vector_search": True,
        "enable_semantic_search": True,
        "enable_graph_search": False,
        "enable_fulltext_search": True,
        "temporal_filter": {
            "start_date": "2025-01-01T00:00:00Z",
            "end_date": "2025-12-31T23:59:59Z"
        },
        "tag_filter": ["security", "updates"],
        "min_importance": 0.5
    }

    response = client.post(
        "/v1/search/hybrid",
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "search_result" in data


@pytest.mark.asyncio
async def test_hybrid_search_with_manual_weights(mock_app_state_pool, mock_hybrid_search_service):
    """Test hybrid search with manually specified weights"""
    mock_result = MagicMock()
    mock_result.total_results = 8
    mock_result.total_time_ms = 150.2
    mock_result.results = []
    mock_result.weights_used = {"vector": 0.7, "semantic": 0.2, "graph": 0.1}
    mock_result.query_analysis = None  # Manual weights override analysis

    mock_hybrid_search_service.search.return_value = mock_result

    payload = {
        "tenant_id": "test-tenant",
        "project_id": "test-project",
        "query": "database optimization",
        "k": 15,
        "enable_vector_search": True,
        "enable_semantic_search": True,
        "enable_graph_search": True,
        "enable_fulltext_search": False,
        "manual_weights": {
            "vector": 0.7,
            "semantic": 0.2,
            "graph": 0.1,
            "fulltext": 0.0
        }
    }

    response = client.post(
        "/v1/search/hybrid",
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "search_result" in data


@pytest.mark.asyncio
async def test_hybrid_search_with_graph_depth(mock_app_state_pool, mock_hybrid_search_service):
    """Test hybrid search with custom graph traversal depth"""
    mock_result = MagicMock()
    mock_result.total_results = 12
    mock_result.total_time_ms = 300.0
    mock_result.results = []
    mock_result.weights_used = {"vector": 0.3, "semantic": 0.3, "graph": 0.4}
    mock_result.query_analysis = {"intent": "exploratory"}

    mock_hybrid_search_service.search.return_value = mock_result

    payload = {
        "tenant_id": "test-tenant",
        "project_id": "test-project",
        "query": "knowledge graph relationships",
        "k": 20,
        "enable_vector_search": True,
        "enable_semantic_search": True,
        "enable_graph_search": True,
        "enable_fulltext_search": True,
        "graph_max_depth": 3
    }

    response = client.post(
        "/v1/search/hybrid",
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "search_result" in data


@pytest.mark.asyncio
async def test_hybrid_search_with_conversation_history(mock_app_state_pool, mock_hybrid_search_service):
    """Test hybrid search with conversation context"""
    mock_result = MagicMock()
    mock_result.total_results = 6
    mock_result.total_time_ms = 180.0
    mock_result.results = []
    mock_result.weights_used = {"vector": 0.5, "semantic": 0.3, "graph": 0.2}
    mock_result.query_analysis = {"intent": "conversational"}

    mock_hybrid_search_service.search.return_value = mock_result

    payload = {
        "tenant_id": "test-tenant",
        "project_id": "test-project",
        "query": "how does it work?",
        "k": 10,
        "enable_vector_search": True,
        "enable_semantic_search": True,
        "enable_graph_search": True,
        "enable_fulltext_search": False,
        "conversation_history": [
            {"role": "user", "content": "Tell me about authentication"},
            {"role": "assistant", "content": "Authentication uses JWT tokens"}
        ]
    }

    response = client.post(
        "/v1/search/hybrid",
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "search_result" in data


@pytest.mark.asyncio
async def test_hybrid_search_empty_query(mock_app_state_pool, mock_hybrid_search_service):
    """Test hybrid search with empty query"""
    mock_result = MagicMock()
    mock_result.total_results = 0
    mock_result.total_time_ms = 5.0
    mock_result.results = []
    mock_result.weights_used = {}
    mock_result.query_analysis = None

    mock_hybrid_search_service.search.return_value = mock_result

    payload = {
        "tenant_id": "test-tenant",
        "project_id": "test-project",
        "query": "",
        "k": 10,
        "enable_vector_search": True,
        "enable_semantic_search": True,
        "enable_graph_search": False,
        "enable_fulltext_search": False
    }

    response = client.post(
        "/v1/search/hybrid",
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"}
    )

    # Should handle empty query gracefully
    assert response.status_code in [200, 400]


@pytest.mark.asyncio
async def test_hybrid_search_service_error(mock_app_state_pool, mock_hybrid_search_service):
    """Test hybrid search when service fails"""
    mock_hybrid_search_service.search.side_effect = Exception("Service error")

    payload = {
        "tenant_id": "test-tenant",
        "project_id": "test-project",
        "query": "test query",
        "k": 10,
        "enable_vector_search": True,
        "enable_semantic_search": True,
        "enable_graph_search": False,
        "enable_fulltext_search": False
    }

    response = client.post(
        "/v1/search/hybrid",
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 500
    assert "error" in response.json()["detail"].lower() or "Service error" in response.json()["detail"]


@pytest.mark.asyncio
async def test_hybrid_search_all_strategies_disabled(mock_app_state_pool, mock_hybrid_search_service):
    """Test hybrid search with all strategies disabled"""
    mock_result = MagicMock()
    mock_result.total_results = 0
    mock_result.total_time_ms = 1.0
    mock_result.results = []
    mock_result.weights_used = {}
    mock_result.query_analysis = None

    mock_hybrid_search_service.search.return_value = mock_result

    payload = {
        "tenant_id": "test-tenant",
        "project_id": "test-project",
        "query": "test query",
        "k": 10,
        "enable_vector_search": False,
        "enable_semantic_search": False,
        "enable_graph_search": False,
        "enable_fulltext_search": False
    }

    response = client.post(
        "/v1/search/hybrid",
        json=payload,
        headers={"X-Tenant-Id": "test-tenant"}
    )

    # Should return 200 with empty results
    assert response.status_code == 200
    data = response.json()
    assert "search_result" in data
