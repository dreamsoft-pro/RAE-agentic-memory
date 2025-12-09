"""
Importance scorer for calculating memory importance.

Uses multiple factors to determine memory importance:
- Recency (exponential decay)
- Access frequency
- User-assigned importance
- Content length and complexity
"""

from datetime import datetime
from typing import Optional

from rae_core.models.memory import MemoryRecord


class ImportanceScorer:
    """
    Importance scorer for memories.

    Calculates importance based on multiple factors with configurable weights.
    """

    def __init__(
        self,
        recency_weight: float = 0.3,
        frequency_weight: float = 0.3,
        user_weight: float = 0.4,
        recency_half_life_days: float = 7.0
    ):
        """
        Initialize importance scorer.

        Args:
            recency_weight: Weight for recency factor (0-1)
            frequency_weight: Weight for frequency factor (0-1)
            user_weight: Weight for user-assigned importance (0-1)
            recency_half_life_days: Half-life for recency decay
        """
        self.recency_weight = recency_weight
        self.frequency_weight = frequency_weight
        self.user_weight = user_weight
        self.recency_half_life_days = recency_half_life_days

        # Normalize weights
        total_weight = recency_weight + frequency_weight + user_weight
        self.recency_weight /= total_weight
        self.frequency_weight /= total_weight
        self.user_weight /= total_weight

    def calculate_importance(
        self,
        memory: MemoryRecord,
        current_time: Optional[datetime] = None
    ) -> float:
        """
        Calculate overall importance score for a memory.

        Args:
            memory: Memory to score
            current_time: Current time for recency calculation (default: now)

        Returns:
            Importance score (0.0 - 1.0)
        """
        if current_time is None:
            current_time = datetime.now()

        # Calculate component scores
        recency_score = self._calculate_recency_score(memory, current_time)
        frequency_score = self._calculate_frequency_score(memory)
        user_score = memory.importance  # User-assigned importance

        # Weighted combination
        importance = (
            recency_score * self.recency_weight +
            frequency_score * self.frequency_weight +
            user_score * self.user_weight
        )

        return min(1.0, max(0.0, importance))

    def _calculate_recency_score(
        self,
        memory: MemoryRecord,
        current_time: datetime
    ) -> float:
        """
        Calculate recency score with exponential decay.

        Recent memories score higher, with exponential decay over time.
        """
        # Time since creation
        age_seconds = (current_time - memory.timestamp).total_seconds()
        age_days = age_seconds / 86400.0

        # Exponential decay
        recency_score = 0.5 ** (age_days / self.recency_half_life_days)

        # Bonus for recent access
        if memory.last_accessed_at:
            access_age_seconds = (current_time - memory.last_accessed_at).total_seconds()
            access_age_days = access_age_seconds / 86400.0
            access_recency = 0.5 ** (access_age_days / (self.recency_half_life_days / 2))

            # Blend creation recency with access recency
            recency_score = recency_score * 0.7 + access_recency * 0.3

        return recency_score

    def _calculate_frequency_score(self, memory: MemoryRecord) -> float:
        """
        Calculate frequency score based on usage count.

        Uses logarithmic scaling to prevent over-emphasizing high counts.
        """
        if memory.usage_count == 0:
            return 0.0

        import math

        # Logarithmic scaling (base 10)
        # usage_count = 1 → 0.0
        # usage_count = 10 → 0.5
        # usage_count = 100 → 1.0
        frequency_score = math.log10(memory.usage_count + 1) / 2.0

        return min(1.0, frequency_score)

    def recalculate_memory_importance(
        self,
        memory: MemoryRecord,
        current_time: Optional[datetime] = None
    ) -> MemoryRecord:
        """
        Recalculate and update memory importance.

        Args:
            memory: Memory to update
            current_time: Current time

        Returns:
            Updated memory record
        """
        new_importance = self.calculate_importance(memory, current_time)
        memory.importance = new_importance
        return memory

    def should_promote(
        self,
        memory: MemoryRecord,
        threshold: float = 0.6
    ) -> bool:
        """
        Check if memory should be promoted to higher layer.

        Args:
            memory: Memory to check
            threshold: Importance threshold for promotion

        Returns:
            True if should promote
        """
        return memory.importance >= threshold

    def should_archive(
        self,
        memory: MemoryRecord,
        threshold: float = 0.2,
        min_age_days: int = 30
    ) -> bool:
        """
        Check if memory should be archived or demoted.

        Args:
            memory: Memory to check
            threshold: Importance threshold for archival
            min_age_days: Minimum age before archival consideration

        Returns:
            True if should archive
        """
        age_seconds = (datetime.now() - memory.timestamp).total_seconds()
        age_days = age_seconds / 86400.0

        return (
            memory.importance < threshold and
            age_days >= min_age_days
        )
