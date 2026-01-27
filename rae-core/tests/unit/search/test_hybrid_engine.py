from typing import Any, cast
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest

from rae_core.math.fusion import RRFFusion
from rae_core.search.engine import HybridSearchEngine
from rae_core.search.strategies import SearchStrategy


class MockStrategy(SearchStrategy):
    def __init__(self, name: str, weight: float, results: list[tuple[Any, float]]):
        self.name = name
        self.weight = weight
        self._results = results
        # We can still use AsyncMock for tracking calls if needed,
        # but the method implementation is key.
        self.search_mock = AsyncMock(return_value=results)

    async def search(
        self,
        query: str,
        tenant_id: str,
        filters: dict[str, Any] | None = None,
        limit: int = 10,
        **kwargs,
    ) -> list[tuple[UUID, float]]:
        # Call the mock to track usage
        return cast(
            list[tuple[UUID, float]],
            await self.search_mock(query, tenant_id, filters, limit, **kwargs),
        )

    def get_strategy_name(self) -> str:
        return self.name

    def get_strategy_weight(self) -> float:
        return self.weight


@pytest.mark.asyncio
async def test_hybrid_search_rrf_logic():
    # Setup
    id1 = uuid4()
    id2 = uuid4()

    # Strategy A: [id1, id2]
    strat_a = MockStrategy("A", 1.0, [(id1, 0.9), (id2, 0.8)])

    # Strategy B: [id2, id1] - reverse order
    strat_b = MockStrategy("B", 1.0, [(id2, 0.9), (id1, 0.8)])

    engine = HybridSearchEngine(
        strategies={"A": strat_a, "B": strat_b},
        fusion_strategy=RRFFusion(k=1),  # Small k to make rank differences significant
    )

    # RRF Score formula: weight / (k + rank)
    # where rank starts at 0
    # id1 score: A(rank 0) + B(rank 1) = 1/(1+0) + 1/(1+1) = 1.0 + 0.5 = 1.5
    # id2 score: A(rank 1) + B(rank 0) = 1/(1+1) + 1/(1+0) = 0.5 + 1.0 = 1.5

    results = await engine.search("query", "tenant")

    assert len(results) == 2
    # Scores should be identical
    assert abs(results[0][1] - 1.5) < 0.01


@pytest.mark.asyncio
async def test_hybrid_search_single_strategy():
    id1 = uuid4()
    strat = MockStrategy("vector", 1.0, [(id1, 0.9)])

    engine = HybridSearchEngine(strategies={"vector": strat})

    results = await engine.search("query", "tenant")

    assert len(results) == 1
    assert results[0][0] == id1
    # For single strategy, RRF score is just 1/(k+rank) * weight
    # Rank is 0-based, so 1.0 / (60 + 0) = 0.01666...
    expected_score = 1.0 / 60.0
    assert abs(results[0][1] - expected_score) < 0.0001


@pytest.mark.asyncio
async def test_weights_influence():
    id1 = uuid4()

    # Strategy A (Weight 10.0) vs Strategy B (Weight 1.0)
    strat_a = MockStrategy("A", 10.0, [(id1, 0.9)])
    strat_b = MockStrategy("B", 1.0, [(id1, 0.9)])

    engine = HybridSearchEngine(strategies={"A": strat_a, "B": strat_b})

    results = await engine.search("q", "t")

    # Score = 10/(60+0) + 1/(60+0) = 11/60
    # Rank is 0-based
    expected = 11.0 / 60.0
    assert abs(results[0][1] - expected) < 0.0001
