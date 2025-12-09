"""
Recency-based search strategy.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from rae_core.models.memory import MemoryRecord, ScoredMemoryRecord
from rae_core.search.strategies.base import SearchStrategy


class RecencySearchStrategy(SearchStrategy):
    """
    Recency-based search prioritizing recent memories.

    Uses exponential decay for time-based scoring.
    """

    def __init__(self, half_life_days: float = 7.0):
        """
        Initialize recency search strategy.

        Args:
            half_life_days: Half-life for exponential decay (days)
        """
        super().__init__(name="recency")
        self.half_life_days = half_life_days

    async def search(
        self,
        memories: List[MemoryRecord],
        query: str,
        k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ScoredMemoryRecord]:
        """
        Execute recency search.

        Scoring:
        - Exponential decay based on age
        - Bonus for recent access
        - Keyword relevance (secondary)
        """
        # Apply filters
        if filters:
            memories = self._apply_filters(memories, filters)

        query_lower = query.lower()
        query_words = set(query_lower.split())
        now = datetime.now()

        results = []

        for memory in memories:
            # Time since creation
            age_seconds = (now - memory.timestamp).total_seconds()
            age_days = age_seconds / 86400.0

            # Exponential decay
            decay_score = 0.5 ** (age_days / self.half_life_days)

            # Recent access bonus
            access_bonus = 0.0
            if memory.last_accessed_at:
                access_age_seconds = (now - memory.last_accessed_at).total_seconds()
                access_age_days = access_age_seconds / 86400.0
                access_bonus = 0.5 ** (access_age_days / (self.half_life_days / 2))

            # Keyword relevance (secondary)
            keyword_score = 0.0
            if query_words:
                content_lower = memory.content.lower()
                content_words = set(content_lower.split())
                intersection = query_words & content_words
                keyword_score = len(intersection) / len(query_words) if query_words else 0.0

            # Combined score
            score = (
                decay_score * 0.5 +
                access_bonus * 0.3 +
                keyword_score * 0.2
            )

            results.append(
                ScoredMemoryRecord(**memory.model_dump(), score=score)
            )

        # Sort by score
        results.sort(key=lambda r: r.score, reverse=True)

        return results[:k]

    def _apply_filters(
        self,
        memories: List[MemoryRecord],
        filters: Dict[str, Any]
    ) -> List[MemoryRecord]:
        """Apply filters to memories."""
        filtered = memories

        if "project" in filters:
            filtered = [m for m in filtered if m.project == filters["project"]]

        if "tags" in filters:
            filtered = [
                m for m in filtered
                if m.tags and any(tag in m.tags for tag in filters["tags"])
            ]

        if "layer" in filters:
            filtered = [m for m in filtered if m.layer == filters["layer"]]

        return filtered
