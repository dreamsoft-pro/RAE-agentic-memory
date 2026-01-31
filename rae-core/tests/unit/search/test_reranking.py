"""
Tests for Emerald Reranker and Hybrid Search Engine refactoring.
"""

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from rae_core.interfaces.embedding import IEmbeddingProvider
from rae_core.interfaces.storage import IMemoryStorage
from rae_core.search.engine import EmeraldReranker, HybridSearchEngine


@pytest.mark.asyncio
async def test_emerald_reranker_logic():
    # Setup mocks
    mock_storage = MagicMock(spec=IMemoryStorage)
    mock_embedding = MagicMock(spec=IEmbeddingProvider)

    m_id1 = uuid4()
    m_id2 = uuid4()

    mock_storage.get_memory = AsyncMock(
        side_effect=[
            {"content": "Relevant memory about cats"},
            {"content": "Irrelevant memory about dogs"},
        ]
    )

    # Simple 2D embeddings for testing logic
    mock_embedding.embed_text = AsyncMock(
        side_effect=[
            [1.0, 0.0],  # query "cats"
            [1.0, 0.0],  # mem1 "cats"
            [0.0, 1.0],  # mem2 "dogs"
        ]
    )

    reranker = EmeraldReranker(mock_embedding, mock_storage)

    candidates = [(m_id1, 0.5), (m_id2, 0.5)]
    results = await reranker.rerank("cats", candidates, "tenant-1", limit=10)

    assert len(results) == 2
    assert results[0][0] == m_id1
    # mem1 should have high semantic score (~1.0)
    # final_score = 1.0 * 0.7 + 0.5 * 0.3 = 0.85
    assert results[0][1] > results[1][1]


@pytest.mark.asyncio
async def test_hybrid_search_engine_uses_reranker():
    mock_strategy = MagicMock()
    mock_strategy.search = AsyncMock(return_value=[(uuid4(), 0.8), (uuid4(), 0.7)])
    mock_strategy.get_strategy_weight.return_value = 1.0

    mock_reranker = MagicMock()
    mock_reranker.rerank = AsyncMock(return_value=[(uuid4(), 0.99)])

    engine = HybridSearchEngine(
        strategies={"test": mock_strategy}, reranker=mock_reranker
    )

    results = await engine.search("query", "tenant", enable_reranking=True)

    assert len(results) == 1
    assert results[0][1] == 0.99
    mock_reranker.rerank.assert_called_once()
