"""Core memory models for RAE-core.

Pydantic models for memory representation across all layers.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class MemoryLayer(str, Enum):
    """Memory layer enumeration."""

    SENSORY = "sensory"
    WORKING = "working"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    REFLECTIVE = "reflective"


class MemoryType(str, Enum):
    """Type of memory content."""

    TEXT = "text"
    CODE = "code"
    IMAGE = "image"
    DOCUMENT = "document"
    CONVERSATION = "conversation"
    REFLECTION = "reflection"
    ENTITY = "entity"
    RELATIONSHIP = "relationship"


class MemoryItem(BaseModel):
    """Core memory item model.

    This is the fundamental unit of memory in RAE-core.
    Storage-agnostic representation that can be persisted in any backend.
    """

    id: UUID = Field(default_factory=uuid4)
    content: str = Field(description="The actual memory content")
    layer: MemoryLayer = Field(description="Which memory layer this belongs to")
    memory_type: MemoryType = Field(
        default=MemoryType.TEXT, description="Type of memory content"
    )

    # Metadata
    tenant_id: str = Field(description="Tenant identifier for multi-tenancy")
    agent_id: str = Field(description="Agent that owns this memory")
    tags: list[str] = Field(default_factory=list, description="Tags for filtering")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    # Vector embedding
    embedding: list[float] | None = Field(
        default=None, description="Vector embedding for similarity search"
    )

    # Scoring and importance
    importance: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Importance score (0.0-1.0)"
    )
    usage_count: int = Field(default=0, description="Number of times accessed")

    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_accessed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    expires_at: datetime | None = Field(
        default=None, description="Optional expiration time for sensory memories"
    )

    # Source tracking
    source: str | None = Field(
        default=None, description="Source of the memory (e.g., 'user_input', 'llm')"
    )
    context: dict[str, Any] | None = Field(
        default=None, description="Context when memory was created"
    )

    # Synchronization & Provenance (Layer 2 Telemetry)
    provenance: dict[str, Any] | None = Field(
        default_factory=dict,
        description="Origin and trust details (e.g., origin_device, trust_level)",
    )
    sync_metadata: dict[str, Any] | None = Field(
        default_factory=dict,
        description="Sync protocol data (e.g., version, path, conflict info)",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "content": "User prefers Python over JavaScript for backend development",
                "layer": "episodic",
                "memory_type": "text",
                "tenant_id": "tenant_123",
                "agent_id": "agent_456",
                "tags": ["preference", "programming"],
                "importance": 0.8,
                "usage_count": 5,
            }
        }
    )


class ScoredMemoryItem(BaseModel):
    """Memory item with relevance score.

    Used for search results and ranked memory lists.
    """

    memory: MemoryItem
    score: float = Field(description="Relevance or similarity score", ge=0.0, le=1.0)
    score_breakdown: dict[str, float] | None = Field(
        default=None,
        description="Breakdown of score components (similarity, importance, recency)",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "memory": {"content": "Example memory", "layer": "episodic"},
                "score": 0.87,
                "score_breakdown": {
                    "similarity": 0.9,
                    "importance": 0.8,
                    "recency": 0.85,
                },
            }
        }
    )


class MemoryStats(BaseModel):
    """Statistics for a memory layer or agent."""

    total_count: int = Field(description="Total number of memories")
    by_layer: dict[MemoryLayer, int] = Field(
        default_factory=dict, description="Count by layer"
    )
    by_type: dict[MemoryType, int] = Field(
        default_factory=dict, description="Count by type"
    )
    average_importance: float = Field(description="Average importance score")
    total_usage: int = Field(description="Total usage count across all memories")
    oldest_memory: datetime | None = Field(
        default=None, description="Timestamp of oldest memory"
    )
    newest_memory: datetime | None = Field(
        default=None, description="Timestamp of newest memory"
    )
