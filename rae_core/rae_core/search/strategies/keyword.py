"""
Keyword-based search strategy.
"""

from typing import Any, Dict, List, Optional

from rae_core.models.memory import MemoryRecord, ScoredMemoryRecord
from rae_core.search.strategies.base import SearchStrategy


class KeywordSearchStrategy(SearchStrategy):
    """
    Keyword-based search using simple term matching.

    Uses TF-IDF-like scoring with keyword overlap.
    """

    def __init__(self):
        """Initialize keyword search strategy."""
        super().__init__(name="keyword")

    async def search(
        self,
        memories: List[MemoryRecord],
        query: str,
        k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ScoredMemoryRecord]:
        """
        Execute keyword search.

        Scoring:
        - Jaccard similarity (word overlap)
        - Term frequency
        - Query coverage
        """
        # Apply filters
        if filters:
            memories = self._apply_filters(memories, filters)

        query_lower = query.lower()
        query_words = set(query_lower.split())

        if not query_words:
            return []

        results = []

        for memory in memories:
            content_lower = memory.content.lower()
            content_words = set(content_lower.split())

            # Jaccard similarity
            intersection = query_words & content_words
            union = query_words | content_words
            jaccard_score = len(intersection) / len(union) if union else 0.0

            # Query coverage (what % of query words are in content)
            coverage_score = len(intersection) / len(query_words)

            # Term frequency (how many times query words appear)
            tf_score = sum(
                content_lower.count(word)
                for word in intersection
            ) / len(content_lower.split()) if content_lower else 0.0

            # Combined score
            score = (
                jaccard_score * 0.4 +
                coverage_score * 0.4 +
                tf_score * 0.2
            )

            if score > 0.0:
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
