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
    # Complete mock object to satisfy Pydantic validation
    mock_result = {
        "results": [],
        "total_results": 5,
        "query_analysis": {
            "intent": "factual",
            "confidence": 0.9,
            "original_query": "authentication system",
            "key_entities": [],
            "key_concepts": [],
            "temporal_markers": [],
            "relation_types": [],
            "recommended_strategies": ["vector", "semantic"],
            "strategy_weights": {"vector": 0.4, "semantic": 0.3, "graph": 0.2, "fulltext": 0.1},
            "requires_temporal_filtering": False,
            "requires_graph_traversal": False,
            "suggested_depth": 2,
            "analyzed_at": datetime.utcnow().isoformat()
        },
        "vector_results_count": 2,
        "semantic_results_count": 1,
        "graph_results_count": 1,
        "fulltext_results_count": 1,
        "total_time_ms": 123,
        "query_analysis_time_ms": 50,
        "search_time_ms": 73,
        "applied_weights": {"vector": 0.4, "semantic": 0.3, "graph": 0.2, "fulltext": 0.1},
        "reranking_used": False
    }

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

    if response.status_code != 200:
        print(f"\nDEBUG: Response {response.status_code}: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert "search_result" in data
    assert "message" in data


@pytest.mark.asyncio
async def test_hybrid_search_with_reranking(mock_app_state_pool, mock_hybrid_search_service):
    """Test hybrid search with LLM re-ranking enabled"""
    mock_result = {
        "results": [],
        "total_results": 3,
        "query_analysis": {
            "intent": "exploratory",
            "confidence": 0.8,
            "original_query": "explain the authentication flow",
            "key_entities": [],
            "key_concepts": [],
            "temporal_markers": [],
            "relation_types": [],
            "recommended_strategies": ["vector", "graph"],
            "strategy_weights": {"vector": 0.5, "semantic": 0.3, "graph": 0.2},
            "requires_temporal_filtering": False,
            "requires_graph_traversal": True,
            "suggested_depth": 3,
            "analyzed_at": datetime.utcnow().isoformat()
        },
        "vector_results_count": 1,
        "semantic_results_count": 1,
        "graph_results_count": 1,
        "fulltext_results_count": 0,
        "total_time_ms": 250,
        "query_analysis_time_ms": 50,
        "search_time_ms": 100,
        "reranking_time_ms": 100,
        "applied_weights": {"vector": 0.5, "semantic": 0.3, "graph": 0.2},
        "reranking_used": True
    }

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

    if response.status_code != 200:
        print(f"\nDEBUG: Response {response.status_code}: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert "search_result" in data


@pytest.mark.asyncio
async def test_hybrid_search_with_filters(mock_app_state_pool, mock_hybrid_search_service):
    """Test hybrid search with temporal and tag filters"""
    mock_result = {
        "results": [],
        "total_results": 2,
        "query_analysis": {
            "intent": "temporal",
            "confidence": 0.85,
            "original_query": "recent security updates",
            "key_entities": [],
            "key_concepts": [],
            "temporal_markers": ["recent"],
            "relation_types": [],
            "recommended_strategies": ["vector", "fulltext"],
            "strategy_weights": {"vector": 0.6, "semantic": 0.4},
            "requires_temporal_filtering": True,
            "requires_graph_traversal": False,
            "suggested_depth": 1,
            "analyzed_at": datetime.utcnow().isoformat()
        },
        "vector_results_count": 1,
        "semantic_results_count": 1,
        "graph_results_count": 0,
        "fulltext_results_count": 0,
        "total_time_ms": 89,
        "query_analysis_time_ms": 40,
        "search_time_ms": 49,
        "applied_weights": {"vector": 0.6, "semantic": 0.4},
        "reranking_used": False
    }

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

    if response.status_code != 200:
        print(f"\nDEBUG: Response {response.status_code}: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert "search_result" in data


@pytest.mark.asyncio
async def test_hybrid_search_with_manual_weights(mock_app_state_pool, mock_hybrid_search_service):
    """Test hybrid search with manually specified weights"""
    mock_result = {
        "results": [],
        "total_results": 8,
        "query_analysis": {
            "intent": "conceptual",
            "confidence": 1.0,
            "original_query": "database optimization",
            "key_entities": [],
            "key_concepts": [],
            "temporal_markers": [],
            "relation_types": [],
            "recommended_strategies": [],
            "strategy_weights": {"vector": 0.7, "semantic": 0.2, "graph": 0.1},
            "requires_temporal_filtering": False,
            "requires_graph_traversal": False,
            "suggested_depth": 1,
            "analyzed_at": datetime.utcnow().isoformat()
        },
        "vector_results_count": 5,
        "semantic_results_count": 2,
        "graph_results_count": 1,
        "fulltext_results_count": 0,
        "total_time_ms": 150,
        "query_analysis_time_ms": 0,
        "search_time_ms": 150,
        "applied_weights": {"vector": 0.7, "semantic": 0.2, "graph": 0.1},
        "reranking_used": False
    }

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

    if response.status_code != 200:
        print(f"\nDEBUG: Response {response.status_code}: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert "search_result" in data


@pytest.mark.asyncio
async def test_hybrid_search_with_graph_depth(mock_app_state_pool, mock_hybrid_search_service):
    """Test hybrid search with custom graph traversal depth"""
    mock_result = {
        "results": [],
        "total_results": 12,
        "query_analysis": {
            "intent": "exploratory",
            "confidence": 0.85,
            "original_query": "knowledge graph relationships",
            "key_entities": [],
            "key_concepts": [],
            "temporal_markers": [],
            "relation_types": [],
            "recommended_strategies": ["graph", "vector"],
            "strategy_weights": {"vector": 0.3, "semantic": 0.3, "graph": 0.4},
            "requires_temporal_filtering": False,
            "requires_graph_traversal": True,
            "suggested_depth": 3,
            "analyzed_at": datetime.utcnow().isoformat()
        },
        "vector_results_count": 3,
        "semantic_results_count": 3,
        "graph_results_count": 4,
        "fulltext_results_count": 2,
        "total_time_ms": 300,
        "query_analysis_time_ms": 50,
        "search_time_ms": 250,
        "applied_weights": {"vector": 0.3, "semantic": 0.3, "graph": 0.4},
        "reranking_used": False
    }

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

    if response.status_code != 200:
        print(f"\nDEBUG: Response {response.status_code}: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert "search_result" in data


@pytest.mark.asyncio
async def test_hybrid_search_with_conversation_history(mock_app_state_pool, mock_hybrid_search_service):
    """Test hybrid search with conversation context"""
    mock_result = {
        "results": [],
        "total_results": 6,
        "query_analysis": {
            "intent": "conversational",
            "confidence": 0.9,
            "original_query": "how does it work?",
            "key_entities": [],
            "key_concepts": [],
            "temporal_markers": [],
            "relation_types": [],
            "recommended_strategies": ["vector"],
            "strategy_weights": {"vector": 0.5, "semantic": 0.3, "graph": 0.2},
            "requires_temporal_filtering": False,
            "requires_graph_traversal": False,
            "suggested_depth": 1,
            "analyzed_at": datetime.utcnow().isoformat()
        },
        "vector_results_count": 3,
        "semantic_results_count": 2,
        "graph_results_count": 1,
        "fulltext_results_count": 0,
        "total_time_ms": 180,
        "query_analysis_time_ms": 50,
        "search_time_ms": 130,
        "applied_weights": {"vector": 0.5, "semantic": 0.3, "graph": 0.2},
        "reranking_used": False
    }

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

    if response.status_code != 200:
        print(f"\nDEBUG: Response {response.status_code}: {response.json()}")

    assert response.status_code == 200
    data = response.json()
    assert "search_result" in data


@pytest.mark.asyncio
async def test_hybrid_search_empty_query(mock_app_state_pool, mock_hybrid_search_service):
    """Test hybrid search with empty query"""
    mock_result = {
        "results": [],
        "total_results": 0,
        "query_analysis": {
            "intent": "factual",
            "confidence": 0.0,
            "original_query": "",
            "key_entities": [],
            "key_concepts": [],
            "temporal_markers": [],
            "relation_types": [],
            "recommended_strategies": [],
            "strategy_weights": {},
            "requires_temporal_filtering": False,
            "requires_graph_traversal": False,
            "suggested_depth": 0,
            "analyzed_at": datetime.utcnow().isoformat()
        },
        "vector_results_count": 0,
        "semantic_results_count": 0,
        "graph_results_count": 0,
        "fulltext_results_count": 0,
        "total_time_ms": 5,
        "query_analysis_time_ms": 0,
        "search_time_ms": 5,
        "applied_weights": {},
        "reranking_used": False
    }

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
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "500"


@pytest.mark.asyncio
async def test_hybrid_search_all_strategies_disabled(mock_app_state_pool, mock_hybrid_search_service):
    """Test hybrid search with all strategies disabled"""
    mock_result = {
        "results": [],
        "total_results": 0,
        "query_analysis": {
            "intent": "factual",
            "confidence": 0.0,
            "original_query": "test query",
            "key_entities": [],
            "key_concepts": [],
            "temporal_markers": [],
            "relation_types": [],
            "recommended_strategies": [],
            "strategy_weights": {},
            "requires_temporal_filtering": False,
            "requires_graph_traversal": False,
            "suggested_depth": 0,
            "analyzed_at": datetime.utcnow().isoformat()
        },
        "vector_results_count": 0,
        "semantic_results_count": 0,
        "graph_results_count": 0,
        "fulltext_results_count": 0,
        "total_time_ms": 1,
        "query_analysis_time_ms": 0,
        "search_time_ms": 1,
        "applied_weights": {},
        "reranking_used": False
    }

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

    if response.status_code != 200:
        print(f"\nDEBUG: Response {response.status_code}: {response.json()}")

    # Should return 200 with empty results
    assert response.status_code == 200
    data = response.json()
    assert "search_result" in data
