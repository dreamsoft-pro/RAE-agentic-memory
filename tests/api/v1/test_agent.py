from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from apps.memory_api.main import app
from apps.memory_api.security.dependencies import get_and_verify_tenant_id
from apps.memory_api.services.llm.base import LLMResult, LLMResultUsage


@pytest.fixture
def mock_context_builder():
    with patch("apps.memory_api.api.v1.agent.ContextBuilder") as MockBuilder:
        instance = MockBuilder.return_value
        # Mock the build_context return value
        working_memory = MagicMock()
        working_memory.context_text = "System Context"
        instance.build_context = AsyncMock(return_value=working_memory)
        yield instance


@pytest.fixture
def mock_services():
    with patch(
        "apps.memory_api.api.v1.agent.get_embedding_service"
    ) as mock_embed, patch(
        "apps.memory_api.api.v1.agent.get_vector_store"
    ) as mock_vec, patch(
        "apps.memory_api.api.v1.agent.get_llm_provider"
    ) as mock_llm, patch(
        "apps.memory_api.api.v1.agent.estimate_tokens"
    ) as mock_est, patch(
        "apps.memory_api.api.v1.agent.track_request_cost"
    ) as mock_track:
        # Setup default behaviors
        mock_embed.return_value.generate_embeddings.return_value = [[0.1] * 384]

        mock_vec_inst = AsyncMock()
        mock_vec.return_value = mock_vec_inst

        mock_llm_inst = MagicMock()
        mock_llm.return_value = mock_llm_inst

        mock_est.return_value = 10
        mock_track.return_value = {"total_cost_usd": 0.001}

        yield {
            "embed": mock_embed,
            "vec": mock_vec_inst,
            "llm": mock_llm_inst,
            "est": mock_est,
            "track": mock_track,
        }


@pytest.fixture
def client_with_auth():
    # Override auth dependency
    app.dependency_overrides[get_and_verify_tenant_id] = lambda: "test-tenant"

    # Mock pool state to avoid AttributeError
    mock_pool = MagicMock()
    mock_pool.close = AsyncMock()
    app.state.pool = mock_pool

    # Mock RAE Core Service
    mock_rae_service = AsyncMock()
    mock_rae_service.update_memory_access_batch = AsyncMock()
    app.state.rae_core_service = mock_rae_service

    # Mock lifespan dependencies to avoid real DB/Redis connections
    with patch(
        "apps.memory_api.main.asyncpg.create_pool",
        new=AsyncMock(return_value=mock_pool),
    ), patch("apps.memory_api.main.rebuild_full_cache", new=AsyncMock()):
        with TestClient(app) as client:
            yield client

    app.dependency_overrides = {}
    if hasattr(app.state, "pool"):
        del app.state.pool
    if hasattr(app.state, "rae_core_service"):
        del app.state.rae_core_service


