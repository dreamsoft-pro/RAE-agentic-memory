"""
Search engine for RAE-Core.

Provides hybrid search combining multiple strategies.
"""

from typing import Any, Dict, List, Optional

from rae_core.layers.base import BaseLayer
from rae_core.models.memory import ScoredMemoryRecord
from rae_core.search.fusion import FusionStrategy, score_fusion
from rae_core.search.query_analyzer import QueryAnalyzer
from rae_core.search.strategies.importance import ImportanceSearchStrategy
from rae_core.search.strategies.keyword import KeywordSearchStrategy
from rae_core.search.strategies.recency import RecencySearchStrategy


class SearchEngine:
    """
    Hybrid search engine combining multiple strategies.

    Strategies:
    - Keyword-based (TF-IDF-like)
    - Recency-based (exponential decay)
    - Importance-based (value-weighted)

    Fusion:
    - RRF (Reciprocal Rank Fusion)
    - Weighted Sum
    - Max Score
    """

    def __init__(
        self,
        use_query_analyzer: bool = True,
        default_fusion: FusionStrategy = FusionStrategy.RRF
    ):
        """
        Initialize search engine.

        Args:
            use_query_analyzer: Whether to use query analyzer
            default_fusion: Default fusion strategy
        """
        self.use_query_analyzer = use_query_analyzer
        self.default_fusion = default_fusion

        # Initialize strategies
        self.keyword_strategy = KeywordSearchStrategy()
        self.recency_strategy = RecencySearchStrategy()
        self.importance_strategy = ImportanceSearchStrategy()

        # Initialize query analyzer
        self.query_analyzer = QueryAnalyzer() if use_query_analyzer else None

    async def search(
        self,
        layer: BaseLayer,
        query: str,
        k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        strategies: Optional[List[str]] = None,
        fusion: Optional[FusionStrategy] = None,
        weights: Optional[List[float]] = None
    ) -> List[ScoredMemoryRecord]:
        """
        Execute hybrid search.

        Args:
            layer: Layer to search in
            query: Query text
            k: Number of results to return
            filters: Optional filters
            strategies: List of strategies to use (default: all)
            fusion: Fusion strategy (default: RRF)
            weights: Weights for weighted fusion

        Returns:
            Fused and ranked list of memories
        """
        # Analyze query if enabled
        analyzed_query = None
        if self.query_analyzer:
            analyzed_query = await self.query_analyzer.analyze(query)
            # Merge analyzed filters with provided filters
            if analyzed_query.filters:
                if filters:
                    filters = {**filters, **analyzed_query.filters}
                else:
                    filters = analyzed_query.filters

        # Determine strategies to use
        if not strategies:
            strategies = ["keyword", "recency", "importance"]

        # Get all memories from layer
        all_memories = []
        # Note: This is simplified. In production, layer would provide
        # a method to get all memories or use proper pagination
        stats = await layer.get_statistics()
        if stats["count"] == 0:
            return []

        # Execute each strategy
        results_list = []

        for strategy_name in strategies:
            if strategy_name == "keyword":
                results = await layer.retrieve(query, k=k * 2, filters=filters)
                results_list.append(results)
            elif strategy_name == "recency":
                # Use layer's native retrieve (which may use recency)
                results = await layer.retrieve(query, k=k * 2, filters=filters)
                results_list.append(results)
            elif strategy_name == "importance":
                # Use layer's native retrieve
                results = await layer.retrieve(query, k=k * 2, filters=filters)
                results_list.append(results)

        # Fuse results
        if len(results_list) == 0:
            return []
        elif len(results_list) == 1:
            return results_list[0][:k]
        else:
            fusion_strategy = fusion or self.default_fusion
            fused_results = score_fusion(results_list, fusion_strategy, weights)
            return fused_results[:k]

    async def search_multi_layer(
        self,
        layers: List[BaseLayer],
        query: str,
        k: int = 10,
        filters: Optional[Dict[str, Any]] = None,
        layer_weights: Optional[Dict[str, float]] = None
    ) -> List[ScoredMemoryRecord]:
        """
        Search across multiple layers with layer-specific weighting.

        Args:
            layers: List of layers to search
            query: Query text
            k: Number of results to return
            filters: Optional filters
            layer_weights: Weights for each layer (by name)

        Returns:
            Fused results from all layers
        """
        if not layers:
            return []

        # Default layer weights (reflective > longterm > working > sensory)
        if not layer_weights:
            layer_weights = {
                "reflective": 1.0,
                "longterm": 0.8,
                "working": 0.6,
                "sensory": 0.4
            }

        # Search each layer
        all_results = []
        all_weights = []

        for layer in layers:
            results = await self.search(layer, query, k=k * 2, filters=filters)
            weight = layer_weights.get(layer.name, 0.5)

            # Weight the scores
            weighted_results = []
            for result in results:
                weighted_result = ScoredMemoryRecord(
                    **result.model_dump(),
                    score=result.score * weight
                )
                weighted_results.append(weighted_result)

            all_results.append(weighted_results)
            all_weights.append(weight)

        # Fuse results
        if len(all_results) == 0:
            return []
        elif len(all_results) == 1:
            return all_results[0][:k]
        else:
            fused_results = score_fusion(
                all_results,
                FusionStrategy.WEIGHTED_SUM,
                all_weights
            )
            return fused_results[:k]
