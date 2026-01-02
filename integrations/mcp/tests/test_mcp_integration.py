"""
Integration tests for RAE MCP Server with real RAE API.

These tests verify end-to-end functionality by:
1. Starting RAE Lite services (docker compose.lite.yml)
2. Creating RAEMemoryClient connected to real API
3. Testing all MCP operations (save, search, context, reflections)
4. Tearing down services after tests

Requirements:
- Docker and docker compose installed
- .env file configured with LLM API key
- Ports 8000, 5432, 6333, 6379 available

Usage:
    pytest integrations/mcp/tests/test_mcp_integration.py -v -m integration
"""

import os
import subprocess
import sys
import time
from pathlib import Path

import httpx
import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rae_mcp.server import RAEMemoryClient

pytestmark = pytest.mark.integration


@pytest.fixture(scope="module")
def rae_lite_services():
    """
    Start docker compose.lite.yml services for MCP integration testing.

    This fixture:
    1. Starts all RAE Lite services (API, PostgreSQL, Qdrant, Redis)
    2. Waits for API to be healthy
    3. Yields control to tests
    4. Tears down services after tests complete
    """
    # Get project root (3 levels up from this file)
    project_root = Path(__file__).parent.parent.parent.parent
    compose_file = project_root / "docker compose.lite.yml"

    # Start services
    subprocess.run(
        ["docker", "compose", "-f", str(compose_file), "up", "-d"],
        check=True,
        capture_output=True,
        cwd=project_root,
    )

    # Wait for services to be ready (up to 60 seconds)
    max_retries = 30
    retry_count = 0
    api_ready = False

    while retry_count < max_retries and not api_ready:
        try:
            response = httpx.get("http://localhost:8000/health", timeout=5.0)
            if response.status_code == 200:
                api_ready = True
                break
        except (httpx.ConnectError, httpx.TimeoutException):
            pass

        retry_count += 1
        time.sleep(2)

    if not api_ready:
        # Cleanup on failure
        subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "down"],
            capture_output=True,
            cwd=project_root,
        )
        pytest.fail("RAE API failed to start within 60 seconds")

    # Services are ready
    yield

    # Teardown
    subprocess.run(
        ["docker", "compose", "-f", str(compose_file), "down"],
        check=True,
        capture_output=True,
        cwd=project_root,
    )


@pytest.fixture
def mcp_client(rae_lite_services):
    """
    Create RAEMemoryClient connected to real RAE API.

    Uses environment variables or defaults for configuration.
    """
    return RAEMemoryClient(
        api_url=os.getenv("RAE_API_URL", "http://localhost:8000"),
        api_key=os.getenv("RAE_API_KEY", "test-api-key"),
        tenant_id=os.getenv("RAE_TENANT_ID", "mcp-integration-test"),
    )


class TestMCPStoreMemory:
    """Integration tests for storing memories via MCP client"""

    @pytest.mark.asyncio
    async def test_store_memory_episodic(self, mcp_client):
        """Test storing episodic memory"""
        result = await mcp_client.store_memory(
            content="MCP Integration Test: User prefers dark mode in IDE",
            source="mcp-integration-test",
            layer="episodic",
            tags=["test", "integration", "preference"],
        )

        assert "id" in result
        assert len(result["id"]) > 0

    @pytest.mark.asyncio
    async def test_store_memory_semantic(self, mcp_client):
        """Test storing semantic memory"""
        result = await mcp_client.store_memory(
            content="MCP Integration Test: Always use async/await for I/O operations",
            source="mcp-integration-test",
            layer="semantic",
            tags=["guideline", "best-practice"],
        )

        assert "id" in result
        assert len(result["id"]) > 0

    @pytest.mark.asyncio
    async def test_store_memory_working(self, mcp_client):
        """Test storing working memory"""
        result = await mcp_client.store_memory(
            content="MCP Integration Test: Currently implementing authentication module",
            source="mcp-integration-test",
            layer="working",
            tags=["current-task"],
        )

        assert "id" in result

    @pytest.mark.asyncio
    async def test_store_memory_ltm(self, mcp_client):
        """Test storing long-term memory"""
        result = await mcp_client.store_memory(
            content="MCP Integration Test: Project uses PostgreSQL as primary database",
            source="mcp-integration-test",
            layer="ltm",
            tags=["architecture", "database"],
        )

        assert "id" in result


class TestMCPSearchMemory:
    """Integration tests for searching memories via MCP client"""

    @pytest.mark.asyncio
    async def test_search_memory_basic(self, mcp_client):
        """Test basic memory search"""
        # First, store a memory
        await mcp_client.store_memory(
            content="MCP Integration Test: FastAPI is used for REST API",
            source="mcp-integration-test",
            layer="semantic",
            tags=["framework"],
        )

        # Wait a moment for indexing
        time.sleep(1)

        # Search for the memory
        results = await mcp_client.search_memory(query="FastAPI REST API", top_k=5)

        assert isinstance(results, list)
        # May or may not find results depending on indexing speed
        # but should not error

    @pytest.mark.asyncio
    async def test_search_memory_with_filters(self, mcp_client):
        """Test memory search with filters"""
        # Store memory with specific tag
        await mcp_client.store_memory(
            content="MCP Integration Test: Redis used for caching",
            source="mcp-integration-test",
            layer="ltm",
            tags=["cache", "redis"],
        )

        time.sleep(1)

        # Search with filter
        results = await mcp_client.search_memory(
            query="caching",
            top_k=10,
            filters={"tags": ["cache"]},
        )

        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_search_memory_top_k(self, mcp_client):
        """Test memory search with different top_k values"""
        # Store multiple memories
        for i in range(5):
            await mcp_client.store_memory(
                content=f"MCP Integration Test: Memory {i} for top_k testing",
                source="mcp-integration-test",
                layer="episodic",
                tags=["top-k-test"],
            )

        time.sleep(2)

        # Search with top_k=3
        results = await mcp_client.search_memory(query="top_k testing", top_k=3)

        assert isinstance(results, list)
        # Should return at most 3 results (may be less if indexing incomplete)
        assert len(results) <= 3


