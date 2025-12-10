"""In-Memory storage adapter for RAE-core.

Fast, thread-safe implementation using Python dictionaries.
Ideal for testing, development, and lightweight deployments.
"""

import asyncio
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from rae_core.interfaces.storage import IMemoryStorage


class InMemoryStorage(IMemoryStorage):
    """In-memory implementation of IMemoryStorage.

    Features:
    - Fast dictionary-based storage
    - Thread-safe operations with asyncio.Lock
    - Automatic timestamps and versioning
    - Filtering by layer, agent, and tags
    - Access count tracking
    """

    def __init__(self):
        """Initialize in-memory storage."""
        # Main storage: {memory_id: memory_dict}
        self._memories: Dict[UUID, Dict[str, Any]] = {}

        # Indexes for fast lookups
        self._by_tenant: Dict[str, set[UUID]] = defaultdict(set)
        self._by_agent: Dict[tuple[str, str], set[UUID]] = defaultdict(set)  # (tenant, agent)
        self._by_layer: Dict[tuple[str, str], set[UUID]] = defaultdict(set)  # (tenant, layer)
        self._by_tags: Dict[tuple[str, str], set[UUID]] = defaultdict(set)  # (tenant, tag)

        # Thread safety
        self._lock = asyncio.Lock()

    async def store_memory(
        self,
        content: str,
        layer: str,
        tenant_id: str,
        agent_id: str,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
        importance: Optional[float] = None,
    ) -> UUID:
        """Store a new memory."""
        async with self._lock:
            memory_id = uuid4()
            now = datetime.utcnow()

            memory = {
                "id": memory_id,
                "content": content,
                "layer": layer,
                "tenant_id": tenant_id,
                "agent_id": agent_id,
                "tags": tags or [],
                "metadata": metadata or {},
                "embedding": embedding,
                "importance": importance or 0.5,
                "created_at": now,
                "modified_at": now,
                "last_accessed_at": now,
                "access_count": 0,
                "version": 1,
            }

            # Store memory
            self._memories[memory_id] = memory

            # Update indexes
            self._by_tenant[tenant_id].add(memory_id)
            self._by_agent[(tenant_id, agent_id)].add(memory_id)
            self._by_layer[(tenant_id, layer)].add(memory_id)

            for tag in tags or []:
                self._by_tags[(tenant_id, tag)].add(memory_id)

            return memory_id

    async def get_memory(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Retrieve a memory by ID."""
        async with self._lock:
            memory = self._memories.get(memory_id)

            if memory and memory["tenant_id"] == tenant_id:
                # Return a copy to prevent external modifications
                return memory.copy()

            return None

    async def update_memory(
        self,
        memory_id: UUID,
        tenant_id: str,
        updates: Dict[str, Any],
    ) -> bool:
        """Update a memory."""
        async with self._lock:
            memory = self._memories.get(memory_id)

            if not memory or memory["tenant_id"] != tenant_id:
                return False

            # Handle tag updates (update index)
            old_tags = set(memory.get("tags", []))
            new_tags = set(updates.get("tags", old_tags))

            removed_tags = old_tags - new_tags
            added_tags = new_tags - old_tags

            for tag in removed_tags:
                self._by_tags[(tenant_id, tag)].discard(memory_id)

            for tag in added_tags:
                self._by_tags[(tenant_id, tag)].add(memory_id)

            # Handle layer updates (update index)
            old_layer = memory.get("layer")
            new_layer = updates.get("layer", old_layer)

            if old_layer != new_layer:
                self._by_layer[(tenant_id, old_layer)].discard(memory_id)
                self._by_layer[(tenant_id, new_layer)].add(memory_id)

            # Update memory
            memory.update(updates)
            memory["modified_at"] = datetime.utcnow()
            memory["version"] = memory.get("version", 1) + 1

            return True

    async def delete_memory(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> bool:
        """Delete a memory."""
        async with self._lock:
            memory = self._memories.get(memory_id)

            if not memory or memory["tenant_id"] != tenant_id:
                return False

            # Remove from indexes
            self._by_tenant[tenant_id].discard(memory_id)
            self._by_agent[(tenant_id, memory["agent_id"])].discard(memory_id)
            self._by_layer[(tenant_id, memory["layer"])].discard(memory_id)

            for tag in memory.get("tags", []):
                self._by_tags[(tenant_id, tag)].discard(memory_id)

            # Remove memory
            del self._memories[memory_id]

            return True

    async def list_memories(
        self,
        tenant_id: str,
        agent_id: Optional[str] = None,
        layer: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """List memories with filtering."""
        async with self._lock:
            # Start with tenant memories
            candidate_ids = self._by_tenant[tenant_id].copy()

            # Apply filters using indexes
            if agent_id:
                candidate_ids &= self._by_agent[(tenant_id, agent_id)]

            if layer:
                candidate_ids &= self._by_layer[(tenant_id, layer)]

            if tags:
                # OR logic for tags
                tag_ids = set()
                for tag in tags:
                    tag_ids |= self._by_tags[(tenant_id, tag)]
                candidate_ids &= tag_ids

            # Get memories and sort by created_at
            memories = [
                self._memories[mid].copy()
                for mid in candidate_ids
                if mid in self._memories
            ]
            memories.sort(key=lambda m: m["created_at"], reverse=True)

            # Apply pagination
            return memories[offset : offset + limit]

    async def count_memories(
        self,
        tenant_id: str,
        agent_id: Optional[str] = None,
        layer: Optional[str] = None,
    ) -> int:
        """Count memories matching filters."""
        async with self._lock:
            # Start with tenant memories
            candidate_ids = self._by_tenant[tenant_id].copy()

            # Apply filters
            if agent_id:
                candidate_ids &= self._by_agent[(tenant_id, agent_id)]

            if layer:
                candidate_ids &= self._by_layer[(tenant_id, layer)]

            return len(candidate_ids)

    async def increment_access_count(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> bool:
        """Increment access count for a memory."""
        async with self._lock:
            memory = self._memories.get(memory_id)

            if not memory or memory["tenant_id"] != tenant_id:
                return False

            memory["access_count"] = memory.get("access_count", 0) + 1
            memory["last_accessed_at"] = datetime.utcnow()

            return True

    async def clear_tenant(self, tenant_id: str) -> int:
        """Clear all memories for a tenant.

        Args:
            tenant_id: Tenant identifier

        Returns:
            Number of memories deleted
        """
        async with self._lock:
            memory_ids = self._by_tenant[tenant_id].copy()

            for memory_id in memory_ids:
                memory = self._memories.get(memory_id)
                if memory:
                    # Remove from all indexes
                    self._by_agent[(tenant_id, memory["agent_id"])].discard(memory_id)
                    self._by_layer[(tenant_id, memory["layer"])].discard(memory_id)

                    for tag in memory.get("tags", []):
                        self._by_tags[(tenant_id, tag)].discard(memory_id)

                    # Remove memory
                    del self._memories[memory_id]

            # Clear tenant index
            del self._by_tenant[tenant_id]

            return len(memory_ids)

    async def get_statistics(self) -> Dict[str, Any]:
        """Get storage statistics.

        Returns:
            Dictionary with storage statistics
        """
        async with self._lock:
            return {
                "total_memories": len(self._memories),
                "tenants": len(self._by_tenant),
                "agents": len(self._by_agent),
                "layers": len(self._by_layer),
                "unique_tags": len(self._by_tags),
            }

    async def clear_all(self) -> int:
        """Clear all data (use with caution!).

        Returns:
            Number of memories deleted
        """
        async with self._lock:
            count = len(self._memories)

            self._memories.clear()
            self._by_tenant.clear()
            self._by_agent.clear()
            self._by_layer.clear()
            self._by_tags.clear()

            return count
