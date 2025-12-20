import uuid
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from apps.memory_api.workers.memory_maintenance import (
    SessionSummaryResponse,
    SummarizationWorker,
)
from apps.memory_api.services.rae_core_service import RAECoreService


@pytest.fixture
def mock_rae_service():
    """Mock for RAECoreService."""
    service = AsyncMock(spec=RAECoreService)
    # Configure mock behavior as needed for these tests
    service.list_memories.return_value = [] # Default empty list for sessions
    service.store_memory.return_value = "mock-summary-id" # For storing summary
    return service


@pytest.mark.asyncio
async def test_summarize_session_llm(mock_rae_service):
    """Test session summarization using LLM."""
    # Mock pool (if needed for the worker itself, not passed to repo directly anymore)
    mock_pool = MagicMock()

    # Mock memories
    memories = [
        {
            "id": 1,
            "content": "User asked for help",
            "created_at": datetime.now(),
            "metadata": {"session_id": "session-1"},
        },
        {
            "id": 2,
            "content": "Agent provided help",
            "created_at": datetime.now(),
            "metadata": {"session_id": "session-1"},
        },
    ]
    mock_rae_service.list_memories.return_value = memories
    mock_rae_service.store_memory.return_value = "summary-id"

    # Mock LLM provider
    mock_llm_provider = AsyncMock()
    mock_llm_provider.generate_structured.return_value = SessionSummaryResponse(
        summary="User asked for help and agent provided it.",
        key_topics=["help", "support"],
        sentiment="positive",
    )

    # Create worker with rae_service
    worker = SummarizationWorker(pool=mock_pool, rae_service=mock_rae_service)
    worker.llm_provider = mock_llm_provider

    # Run summarization (min_events=2 to trigger)
    session_id = uuid.uuid4()
    result = await worker.summarize_session(
        tenant_id="tenant-1", project_id="default", session_id=session_id, min_events=2
    )

    # Verify interaction
    assert result is not None
    assert result["id"] == "summary-id"
    mock_llm_provider.generate_structured.assert_called_once()

    # Verify content passed to store_memory
    call_args = mock_rae_service.store_memory.call_args[1]
    assert "User asked for help and agent provided it." in call_args["content"]
    assert "Key Topics: help, support" in call_args["content"]
    assert "Sentiment: positive" in call_args["content"]


@pytest.mark.asyncio
async def test_summarize_long_sessions(mock_rae_service):
    """Test summarization of long sessions."""
    # Mock pool with fetch return value
    mock_pool = MagicMock()
    mock_conn = AsyncMock()
    mock_pool.acquire.return_value.__aenter__.return_value = mock_conn

    # Mock return of long sessions query
    session_id_1 = str(uuid.uuid4())
    session_id_2 = str(uuid.uuid4())
    mock_conn.fetch.return_value = [
        {"session_id": session_id_1, "event_count": 150},
        {"session_id": session_id_2, "event_count": 200},
    ]

    # Create worker with rae_service
    worker = SummarizationWorker(pool=mock_pool, rae_service=mock_rae_service)

    # Mock summarize_session to avoid real call
    worker.summarize_session = AsyncMock()
    worker.summarize_session.return_value = {"id": "summary-id"}

    # Run long session summarization
    summaries = await worker.summarize_long_sessions(
        tenant_id="tenant-1", project_id="default", event_threshold=100
    )

    # Verify results
    assert len(summaries) == 2
    assert worker.summarize_session.call_count == 2

    # Verify calls
    calls = worker.summarize_session.call_args_list
    assert str(calls[0].kwargs["session_id"]) == session_id_1
    assert str(calls[1].kwargs["session_id"]) == session_id_2
