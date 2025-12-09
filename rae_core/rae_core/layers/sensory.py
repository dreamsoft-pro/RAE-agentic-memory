"""
Sensory Layer - Raw input buffer (Layer 1).

Holds raw, unprocessed inputs for milliseconds to seconds.
Acts as an attention buffer before selection into working memory.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from rae_core.layers.base import BaseLayer
from rae_core.models.memory import MemoryRecord, ScoredMemoryRecord


class SensoryLayer(BaseLayer):
    """
    Sensory layer - raw input buffer.

    Characteristics:
    - Very short retention (seconds)
    - High throughput
    - Minimal processing
    - Automatic decay
    - Attention-based selection for working memory

    This layer mimics sensory memory in cognitive psychology.
    """

    def __init__(self, max_size: int = 100, retention_seconds: int = 10):
        """
        Initialize sensory layer.

        Args:
            max_size: Maximum number of memories (FIFO eviction)
            retention_seconds: Auto-decay time
        """
        super().__init__(name="sensory")
        self.max_size = max_size
        self.retention_seconds = retention_seconds
        self._memories: Dict[str, MemoryRecord] = {}

    async def store(self, memory: MemoryRecord) -> str:
        """Store memory in sensory buffer."""
        # Auto-decay old memories
        await self._decay_old_memories()

        # FIFO eviction if at capacity
        if len(self._memories) >= self.max_size:
            oldest_id = min(
                self._memories.keys(),
                key=lambda k: self._memories[k].timestamp
            )
            del self._memories[oldest_id]

        self._memories[memory.id] = memory
        self.memory_count = len(self._memories)

        return memory.id

    async def retrieve(
        self,
        query: str,
        k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ScoredMemoryRecord]:
        """
        Retrieve from sensory buffer.

        Simple recency-based retrieval (no semantic search in sensory layer).
        """
        await self._decay_old_memories()

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

        # Sort by recency
        memories.sort(key=lambda m: m.timestamp, reverse=True)

        # Simple scoring: 1.0 for most recent, decaying
        results = []
        for i, mem in enumerate(memories[:k]):
            score = 1.0 - (i / len(memories))
            results.append(
                ScoredMemoryRecord(**mem.model_dump(), score=score)
            )

        return results

    async def get_by_id(self, memory_id: str) -> Optional[MemoryRecord]:
        """Get memory by ID."""
        await self._decay_old_memories()
        return self._memories.get(memory_id)

    async def delete(self, memory_id: str) -> bool:
        """Delete memory."""
        if memory_id in self._memories:
            del self._memories[memory_id]
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
        Consolidate to working memory based on attention/importance.

        Args:
            target_layer: Working memory layer
            criteria: Selection criteria (importance_threshold, etc.)
        """
        await self._decay_old_memories()

        # Default criteria
        importance_threshold = 0.5
        if criteria:
            importance_threshold = criteria.get("importance_threshold", 0.5)

        # Select memories for consolidation
        selected = [
            mem for mem in self._memories.values()
            if mem.importance >= importance_threshold
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
        await self._decay_old_memories()

        if not self._memories:
            return {
                "count": 0,
                "capacity_used": 0.0,
                "oldest": None,
                "newest": None
            }

        memories = list(self._memories.values())
        return {
            "count": len(memories),
            "capacity_used": len(memories) / self.max_size,
            "oldest": min(m.timestamp for m in memories),
            "newest": max(m.timestamp for m in memories),
            "avg_importance": sum(m.importance for m in memories) / len(memories)
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
            count = len(to_delete)
        else:
            count = len(self._memories)
            self._memories.clear()

        self.memory_count = len(self._memories)
        return count

    async def _decay_old_memories(self):
        """Remove memories older than retention period."""
        cutoff = datetime.now() - timedelta(seconds=self.retention_seconds)
        to_delete = [
            mid for mid, mem in self._memories.items()
            if mem.timestamp < cutoff
        ]
        for mid in to_delete:
            del self._memories[mid]

        self.memory_count = len(self._memories)