@pytest.mark.asyncio
async def test_agent_execute_happy_path(
    client_with_auth, mock_context_builder, mock_services
):
    """Test successful agent execution pipeline."""

    # Mock vector store results with concrete attributes for Pydantic validation
    mock_item = MagicMock()
    mock_item.id = str(uuid4())
    mock_item.content = "Episodic memory"
    mock_item.score = 0.9
    mock_item.source = "user"
    mock_item.layer = "em"  # Must match enum in ScoredMemoryRecord (stm, ltm, rm, em)
    mock_item.project = "test-project"
    mock_item.importance = 0.5
    mock_item.tags = []
    mock_item.timestamp = datetime.now()
    mock_item.last_accessed_at = datetime.now()
    mock_item.usage_count = 1

    mock_services["vec"].query.return_value = [mock_item]

    # Mock LLM response
    mock_services["llm"].generate = AsyncMock(
        return_value=LLMResult(
            text="Agent Answer",
            usage=LLMResultUsage(
                prompt_tokens=50, candidates_tokens=20, total_tokens=70
            ),
            model_name="gpt-4",
            finish_reason="stop",
        )
    )

    # Mock HTTP calls (Reranker + Reflection)
    with patch("httpx.AsyncClient") as MockClient:
        mock_client_instance = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client_instance

        # Reranker response
        mock_client_instance.post.return_value.json = AsyncMock(
            return_value={"items": [{"id": mock_item.id, "score": 0.95}]}
        )
        # Make raise_for_status a no-op
        mock_client_instance.post.return_value.raise_for_status = MagicMock()

        payload = {
            "tenant_id": "test-tenant",
            "project": "test-project",
            "prompt": "Hello",
        }

        response = client_with_auth.post("/v1/agent/execute", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["answer"] == "Agent Answer"
        assert len(data["used_memories"]["results"]) == 1
        assert data["cost"]["total_estimate"] == 0.001

        # Verify calls
        mock_context_builder.build_context.assert_called_once()
        mock_services["vec"].query.assert_called_once()
        # Should call reranker and reflection hook (2 posts)
        assert mock_client_instance.post.call_count == 2


@pytest.mark.asyncio
async def test_agent_execute_no_episodic_memories(
    client_with_auth, mock_context_builder, mock_services
):
    """Test execution when no episodic memories are found."""

    mock_services["vec"].query.return_value = []

    mock_services["llm"].generate = AsyncMock(
        return_value=LLMResult(
            text="Answer without context",
            usage=LLMResultUsage(
                prompt_tokens=10, candidates_tokens=5, total_tokens=15
            ),
            model_name="gpt-4",
            finish_reason="stop",
        )
    )

    with patch("httpx.AsyncClient") as MockClient:
        mock_client_instance = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client_instance

        response = client_with_auth.post(
            "/v1/agent/execute",
            json={
                "tenant_id": "test-tenant",
                "project": "test-project",
                "prompt": "Query",
            },
        )

        assert response.status_code == 200
        assert response.json()["answer"] == "Answer without context"
        # Reranker shouldn't be called if no memories
        # But reflection hook should still be called
        assert mock_client_instance.post.call_count == 1


@pytest.mark.asyncio
async def test_agent_execute_reranker_failure(
    client_with_auth, mock_context_builder, mock_services
):
    """Test execution when reranker service fails."""

    mock_item = MagicMock()
    mock_item.id = str(uuid4())
    mock_item.content = "Memory"
    mock_item.score = 0.9
    mock_services["vec"].query.return_value = [mock_item]

    with patch("httpx.AsyncClient") as MockClient:
        mock_client_instance = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client_instance

        # Simulate Reranker failure
        mock_client_instance.post.side_effect = Exception("Reranker Down")

        response = client_with_auth.post(
            "/v1/agent/execute",
            json={
                "tenant_id": "test-tenant",
                "project": "test-project",
                "prompt": "Query",
            },
        )

        assert response.status_code == 502
        # Verify error details
        data = response.json()
        # Check if 'detail' or 'error' key is present, adapting to custom error handler
        if "detail" in data:
            assert "Reranker error" in data["detail"]
        else:
            assert "error" in data
            assert "Reranker error" in data["error"]["message"]


@pytest.mark.asyncio
async def test_agent_execute_llm_failure(
    client_with_auth, mock_context_builder, mock_services
):
    """Test execution when LLM provider fails."""

    mock_services["vec"].query.return_value = []
    mock_services["llm"].generate = AsyncMock(side_effect=Exception("LLM Error"))

    with patch("httpx.AsyncClient"):
        response = client_with_auth.post(
            "/v1/agent/execute",
            json={
                "tenant_id": "test-tenant",
                "project": "test-project",
                "prompt": "Query",
            },
        )

        assert response.status_code == 500
        data = response.json()
        if "detail" in data:
            assert "LLM call failed" in data["detail"]
        else:
            assert "error" in data
            assert "LLM call failed" in data["error"]["message"]


@pytest.mark.asyncio
async def test_agent_execute_reflection_failure_ignored(
    client_with_auth, mock_context_builder, mock_services
):
    """Test that reflection hook failure doesn't break the response."""

    mock_services["vec"].query.return_value = []
    mock_services["llm"].generate = AsyncMock(
        return_value=LLMResult(
            text="Answer",
            usage=LLMResultUsage(
                prompt_tokens=10, candidates_tokens=5, total_tokens=15
            ),
            model_name="gpt-4",
            finish_reason="stop",
        )
    )

    with patch("httpx.AsyncClient") as MockClient:
        mock_client_instance = AsyncMock()
        MockClient.return_value.__aenter__.return_value = mock_client_instance

        # Reflection hook fails
        mock_client_instance.post.side_effect = Exception("Reflection API Error")

        response = client_with_auth.post(
            "/v1/agent/execute",
            json={
                "tenant_id": "test-tenant",
                "project": "test-project",
                "prompt": "Query",
            },
        )

        assert response.status_code == 200
        assert response.json()["answer"] == "Answer"


@pytest.mark.asyncio
async def test_agent_execute_vector_store_failure(
    client_with_auth, mock_context_builder, mock_services
):
    """Test execution when vector store fails."""

    mock_services["vec"].query.side_effect = Exception("Qdrant Error")

    response = client_with_auth.post(
        "/v1/agent/execute",
        json={"tenant_id": "test-tenant", "project": "test-project", "prompt": "Query"},
    )

    assert response.status_code == 502
    data = response.json()
    if "detail" in data:
        assert "Error querying vector store" in data["detail"]
    else:
        assert "error" in data
        assert "Error querying vector store" in data["error"]["message"]
