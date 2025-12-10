"""Hybrid search engine that orchestrates multiple search strategies."""

from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

from rae_core.search.cache import SearchCache
from rae_core.search.strategies import SearchStrategy


class HybridSearchEngine:
    """Hybrid search engine combining multiple strategies.

    Implements Reciprocal Rank Fusion (RRF) to combine results
    from multiple search strategies (vector, graph, sparse, fulltext).
    """

    def __init__(
        self,
        strategies: Dict[str, SearchStrategy],
        cache: Optional[SearchCache] = None,
        rrf_k: int = 60,
    ):
        """Initialize hybrid search engine.

        Args:
            strategies: Dictionary of strategy_name -> strategy instance
            cache: Optional search cache
            rrf_k: RRF constant (typically 60)
        """
        self.strategies = strategies
        self.cache = cache
        self.rrf_k = rrf_k

    def _reciprocal_rank_fusion(
        self,
        strategy_results: Dict[str, List[Tuple[UUID, float]]],
        strategy_weights: Dict[str, float],
    ) -> List[Tuple[UUID, float]]:
        """Combine multiple result sets using Reciprocal Rank Fusion.

        RRF Formula: score(d) = Σ weight_s / (k + rank_s(d))
        where k is a constant (typically 60) and rank_s(d) is the rank
        of document d in strategy s.

        Args:
            strategy_results: Results from each strategy
            strategy_weights: Weight for each strategy

        Returns:
            Fused results sorted by combined score
        """
        # Build unified score map
        unified_scores: Dict[UUID, float] = {}

        for strategy_name, results in strategy_results.items():
            weight = strategy_weights.get(strategy_name, 1.0)

            for rank, (memory_id, _) in enumerate(results, start=1):
                # RRF score contribution
                rrf_score = weight / (self.rrf_k + rank)

                if memory_id in unified_scores:
                    unified_scores[memory_id] += rrf_score
                else:
                    unified_scores[memory_id] = rrf_score

        # Convert to sorted list
        fused_results = sorted(
            unified_scores.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        return fused_results

    async def search(
        self,
        query: str,
        tenant_id: str,
        strategies: Optional[List[str]] = None,
        strategy_weights: Optional[Dict[str, float]] = None,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        use_cache: bool = True,
    ) -> List[Tuple[UUID, float]]:
        """Execute hybrid search across multiple strategies.

        Args:
            query: Search query text
            tenant_id: Tenant identifier
            strategies: List of strategy names to use (all if None)
            strategy_weights: Custom weights for strategies (uses defaults if None)
            filters: Optional filters passed to all strategies
            limit: Maximum number of results
            use_cache: Whether to use cache for results

        Returns:
            List of (memory_id, fused_score) tuples
        """
        # Determine which strategies to use
        active_strategies = strategies or list(self.strategies.keys())

        # Determine weights
        weights = strategy_weights or {}
        for strategy_name in active_strategies:
            if strategy_name not in weights:
                strategy = self.strategies.get(strategy_name)
                if strategy:
                    weights[strategy_name] = strategy.get_strategy_weight()

        # Collect results from each strategy
        strategy_results: Dict[str, List[Tuple[UUID, float]]] = {}

        for strategy_name in active_strategies:
            strategy = self.strategies.get(strategy_name)
            if not strategy:
                continue

            # Check cache first
            cached_result = None
            if use_cache and self.cache:
                cached_result = await self.cache.get(
                    query=query,
                    tenant_id=tenant_id,
                    strategy=strategy_name,
                    filters=filters,
                )

            if cached_result is not None:
                strategy_results[strategy_name] = cached_result
            else:
                # Execute strategy
                results = await strategy.search(
                    query=query,
                    tenant_id=tenant_id,
                    filters=filters,
                    limit=limit * 2,  # Fetch more for fusion
                )
                strategy_results[strategy_name] = results

                # Cache results
                if use_cache and self.cache:
                    await self.cache.set(
                        query=query,
                        tenant_id=tenant_id,
                        strategy=strategy_name,
                        results=results,
                        filters=filters,
                    )

        # Fuse results using RRF
        fused_results = self._reciprocal_rank_fusion(
            strategy_results=strategy_results,
            strategy_weights=weights,
        )

        return fused_results[:limit]

    async def search_single_strategy(
        self,
        strategy_name: str,
        query: str,
        tenant_id: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
        use_cache: bool = True,
    ) -> List[Tuple[UUID, float]]:
        """Execute search using a single strategy.

        Args:
            strategy_name: Name of strategy to use
            query: Search query text
            tenant_id: Tenant identifier
            filters: Optional filters
            limit: Maximum number of results
            use_cache: Whether to use cache

        Returns:
            List of (memory_id, score) tuples
        """
        strategy = self.strategies.get(strategy_name)
        if not strategy:
            raise ValueError(f"Unknown strategy: {strategy_name}")

        # Check cache
        if use_cache and self.cache:
            cached_result = await self.cache.get(
                query=query,
                tenant_id=tenant_id,
                strategy=strategy_name,
                filters=filters,
            )
            if cached_result is not None:
                return cached_result[:limit]

        # Execute strategy
        results = await strategy.search(
            query=query,
            tenant_id=tenant_id,
            filters=filters,
            limit=limit,
        )

        # Cache results
        if use_cache and self.cache:
            await self.cache.set(
                query=query,
                tenant_id=tenant_id,
                strategy=strategy_name,
                results=results,
                filters=filters,
            )

        return results

    def get_available_strategies(self) -> List[str]:
        """Get list of available strategy names."""
        return list(self.strategies.keys())
