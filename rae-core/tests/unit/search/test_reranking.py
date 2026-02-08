from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from rae_core.search.engine import EmeraldReranker, HybridSearchEngine


@pytest.mark.asyncio
async def test_emerald_reranker_logic():
    mock_embedding = MagicMock()
    mock_storage = MagicMock()
    reranker = EmeraldReranker(mock_embedding, mock_storage)

    candidates = [(uuid4(), 0.9, 0.5), (uuid4(), 0.8, 0.4)]
    res = await reranker.rerank("query", candidates, "tenant1", limit=1)
    assert len(res) == 1


@pytest.mark.asyncio
async def test_hybrid_search_engine_uses_reranker():
    mock_strategy = MagicMock()
    mock_strategy.search = AsyncMock(
        return_value=[(uuid4(), 0.8, 0.5), (uuid4(), 0.7, 0.4)]
    )
    mock_strategy.get_strategy_weight.return_value = 1.0
    mock_strategy.get_strategy_name.return_value = "test"

    mock_reranker = MagicMock()
    mock_reranker.rerank = AsyncMock(return_value=[(uuid4(), 0.99, 0.5)])

    mock_embedding = MagicMock()
    mock_storage = MagicMock()

    engine = HybridSearchEngine(
        strategies={"test": mock_strategy},
        embedding_provider=mock_embedding,
        memory_storage=mock_storage,
        reranker=mock_reranker,
    )

    res = await engine.search("query", "tenant1", enable_reranking=True)
    assert len(res) == 1
    assert mock_reranker.rerank.called
