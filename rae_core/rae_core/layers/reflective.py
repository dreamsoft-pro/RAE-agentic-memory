"""
Reflective Memory Layer - Meta-learning and insights (Layer 4).

Holds synthesized patterns, insights, and meta-learning from long-term memory.
This is the highest layer representing deep understanding and strategic knowledge.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from rae_core.layers.base import BaseLayer
from rae_core.models.memory import MemoryRecord, ScoredMemoryRecord


class ReflectiveMemoryLayer(BaseLayer):
    """
    Reflective memory layer - meta-learning and insights.

    Characteristics:
    - Synthesized patterns and insights
    - Meta-cognitive understanding
    - Strategic knowledge
    - Generated periodically from LTM patterns

    This layer represents the highest level of cognitive processing:
    learning about learning, understanding patterns, strategic thinking.
    """

    def __init__(self):
        """Initialize reflective memory layer."""
        super().__init__(name="reflective")
        self._reflections: Dict[str, MemoryRecord] = {}
        self._patterns: Dict[str, List[str]] = {}  # Pattern -> memory IDs

    async def store(self, memory: MemoryRecord) -> str:
        """
        Store reflection in reflective memory.

        Reflections are typically synthesized insights, not raw memories.
        """
        self._reflections[memory.id] = memory
        self.memory_count = len(self._reflections)

        # Index by tags (patterns)
        if memory.tags:
            for tag in memory.tags:
                if tag not in self._patterns:
                    self._patterns[tag] = []
                if memory.id not in self._patterns[tag]:
                    self._patterns[tag].append(memory.id)

        return memory.id

    async def retrieve(
        self,
        query: str,
        k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ScoredMemoryRecord]:
        """
        Retrieve reflections.

        Focuses on high-level pattern matching and conceptual understanding.
        """
        reflections = list(self._reflections.values())

        # Apply filters
        if filters:
            if "project" in filters:
                reflections = [r for r in reflections if r.project == filters["project"]]
            if "tags" in filters:
                reflections = [
                    r for r in reflections
                    if r.tags and any(tag in r.tags for tag in filters["tags"])
                ]
            if "min_importance" in filters:
                reflections = [
                    r for r in reflections
                    if r.importance >= filters["min_importance"]
                ]

        # Semantic matching (keyword-based for patterns)
        query_lower = query.lower()
        query_words = set(query_lower.split())
        results = []

        for reflection in reflections:
            # Content matching
            content_lower = reflection.content.lower()
            content_words = set(content_lower.split())

            # Tag matching (patterns)
            tag_match = 0.0
            if reflection.tags and query_words:
                tag_words = set(' '.join(reflection.tags).lower().split())
                tag_match = len(query_words & tag_words) / len(query_words)

            # Content matching
            if query_words:
                intersection = query_words & content_words
                union = query_words | content_words
                content_match = len(intersection) / len(union) if union else 0.0
            else:
                content_match = 0.0

            # Combined score (reflections prioritize pattern matching)
            score = (
                content_match * 0.4 +
                tag_match * 0.3 +
                reflection.importance * 0.3
            )

            if score > 0.0:
                results.append(
                    ScoredMemoryRecord(**reflection.model_dump(), score=score)
                )

        # Sort by score
        results.sort(key=lambda r: r.score, reverse=True)

        # Update access counts
        for result in results[:k]:
            self._reflections[result.id].usage_count += 1
            self._reflections[result.id].last_accessed_at = datetime.now()

        return results[:k]

    async def get_by_id(self, memory_id: str) -> Optional[MemoryRecord]:
        """Get reflection by ID."""
        reflection = self._reflections.get(memory_id)
        if reflection:
            reflection.usage_count += 1
            reflection.last_accessed_at = datetime.now()
        return reflection

    async def delete(self, memory_id: str) -> bool:
        """Delete reflection."""
        if memory_id in self._reflections:
            reflection = self._reflections[memory_id]

            # Remove from pattern index
            if reflection.tags:
                for tag in reflection.tags:
                    if tag in self._patterns and memory_id in self._patterns[tag]:
                        self._patterns[tag].remove(memory_id)
                        if not self._patterns[tag]:
                            del self._patterns[tag]

            del self._reflections[memory_id]
            self.memory_count = len(self._reflections)
            return True
        return False

    async def update(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """Update reflection."""
        reflection = self._reflections.get(memory_id)
        if not reflection:
            return False

        # Remove old tags from index if tags changed
        if "tags" in updates and reflection.tags:
            for tag in reflection.tags:
                if tag in self._patterns and memory_id in self._patterns[tag]:
                    self._patterns[tag].remove(memory_id)

        # Update fields
        for key, value in updates.items():
            if hasattr(reflection, key):
                setattr(reflection, key, value)

        # Re-index new tags
        if "tags" in updates and reflection.tags:
            for tag in reflection.tags:
                if tag not in self._patterns:
                    self._patterns[tag] = []
                if memory_id not in self._patterns[tag]:
                    self._patterns[tag].append(memory_id)

        return True

    async def consolidate(
        self,
        target_layer: BaseLayer,
        criteria: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Consolidate reflections.

        Reflective layer is typically the top layer, so consolidation
        usually means synthesizing multiple reflections into higher-level insights.

        For now, this is a no-op (reflections stay in reflective layer).
        """
        # Reflective layer doesn't consolidate upward (it's the top)
        # Future: Could consolidate similar reflections into meta-reflections
        return []

    async def get_statistics(self) -> Dict[str, Any]:
        """Get statistics."""
        if not self._reflections:
            return {
                "count": 0,
                "pattern_count": 0,
                "avg_importance": 0.0
            }

        reflections = list(self._reflections.values())
        return {
            "count": len(reflections),
            "pattern_count": len(self._patterns),
            "avg_importance": sum(r.importance for r in reflections) / len(reflections),
            "total_accesses": sum(r.usage_count for r in reflections),
            "high_importance_count": sum(1 for r in reflections if r.importance >= 0.8)
        }

    async def clear(self, tenant_id: Optional[str] = None) -> int:
        """Clear reflections."""
        if tenant_id:
            to_delete = [
                rid for rid, refl in self._reflections.items()
                if refl.tenant_id == tenant_id
            ]
            for rid in to_delete:
                await self.delete(rid)
            count = len(to_delete)
        else:
            count = len(self._reflections)
            self._reflections.clear()
            self._patterns.clear()

        self.memory_count = len(self._reflections)
        return count

    async def get_patterns(self) -> Dict[str, int]:
        """
        Get identified patterns with counts.

        Returns:
            Dictionary of pattern -> occurrence count
        """
        return {
            pattern: len(memory_ids)
            for pattern, memory_ids in self._patterns.items()
        }

    async def get_reflections_by_pattern(self, pattern: str) -> List[MemoryRecord]:
        """
        Get all reflections associated with a pattern.

        Args:
            pattern: Pattern/tag to search for

        Returns:
            List of reflections with this pattern
        """
        memory_ids = self._patterns.get(pattern, [])
        return [
            self._reflections[mid]
            for mid in memory_ids
            if mid in self._reflections
        ]
