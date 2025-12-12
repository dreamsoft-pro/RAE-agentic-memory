"""Storage adapter wrapper for RAE-Server.

Configures RAE-core PostgreSQLStorage with RAE-Server settings.
"""

import asyncpg
from rae_core.adapters import PostgreSQLStorage


def get_storage_adapter(pool: asyncpg.Pool) -> PostgreSQLStorage:
    """Get configured PostgreSQL storage adapter.

    Args:
        pool: PostgreSQL connection pool from RAE-Server

    Returns:
        Configured PostgreSQLStorage instance
    """
    return PostgreSQLStorage(pool=pool)
