"""Search strategy interfaces and implementations."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID


class SearchStrategy(ABC):
    """Base class for all search strategies."""

    @abstractmethod
    async def search(
        self,
        query: str,
        tenant_id: str,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10,
    ) -> List[Tuple[UUID, float]]:
        """Execute search and return (memory_id, score) tuples.

        Args:
            query: Search query string
            tenant_id: Tenant identifier
            filters: Optional filters (layer, agent_id, tags, etc.)
            limit: Maximum number of results

        Returns:
            List of (memory_id, score) tuples sorted by score descending
        """
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Return the name of this strategy."""
        pass

    @abstractmethod
    def get_strategy_weight(self) -> float:
        """Return default weight for hybrid search fusion (0.0-1.0)."""
        pass
