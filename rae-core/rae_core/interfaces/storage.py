"""Abstract storage interface for RAE-core.

This module defines the storage interface that all storage adapters must implement.
Storage can be PostgreSQL, SQLite, in-memory, or any other backend.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from uuid import UUID


class IMemoryStorage(ABC):
    """Abstract interface for memory storage.

    Implementations must provide persistent storage for memories across
    all memory layers (sensory, working, episodic, semantic, reflective).
    """

    @abstractmethod
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
        expires_at: Optional[Any] = None,  # Added parameter
    ) -> UUID:
        """Store a new memory.

        Args:
            content: The memory content
            layer: Memory layer (sensory, working, episodic, semantic, reflective)
            tenant_id: Tenant identifier
            agent_id: Agent identifier
            tags: Optional list of tags
            metadata: Optional metadata dictionary
            embedding: Optional vector embedding
            importance: Optional importance score (0.0-1.0)
            expires_at: Optional expiration timestamp

        Returns:
            UUID of the stored memory
        """
        pass

    @abstractmethod
    async def get_memory(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> Optional[Dict[str, Any]]:
        """Retrieve a memory by ID.

        Args:
            memory_id: UUID of the memory
            tenant_id: Tenant identifier

        Returns:
            Memory dictionary or None if not found
        """
        pass

    @abstractmethod
    async def update_memory(
        self,
        memory_id: UUID,
        tenant_id: str,
        updates: Dict[str, Any],
    ) -> bool:
        """Update a memory.

        Args:
            memory_id: UUID of the memory
            tenant_id: Tenant identifier
            updates: Dictionary of fields to update

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def delete_memory(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> bool:
        """Delete a memory.

        Args:
            memory_id: UUID of the memory
            tenant_id: Tenant identifier

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def list_memories(
        self,
        tenant_id: str,
        agent_id: Optional[str] = None,
        layer: Optional[str] = None,
        tags: Optional[List[str]] = None,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        offset: int = 0,
        order_by: str = "created_at",
        order_direction: str = "desc",
    ) -> List[Dict[str, Any]]:
        """List memories with filtering and sorting.

        Args:
            tenant_id: Tenant identifier
            agent_id: Optional agent filter
            layer: Optional layer filter
            tags: Optional tags filter (OR logic)
            filters: Optional additional filters
            limit: Maximum number of results
            offset: Pagination offset
            order_by: Field to sort by
            order_direction: "asc" or "desc"

        Returns:
            List of memory dictionaries
        """
        pass

    @abstractmethod
    async def delete_memories_with_metadata_filter(
        self,
        tenant_id: str,
        agent_id: str,
        layer: str,
        metadata_filter: Dict[str, Any],
    ) -> int:
        """Delete memories matching metadata filter.

        Args:
            tenant_id: Tenant identifier
            agent_id: Agent identifier
            layer: Memory layer
            metadata_filter: Filter criteria

        Returns:
            Number of memories deleted
        """
        pass

    @abstractmethod
    async def delete_memories_below_importance(
        self,
        tenant_id: str,
        agent_id: str,
        layer: str,
        importance_threshold: float,
    ) -> int:
        """Delete memories below importance threshold.

        Args:
            tenant_id: Tenant identifier
            agent_id: Agent identifier
            layer: Memory layer
            importance_threshold: Minimum importance to keep

        Returns:
            Number of memories deleted
        """
        pass

    @abstractmethod
    async def count_memories(
        self,
        tenant_id: str,
        agent_id: Optional[str] = None,
        layer: Optional[str] = None,
    ) -> int:
        """Count memories matching filters.

        Args:
            tenant_id: Tenant identifier
            agent_id: Optional agent filter
            layer: Optional layer filter

        Returns:
            Count of matching memories
        """
        pass

    @abstractmethod
    async def search_memories(
        self,
        query: str,
        tenant_id: str,
        agent_id: str,
        layer: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search memories using full-text search.

        Args:
            query: Search query
            tenant_id: Tenant identifier
            agent_id: Agent identifier
            layer: Memory layer
            limit: Maximum number of results
            filters: Optional filters

        Returns:
            List of dictionaries containing 'memory' (dict) and 'score' (float)
        """
        pass

    @abstractmethod
    async def delete_expired_memories(
        self,
        tenant_id: str,
        agent_id: str,
        layer: str,
    ) -> int:
        """Delete expired memories.

        Args:
            tenant_id: Tenant identifier
            agent_id: Agent identifier
            layer: Memory layer

        Returns:
            Number of memories deleted
        """
        pass

    @abstractmethod
    async def update_memory_access(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> bool:
        """Update last access time and increment usage count.

        Args:
            memory_id: UUID of the memory
            tenant_id: Tenant identifier

        Returns:
            True if successful, False otherwise
        """
        pass

    @abstractmethod
    async def update_memory_expiration(
        self,
        memory_id: UUID,
        tenant_id: str,
        expires_at: Any,
    ) -> bool:
        """Update memory expiration time.

        Args:
            memory_id: UUID of the memory
            tenant_id: Tenant identifier
            expires_at: New expiration timestamp

        Returns:
            True if successful, False otherwise
        """
        pass
