from abc import ABC, abstractmethod
from typing import Any, List, Dict
from uuid import UUID

class IMathematicalTheory(ABC):
    @abstractmethod
    def process(self, candidates: List[Dict[str, Any]], query: str, profile: Dict[str, Any]) -> List[tuple[UUID, float]]:
        """Processes candidates using a specific mathematical theory."""
        pass
