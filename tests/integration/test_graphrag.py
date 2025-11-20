"""
Integration tests for GraphRAG functionality.

These tests verify the complete GraphRAG pipeline:
- Graph extraction from episodic memories
- Knowledge graph storage
- Hybrid search with graph traversal
- Context synthesis

Prerequisites:
- Running PostgreSQL instance
- Running Qdrant/pgvector instance
- Configured LLM provider (OpenAI, Anthropic, or Gemini)
"""

import pytest
import asyncio
from typing import List, Dict
import asyncpg
from datetime import datetime

from apps.memory_api.services.graph_extraction import (
    GraphExtractionService,
    GraphTriple,
    GraphExtractionResult
)
from apps.memory_api.services.reflection_engine import ReflectionEngine
from apps.memory_api.services.hybrid_search import HybridSearchService, TraversalStrategy
from apps.memory_api.config import settings


@pytest.fixture
async def db_pool():
    """Create a database connection pool for testing."""
    pool = await asyncpg.create_pool(
        host=settings.POSTGRES_HOST,
        database=settings.POSTGRES_DB,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
    )
    yield pool
    await pool.close()


@pytest.fixture
async def test_tenant_id():
    """Return a test tenant ID."""
    return "test-tenant-graphrag"


@pytest.fixture
async def test_project_id():
    """Return a test project ID."""
    return "test-project-graphrag"


@pytest.fixture
async def setup_test_memories(db_pool, test_tenant_id, test_project_id):
    """
    Create test episodic memories for graph extraction.

    These memories contain entities and relationships that should be
    extracted into the knowledge graph.
    """
    test_memories = [
        {
            "content": "User John reported bug #123 in the authentication module. "
                      "The bug causes login failures for users with special characters in their passwords.",
            "tags": ["bug", "authentication"],
            "source": "bug-tracker"
        },
        {
            "content": "Developer Alice fixed bug #123 by updating the password validation logic "
                      "in the AuthService module.",
            "tags": ["fix", "authentication"],
            "source": "git-commit"
        },
        {
            "content": "The AuthService module depends on the EncryptionService for password hashing. "
                      "This dependency was added in version 2.0.",
            "tags": ["architecture", "dependencies"],
            "source": "documentation"
        },
        {
            "content": "Feature request #456: Add support for OAuth2 authentication. "
                      "This feature will integrate with the existing AuthService.",
            "tags": ["feature", "authentication"],
            "source": "feature-tracker"
        }
    ]

    memory_ids = []

    async with db_pool.acquire() as conn:
        for memory in test_memories:
            memory_id = await conn.fetchval(
                """
                INSERT INTO memories (tenant_id, project, content, layer, tags, source, created_at)
                VALUES ($1, $2, $3, 'em', $4, $5, NOW())
                RETURNING id
                """,
                test_tenant_id,
                test_project_id,
                memory["content"],
                memory["tags"],
                memory["source"]
            )
            memory_ids.append(str(memory_id))

    yield memory_ids

    # Cleanup: Delete test memories and graph data
    async with db_pool.acquire() as conn:
        await conn.execute(
            "DELETE FROM memories WHERE tenant_id = $1 AND project = $2",
            test_tenant_id,
            test_project_id
        )
        await conn.execute(
            "DELETE FROM knowledge_graph_edges WHERE tenant_id = $1 AND project_id = $2",
            test_tenant_id,
            test_project_id
        )
        await conn.execute(
            "DELETE FROM knowledge_graph_nodes WHERE tenant_id = $1 AND project_id = $2",
            test_tenant_id,
            test_project_id
        )


@pytest.mark.asyncio
async def test_graph_extraction_basic(db_pool, test_tenant_id, test_project_id, setup_test_memories):
    """
    Test basic knowledge graph extraction from episodic memories.

    Verifies that:
    - Triples are extracted from memories
    - Entities are identified
    - Confidence scores are assigned
    """
    # Initialize graph extraction service
    graph_service = GraphExtractionService(db_pool)

    # Perform extraction
    result = await graph_service.extract_knowledge_graph(
        project_id=test_project_id,
        tenant_id=test_tenant_id,
        limit=10,
        min_confidence=0.3  # Lower threshold for testing
    )

    # Assertions
    assert isinstance(result, GraphExtractionResult)
    assert len(result.triples) > 0, "Should extract at least one triple"
    assert len(result.extracted_entities) > 0, "Should identify at least one entity"

    # Verify triple structure
    for triple in result.triples:
        assert isinstance(triple, GraphTriple)
        assert triple.source, "Triple should have a source"
        assert triple.relation, "Triple should have a relation"
        assert triple.target, "Triple should have a target"
        assert 0.0 <= triple.confidence <= 1.0, "Confidence should be between 0 and 1"

    # Verify statistics
    assert "memories_processed" in result.statistics
    assert "entities_count" in result.statistics
    assert "triples_count" in result.statistics


