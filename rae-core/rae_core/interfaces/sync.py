"""Abstract sync provider interface for RAE-core."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from uuid import UUID


class ISyncProvider(ABC):
    """Abstract interface for sync protocol (RAE-Sync)."""

    @abstractmethod
    async def push_changes(
        self, tenant_id: str, changes: List[Dict[str, Any]]
    ) -> bool:
        """Push local changes to sync endpoint."""
        pass

    @abstractmethod
    async def pull_changes(
        self, tenant_id: str, since_timestamp: str
    ) -> List[Dict[str, Any]]:
        """Pull changes from sync endpoint since timestamp."""
        pass

    @abstractmethod
    async def resolve_conflict(
        self, memory_id: UUID, local_version: Dict, remote_version: Dict
    ) -> Dict[str, Any]:
        """Resolve conflict using CRDT merge strategy."""
        pass
