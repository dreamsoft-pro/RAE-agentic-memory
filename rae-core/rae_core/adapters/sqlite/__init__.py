"""SQLite adapters for RAE-core.

Lightweight, file-based implementations for RAE-Lite offline-first architecture.
"""

from rae_core.adapters.sqlite.storage import SQLiteStorage
from rae_core.adapters.sqlite.vector import SQLiteVectorStore

__all__ = [
    "SQLiteStorage",
    "SQLiteVectorStore",
]
