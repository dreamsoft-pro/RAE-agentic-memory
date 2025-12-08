"""
Pytest configuration and shared fixtures for RAE Memory API tests.
"""

import asyncio
import warnings
from typing import Any, Generator
from unittest.mock import AsyncMock, Mock, patch

import asyncpg
import pytest

# Suppress NVML initialization warning (no GPU in test environment)
warnings.filterwarnings("ignore", message="Can't initialize NVML")
# Suppress Click Parser Deprecation (via spacy)
warnings.filterwarnings("ignore", module="spacy.cli._util")


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

    # Patch asyncpg.create_pool to return our mock pool
    # This prevents the app from trying to connect to a real DB during test startup
    with patch(
        "apps.memory_api.main.asyncpg.create_pool", new_callable=AsyncMock
    ) as mock_create_pool:
        mock_create_pool.return_value = pool
        yield pool


# =============================================================================
# Testcontainers Fixtures (Real Database for Integration Tests)
# =============================================================================


@pytest.fixture(scope="session")
def postgres_container():
    """
    Start a PostgreSQL container with pgvector extension for integration tests.

    This fixture provides a real PostgreSQL database running in a Docker container,
    using the ankane/pgvector image which includes the pgvector extension.

    The container is started once per test session and reused across all tests.
    """
    # Check if testcontainers is available
    try:
        from testcontainers.postgres import PostgresContainer
    except ImportError:
        pytest.skip("testcontainers not installed - skipping integration tests")

    # Start PostgreSQL container with pgvector
    container = PostgresContainer(
        image="ankane/pgvector:latest",
        username="test_user",
        password="test_password",
        dbname="test_db",
    )
    container.start()

    yield container

    # Cleanup
    container.stop()


@pytest.fixture(scope="function")
async def db_pool(postgres_container):
    """
    Create an asyncpg connection pool connected to the test database.

    This fixture:
    1. Connects to the testcontainer PostgreSQL instance
    2. Runs Alembic migrations to set up the schema
    3. Provides a clean database pool for each test
    4. Cleans up after the test

    Usage:
        async def test_something(db_pool):
            async with db_pool.acquire() as conn:
                result = await conn.fetch("SELECT 1")
    """
    # Get connection details from container
    host = postgres_container.get_container_host_ip()
    port = postgres_container.get_exposed_port(5432)
    database = postgres_container.dbname
    user = postgres_container.username
    password = postgres_container.password

    # Create connection pool
    pool = await asyncpg.create_pool(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
        min_size=1,
        max_size=5,
    )

    try:
        # Run migrations using Alembic
        # Note: This requires alembic.ini to be configured properly
        # For now, we'll create minimal schema manually
        async with pool.acquire() as conn:
            # Enable pgvector extension
            await conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")

            # Create minimal schema for tests
            # In production, this should be replaced with proper Alembic migrations
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id SERIAL PRIMARY KEY,
                    tenant_id VARCHAR(255) NOT NULL,
                    project VARCHAR(255),
                    content TEXT NOT NULL,
                    source VARCHAR(255),
                    importance FLOAT DEFAULT 0.5,
                    layer VARCHAR(10),
                    tags TEXT[],
                    metadata JSONB,
                    timestamp TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    usage_count INTEGER DEFAULT 0,
                    strength FLOAT DEFAULT 0.5
                );
            """
            )

            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS knowledge_graph_nodes (
                    id SERIAL PRIMARY KEY,
                    tenant_id VARCHAR(255) NOT NULL,
                    project_id VARCHAR(255) NOT NULL,
                    node_id VARCHAR(255) NOT NULL,
                    label VARCHAR(500) NOT NULL,
                    properties JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(tenant_id, project_id, node_id)
                );
            """
            )

            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS knowledge_graph_edges (
                    id SERIAL PRIMARY KEY,
                    tenant_id VARCHAR(255) NOT NULL,
                    project_id VARCHAR(255) NOT NULL,
                    source_node_id INTEGER REFERENCES knowledge_graph_nodes(id) ON DELETE CASCADE,
                    target_node_id INTEGER REFERENCES knowledge_graph_nodes(id) ON DELETE CASCADE,
                    relation VARCHAR(255) NOT NULL,
                    properties JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(tenant_id, project_id, source_node_id, target_node_id, relation)
                );
            """
            )

        yield pool

    finally:
        # Cleanup: Close pool
        await pool.close()


@pytest.fixture
def use_real_db():
    """
    Marker fixture to indicate that a test should use real database (testcontainers).

    Tests using this fixture will use db_pool instead of mock_pool.

    Usage:
        async def test_with_real_db(db_pool, use_real_db):
            async with db_pool.acquire() as conn:
                result = await conn.fetch("SELECT 1")
    """
    return True
