"""
Long-Term Memory Layer - Persistent storage (Layer 3).

Holds consolidated, important information indefinitely.
Implements semantic search and importance-based retrieval.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from rae_core.layers.base import BaseLayer
from rae_core.models.memory import MemoryRecord, ScoredMemoryRecord


class LongTermMemoryLayer(BaseLayer):
    """
    Long-term memory layer - persistent storage.

    Characteristics:
    - Unlimited capacity (or very large)
    - Semantic organization
    - Importance-based retrieval
    - Periodic consolidation to reflective layer

    This layer mimics long-term memory in cognitive psychology.
    """

    def __init__(self):
        """Initialize long-term memory layer."""
        super().__init__(name="longterm")
        self._memories: Dict[str, MemoryRecord] = {}
        self._index: Dict[str, List[str]] = {}  # Simple keyword index

    async def store(self, memory: MemoryRecord) -> str:
        """Store memory in long-term memory."""
        self._memories[memory.id] = memory
        self.memory_count = len(self._memories)

        # Update keyword index
        self._update_index(memory)

        return memory.id

    async def retrieve(
        self,
        query: str,
        k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ScoredMemoryRecord]:
        """
        Retrieve from long-term memory.

        Uses semantic search (simplified keyword-based) + importance.
        """
        memories = list(self._memories.values())

        # Apply filters
        if filters:
            if "project" in filters:
                memories = [m for m in memories if m.project == filters["project"]]
            if "tags" in filters:
                memories = [
                    m for m in memories
                    if m.tags and any(tag in m.tags for tag in filters["tags"])
                ]
            if "min_importance" in filters:
                memories = [
                    m for m in memories
                    if m.importance >= filters["min_importance"]
                ]
            if "layer" in filters:
                memories = [m for m in memories if m.layer == filters["layer"]]

        # Keyword-based semantic search
        query_lower = query.lower()
        query_words = set(query_lower.split())
        results = []

        for mem in memories:
            # Keyword match score
            content_lower = mem.content.lower()
            content_words = set(content_lower.split())

            # Jaccard similarity
            if query_words:
                intersection = query_words & content_words
                union = query_words | content_words
                keyword_score = len(intersection) / len(union) if union else 0.0
            else:
                keyword_score = 0.0

            # Usage frequency score
            usage_score = min(1.0, mem.usage_count / 10.0)

            # Combined score
            score = (
                keyword_score * 0.5 +
                mem.importance * 0.3 +
                usage_score * 0.2
            )

            if score > 0.0:  # Only include relevant results
                results.append(
                    ScoredMemoryRecord(**mem.model_dump(), score=score)
                )

        # Sort by score
        results.sort(key=lambda r: r.score, reverse=True)

        # Update access counts
        for result in results[:k]:
            self._memories[result.id].usage_count += 1
            self._memories[result.id].last_accessed_at = datetime.now()

        return results[:k]

    async def get_by_id(self, memory_id: str) -> Optional[MemoryRecord]:
        """Get memory by ID."""
        memory = self._memories.get(memory_id)
        if memory:
            memory.usage_count += 1
            memory.last_accessed_at = datetime.now()
        return memory

    async def delete(self, memory_id: str) -> bool:
        """Delete memory."""
        if memory_id in self._memories:
            memory = self._memories[memory_id]
            del self._memories[memory_id]
            self._remove_from_index(memory)
            self.memory_count = len(self._memories)
            return True
        return False

    async def update(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """Update memory."""
        memory = self._memories.get(memory_id)
        if not memory:
            return False

        # Remove old index entries if content changed
        if "content" in updates:
            self._remove_from_index(memory)

        for key, value in updates.items():
            if hasattr(memory, key):
                setattr(memory, key, value)

        # Update index if content changed
        if "content" in updates:
            self._update_index(memory)

        return True

    async def consolidate(
        self,
        target_layer: BaseLayer,
        criteria: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Consolidate to reflective memory based on patterns and insights.

        This typically involves:
        - Finding frequently accessed memories
        - Identifying patterns across memories
        - Creating meta-learning insights

        Args:
            target_layer: Reflective memory layer
            criteria: Selection criteria (min_usage, importance, etc.)
        """
        # Default criteria
        min_usage = 5
        min_importance = 0.7

        if criteria:
            min_usage = criteria.get("min_usage", 5)
            min_importance = criteria.get("min_importance", 0.7)

        # Select high-value memories for reflection
        selected = [
            mem for mem in self._memories.values()
            if mem.usage_count >= min_usage and mem.importance >= min_importance
        ]

        # Sort by importance * usage
        selected.sort(
            key=lambda m: m.importance * m.usage_count,
            reverse=True
        )

        # Move top candidates to reflective layer
        consolidated_ids = []
        max_consolidate = criteria.get("max_count", 10) if criteria else 10

        for memory in selected[:max_consolidate]:
            await target_layer.store(memory)
            consolidated_ids.append(memory.id)
            # Note: Don't delete from LTM, reflective layer is additional

        return consolidated_ids

    async def get_statistics(self) -> Dict[str, Any]:
        """Get statistics."""
        if not self._memories:
            return {
                "count": 0,
                "avg_importance": 0.0,
                "avg_usage": 0.0,
                "total_accesses": 0
            }

        memories = list(self._memories.values())
        return {
            "count": len(memories),
            "avg_importance": sum(m.importance for m in memories) / len(memories),
            "avg_usage": sum(m.usage_count for m in memories) / len(memories),
            "total_accesses": sum(m.usage_count for m in memories),
            "high_importance_count": sum(1 for m in memories if m.importance >= 0.7),
            "high_usage_count": sum(1 for m in memories if m.usage_count >= 5)
        }

    async def clear(self, tenant_id: Optional[str] = None) -> int:
        """Clear memories."""
        if tenant_id:
            to_delete = [
                mid for mid, mem in self._memories.items()
                if mem.tenant_id == tenant_id
            ]
            for mid in to_delete:
                memory = self._memories[mid]
                del self._memories[mid]
                self._remove_from_index(memory)
            count = len(to_delete)
        else:
            count = len(self._memories)
            self._memories.clear()
            self._index.clear()

        self.memory_count = len(self._memories)
        return count

    def _update_index(self, memory: MemoryRecord):
        """Update keyword index for memory."""
        words = memory.content.lower().split()
        for word in words:
            if word not in self._index:
                self._index[word] = []
            if memory.id not in self._index[word]:
                self._index[word].append(memory.id)

    def _remove_from_index(self, memory: MemoryRecord):
        """Remove memory from keyword index."""
        words = memory.content.lower().split()
        for word in words:
            if word in self._index and memory.id in self._index[word]:
                self._index[word].remove(memory.id)
                if not self._index[word]:
                    del self._index[word]
