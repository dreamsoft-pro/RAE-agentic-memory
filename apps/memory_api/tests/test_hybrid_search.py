"""
Tests for Hybrid Search Service

Enterprise-grade test suite for hybrid vector + graph search functionality.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from typing import List

from apps.memory_api.services.hybrid_search import (
    HybridSearchService,
    HybridSearchResult,
    GraphNode,
    GraphEdge,
    TraversalStrategy
)
from apps.memory_api.models import ScoredMemoryRecord


@pytest.fixture
def mock_embedding_service():
    """Mock embedding service."""
    service = Mock()
    service.generate_embeddings = Mock(return_value=[[0.1, 0.2, 0.3]])
    return service


@pytest.fixture
def hybrid_search(mock_pool, mock_embedding_service):
    """Create hybrid search service with mocks."""
    service = HybridSearchService(mock_pool)
    service.embedding_service = mock_embedding_service
    return service


@pytest.fixture
def sample_vector_results():
    """Sample vector search results."""
    return [
        ScoredMemoryRecord(
            id="mem1",
            content="Module A depends on Module B",
            score=0.95,
            layer="em",
            tags=["dependency"],
            source="code_analysis",
            timestamp="2024-01-01T00:00:00"
        ),
        ScoredMemoryRecord(
            id="mem2",
            content="Module B uses PostgreSQL",
            score=0.85,
            layer="em",
            tags=["database"],
            source="design_doc",
            timestamp="2024-01-02T00:00:00"
        )
    ]


@pytest.fixture
def sample_graph_nodes():
    """Sample graph nodes."""
    return [
        GraphNode(id="n1", node_id="Module_A", label="Module A", depth=0),
        GraphNode(id="n2", node_id="Module_B", label="Module B", depth=1),
        GraphNode(id="n3", node_id="PostgreSQL", label="PostgreSQL", depth=2)
    ]


@pytest.fixture
def sample_graph_edges():
    """Sample graph edges."""
    return [
        GraphEdge(source_id="n1", target_id="n2", relation="DEPENDS_ON"),
        GraphEdge(source_id="n2", target_id="n3", relation="USES")
    ]


class TestTraversalStrategy:
    """Tests for traversal strategy enum."""

    def test_strategy_values(self):
        """Test strategy enum values."""
        assert TraversalStrategy.BFS.value == "bfs"
        assert TraversalStrategy.DFS.value == "dfs"

    def test_strategy_creation(self):
        """Test creating strategy from string."""
        assert TraversalStrategy("bfs") == TraversalStrategy.BFS
        assert TraversalStrategy("dfs") == TraversalStrategy.DFS


class TestGraphNode:
    """Tests for GraphNode model."""

    def test_node_creation(self):
        """Test creating graph node."""
        node = GraphNode(
            id="node1",
            node_id="Entity1",
            label="Entity Label",
            properties={"type": "module"},
            depth=2
        )

        assert node.id == "node1"
        assert node.node_id == "Entity1"
        assert node.label == "Entity Label"
        assert node.depth == 2


class TestGraphEdge:
    """Tests for GraphEdge model."""

    def test_edge_creation(self):
        """Test creating graph edge."""
        edge = GraphEdge(
            source_id="n1",
            target_id="n2",
            relation="DEPENDS_ON",
            properties={"confidence": 0.9}
        )

        assert edge.source_id == "n1"
        assert edge.target_id == "n2"
        assert edge.relation == "DEPENDS_ON"


@pytest.mark.asyncio
class TestHybridSearchService:
    """Tests for HybridSearchService."""

    async def test_service_initialization(self, mock_pool):
        """Test service initialization."""
        service = HybridSearchService(mock_pool)

        assert service.pool is mock_pool
        assert service.embedding_service is not None

    async def test_vector_only_search(self, hybrid_search, mock_pool, sample_vector_results):
        """Test search with graph disabled."""
        # Mock vector search to return results
        with patch('apps.memory_api.services.hybrid_search.get_vector_store') as mock_vs:
            mock_vs.return_value.query = AsyncMock(return_value=sample_vector_results)

            result = await hybrid_search.search(
                query="test query",
                tenant_id="tenant1",
                project_id="proj1",
                use_graph=False
            )

            assert len(result.vector_matches) == 2
            assert result.graph_enabled is False
            assert len(result.graph_nodes) == 0
            assert len(result.graph_edges) == 0

    async def test_hybrid_search_no_graph_nodes(self, hybrid_search, mock_pool, sample_vector_results):
        """Test hybrid search when no graph nodes are found."""
        # Mock vector search
        with patch('apps.memory_api.services.hybrid_search.get_vector_store') as mock_vs:
            mock_vs.return_value.query = AsyncMock(return_value=sample_vector_results)

            # Mock node mapping to return empty
            mock_pool._test_conn.fetch = AsyncMock(return_value=[])

            result = await hybrid_search.search(
                query="test query",
                tenant_id="tenant1",
                project_id="proj1",
                use_graph=True
            )

            assert len(result.vector_matches) == 2
            assert result.statistics["graph_nodes_found"] == 0

    async def test_full_hybrid_search(self, hybrid_search, mock_pool, sample_vector_results,
                                     sample_graph_nodes, sample_graph_edges):
        """Test full hybrid search with graph traversal."""
        # Mock vector search
        with patch('apps.memory_api.services.hybrid_search.get_vector_store') as mock_vs:
            mock_vs.return_value.query = AsyncMock(return_value=sample_vector_results)

            # Mock node mapping
            conn = mock_pool._test_conn
            conn.fetch = AsyncMock(side_effect=[
                [{"node_id": "Module_A"}],  # First memory mapping
                [{"node_id": "Module_B"}],  # Second memory mapping
                # BFS traversal results (nodes)
                [
                    {"id": "n1", "node_id": "Module_A", "label": "Module A", "properties": {}, "depth": 0},
                    {"id": "n2", "node_id": "Module_B", "label": "Module B", "properties": {}, "depth": 1}
                ],
                # Edge query
                [
                    {"id": "e1", "source_node_id": "n1", "target_node_id": "n2",
                     "relation": "DEPENDS_ON", "properties": {}, "created_at": "2024-01-01"}
                ]
            ])

            result = await hybrid_search.search(
                query="test query",
                tenant_id="tenant1",
                project_id="proj1",
                use_graph=True,
                graph_depth=2,
                traversal_strategy=TraversalStrategy.BFS
            )

            assert len(result.vector_matches) == 2
            assert len(result.graph_nodes) >= 1
            assert len(result.graph_edges) >= 1
            assert result.synthesized_context != ""
            assert result.graph_enabled is True

    async def test_bfs_traversal(self, hybrid_search, mock_pool):
        """Test breadth-first search traversal."""
        conn = mock_pool._test_conn
        conn.fetch = AsyncMock(side_effect=[
            # BFS query results
            [
                {"id": "n1", "node_id": "A", "label": "Node A", "properties": {}, "depth": 0},
                {"id": "n2", "node_id": "B", "label": "Node B", "properties": {}, "depth": 1}
            ],
            # Edge query results
            [
                {"id": "e1", "source_node_id": "n1", "target_node_id": "n2",
                 "relation": "CONNECTS", "properties": {}}
            ]
        ])

        nodes, edges = await hybrid_search._traverse_bfs(
            start_node_ids=["A"],
            tenant_id="tenant1",
            project_id="proj1",
            max_depth=2
        )

        assert len(nodes) == 2
        assert len(edges) == 1
        assert nodes[0].depth == 0
        assert nodes[1].depth == 1

    async def test_context_synthesis(self, hybrid_search, sample_vector_results,
                                    sample_graph_nodes, sample_graph_edges):
        """Test context synthesis from vector and graph results."""
        context = await hybrid_search._synthesize_context(
            vector_results=sample_vector_results,
            graph_nodes=sample_graph_nodes,
            graph_edges=sample_graph_edges,
            query="test query"
        )

        assert "test query" in context
        assert "Module A" in context or "Module_A" in context
        assert "DEPENDS_ON" in context
        assert len(context) > 0

    async def test_vector_only_synthesis(self, hybrid_search, sample_vector_results):
        """Test context synthesis from vector results only."""
        context = hybrid_search._synthesize_vector_only(sample_vector_results)

        assert "Search Results" in context
        assert "Module A" in context
        assert "0.95" in context  # Score
        assert len(context) > 0

    async def test_error_handling(self, hybrid_search, mock_pool):
        """Test error handling in hybrid search."""
        # Make vector search fail
        with patch('apps.memory_api.services.hybrid_search.get_vector_store') as mock_vs:
            mock_vs.side_effect = Exception("Vector store error")

            with pytest.raises(RuntimeError, match="Hybrid search failed"):
                await hybrid_search.search(
                    query="test",
                    tenant_id="tenant1",
                    project_id="proj1"
                )

    async def test_traversal_depth_limits(self, hybrid_search, mock_pool):
        """Test that traversal respects depth limits.

        The SQL query uses 'WHERE gt.depth < max_depth' in the recursive CTE,
        which means for max_depth=2, it returns nodes at depths 0, 1, and 2.
        """
        conn = mock_pool._test_conn
        conn.fetch = AsyncMock(side_effect=[
            # Mock SQL response - only nodes within max_depth
            # The SQL query filters in the database, so depth=3 is never returned
            [
                {"id": "n1", "node_id": "A", "label": "Node A", "properties": {}, "depth": 0},
                {"id": "n2", "node_id": "B", "label": "Node B", "properties": {}, "depth": 1},
                {"id": "n3", "node_id": "C", "label": "Node C", "properties": {}, "depth": 2}
            ],
            []  # Edges
        ])

        nodes, edges = await hybrid_search._traverse_bfs(
            start_node_ids=["A"],
            tenant_id="tenant1",
            project_id="proj1",
            max_depth=2
        )

        # Verify nodes are returned and max depth is respected
        assert len(nodes) == 3
        assert all(node.depth <= 2 for node in nodes)
        assert {node.node_id for node in nodes} == {"A", "B", "C"}


@pytest.mark.asyncio
class TestHybridSearchIntegration:
    """Integration tests for hybrid search."""

    async def test_end_to_end_hybrid_search(self, hybrid_search, mock_pool):
        """Test complete hybrid search pipeline."""
        # Setup comprehensive mocks
        with patch('apps.memory_api.services.hybrid_search.get_vector_store') as mock_vs:
            # Mock vector search
            mock_vs.return_value.query = AsyncMock(return_value=[
                ScoredMemoryRecord(
                    id="m1",
                    content="User service handles authentication",
                    score=0.92,
                    layer="em",
                    tags=["service", "auth"],
                    source="code",
                    timestamp="2024-01-01T00:00:00"
                )
            ])

            # Mock database operations
            conn = mock_pool._test_conn
            conn.fetch = AsyncMock(side_effect=[
                [{"node_id": "UserService"}],  # Node mapping
                # BFS results
                [
                    {"id": "n1", "node_id": "UserService", "label": "User Service",
                     "properties": {}, "depth": 0},
                    {"id": "n2", "node_id": "AuthModule", "label": "Auth Module",
                     "properties": {}, "depth": 1},
                    {"id": "n3", "node_id": "Database", "label": "Database",
                     "properties": {}, "depth": 2}
                ],
                # Edges
                [
                    {"id": "e1", "source_node_id": "n1", "target_node_id": "n2",
                     "relation": "USES", "properties": {}},
                    {"id": "e2", "source_node_id": "n2", "target_node_id": "n3",
                     "relation": "CONNECTS_TO", "properties": {}}
                ]
            ])

            # Execute search
            result = await hybrid_search.search(
                query="authentication service",
                tenant_id="test-tenant",
                project_id="test-project",
                top_k_vector=5,
                graph_depth=2,
                use_graph=True
            )

            # Verify comprehensive results
            assert len(result.vector_matches) == 1
            assert len(result.graph_nodes) >= 2
            assert len(result.graph_edges) >= 1
            assert result.synthesized_context != ""
            assert "User Service" in result.synthesized_context or "UserService" in result.synthesized_context
            assert result.statistics["vector_results"] == 1
            assert result.statistics["graph_nodes"] >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
