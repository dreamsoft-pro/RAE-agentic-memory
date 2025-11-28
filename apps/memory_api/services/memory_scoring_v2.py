"""
Memory Scoring V2 - Unified Relevance + Importance + Recency

This module implements the unified memory scoring function described in
RAE v1 Implementation Plan, combining:
- Relevance (vector similarity)
- Importance (LLM-driven or manual)
- Recency (time-based decay with access count consideration)
"""

import math
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import structlog

logger = structlog.get_logger(__name__)


# ============================================================================
# Configuration
# ============================================================================


@dataclass
class ScoringWeights:
    """
    Weights for combining scoring components.

    Default weights:
    - alpha (relevance): 0.5 - Semantic similarity is most important
    - beta (importance): 0.3 - Content importance matters
    - gamma (recency): 0.2 - Time decay has moderate impact

    Weights should sum to 1.0 for normalized scores.
    """

    alpha: float = 0.5  # Relevance weight
    beta: float = 0.3  # Importance weight
    gamma: float = 0.2  # Recency weight

    def __post_init__(self):
        total = self.alpha + self.beta + self.gamma
        if not math.isclose(total, 1.0, rel_tol=1e-5):
            logger.warning(
                "scoring_weights_not_normalized",
                total=total,
                weights={"alpha": self.alpha, "beta": self.beta, "gamma": self.gamma},
            )


@dataclass
class DecayConfig:
    """
    Configuration for recency decay calculation.
    """

    base_decay_rate: float = 0.001  # Base decay rate per second
    access_count_boost: bool = True  # Whether to consider access count
    min_decay_rate: float = 0.0001  # Minimum decay rate (for frequently accessed)
    max_decay_rate: float = 0.01  # Maximum decay rate (for rarely accessed)


# ============================================================================
# Memory Score Result
# ============================================================================


@dataclass
class MemoryScoreResult:
    """
    Result of memory scoring with component breakdown.
    """

    # Final score
    final_score: float

    # Component scores
    relevance_score: float
    importance_score: float
    recency_score: float

    # Metadata
    memory_id: str
    age_seconds: float
    access_count: int
    effective_decay_rate: float


# ============================================================================
# Scoring Function
# ============================================================================


def compute_memory_score(
    similarity: float,
    importance: float,
    last_accessed_at: Optional[datetime],
    created_at: datetime,
    access_count: int = 0,
    now: Optional[datetime] = None,
    weights: Optional[ScoringWeights] = None,
    decay_config: Optional[DecayConfig] = None,
    memory_id: Optional[str] = None,
) -> MemoryScoreResult:
    """
    Compute unified memory score combining relevance, importance, and recency.

    This is the core scoring function implementing the formula from the plan:
        score = alpha * similarity + beta * importance + gamma * recency_component

    Where recency_component considers:
    - Time since last access (or creation)
    - Access count (more accessed = slower decay)
    - Configurable decay rate

    Args:
        similarity: Relevance score from vector similarity (0.0-1.0)
        importance: Importance score (0.0-1.0)
        last_accessed_at: Last access timestamp (None = never accessed)
        created_at: Creation timestamp
        access_count: Number of times memory was accessed
        now: Current time (defaults to UTC now)
        weights: Custom scoring weights (defaults to standard weights)
        decay_config: Custom decay configuration
        memory_id: Optional memory ID for logging

    Returns:
        MemoryScoreResult with final score and component breakdown

    Example:
        >>> score = compute_memory_score(
        ...     similarity=0.85,
        ...     importance=0.7,
        ...     last_accessed_at=datetime(2024, 1, 1),
        ...     created_at=datetime(2024, 1, 1),
        ...     access_count=5,
        ...     now=datetime(2024, 1, 8)
        ... )
        >>> print(f"Final score: {score.final_score:.3f}")
        >>> print(f"Components: rel={score.relevance_score:.3f}, "
        ...       f"imp={score.importance_score:.3f}, rec={score.recency_score:.3f}")
    """
    # Initialize configs
    if weights is None:
        weights = ScoringWeights()
    if decay_config is None:
        decay_config = DecayConfig()
    if now is None:
        now = datetime.now(timezone.utc)

    # Ensure timestamps are timezone-aware
    created_at = _ensure_utc(created_at)
    if last_accessed_at:
        last_accessed_at = _ensure_utc(last_accessed_at)

    # 1. Relevance component (normalized similarity)
    relevance_score = max(0.0, min(1.0, similarity))

    # 2. Importance component (already normalized)
    importance_score = max(0.0, min(1.0, importance))

    # 3. Recency component (exponential decay with access count adjustment)
    recency_score, age_seconds, effective_decay = _calculate_recency_component(
        last_accessed_at=last_accessed_at,
        created_at=created_at,
        access_count=access_count,
        now=now,
        decay_config=decay_config,
    )

    # 4. Weighted combination
    final_score = (
        weights.alpha * relevance_score
        + weights.beta * importance_score
        + weights.gamma * recency_score
    )

    # Ensure final score is in [0, 1]
    final_score = max(0.0, min(1.0, final_score))

    logger.debug(
        "memory_score_computed",
        memory_id=memory_id,
        final_score=round(final_score, 4),
        components={
            "relevance": round(relevance_score, 4),
            "importance": round(importance_score, 4),
            "recency": round(recency_score, 4),
        },
        age_seconds=int(age_seconds),
        access_count=access_count,
        effective_decay_rate=round(effective_decay, 6),
    )

    return MemoryScoreResult(
        final_score=final_score,
        relevance_score=relevance_score,
        importance_score=importance_score,
        recency_score=recency_score,
        memory_id=memory_id or "unknown",
        age_seconds=age_seconds,
        access_count=access_count,
        effective_decay_rate=effective_decay,
    )


