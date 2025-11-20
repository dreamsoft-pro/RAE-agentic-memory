"""
Pytest configuration and shared fixtures for RAE Memory API tests.
"""

import pytest
import asyncio
from typing import Generator, Any
from unittest.mock import AsyncMock, Mock


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def anyio_backend():
    """Use asyncio as the async backend for tests."""
    return "asyncio"


# =============================================================================
# Helper Classes for Async Mocking
# =============================================================================

class DummyAsyncContextManager:
    """
    Helper class for mocking async context managers that mimics asyncpg's pool.acquire().

    Asyncpg's pool.acquire() returns an object that is BOTH:
    - awaitable: await pool.acquire()
    - async context manager: async with pool.acquire() as conn:

    This class implements both interfaces.

    Usage:
        mock_pool.acquire.return_value = DummyAsyncContextManager(mock_conn)
    """

    def __init__(self, value: Any):
        self._value = value

    def __await__(self):
        """Make this awaitable - returns self so it can be used as context manager."""
        async def _impl():
            return self
        return _impl().__await__()

    async def __aenter__(self):
        """Enter async context - returns the wrapped value."""
        return self._value

    async def __aexit__(self, exc_type, exc, tb):
        """Exit async context."""
        return False


# =============================================================================
# Common Fixtures
# =============================================================================

@pytest.fixture
def mock_pool():
    """
    Mock asyncpg connection pool with proper async context manager support.

    This fixture provides a properly configured mock that works with BOTH:
        async with pool.acquire() as conn:
            await conn.fetch(...)

    AND:
        conn = await pool.acquire()
        try:
            await conn.fetch(...)
        finally:
            await pool.release(conn)

    The mock_pool._test_conn attribute gives direct access to the connection
    object for customization in individual tests.

    Example usage in tests:
        # Customize connection behavior
        mock_pool._test_conn.fetch = AsyncMock(return_value=[...])

        # Or use the pool directly
        async with pool.acquire() as conn:
            result = await conn.fetch(...)
    """
    pool = Mock()
    conn = AsyncMock()

    # Set up default connection behavior
    conn.fetch = AsyncMock(return_value=[])
    conn.fetchrow = AsyncMock(return_value=None)
    conn.execute = AsyncMock(return_value="INSERT 0 1")

    # Make conn.transaction() return proper async context manager
    # transaction() should work with: async with conn.transaction():
    conn.transaction = Mock(return_value=DummyAsyncContextManager(None))

    # Create context manager instance that's also awaitable
    context_manager = DummyAsyncContextManager(conn)

    # Make pool.acquire() return the context manager directly
    # This works because DummyAsyncContextManager is both awaitable AND a context manager
    pool.acquire = Mock(return_value=context_manager)

    # Expose conn and context for test customization
    pool._test_conn = conn
    pool._test_context = context_manager

    return pool