@pytest.mark.asyncio
async def test_graph_storage(db_pool, test_tenant_id, test_project_id, setup_test_memories):
    """
    Test that extracted triples are correctly stored in the database.

    Verifies that:
    - Nodes are created for entities
    - Edges are created for relationships
    - No duplicate nodes are created
    """
    # Initialize services
    graph_service = GraphExtractionService(db_pool)

    # Extract and store
    result = await graph_service.extract_knowledge_graph(
        project_id=test_project_id,
        tenant_id=test_tenant_id,
        limit=10,
        min_confidence=0.3
    )

    storage_stats = await graph_service.store_graph_triples(
        triples=result.triples,
        project_id=test_project_id,
        tenant_id=test_tenant_id
    )

    # Assertions
    assert storage_stats["nodes_created"] >= 0
    assert storage_stats["edges_created"] >= 0

    # Verify data in database
    async with db_pool.acquire() as conn:
        node_count = await conn.fetchval(
            "SELECT COUNT(*) FROM knowledge_graph_nodes WHERE tenant_id = $1 AND project_id = $2",
            test_tenant_id,
            test_project_id
        )

        edge_count = await conn.fetchval(
            "SELECT COUNT(*) FROM knowledge_graph_edges WHERE tenant_id = $1 AND project_id = $2",
            test_tenant_id,
            test_project_id
        )

        assert node_count > 0, "Should have created nodes"
        assert edge_count > 0, "Should have created edges"


@pytest.mark.asyncio
async def test_hybrid_search(db_pool, test_tenant_id, test_project_id, setup_test_memories):
    """
    Test hybrid search combining vector search and graph traversal.

    Verifies that:
    - Vector search finds relevant memories
    - Graph traversal discovers related entities
    - Context is synthesized from both sources
    """
    # First, extract and store graph
    graph_service = GraphExtractionService(db_pool)
    extraction_result = await graph_service.extract_knowledge_graph(
        project_id=test_project_id,
        tenant_id=test_tenant_id,
        limit=10,
        min_confidence=0.3
    )

    await graph_service.store_graph_triples(
        triples=extraction_result.triples,
        project_id=test_project_id,
        tenant_id=test_tenant_id
    )

    # Perform hybrid search
    hybrid_search = HybridSearchService(db_pool)

    search_result = await hybrid_search.search(
        query="authentication bugs and fixes",
        tenant_id=test_tenant_id,
        project_id=test_project_id,
        top_k_vector=3,
        graph_depth=2,
        traversal_strategy=TraversalStrategy.BFS,
        use_graph=True
    )

    # Assertions
    assert len(search_result.vector_matches) > 0, "Should find vector matches"
    assert search_result.synthesized_context, "Should synthesize context"
    assert "statistics" in search_result.model_dump()

    # If graph nodes were found, verify structure
    if search_result.graph_nodes:
        assert len(search_result.graph_nodes) > 0
        for node in search_result.graph_nodes:
            assert node.node_id
            assert node.label
            assert node.depth >= 0


@pytest.mark.asyncio
async def test_graph_traversal_depth(db_pool, test_tenant_id, test_project_id, setup_test_memories):
    """
    Test that graph traversal respects depth limits.

    Verifies that:
    - Traversal stops at specified depth
    - Different depths return different result sizes
    """
    # Setup graph
    graph_service = GraphExtractionService(db_pool)
    extraction_result = await graph_service.extract_knowledge_graph(
        project_id=test_project_id,
        tenant_id=test_tenant_id,
        limit=10,
        min_confidence=0.3
    )

    await graph_service.store_graph_triples(
        triples=extraction_result.triples,
        project_id=test_project_id,
        tenant_id=test_tenant_id
    )

    hybrid_search = HybridSearchService(db_pool)

    # Test different depths
    results_depth_1 = await hybrid_search.search(
        query="authentication",
        tenant_id=test_tenant_id,
        project_id=test_project_id,
        top_k_vector=3,
        graph_depth=1,
        use_graph=True
    )

    results_depth_2 = await hybrid_search.search(
        query="authentication",
        tenant_id=test_tenant_id,
        project_id=test_project_id,
        top_k_vector=3,
        graph_depth=2,
        use_graph=True
    )

    # Verify depth limits are respected
    assert results_depth_1.statistics["graph_depth"] == 1
    assert results_depth_2.statistics["graph_depth"] == 2

    # Depth 2 should generally find more or equal nodes than depth 1
    # (unless there are no connections at depth 2)
    if results_depth_1.graph_nodes and results_depth_2.graph_nodes:
        assert len(results_depth_2.graph_nodes) >= len(results_depth_1.graph_nodes)


@pytest.mark.asyncio
async def test_hierarchical_reflection(db_pool, test_tenant_id, test_project_id, setup_test_memories):
    """
    Test hierarchical (map-reduce) reflection generation.

    Verifies that:
    - Large collections of episodes are processed in buckets
    - Summaries are recursively merged
    - Final reflection is coherent
    """
    # Initialize reflection engine
    reflection_engine = ReflectionEngine(db_pool)

    # Generate hierarchical reflection
    summary = await reflection_engine.generate_hierarchical_reflection(
        project=test_project_id,
        tenant_id=test_tenant_id,
        bucket_size=2,  # Small bucket size to test hierarchy
        max_episodes=None
    )

    # Assertions
    assert summary, "Should generate a summary"
    assert len(summary) > 0, "Summary should not be empty"
    assert "No episodes available" not in summary, "Should process episodes"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
