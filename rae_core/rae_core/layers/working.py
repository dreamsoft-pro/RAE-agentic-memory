"""
Working Memory Layer - Active processing (Layer 2).

Holds actively processed information for seconds to minutes.
Implements attention-based selection and importance scoring.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from rae_core.layers.base import BaseLayer
from rae_core.models.memory import MemoryRecord, ScoredMemoryRecord


class WorkingMemoryLayer(BaseLayer):
    """
    Working memory layer - active processing.

    Characteristics:
    - Limited capacity (7±2 items - Miller's Law)
    - Active rehearsal
    - Importance-based retention
    - Consolidation to long-term memory

    This layer mimics working memory in cognitive psychology.
    """

    def __init__(self, max_size: int = 50, retention_minutes: int = 30):
        """
        Initialize working memory layer.

        Args:
            max_size: Maximum number of memories (capacity-based eviction)
            retention_minutes: Auto-decay time for low-importance items
        """
        super().__init__(name="working")
        self.max_size = max_size
        self.retention_minutes = retention_minutes
        self._memories: Dict[str, MemoryRecord] = {}
        self._access_times: Dict[str, datetime] = {}

    async def store(self, memory: MemoryRecord) -> str:
        """Store memory in working memory."""
        # Capacity-based eviction (remove lowest importance if at capacity)
        if len(self._memories) >= self.max_size:
            lowest_id = min(
                self._memories.keys(),
                key=lambda k: (
                    self._memories[k].importance,
                    -self._memories[k].usage_count,
                    self._memories[k].timestamp
                )
            )
            del self._memories[lowest_id]
            if lowest_id in self._access_times:
                del self._access_times[lowest_id]

        self._memories[memory.id] = memory
        self._access_times[memory.id] = datetime.now()
        self.memory_count = len(self._memories)

        return memory.id

    async def retrieve(
        self,
        query: str,
        k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ScoredMemoryRecord]:
        """
        Retrieve from working memory.

        Uses importance + recency scoring.
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

        # Simple keyword matching + importance scoring
        query_lower = query.lower()
        results = []

        for mem in memories:
            # Keyword match score
            content_lower = mem.content.lower()
            keyword_score = sum(
                1.0 for word in query_lower.split()
                if word in content_lower
            ) / max(len(query_lower.split()), 1)

            # Recency score
            age_seconds = (datetime.now() - mem.timestamp).total_seconds()
            recency_score = max(0.0, 1.0 - (age_seconds / (self.retention_minutes * 60)))

            # Combined score
            score = (
                keyword_score * 0.4 +
                mem.importance * 0.4 +
                recency_score * 0.2
            )

            results.append(
                ScoredMemoryRecord(**mem.model_dump(), score=score)
            )

        # Sort by score
        results.sort(key=lambda r: r.score, reverse=True)

        # Update access times
        for result in results[:k]:
            self._access_times[result.id] = datetime.now()
            self._memories[result.id].usage_count += 1
            self._memories[result.id].last_accessed_at = datetime.now()

        return results[:k]

    async def get_by_id(self, memory_id: str) -> Optional[MemoryRecord]:
        """Get memory by ID."""
        memory = self._memories.get(memory_id)
        if memory:
            self._access_times[memory_id] = datetime.now()
            memory.usage_count += 1
            memory.last_accessed_at = datetime.now()
        return memory

    async def delete(self, memory_id: str) -> bool:
        """Delete memory."""
        if memory_id in self._memories:
            del self._memories[memory_id]
            if memory_id in self._access_times:
                del self._access_times[memory_id]
            self.memory_count = len(self._memories)
            return True
        return False

    async def update(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """Update memory."""
        memory = self._memories.get(memory_id)
        if not memory:
            return False

        for key, value in updates.items():
            if hasattr(memory, key):
                setattr(memory, key, value)

        return True

    async def consolidate(
        self,
        target_layer: BaseLayer,
        criteria: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Consolidate to long-term memory based on importance and usage.

        Args:
            target_layer: Long-term memory layer
            criteria: Selection criteria (importance_threshold, min_usage, etc.)
        """
        # Default criteria
        importance_threshold = 0.6
        min_usage = 2
        min_age_minutes = 10

        if criteria:
            importance_threshold = criteria.get("importance_threshold", 0.6)
            min_usage = criteria.get("min_usage", 2)
            min_age_minutes = criteria.get("min_age_minutes", 10)

        # Select memories for consolidation
        cutoff_time = datetime.now() - timedelta(minutes=min_age_minutes)
        selected = [
            mem for mem in self._memories.values()
            if (
                mem.importance >= importance_threshold and
                mem.usage_count >= min_usage and
                mem.timestamp < cutoff_time
            )
        ]

        # Move to target layer
        consolidated_ids = []
        for memory in selected:
            await target_layer.store(memory)
            await self.delete(memory.id)
            consolidated_ids.append(memory.id)

        return consolidated_ids

    async def get_statistics(self) -> Dict[str, Any]:
        """Get statistics."""
        if not self._memories:
            return {
                "count": 0,
                "capacity_used": 0.0,
                "avg_importance": 0.0,
                "avg_usage": 0.0
            }

        memories = list(self._memories.values())
        return {
            "count": len(memories),
            "capacity_used": len(memories) / self.max_size,
            "avg_importance": sum(m.importance for m in memories) / len(memories),
            "avg_usage": sum(m.usage_count for m in memories) / len(memories),
            "high_importance_count": sum(1 for m in memories if m.importance >= 0.7)
        }

    async def clear(self, tenant_id: Optional[str] = None) -> int:
        """Clear memories."""
        if tenant_id:
            to_delete = [
                mid for mid, mem in self._memories.items()
                if mem.tenant_id == tenant_id
            ]
            for mid in to_delete:
                del self._memories[mid]
                if mid in self._access_times:
                    del self._access_times[mid]
            count = len(to_delete)
        else:
            count = len(self._memories)
            self._memories.clear()
            self._access_times.clear()

        self.memory_count = len(self._memories)
        return count
