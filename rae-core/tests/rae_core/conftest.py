"""Core testing fixtures and mocks."""

import asyncio
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

import pytest

from rae_core.interfaces.storage import IMemoryStorage


class MockMemoryStorage(IMemoryStorage):
    """Simple mock storage for unit tests."""

    def __init__(self):
        self._memories: dict[UUID, dict[str, Any]] = {}
        self._lock = asyncio.Lock()  # To simulate async behavior

    async def store_memory(self, **kwargs: Any) -> UUID:
        async with self._lock:
            memory_id = uuid4()
            now = datetime.now(timezone.utc)

            memory = {
                "id": memory_id,
                "content": kwargs.get("content", ""),
                "layer": kwargs.get("layer", "episodic"),
                "tenant_id": kwargs.get("tenant_id", "default"),
                "agent_id": kwargs.get("agent_id", "default"),
                "importance": kwargs.get("importance", 0.5),
                "created_at": now,
            }
            self._memories[memory_id] = memory
            return memory_id

    async def get_memory(
        self, memory_id: UUID, tenant_id: str
    ) -> dict[str, Any] | None:
        async with self._lock:
            memory = self._memories.get(memory_id)
            if memory and memory["tenant_id"] == tenant_id:
                return memory.copy()
            return None

    async def update_memory(
        self, memory_id: UUID, tenant_id: str, updates: dict[str, Any]
    ) -> bool:
        async with self._lock:
            memory = self._memories.get(memory_id)
            if memory and memory["tenant_id"] == tenant_id:
                memory.update(updates)
                return True
            return False

    async def delete_memory(self, memory_id: UUID, tenant_id: str) -> bool:
        async with self._lock:
            memory = self._memories.get(memory_id)
            if memory and memory["tenant_id"] == tenant_id:
                del self._memories[memory_id]
                return True
            return False

    async def list_memories(
        self, tenant_id: str, **kwargs: Any
    ) -> list[dict[str, Any]]:
        async with self._lock:
            return [
                m.copy() for m in self._memories.values() if m["tenant_id"] == tenant_id
            ]

    async def delete_memories_with_metadata_filter(
        self,
        tenant_id: str | None = None,
        agent_id: str | None = None,
        layer: str | None = None,
        metadata_filter: dict[str, Any] | None = None,
    ) -> int:
        return 0

    async def delete_memories_below_importance(
        self, tenant_id: str, agent_id: str, layer: str, importance_threshold: float
    ) -> int:
        return 0

    async def count_memories(
        self,
        tenant_id: str | None = None,
        agent_id: str | None = None,
        layer: str | None = None,
    ) -> int:
        return len(self._memories)

    async def search_memories(
        self,
        query: str,
        tenant_id: str,
        agent_id: str,
        layer: str,
        limit: int = 10,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        return []

    async def delete_expired_memories(
        self,
        tenant_id: str,
        agent_id: str | None = None,
        layer: str | None = None,
    ) -> int:
        return 0

    async def update_memory_access(self, memory_id: UUID, tenant_id: str) -> bool:
        return True

    async def update_memory_expiration(
        self, memory_id: UUID, tenant_id: str, expires_at: datetime | None
    ) -> bool:
        return True

    async def get_metric_aggregate(
        self,
        tenant_id: str,
        metric: str,
        func: str,
        filters: dict[str, Any] | None = None,
    ) -> float:
        return 0.0

    async def update_memory_access_batch(
        self, memory_ids: list[UUID], tenant_id: str
    ) -> bool:
        return True

    async def adjust_importance(
        self, memory_id: UUID, delta: float, tenant_id: str
    ) -> float:
        return 0.5

    async def save_embedding(
        self,
        memory_id: UUID,
        model_name: str,
        embedding: list[float],
        tenant_id: str,
    ) -> bool:
        return True

    async def decay_importance(self, tenant_id: str, decay_factor: float) -> int:
        return 0

    async def close(self) -> None:
        pass


@pytest.fixture
def mock_storage():
    return MockMemoryStorage()
