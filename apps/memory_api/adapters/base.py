from abc import ABC, abstractmethod
from typing import Any

from apps.memory_api.core.contract import MemoryContract, ValidationResult


class MemoryAdapter(ABC):
    """
    Abstract base class for memory backend adapters.
    Each adapter (Postgres, Redis, Qdrant, etc.) must implement this interface
    to participate in the Memory Contract Validation process.
    """

    @abstractmethod
    async def validate(self, contract: MemoryContract) -> ValidationResult:
        """
        Validates that the backend storage conforms to the provided memory contract.

        Args:
            contract: The abstract memory contract definition.

        Returns:
            ValidationResult indicating validity and any violations.
        """
        pass
