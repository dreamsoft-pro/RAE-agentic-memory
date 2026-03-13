from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from rae_core.search.strategies.vector import VectorSearchStrategy


@pytest.mark.asyncio
async def test_vector_strategy_flow():
    mock_store = AsyncMock()
    mock_embedder = AsyncMock()

    strategy = VectorSearchStrategy(
        vector_store=mock_store, embedding_provider=mock_embedder, default_weight=0.5
    )

    expected_id = uuid4()
    mock_store.search_similar.return_value = [(expected_id, 0.85)]
    mock_embedder.embed_text.return_value = [0.1] * 384

    results = await strategy.search("test query", "tenant_1")

    assert len(results) == 1
    # Modern VectorSearchStrategy returns (id, score, importance)
    assert results[0][0] == expected_id
    assert results[0][1] == 0.85
    assert results[0][2] == 0.0  # importance stub
