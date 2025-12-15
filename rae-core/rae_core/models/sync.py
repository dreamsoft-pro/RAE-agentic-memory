"""Sync models for RAE-Sync protocol."""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class SyncOperation(str, Enum):
    """Sync operation type."""

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class SyncChange(BaseModel):
    """Single sync change."""

    memory_id: UUID
    operation: SyncOperation
    data: dict[str, Any]
    timestamp: datetime
    version: int = Field(description="Version number for conflict resolution")


class SyncState(BaseModel):
    """Sync state for a tenant."""

    tenant_id: str
    last_sync_timestamp: datetime
    pending_changes: int = Field(default=0)
    sync_enabled: bool = Field(default=False)


class SyncConflict(BaseModel):
    """Sync conflict."""

    memory_id: UUID
    local_version: dict[str, Any]
    remote_version: dict[str, Any]
    resolved: bool = Field(default=False)
    resolution: dict[str, Any] | None = None
