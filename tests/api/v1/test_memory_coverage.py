from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from apps.memory_api.main import app
from apps.memory_api.security import auth
from apps.memory_api.security.dependencies import get_and_verify_tenant_id


@pytest.fixture
def mock_pool():
    pool = MagicMock()
    conn = AsyncMock()
    # Mock transaction
    trans = MagicMock()
    trans.__aenter__.return_value = None
    trans.__aexit__.return_value = None
    conn.transaction.return_value = trans

    pool_ctx = MagicMock()
    pool_ctx.__aenter__.return_value = conn
    pool_ctx.__aexit__.return_value = None
    pool.acquire.return_value = pool_ctx

    # Make close awaitable for lifespan shutdown
    pool.close = AsyncMock()

    return pool


@pytest.fixture
def client_with_auth(mock_pool):
    # Override verify_token
    app.dependency_overrides[auth.verify_token] = lambda: {
        "sub": "test-user",
        "role": "admin",
    }
    # Override tenant verification
    app.dependency_overrides[get_and_verify_tenant_id] = lambda: "t1"

    # Mock lifespan dependencies to avoid real DB/Redis connections
    with patch(
        "apps.memory_api.main.asyncpg.create_pool",
        new=AsyncMock(return_value=mock_pool),
    ), patch("apps.memory_api.main.rebuild_full_cache", new=AsyncMock()):
        with TestClient(app) as client:
            yield client

    # Cleanup
    app.dependency_overrides = {}


@pytest.fixture
def mock_memory_repo():
    with patch("apps.memory_api.api.v1.memory.MemoryRepository") as mock:
        repo = AsyncMock()
        mock.return_value = repo
        yield repo


@pytest.fixture
def mock_embedding_service():
    with patch("apps.memory_api.api.v1.memory.get_embedding_service") as mock:
        service = MagicMock()
        service.generate_embeddings.return_value = [[0.1, 0.2, 0.3]]
        mock.return_value = service
        yield service


@pytest.fixture
def mock_vector_store():
    with patch("apps.memory_api.api.v1.memory.get_vector_store") as mock:
        store = AsyncMock()
        mock.return_value = store
        yield store


@pytest.fixture
def mock_pii_scrubber():
    with patch("apps.memory_api.api.v1.memory.pii_scrubber") as mock:
        mock.scrub_text.side_effect = lambda x: x
        yield mock


# ... (rest of the file)

# ============================================================================
# PREVIOUSLY FROZEN TESTS - Now Unfrozen
# ============================================================================
# These tests were frozen due to PostgreSQL auth issues in CI
# Now unfrozen - tests use mocks and don't require database connection
# Database credentials have been fixed in docker-compose.yml and .env.example
# ============================================================================


# @pytest.mark.skip removed - tests now enabled
@pytest.mark.asyncio
async def test_store_memory_vector_failure(
    client_with_auth,
    mock_memory_repo,
    mock_embedding_service,
    mock_vector_store,
    mock_pii_scrubber,
):
    mock_memory_repo.insert_memory.return_value = {
        "id": str(uuid4()),
        "created_at": datetime.now(),
        "last_accessed_at": None,
        "usage_count": 0,
    }
    mock_vector_store.upsert.side_effect = Exception("Vector Error")

    payload = {
        "content": "Test memory content",
        "source": "user",
        "project": "test-project",
        "layer": "em",
        "importance": 0.5,  # Added importance
        "tags": ["test"],
    }

    response = client_with_auth.post(
        "/v1/memory/store", json=payload, headers={"X-Tenant-Id": "t1"}
    )
    assert response.status_code == 502, response.text

    data = response.json()
    if "detail" in data:
        assert "Vector store error" in data["detail"]
    elif "error" in data:
        # The error message might be in data['error']['message'] or data['error'] string
        error_content = data["error"]
        if isinstance(error_content, dict):
            assert "Vector store error" in error_content.get(
                "message", str(error_content)
            )
        else:
            assert "Vector store error" in str(error_content)
    else:
        pytest.fail(f"Unexpected error format: {data}")


@pytest.mark.asyncio
async def test_store_memory_db_failure(
    client_with_auth, mock_memory_repo, mock_pii_scrubber
):
    mock_memory_repo.insert_memory.side_effect = Exception("DB Error")

    payload = {
        "content": "Test memory content",
        "source": "user",
        "project": "test-project",
        "layer": "em",
        "importance": 0.5,  # Added importance
    }

    response = client_with_auth.post(
        "/v1/memory/store", json=payload, headers={"X-Tenant-Id": "t1"}
    )
    assert response.status_code == 500

    data = response.json()
    if "detail" in data:
        assert "Database error" in data["detail"]
    elif "error" in data:
        error_content = data["error"]
        if isinstance(error_content, dict):
            assert "Database error" in error_content.get("message", str(error_content))
        else:
            assert "Database error" in str(error_content)
    else:
        pytest.fail(f"Unexpected error format: {data}")


@pytest.mark.asyncio
async def test_query_memory_hybrid_missing_project(client_with_auth):
    payload = {"query_text": "test query", "use_graph": True}
    response = client_with_auth.post(
        "/v1/memory/query", json=payload, headers={"X-Tenant-Id": "t1"}
    )
    assert response.status_code == 400

    # Check for 'detail' (standard FastAPI) or 'error' (custom handler)
    data = response.json()
    if "detail" in data:
        assert "project parameter is required" in data["detail"]
    elif "error" in data:
        assert "project parameter is required" in data["error"]["message"]
    else:
        pytest.fail(f"Unexpected error format: {data}")


@pytest.mark.asyncio
async def test_delete_memory_success(
    client_with_auth, mock_memory_repo, mock_vector_store
):
    # Ensure delete returns True
    mock_memory_repo.delete_memory.return_value = True

    response = client_with_auth.delete(
        "/v1/memory/delete",
        params={"memory_id": "mem-1"},
        headers={"X-Tenant-Id": "t1"},
    )

    assert response.status_code == 200, response.text
    mock_memory_repo.delete_memory.assert_called_once()
    mock_vector_store.delete.assert_called_once_with("mem-1")


@pytest.mark.asyncio
async def test_delete_memory_not_found(client_with_auth, mock_memory_repo):
    mock_memory_repo.delete_memory.return_value = False

    response = client_with_auth.delete(
        "/v1/memory/delete",
        params={"memory_id": "mem-1"},
        headers={"X-Tenant-Id": "t1"},
    )

    assert response.status_code == 404


# --- Test Background Tasks Trigger ---


@pytest.mark.asyncio
async def test_rebuild_reflections(client_with_auth):
    with patch(
        "apps.memory_api.api.v1.memory.generate_reflection_for_project"
    ) as mock_task:
        payload = {"project": "p1", "tenant_id": "t1"}
        response = client_with_auth.post(
            "/v1/memory/rebuild-reflections",
            json=payload,
            headers={"X-Tenant-Id": "t1"},
        )

        assert response.status_code == 202
        mock_task.delay.assert_called_once_with(project="p1", tenant_id="t1")


# --- Test Reflection Stats ---


@pytest.mark.asyncio
async def test_get_reflection_stats(client_with_auth, mock_memory_repo):
    mock_memory_repo.count_memories_by_layer.return_value = 10
    mock_memory_repo.get_average_strength.return_value = 0.75

    response = client_with_auth.get(
        "/v1/memory/reflection-stats",
        params={"project": "p1"},
        headers={"X-Tenant-Id": "t1"},
    )

    assert response.status_code == 200
    assert response.json() == {"reflective_memory_count": 10, "average_strength": 0.75}
