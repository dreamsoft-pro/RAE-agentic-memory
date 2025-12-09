"""
Base search strategy interface.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from rae_core.models.memory import MemoryRecord, ScoredMemoryRecord


class SearchStrategy(ABC):
    """
    Abstract base class for search strategies.

    Each strategy implements a different retrieval approach:
    - Keyword-based
    - Recency-based
    - Importance-based
    - Semantic (requires embeddings)
    - Graph-based (requires knowledge graph)
    """

    def __init__(self, name: str):
        """
        Initialize search strategy.

        Args:
            name: Strategy identifier
        """
        self.name = name

    @abstractmethod
    async def search(
        self,
        memories: List[MemoryRecord],
        query: str,
        k: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ScoredMemoryRecord]:
        """
        Execute search strategy.

        Args:
            memories: List of memories to search
            query: Query text
            k: Number of results to return
            filters: Optional filters

        Returns:
            List of scored memory records
        """
        pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name='{self.name}'>"
