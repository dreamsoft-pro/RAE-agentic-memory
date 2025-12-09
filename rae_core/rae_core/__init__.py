"""
RAE-Core - Pure Python Memory Engine.

4-layer memory architecture with hybrid search and consolidation.
"""

from rae_core.engine import RAEEngine
from rae_core.models.memory import (
    MemoryRecord,
    QueryMemoryResponse,
    ScoredMemoryRecord,
)

__version__ = "0.1.0"

__all__ = [
    "RAEEngine",
    "MemoryRecord",
    "QueryMemoryResponse",
    "ScoredMemoryRecord",
]
