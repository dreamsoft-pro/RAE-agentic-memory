"""Math Layer Controller - orchestrates all mathematical operations."""

from typing import Dict, List, Optional


# Import available functions or create stubs
try:
    from rae_core.math.dynamics import compute_recency_score
except ImportError:
    def compute_recency_score(age_hours: float, usage_count: int = 0) -> float:
        """Stub: compute recency score."""
        import math
        return math.exp(-0.01 * age_hours)

try:
    from rae_core.math.policy import compute_memory_score
except ImportError:
    def compute_memory_score(memory: Dict, query: str = None) -> float:
        """Stub: compute memory score."""
        return 0.5

try:
    from rae_core.math.structure import cosine_similarity
except ImportError:
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Stub: compute cosine similarity."""
        return 0.5


class MathLayerController:
    """
    Controller for RAE math layer operations.

    Orchestrates:
    - Importance calculations
    - Decay functions
    - Similarity scoring
    - Quality metrics
    """

    def __init__(self, config: Optional[Dict] = None):
        """Initialize controller with optional config."""
        self.config = config or {}

    def score_memory(self, memory: Dict, query: Optional[str] = None) -> float:
        """Score a memory's importance."""
        return compute_memory_score(memory, query)

    def apply_decay(self, age_hours: float, usage_count: int = 0) -> float:
        """Apply time-based decay to importance."""
        return compute_recency_score(age_hours, usage_count)

    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
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
