"""
Tests for Graph Extraction Service

Enterprise-grade test suite for knowledge graph extraction from episodic memories.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime

from apps.memory_api.services.graph_extraction import (
    GraphExtractionService,
    GraphTriple,
    GraphExtractionResult
)


@pytest.fixture
def mock_llm_provider():
    """Mock LLM provider."""
    provider = Mock()
    provider.generate_structured = AsyncMock(return_value=GraphExtractionResult(
        triples=[
            GraphTriple(
                source="Module A",
                relation="DEPENDS_ON",
                target="Module B",
                confidence=0.95
            )
        ],
        extracted_entities=["Module A", "Module B"],
        statistics={}
    ))
    return provider


@pytest.fixture
def extraction_service(mock_pool, mock_llm_provider):
    """Create extraction service with mocks."""
    service = GraphExtractionService(mock_pool)
    service.llm_provider = mock_llm_provider
    return service


class TestGraphTriple:
    """Tests for GraphTriple model."""

    def test_triple_creation(self):
        """Test creating a valid triple."""
        triple = GraphTriple(
            source="Entity1",
            relation="RELATES_TO",
            target="Entity2",
            confidence=0.9
        )

        # Entity names are normalized to lowercase
        assert triple.source == "entity1"
        assert triple.relation == "RELATES_TO"
        assert triple.target == "entity2"
        assert triple.confidence == 0.9

    def test_relation_normalization(self):
        """Test that relation is normalized to uppercase."""
        triple = GraphTriple(
            source="A",
            relation="depends on",
            target="B"
        )

        assert triple.relation == "DEPENDS_ON"

    def test_triple_equality(self):
        """Test triple equality for deduplication."""
        triple1 = GraphTriple(source="A", relation="RELATES", target="B")
        triple2 = GraphTriple(source="A", relation="RELATES", target="B")
        triple3 = GraphTriple(source="A", relation="DIFFERENT", target="B")

        assert triple1 == triple2
        assert triple1 != triple3

    def test_triple_hash(self):
        """Test triple hashing for set operations."""
        triple1 = GraphTriple(source="A", relation="RELATES", target="B")
        triple2 = GraphTriple(source="A", relation="RELATES", target="B")

        assert hash(triple1) == hash(triple2)
        assert len({triple1, triple2}) == 1  # Deduplication in set

    def test_confidence_bounds(self):
        """Test confidence score validation."""
        with pytest.raises(ValueError):
            GraphTriple(source="A", relation="R", target="B", confidence=1.5)

        with pytest.raises(ValueError):
            GraphTriple(source="A", relation="R", target="B", confidence=-0.1)


class TestGraphExtractionResult:
    """Tests for GraphExtractionResult model."""

    def test_empty_result(self):
        """Test creating empty extraction result."""
        result = GraphExtractionResult()

        assert result.triples == []
        assert result.extracted_entities == []
        assert result.statistics == {}

    def test_result_with_data(self):
        """Test extraction result with data."""
        triple = GraphTriple(source="A", relation="R", target="B")
        result = GraphExtractionResult(
            triples=[triple],
            extracted_entities=["A", "B"],
            statistics={"count": 1}
        )

        assert len(result.triples) == 1
        assert len(result.extracted_entities) == 2
        assert result.statistics["count"] == 1


@pytest.mark.asyncio
class TestGraphExtractionService:
    """Tests for GraphExtractionService."""

    async def test_service_initialization(self, mock_pool, mock_llm_provider):
        """Test service initialization."""
        service = GraphExtractionService(mock_pool)
        service.llm_provider = mock_llm_provider

        assert service.pool is mock_pool
        assert service.llm_provider is mock_llm_provider

    async def test_fetch_episodic_memories(self, extraction_service, mock_pool):
        """Test fetching episodic memories."""
        # Mock database response using the exposed conn object
        mock_pool._test_conn.fetch = AsyncMock(return_value=[
            {
                "id": "mem1",
                "content": "Test memory",
                "created_at": datetime.now(),
                "tags": ["tag1"],
                "source": "test"
            }
        ])

        memories = await extraction_service._fetch_episodic_memories("proj1", "tenant1", 10)

        assert len(memories) == 1
        assert memories[0]["content"] == "Test memory"

    async def test_format_memories(self, extraction_service):
        """Test memory formatting for LLM."""
        memories = [
            {
                "id": "1",
                "content": "Memory 1",
                "tags": ["tag1"],
                "source": "test",
                "created_at": datetime(2024, 1, 1)
            },
            {
                "id": "2",
                "content": "Memory 2",
                "tags": [],
                "source": "test2",
                "created_at": datetime(2024, 1, 2)
            }
        ]

        formatted = extraction_service._format_memories(memories)

        assert "Memory 1" in formatted
        assert "Memory 2" in formatted
        assert "tag1" in formatted
        assert "test" in formatted

    async def test_extract_knowledge_graph_empty(self, extraction_service, mock_pool):
        """Test extraction with no memories."""
        # Mock empty database response
        mock_pool._test_conn.fetch = AsyncMock(return_value=[])

        result = await extraction_service.extract_knowledge_graph(
            project_id="proj1",
            tenant_id="tenant1",
            limit=10
        )

        # Verify result structure matches actual GraphExtractionResult contract
        assert result.statistics["memories_processed"] == 0
        assert result.statistics["entities_count"] == 0
        assert result.statistics["triples_count"] == 0
        assert result.triples == []
        assert result.extracted_entities == []

    async def test_extract_knowledge_graph_success(self, extraction_service, mock_pool):
        """Test successful graph extraction."""
        # Mock database with memories using the new helper
        mock_pool._test_conn.fetch = AsyncMock(return_value=[
            {
                "id": "mem1",
                "content": "Module A depends on Module B",
                "created_at": datetime.now(),
                "tags": ["dependency"],
                "source": "code_analysis"
            }
        ])

        result = await extraction_service.extract_knowledge_graph(
            project_id="proj1",
            tenant_id="tenant1",
            limit=10,
            min_confidence=0.5
        )

        assert result.statistics["memories_processed"] == 1
        assert len(result.triples) > 0
        assert len(result.extracted_entities) > 0

    async def test_confidence_filtering(self, extraction_service, mock_pool):
        """Test filtering triples by confidence threshold."""
        # Mock LLM to return triples with varying confidence
        extraction_service.llm_provider.generate_structured = AsyncMock(return_value=GraphExtractionResult(
            triples=[
                GraphTriple(source="A", relation="R1", target="B", confidence=0.9),
                GraphTriple(source="C", relation="R2", target="D", confidence=0.3),
                GraphTriple(source="E", relation="R3", target="F", confidence=0.7)
            ],
            extracted_entities=["A", "B", "C", "D", "E", "F"]
        ))

        # Mock memories
        mock_pool._test_conn.fetch = AsyncMock(return_value=[
            {"id": "1", "content": "Test", "created_at": datetime.now(), "tags": [], "source": "test"}
        ])

        result = await extraction_service.extract_knowledge_graph(
            project_id="proj1",
            tenant_id="tenant1",
            limit=10,
            min_confidence=0.5
        )

        # Should only include triples with confidence >= 0.5
        assert len(result.triples) == 2
        assert all(t.confidence >= 0.5 for t in result.triples)

    async def test_store_graph_triples(self, extraction_service, mock_pool):
        """Test storing extracted triples in database."""
        triples = [
            GraphTriple(source="A", relation="DEPENDS_ON", target="B", confidence=0.9),
            GraphTriple(source="B", relation="USES", target="C", confidence=0.8)
        ]

        # Mock database operations
        conn = mock_pool._test_conn
        conn.execute = AsyncMock(return_value="INSERT 0 1")
        conn.fetchrow = AsyncMock(side_effect=[
            {"id": "node-a-id"},  # source node A
            {"id": "node-b-id"},  # target node B
            {"id": "node-b-id"},  # source node B
            {"id": "node-c-id"}   # target node C
        ])

        result = await extraction_service.store_graph_triples(
            triples=triples,
            project_id="proj1",
            tenant_id="tenant1"
        )

        assert result["nodes_created"] >= 0
        assert result["edges_created"] >= 0

    async def test_error_handling(self, extraction_service, mock_pool):
        """Test error handling in extraction."""
        # Make LLM fail
        extraction_service.llm_provider.generate_structured = AsyncMock(side_effect=Exception("LLM Error"))

        # Mock memories
        mock_pool._test_conn.fetch = AsyncMock(return_value=[
            {"id": "1", "content": "Test", "created_at": datetime.now(), "tags": [], "source": "test"}
        ])

        with pytest.raises(RuntimeError, match="Graph extraction failed"):
            await extraction_service.extract_knowledge_graph(
                project_id="proj1",
                tenant_id="tenant1"
            )


@pytest.mark.asyncio
class TestGraphExtractionIntegration:
    """Integration tests for full extraction pipeline."""

    async def test_end_to_end_extraction(self, extraction_service, mock_pool):
        """Test complete extraction flow."""
        # Setup mocks
        mock_pool._test_conn.fetch = AsyncMock(return_value=[
            {
                "id": "mem1",
                "content": "User authentication module depends on database service",
                "created_at": datetime.now(),
                "tags": ["architecture", "dependency"],
                "source": "code_review"
            },
            {
                "id": "mem2",
                "content": "Database service uses PostgreSQL",
                "created_at": datetime.now(),
                "tags": ["database", "tech"],
                "source": "design_doc"
            }
        ])

        extraction_service.llm_provider.generate_structured = AsyncMock(return_value=GraphExtractionResult(
            triples=[
                GraphTriple(source="UserAuth", relation="DEPENDS_ON", target="Database", confidence=0.95),
                GraphTriple(source="Database", relation="USES", target="PostgreSQL", confidence=0.9)
            ],
            extracted_entities=["UserAuth", "Database", "PostgreSQL"],
            statistics={}
        ))

        # Execute extraction
        result = await extraction_service.extract_knowledge_graph(
            project_id="test-project",
            tenant_id="test-tenant",
            limit=50,
            min_confidence=0.8
        )

        # Verify results
        assert result.statistics["memories_processed"] == 2
        assert len(result.triples) == 2
        assert len(result.extracted_entities) == 3
        assert all(t.confidence >= 0.8 for t in result.triples)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
