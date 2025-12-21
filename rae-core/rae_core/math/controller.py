"""Math Layer Controller - orchestrates all mathematical operations."""


from typing import Any, Dict, List, Optional, cast

# Import available functions
from rae_core.math.dynamics import calculate_recency_score
from rae_core.math.policy import compute_memory_score
from rae_core.math.structure import cosine_similarity


class MathLayerController:
    """
    Controller for RAE math layer operations.

    Orchestrates:
    - Importance calculations
    - Decay functions
    - Similarity scoring
    - Quality metrics
    """

    def __init__(self, config: dict | None = None):
        """Initialize controller with optional config."""
        self.config = config or {}

    def score_memory(self, memory: dict, query_similarity: float = 0.5) -> float:
        """Score a memory's importance."""
        result = compute_memory_score(
            similarity=query_similarity,
            importance=memory.get("importance", 0.5),
            last_accessed_at=memory.get("last_accessed_at"),
            created_at=memory.get("created_at"),  # type: ignore
            access_count=memory.get("access_count", 0),
        )
        return float(result.final_score)

    def apply_decay(self, age_hours: float, usage_count: int = 0) -> float:
        """Apply time-based decay to importance."""
        # recency_score, age_seconds, effective_decay
        score, _, _ = calculate_recency_score(
            last_accessed_at=None,
            created_at=None,  # type: ignore
            access_count=usage_count,
            age_seconds=age_hours * 3600,
        )
        return float(score)

    def compute_similarity(
        self, embedding1: list[float], embedding2: list[float]
    ) -> float:
        """Compute cosine similarity between embeddings."""
        try:
            return cosine_similarity(embedding1, embedding2)
        except:
            # Fallback if function doesn't exist
            import math

            dot = sum(a * b for a, b in zip(embedding1, embedding2))
            mag1 = math.sqrt(sum(a * a for a in embedding1))
            mag2 = math.sqrt(sum(b * b for b in embedding2))
            return dot / (mag1 * mag2) if (mag1 * mag2) > 0 else 0.0
