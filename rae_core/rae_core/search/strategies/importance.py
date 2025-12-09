"""
Importance-based search strategy.
"""

from typing import Any, Dict, List, Optional

from rae_core.models.memory import MemoryRecord, ScoredMemoryRecord
from rae_core.search.strategies.base import SearchStrategy


class ImportanceSearchStrategy(SearchStrategy):
    """
    Importance-based search prioritizing high-value memories.

    Combines importance score with usage frequency and keyword relevance.
    """

    def __init__(self):
        """Initialize importance search strategy."""
        super().__init__(name="importance")

    async def search(
        self,
        memories: List[MemoryRecord],
        query: str,
        k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ScoredMemoryRecord]:
        """
        Execute importance search.

        Scoring:
        - Memory importance (primary)
        - Usage frequency
        - Keyword relevance (secondary)
        """
        # Apply filters
        if filters:
            memories = self._apply_filters(memories, filters)

        query_lower = query.lower()
        query_words = set(query_lower.split())

        results = []

        for memory in memories:
            # Importance score (primary factor)
            importance_score = memory.importance

            # Usage frequency score (logarithmic)
            usage_score = 0.0
            if memory.usage_count > 0:
                import math
                usage_score = min(1.0, math.log10(memory.usage_count + 1) / 2.0)

            # Keyword relevance (secondary)
            keyword_score = 0.0
            if query_words:
                content_lower = memory.content.lower()
                content_words = set(content_lower.split())
                intersection = query_words & content_words
                keyword_score = len(intersection) / len(query_words) if query_words else 0.0

            # Combined score
            score = (
                importance_score * 0.5 +
                usage_score * 0.3 +
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

        if "min_importance" in filters:
            filtered = [
                m for m in filtered
                if m.importance >= filters["min_importance"]
            ]

        return filtered