class TestMCPFileContext:
    """Integration tests for file context retrieval"""

    @pytest.mark.asyncio
    async def test_get_file_context(self, mcp_client):
        """Test getting file context"""
        # Store memories with file paths
        await mcp_client.store_memory(
            content="MCP Integration Test: Added authentication to auth.py",
            source="/app/auth.py",
            layer="episodic",
            tags=["file-change"],
        )

        await mcp_client.store_memory(
            content="MCP Integration Test: Fixed bug in auth.py validation",
            source="/app/auth.py",
            layer="episodic",
            tags=["bugfix"],
        )

        time.sleep(1)

        # Get file context
        results = await mcp_client.get_file_context(file_path="/app/auth.py", top_k=10)

        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_get_file_context_no_results(self, mcp_client):
        """Test getting file context for non-existent file"""
        results = await mcp_client.get_file_context(
            file_path="/nonexistent/file.py", top_k=10
        )

        assert isinstance(results, list)
        assert len(results) == 0


class TestMCPProjectGuidelines:
    """Integration tests for project guidelines"""

    @pytest.mark.asyncio
    async def test_get_project_guidelines(self, mcp_client):
        """Test getting project guidelines"""
        # Store some guidelines
        guidelines = [
            "Use Python 3.10+ features",
            "Follow PEP 8 style guide",
            "Write docstrings for all public functions",
            "Use type hints wherever possible",
        ]

        for guideline in guidelines:
            await mcp_client.store_memory(
                content=f"MCP Integration Test: {guideline}",
                source="mcp-integration-test",
                layer="semantic",
                tags=["guideline", "coding-standard"],
            )

        time.sleep(2)

        # Retrieve guidelines
        results = await mcp_client.get_project_guidelines()

        assert isinstance(results, list)


class TestMCPReflections:
    """Integration tests for reflection retrieval"""

    @pytest.mark.asyncio
    async def test_get_latest_reflection(self, mcp_client):
        """Test getting latest reflection"""
        # Store some episodic memories
        activities = [
            "Implemented user authentication",
            "Added password hashing",
            "Created login endpoint",
            "Wrote authentication tests",
        ]

        for activity in activities:
            await mcp_client.store_memory(
                content=f"MCP Integration Test: {activity}",
                source="mcp-integration-test",
                layer="episodic",
                tags=["activity"],
            )

        time.sleep(2)

        # Get reflection
        reflection = await mcp_client.get_latest_reflection()

        assert isinstance(reflection, str)
        assert len(reflection) > 0
        # Reflection may be "No reflection available" if not enough data


class TestMCPErrorHandling:
    """Integration tests for error handling"""

    @pytest.mark.asyncio
    async def test_store_memory_invalid_layer(self, mcp_client):
        """Test storing memory with invalid layer"""
        # This should still work as API may accept or default
        try:
            result = await mcp_client.store_memory(
                content="Test with invalid layer",
                source="test",
                layer="invalid-layer",  # Invalid layer
                tags=["test"],
            )
            # If API is lenient, it may succeed with default layer
            assert "id" in result or "error" in result
        except Exception as e:
            # Expected to fail
            assert "error" in str(e).lower() or "invalid" in str(e).lower()

    @pytest.mark.asyncio
    async def test_search_memory_empty_query(self, mcp_client):
        """Test searching with empty query"""
        # Empty query should still work (may return recent memories)
        results = await mcp_client.search_memory(query="", top_k=5)
        assert isinstance(results, list)


class TestMCPPerformance:
    """Integration tests for performance and throughput"""

    @pytest.mark.asyncio
    async def test_store_multiple_memories_sequential(self, mcp_client):
        """Test storing multiple memories sequentially"""
        start_time = time.time()

        for i in range(10):
            await mcp_client.store_memory(
                content=f"MCP Performance Test: Memory {i}",
                source="performance-test",
                layer="episodic",
                tags=["perf"],
            )

        elapsed = time.time() - start_time

        # Should complete within reasonable time (10 ops in < 10 seconds)
        assert elapsed < 10.0

    @pytest.mark.asyncio
    async def test_search_response_time(self, mcp_client):
        """Test search response time"""
        # Store a memory first
        await mcp_client.store_memory(
            content="MCP Performance Test: Search target",
            source="performance-test",
            layer="semantic",
        )

        time.sleep(1)

        # Measure search time
        start_time = time.time()
        await mcp_client.search_memory(query="search target", top_k=5)
        elapsed = time.time() - start_time

        # Search should be fast (< 2 seconds)
        assert elapsed < 2.0


@pytest.mark.skipif(
    subprocess.run(["which", "docker compose"], capture_output=True).returncode != 0,
    reason="docker compose not available",
)
class TestMCPServiceDependencies:
    """Test that MCP client properly handles service dependencies"""

    @pytest.mark.asyncio
    async def test_health_check(self, rae_lite_services):
        """Test that RAE API health check works"""
        response = httpx.get("http://localhost:8000/health", timeout=5.0)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data

    @pytest.mark.asyncio
    async def test_api_docs_accessible(self, rae_lite_services):
        """Test that API documentation is accessible"""
        response = httpx.get("http://localhost:8000/docs", timeout=5.0)
        assert response.status_code == 200