def _calculate_recency_component(
    last_accessed_at: Optional[datetime],
    created_at: datetime,
    access_count: int,
    now: datetime,
    decay_config: DecayConfig,
) -> tuple[float, float, float]:
    """
    Calculate recency component with access count consideration.

    Formula:
        time_ref = last_accessed_at or created_at
        time_diff = (now - time_ref).total_seconds()

        effective_decay = base_decay_rate / (log(1 + access_count) + 1)
        recency_score = exp(-effective_decay * time_diff)

    Returns:
        Tuple of (recency_score, age_seconds, effective_decay_rate)
    """
    # Determine reference time (last access or creation)
    time_ref = last_accessed_at if last_accessed_at else created_at
    time_diff = (now - time_ref).total_seconds()

    # Handle edge case: future timestamps (shouldn't happen, but safeguard)
    if time_diff < 0:
        logger.warning(
            "future_timestamp_detected",
            time_ref=time_ref.isoformat(),
            now=now.isoformat(),
        )
        return 1.0, 0.0, 0.0

    # Calculate effective decay rate based on access count
    if decay_config.access_count_boost and access_count > 0:
        # More accessed memories decay slower
        # log(1 + access_count) + 1 ensures:
        # - access_count=0: divisor=1 (no reduction)
        # - access_count=9: divisor≈2.3 (decay rate ~43% of base)
        # - access_count=99: divisor≈5.6 (decay rate ~18% of base)
        effective_decay = decay_config.base_decay_rate / (
            math.log(1 + access_count) + 1
        )
    else:
        effective_decay = decay_config.base_decay_rate

    # Clamp to min/max
    effective_decay = max(
        decay_config.min_decay_rate, min(decay_config.max_decay_rate, effective_decay)
    )

    # Exponential decay: score = e^(-decay * time)
    recency_score = math.exp(-effective_decay * time_diff)

    # Ensure score is in [0, 1]
    recency_score = max(0.0, min(1.0, recency_score))

    return recency_score, time_diff, effective_decay


def _ensure_utc(dt: datetime) -> datetime:
    """Ensure datetime is timezone-aware (UTC)"""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


# ============================================================================
# Batch Scoring
# ============================================================================


def compute_batch_scores(
    memories: List[Dict[str, Any]],
    similarity_scores: List[float],
    now: Optional[datetime] = None,
    weights: Optional[ScoringWeights] = None,
    decay_config: Optional[DecayConfig] = None,
) -> List[MemoryScoreResult]:
    """
    Compute scores for a batch of memories.

    Args:
        memories: List of memory dicts with keys: id, importance,
                  last_accessed_at, created_at, usage_count (or access_count)
        similarity_scores: Corresponding similarity scores for each memory
        now: Current time
        weights: Scoring weights
        decay_config: Decay configuration

    Returns:
        List of MemoryScoreResult objects, one per memory

    Example:
        >>> memories = [
        ...     {
        ...         "id": "mem1",
        ...         "importance": 0.8,
        ...         "last_accessed_at": datetime(2024, 1, 1),
        ...         "created_at": datetime(2024, 1, 1),
        ...         "usage_count": 10,
        ...     },
        ...     # ... more memories
        ... ]
        >>> similarities = [0.9, 0.7, 0.6]
        >>> results = compute_batch_scores(memories, similarities)
        >>> sorted_results = sorted(results, key=lambda r: r.final_score, reverse=True)
    """
    if len(memories) != len(similarity_scores):
        raise ValueError(
            f"Mismatch: {len(memories)} memories but {len(similarity_scores)} similarity scores"
        )

    results = []
    for memory, similarity in zip(memories, similarity_scores):
        # Extract fields (handle both usage_count and access_count)
        access_count = memory.get("usage_count") or memory.get("access_count") or 0

        result = compute_memory_score(
            similarity=similarity,
            importance=memory.get("importance", 0.5),
            last_accessed_at=memory.get("last_accessed_at"),
            created_at=memory["created_at"],
            access_count=access_count,
            now=now,
            weights=weights,
            decay_config=decay_config,
            memory_id=str(memory.get("id", "unknown")),
        )
        results.append(result)

    return results


def rank_memories_by_score(
    memories: List[Dict[str, Any]], score_results: List[MemoryScoreResult]
) -> List[Dict[str, Any]]:
    """
    Rank memories by their computed scores.

    Args:
        memories: Original memory records
        score_results: Corresponding score results

    Returns:
        List of memories sorted by score (descending), with 'final_score' added
    """
    if len(memories) != len(score_results):
        raise ValueError("Memories and score_results must have same length")

    # Combine memories with scores
    ranked = []
    for memory, score_result in zip(memories, score_results):
        memory_with_score = {**memory, "final_score": score_result.final_score}
        ranked.append(memory_with_score)

    # Sort by final_score descending
    ranked.sort(key=lambda m: m["final_score"], reverse=True)

    return ranked
