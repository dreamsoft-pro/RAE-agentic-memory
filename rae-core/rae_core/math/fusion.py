"""
Fusion Strategies for Hybrid Search.

This module provides fusion strategies like RRF and Confidence-Weighted Fusion.
"""

from uuid import UUID

import structlog

logger = structlog.get_logger(__name__)

class RRFFusion:
    """
    Reciprocal Rank Fusion (RRF) Strategy.
    Standard algorithm for combining ranked lists without needing score normalization.
    """
    def __init__(self, k: int = 60):
        self.k = k

    def fuse(
        self,
        strategy_results: dict[str, list[tuple[UUID, float]]],
        weights: dict[str, float]
    ) -> list[tuple[UUID, float]]:

        rrf_scores: dict[UUID, float] = {}

        for strategy_name, results in strategy_results.items():
            weight = weights.get(strategy_name, 1.0)

            for rank, (item_id, _) in enumerate(results):
                # RRF formula: 1 / (k + rank)
                # Weighted RRF: weight / (k + rank)
                score = weight / (self.k + rank)

                if item_id in rrf_scores:
                    rrf_scores[item_id] += score
                else:
                    rrf_scores[item_id] = score

        return sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)


class ConfidenceWeightedFusion:
    """
    Confidence-Weighted Fusion (ORB 2.0).
    Uses signal confidence (entropy/variance) to dynamically weight strategies.
    """
    def __init__(self, default_weights: dict[str, float] = None):
        self.default_weights = default_weights or {"vector": 1.0, "fulltext": 1.0}

    def fuse(
        self,
        strategy_results: dict[str, list[tuple[UUID, float]]],
        manual_weights: dict[str, float]
    ) -> list[tuple[UUID, float]]:

        # 1. Normalize Scores (Min-Max) per strategy
        normalized_results = {}
        for name, results in strategy_results.items():
            if not results:
                continue
            scores = [s for _, s in results]
            min_s, max_s = min(scores), max(scores)
            if max_s == min_s:
                norm_results = [(id, 1.0) for id, _ in results]
            else:
                norm_results = [(id, (s - min_s) / (max_s - min_s)) for id, s in results]
            normalized_results[name] = norm_results

        # 2. Apply Weights (Manual > Default)
        final_scores: dict[UUID, float] = {}
        for name, results in normalized_results.items():
            weight = manual_weights.get(name, self.default_weights.get(name, 1.0))

            for item_id, score in results:
                weighted_score = score * weight
                final_scores[item_id] = final_scores.get(item_id, 0.0) + weighted_score

        return sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
