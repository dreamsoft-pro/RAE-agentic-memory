"""Hybrid search engine that orchestrates multiple search strategies."""

from typing import Any, Dict, List, Tuple, Optional
from uuid import UUID
import structlog

from rae_core.math.fusion import RRFFusion

logger = structlog.get_logger(__name__)

class HybridSearchEngine:
    """
    Hybrid search engine using Reciprocal Rank Fusion (RRF).
    """

    def __init__(
        self,
        strategies: dict[str, Any],
        fusion_strategy: Optional[Any] = None,
        cache: Any = None,
    ):
        self.strategies = strategies
        # Use RRF as the stable default
        self.fusion_strategy = fusion_strategy or RRFFusion(k=60)
        self.cache = cache

    async def search(
        self,
        query: str,
        tenant_id: str,
        strategies: list[str] | None = None,
        strategy_weights: dict[str, float] | None = None,
        filters: dict[str, Any] | None = None,
        limit: int = 10,
        use_cache: bool = True,
    ) -> list[tuple[UUID, float]]:
        """
        Execute hybrid search across multiple strategies.
        """
        active_strategy_names = strategies or list(self.strategies.keys())
        
        # Determine weights
        weights = strategy_weights or {}
        for name in active_strategy_names:
            if name not in weights:
                strategy = self.strategies.get(name)
                if strategy:
                    # In RRF, weight is often just 1.0
                    weights[name] = 1.0

        strategy_results: dict[str, list[tuple[UUID, float]]] = {}

        for name in active_strategy_names:
            strategy = self.strategies.get(name)
            if not strategy:
                continue

            try:
                # Extract project from filters for explicit passing
                p_id = (filters or {}).get("project")
                
                results = await strategy.search(
                    query=query,
                    tenant_id=tenant_id,
                    filters=filters,
                    limit=limit * 2,
                    project=p_id,
                )
                strategy_results[name] = results or []
                logger.info("strategy_success", strategy=name, count=len(strategy_results[name]))
            except Exception as e:
                logger.error("strategy_failed", strategy=name, error=str(e))
                strategy_results[name] = []

        # Fuse results using the selected strategy (default RRF)
        fused_results = self.fusion_strategy.fuse(strategy_results, weights)
        
        return fused_results[:limit]

    async def rerank(
        self,
        query: str,
        results: list[tuple[UUID, float]],
    ) -> list[tuple[UUID, float]]:
        """Placeholder for L2 reranking."""
        return results
