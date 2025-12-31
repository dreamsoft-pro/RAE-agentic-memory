from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class SyncDirection(str, Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"


class SyncStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    CONFLICT = "conflict"


class SyncLog(BaseModel):
    """
    Log entry for a synchronization event between RAE instances.
    """

    id: UUID = Field(default_factory=uuid4, description="Unique ID of the sync event")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When the sync occurred",
    )
    peer_id: str = Field(description="ID of the remote peer (e.g., mobile-device-id)")
    direction: SyncDirection = Field(description="Direction of sync")
    status: SyncStatus = Field(description="Outcome of the sync operation")
    items_synced: int = Field(default=0, description="Number of items processed")
    conflicts_resolved: int = Field(
        default=0, description="Number of conflicts automatically resolved"
    )
    duration_ms: float = Field(description="Duration of the sync operation in ms")

    # Layer 2 Telemetry Data
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Detailed sync metadata (versions, paths, error details)",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "timestamp": "2023-10-27T10:00:00Z",
                "peer_id": "rae-mobile-pixel7",
                "direction": "incoming",
                "status": "success",
                "items_synced": 42,
                "conflicts_resolved": 2,
                "duration_ms": 150.5,
                "metadata": {
                    "rae.sync.version": 105,
                    "rae.sync.path": "mobile -> server",
                    "error": None,
                },
            }
        }
