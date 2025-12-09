"""
Score fusion strategies for hybrid search.

Combines multiple search results into a single ranked list.
"""

from enum import Enum
from typing import Dict, List

from rae_core.models.memory import ScoredMemoryRecord


class FusionStrategy(str, Enum):
    """Fusion strategies for combining search results."""

    RRF = "rrf"  # Reciprocal Rank Fusion
    WEIGHTED_SUM = "weighted_sum"  # Weighted score sum
    MAX_SCORE = "max_score"  # Maximum score across strategies


def score_fusion(
    results_list: List[List[ScoredMemoryRecord]],
    strategy: FusionStrategy = FusionStrategy.RRF,
    weights: List[float] = None
) -> List[ScoredMemoryRecord]:
    """
    Fuse multiple search result lists into one ranked list.

    Args:
        results_list: List of result lists from different strategies
        strategy: Fusion strategy to use
        weights: Optional weights for each result list (for WEIGHTED_SUM)

    Returns:
        Fused and ranked list of memories
    """
    if not results_list:
        return []

    if len(results_list) == 1:
        return results_list[0]

    # Build unified memory index
    memory_index: Dict[str, ScoredMemoryRecord] = {}
    for results in results_list:
        for result in results:
            if result.id not in memory_index:
                memory_index[result.id] = result

    if strategy == FusionStrategy.RRF:
        return _rrf_fusion(results_list, memory_index)
    elif strategy == FusionStrategy.WEIGHTED_SUM:
        if not weights:
            weights = [1.0] * len(results_list)
        return _weighted_sum_fusion(results_list, memory_index, weights)
    elif strategy == FusionStrategy.MAX_SCORE:
        return _max_score_fusion(results_list, memory_index)
    else:
        raise ValueError(f"Unknown fusion strategy: {strategy}")


def _rrf_fusion(
    results_list: List[List[ScoredMemoryRecord]],
    memory_index: Dict[str, ScoredMemoryRecord],
    k: int = 60
) -> List[ScoredMemoryRecord]:
    """
    Reciprocal Rank Fusion (RRF).

    RRF score = sum(1 / (k + rank_i)) for each result list.
    """
    rrf_scores: Dict[str, float] = {}

    for results in results_list:
        for rank, result in enumerate(results, start=1):
            if result.id not in rrf_scores:
                rrf_scores[result.id] = 0.0
            rrf_scores[result.id] += 1.0 / (k + rank)

    # Create scored results
    fused_results = []
    for memory_id, rrf_score in rrf_scores.items():
        memory = memory_index[memory_id]
        fused_results.append(
            ScoredMemoryRecord(**memory.model_dump(), score=rrf_score)
        )

    # Sort by RRF score
    fused_results.sort(key=lambda r: r.score, reverse=True)

    return fused_results


def _weighted_sum_fusion(
    results_list: List[List[ScoredMemoryRecord]],
    memory_index: Dict[str, ScoredMemoryRecord],
    weights: List[float]
) -> List[ScoredMemoryRecord]:
    """
    Weighted sum fusion.

    Final score = sum(weight_i * score_i) for each result list.
    """
    # Normalize weights
    weight_sum = sum(weights)
    normalized_weights = [w / weight_sum for w in weights]

    weighted_scores: Dict[str, float] = {}

    for results, weight in zip(results_list, normalized_weights):
        for result in results:
            if result.id not in weighted_scores:
                weighted_scores[result.id] = 0.0
            weighted_scores[result.id] += weight * result.score

    # Create scored results
    fused_results = []
    for memory_id, weighted_score in weighted_scores.items():
        memory = memory_index[memory_id]
        fused_results.append(
            ScoredMemoryRecord(**memory.model_dump(), score=weighted_score)
        )

    # Sort by weighted score
    fused_results.sort(key=lambda r: r.score, reverse=True)

    return fused_results


def _max_score_fusion(
    results_list: List[List[ScoredMemoryRecord]],
    memory_index: Dict[str, ScoredMemoryRecord]
) -> List[ScoredMemoryRecord]:
    """
    Maximum score fusion.

    Final score = max(score_i) across all result lists.
    """
    max_scores: Dict[str, float] = {}

    for results in results_list:
        for result in results:
            if result.id not in max_scores:
                max_scores[result.id] = result.score
            else:
                max_scores[result.id] = max(max_scores[result.id], result.score)

    # Create scored results
    fused_results = []
    for memory_id, max_score in max_scores.items():
        memory = memory_index[memory_id]
        fused_results.append(
            ScoredMemoryRecord(**memory.model_dump(), score=max_score)
        )

    # Sort by max score
    fused_results.sort(key=lambda r: r.score, reverse=True)

    return fused_results
