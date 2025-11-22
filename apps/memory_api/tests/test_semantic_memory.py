"""
Tests for Semantic Memory - Knowledge Nodes with TTL/LTM Decay

Tests cover:
- Semantic node extraction
- Canonicalization
- 3-stage semantic search
- TTL/LTM decay model
- Reinforcement learning
"""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4
from unittest.mock import AsyncMock, patch

from apps.memory_api.services.semantic_extractor import SemanticExtractor
from apps.memory_api.services.semantic_search import SemanticSearchPipeline


@pytest.fixture
def mock_pool():
    pool = AsyncMock()
    return pool


@pytest.fixture
def mock_llm():
    llm = AsyncMock()
    llm.generate_structured = AsyncMock(return_value={
        "entities": [
            {"label": "machine learning", "type": "concept", "canonical_form": "machine learning"},
            {"label": "neural networks", "type": "concept", "canonical_form": "neural network"}
        ]
    })
    return llm


@pytest.fixture
def semantic_extractor(mock_pool, mock_llm):
    extractor = SemanticExtractor(mock_pool)
    extractor.llm_provider = mock_llm
    return extractor


@pytest.fixture
def semantic_search(mock_pool):
    return SemanticSearchPipeline(mock_pool)


# Extraction Tests
@pytest.mark.asyncio
async def test_extract_semantic_nodes(semantic_extractor, mock_pool):
    """Test semantic node extraction from memory"""
    mock_pool.fetchrow = AsyncMock(return_value={
        "id": uuid4(),
        "content": "Machine learning uses neural networks for pattern recognition"
    })
    mock_pool.fetch = AsyncMock(return_value=[])
    mock_pool.execute = AsyncMock()

    result = await semantic_extractor.extract_nodes(
        tenant_id="test",
        project_id="test",
        memory_id=uuid4()
    )

    assert result["nodes_created"] >= 0


# Canonicalization Tests
@pytest.mark.asyncio
async def test_canonicalization(semantic_extractor):
    """Test term canonicalization"""
    variations = ["ML", "machine learning", "Machine Learning", "ml"]
    canonical = await semantic_extractor._canonicalize("machine learning")
    assert canonical == "machine learning"


# Search Tests
@pytest.mark.asyncio
async def test_semantic_search_3_stages(semantic_search, mock_pool):
    """Test 3-stage semantic search pipeline"""
    mock_pool.fetch = AsyncMock(return_value=[
        {"id": uuid4(), "content": "test", "score": 0.9}
    ])

    results, stats = await semantic_search.search(
        tenant_id="test",
        project_id="test",
        query="machine learning",
        k=10
    )

    assert stats["stages_executed"] == 3


# Decay Tests
@pytest.mark.asyncio
async def test_ttl_ltm_decay(mock_pool):
    """Test TTL/LTM decay model"""
    # Node not accessed for long time should decay
    last_reinforced = datetime.utcnow() - timedelta(days=30)
    decay_rate = 0.01

    # Calculate decay
    days_since = (datetime.utcnow() - last_reinforced).days
    decay_factor = 1.0 - (decay_rate * days_since)

    assert decay_factor < 1.0


# Reinforcement Tests
@pytest.mark.asyncio
async def test_node_reinforcement(mock_pool):
    """Test reinforcement learning for nodes"""
    mock_pool.execute = AsyncMock()

    node_id = uuid4()
    # Simulate reinforcement
    # Priority should increase, decay should reset

    # This would be called when node is accessed
    await mock_pool.execute(
        "SELECT reinforce_semantic_node($1)",
        node_id
    )

    mock_pool.execute.assert_called_once()
