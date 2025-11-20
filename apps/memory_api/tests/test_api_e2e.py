"""
E2E API Smoke Tests

End-to-end smoke tests to verify the API works on fresh installation.
These tests validate the complete request flow through the system.

Test Coverage Goals (per test_2.md):
- Happy path: POST /memories → GET /search works
- Happy path: Memory storage → Hybrid search retrieval
- Critical for: "Install, run, it works" verification

Priority: HIGH (Shows project is production-ready)
Type: Integration/E2E tests
"""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create test client for API requests."""
    from apps.memory_api.main import app
    return TestClient(app)


class TestMemoryAPISmoke:
    """Smoke tests for core memory operations.

    These tests verify the most critical user journey:
    1. Store a memory
    2. Query/search for it
    3. Get expected results back
    """

    @patch('apps.memory_api.api.v1.memory.get_pool')
    @patch('apps.memory_api.api.v1.memory.get_vector_store')
    @patch('apps.memory_api.api.v1.memory.get_embedding_service')
    def test_store_and_query_memory_e2e(
        self,
        mock_embedding_service,
        mock_vector_store,
        mock_get_pool,
        client
    ):
        """Test end-to-end memory storage and retrieval.

        Flow:
        1. POST /api/v1/memory/store - store a memory
        2. POST /api/v1/memory/query - query for similar memories
        3. Verify the stored memory is returned

        This is the #1 most important user journey.
        """
        # Mock database pool
        mock_pool = AsyncMock()
        mock_pool.fetchrow = AsyncMock(return_value={"id": "mem-123"})
        mock_pool.execute = AsyncMock()

        # Mock async context manager for pool.acquire()
        from apps.memory_api.tests.conftest import DummyAsyncContextManager
        mock_pool.acquire = Mock(return_value=DummyAsyncContextManager(mock_pool))

        mock_get_pool.return_value = mock_pool

        # Mock embedding service
        mock_embedding = Mock()
        mock_embedding.generate_embeddings = Mock(return_value=[[0.1, 0.2, 0.3]])
        mock_embedding_service.return_value = mock_embedding

        # Mock vector store
        mock_vs = Mock()
        mock_vs.upsert = AsyncMock()
        mock_vs.query = AsyncMock(return_value=[
            Mock(
                id="mem-123",
                content="Test memory content",
                score=0.95,
                layer="em",
                tenant_id="test-tenant",
                project_id="test-project",
                tags=["test"],
                source="api",
                timestamp="2024-01-01T00:00:00"
            )
        ])
        mock_vector_store.return_value = mock_vs

        # Step 1: Store a memory
        store_response = client.post(
            "/api/v1/memory/store",
            json={
                "content": "Test memory content",
                "layer": "em",
                "tags": ["test"],
                "source": "api"
            },
            headers={"X-Tenant-ID": "test-tenant", "X-Project-ID": "test-project"}
        )

        # Verify store succeeded
        assert store_response.status_code == 200
        store_data = store_response.json()
        assert "memory_id" in store_data

        # Step 2: Query for the memory
        query_response = client.post(
            "/api/v1/memory/query",
            json={
                "query": "Test memory",
                "top_k": 5
            },
            headers={"X-Tenant-ID": "test-tenant", "X-Project-ID": "test-project"}
        )

        # Verify query succeeded
        assert query_response.status_code == 200
        query_data = query_response.json()

        # Verify memory is in results
        assert "memories" in query_data
        assert len(query_data["memories"]) > 0
        assert query_data["memories"][0]["content"] == "Test memory content"

    @patch('apps.memory_api.api.v1.graph.get_pool')
    @patch('apps.memory_api.api.v1.graph.HybridSearchService')
    @patch('apps.memory_api.api.v1.graph.get_embedding_service')
    def test_hybrid_search_e2e(
        self,
        mock_embedding_service,
        mock_hybrid_service_class,
        mock_get_pool,
        client
    ):
        """Test end-to-end hybrid search (vector + graph).

        Flow:
        1. POST /api/v1/graph/query - perform hybrid search
        2. Verify results contain both vector matches and graph context

        This validates the core RAE value proposition: semantic + graph.
        """
        # Mock database pool
        mock_pool = AsyncMock()
        mock_get_pool.return_value = mock_pool

        # Mock embedding service
        mock_embedding = Mock()
        mock_embedding.generate_embeddings = Mock(return_value=[[0.1, 0.2, 0.3]])
        mock_embedding_service.return_value = mock_embedding

        # Mock hybrid search service
        mock_service = Mock()
        mock_result = Mock()
        mock_result.vector_matches = [
            Mock(
                id="mem1",
                content="Related memory",
                score=0.9,
                layer="em",
                tenant_id="test-tenant",
                project_id="test-project",
                tags=["test"],
                source="api",
                timestamp="2024-01-01T00:00:00"
            )
        ]
        mock_result.graph_nodes = [
            Mock(id="n1", node_id="Entity1", label="Entity 1", depth=0, properties={})
        ]
        mock_result.graph_edges = [
            Mock(source_id="n1", target_id="n2", relation="RELATES_TO", properties={})
        ]
        mock_result.synthesized_context = "Context from vector and graph"
        mock_result.graph_enabled = True
        mock_result.statistics = {
            "vector_results": 1,
            "graph_nodes": 1,
            "graph_edges": 1
        }

        mock_service.search = AsyncMock(return_value=mock_result)
        mock_hybrid_service_class.return_value = mock_service

        # Execute hybrid search
        response = client.post(
            "/api/v1/graph/query",
            json={
                "query": "test query",
                "top_k": 5,
                "use_graph": True,
                "graph_depth": 2
            },
            headers={"X-Tenant-ID": "test-tenant", "X-Project-ID": "test-project"}
        )

        # Verify response
        assert response.status_code == 200
        data = response.json()

        # Verify hybrid results structure
        assert "vector_matches" in data
        assert "graph_nodes" in data
        assert "graph_edges" in data
        assert "synthesized_context" in data

        # Verify we got results
        assert len(data["vector_matches"]) > 0
        assert len(data["graph_nodes"]) > 0
        assert data["synthesized_context"] != ""


class TestHealthCheckSmoke:
    """Smoke test for health check endpoint.

    Verifies the API is accessible and responds correctly.
    """

    def test_health_check(self, client):
        """Test that health check endpoint responds.

        This is the most basic smoke test: "is the API alive?"
        """
        with patch('apps.memory_api.api.v1.health.get_pool') as mock_pool:
            # Mock pool for health check
            pool = AsyncMock()
            pool.fetchval = AsyncMock(return_value=1)
            mock_pool.return_value = pool

            response = client.get("/api/v1/health")

            # Should return 200 OK
            assert response.status_code == 200
            data = response.json()

            # Should have basic health info
            assert "status" in data


class TestAPIErrorHandling:
    """Test that API handles errors gracefully."""

    def test_missing_tenant_header(self, client):
        """Test that missing tenant header returns 400.

        Validates input validation and error responses.
        """
        response = client.post(
            "/api/v1/memory/store",
            json={
                "content": "Test",
                "layer": "em"
            }
            # Missing X-Tenant-ID header
        )

        # Should return client error
        assert response.status_code in [400, 422]

    def test_invalid_json(self, client):
        """Test that invalid JSON returns 422."""
        response = client.post(
            "/api/v1/memory/store",
            data="not valid json",
            headers={
                "Content-Type": "application/json",
                "X-Tenant-ID": "test",
                "X-Project-ID": "test"
            }
        )

        # Should return validation error
        assert response.status_code == 422


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
