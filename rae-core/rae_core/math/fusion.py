"""Result fusion strategies for RAE retrieval."""

from typing import Any
from uuid import UUID

from .logic_gateway import LogicGateway


class FusionStrategy:
    """Base class for result fusion using LogicGateway."""

    def __init__(self, config: dict[str, Any] | None = None):
        self.gateway = LogicGateway(config)

    async def fuse(
        self,
        strategy_results: dict[str, list[tuple[UUID, float, float]]],
        weights: dict[str, float] | None = None,
        query: str | None = None,
        config_override: dict[str, Any] | None = None,
        memory_contents: dict[UUID, str] | None = None,
        **kwargs: Any,
    ) -> list[tuple[UUID, float, float]]:
        """
        Fuse results from multiple strategies using LogicGateway.

        Args:
            strategy_results: Map of strategy name -> list of (id, score, importance)
            weights: Optional strategy weight overrides
            query: The search query
            config_override: Optional runtime config for LogicGateway
            memory_contents: Optional map of memory ID -> content text
            **kwargs: Additional arguments for LogicGateway (like profile)

        Returns:
            Fused list of (id, score, importance)
        """
        # LogicGateway currently expects (id, score) in its input
        # and returns (id, score). We need to handle importance.

        # 1. Prepare input for gateway (strip importance for now)
        gateway_input = {
            name: [(r[0], r[1]) for r in results]
            for name, results in strategy_results.items()
        }

        # 2. Extract importance map for propagation
        importance_map: dict[UUID, float] = {}
        for results in strategy_results.values():
            for m_id, _, imp in results:
                if m_id not in importance_map or imp > importance_map[m_id]:
                    importance_map[m_id] = imp

        # 3. Fuse scores
        fused_results = await self.gateway.fuse(
            strategy_results=gateway_input,
            weights=weights,
            query=query or "",
            config_override=config_override,
            memory_contents=memory_contents,
            **kwargs,
        )

        # 4. Return the full tuples (id, score, importance, audit_log)
        return fused_results


class RRFFusion(FusionStrategy):
    """Simple Reciprocal Rank Fusion."""

    async def fuse(
        self,
        strategy_results: dict[str, list[tuple[UUID, float, float]]],
        weights: dict[str, float] | None = None,
        query: str | None = None,
        config_override: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> list[tuple[UUID, float, float]]:
        # RRF logic: sum(1 / (k + rank))
        k = 60
        scores: dict[UUID, float] = {}
        importance_map: dict[UUID, float] = {}

        for results in strategy_results.values():
            for rank, (m_id, _, imp) in enumerate(results, 1):
                scores[m_id] = scores.get(m_id, 0.0) + (1.0 / (k + rank))
                if m_id not in importance_map or imp > importance_map[m_id]:
                    importance_map[m_id] = imp

        sorted_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [
            (m_id, score, importance_map.get(m_id, 0.0)) for m_id, score in sorted_ids
        ]
