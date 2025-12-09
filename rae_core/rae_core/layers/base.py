"""
Base layer abstraction for RAE-Core memory architecture.

Defines the abstract interface that all memory layers must implement.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional

from rae_core.models.memory import MemoryRecord, ScoredMemoryRecord


class BaseLayer(ABC):
    """
    Abstract base class for all memory layers.

    Each layer implements its own storage, retrieval, and consolidation logic.
    Layers are:
    - Sensory: Raw input buffer (milliseconds to seconds)
    - Working: Active processing (seconds to minutes)
    - Long-term: Persistent storage (minutes to forever)
    - Reflective: Meta-learning and insights (periodic consolidation)
    """

    def __init__(self, name: str):
        """
        Initialize base layer.

        Args:
            name: Layer identifier (e.g., "sensory", "working", "longterm", "reflective")
        """
        self.name = name
        self.memory_count = 0
        self.created_at = datetime.now()

    @abstractmethod
    async def store(self, memory: MemoryRecord) -> str:
        """
        Store a memory in this layer.

        Args:
            memory: Memory record to store

        Returns:
            Memory ID

        Raises:
            ValueError: If memory validation fails
        """
        pass

    @abstractmethod
    async def retrieve(
        self,
        query: str,
        k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ScoredMemoryRecord]:
        """
        Retrieve memories from this layer.

        Args:
            query: Query text for semantic search
            k: Number of results to return
            filters: Optional filters (tags, project, etc.)

        Returns:
            List of scored memory records
        """
        pass

    @abstractmethod
    async def get_by_id(self, memory_id: str) -> Optional[MemoryRecord]:
        """
        Retrieve a specific memory by ID.

        Args:
            memory_id: Memory identifier

        Returns:
            Memory record or None if not found
        """
        pass

    @abstractmethod
    async def delete(self, memory_id: str) -> bool:
        """
        Delete a memory from this layer.

        Args:
            memory_id: Memory identifier

        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    async def update(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update memory fields.

        Args:
            memory_id: Memory identifier
            updates: Fields to update

        Returns:
            True if updated, False if not found
        """
        pass

    @abstractmethod
    async def consolidate(
        self,
        target_layer: "BaseLayer",
        criteria: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Consolidate memories from this layer to target layer.

        This is the core mechanism for memory promotion through layers:
        - Sensory → Working (attention-based selection)
        - Working → Long-term (importance-based consolidation)
        - Long-term → Reflective (pattern extraction)

        Args:
            target_layer: Destination layer
            criteria: Consolidation criteria (importance, age, access_count, etc.)

        Returns:
            List of consolidated memory IDs
        """
        pass

    @abstractmethod
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Get layer statistics.

        Returns:
            Dictionary with stats (count, size, oldest, newest, etc.)
        """
        pass

    @abstractmethod
    async def clear(self, tenant_id: Optional[str] = None) -> int:
        """
        Clear all memories in this layer.

        Args:
            tenant_id: Optional tenant filter

        Returns:
            Number of memories cleared
        """
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name='{self.name}' count={self.memory_count}>"
