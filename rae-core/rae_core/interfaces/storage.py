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
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """List memories with filtering.

        Args:
            tenant_id: Tenant identifier
            agent_id: Optional agent filter
            layer: Optional layer filter
            tags: Optional tags filter (OR logic)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            List of memory dictionaries
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
    async def increment_access_count(
        self,
        memory_id: UUID,
        tenant_id: str,
    ) -> bool:
        """Increment access count for a memory.

        Args:
            memory_id: UUID of the memory
            tenant_id: Tenant identifier

        Returns:
            True if successful, False otherwise
        """
        pass
