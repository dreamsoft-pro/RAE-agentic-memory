from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

import apps.memory_api.services.reflection_pipeline as pipeline_module
from apps.memory_api.models.reflection_models import (
    ReflectionScoring,
    ReflectionTelemetry,
    ReflectionType,
    ReflectionUnit,
)
from apps.memory_api.services.reflection_pipeline import ReflectionPipeline


@pytest.fixture
def mock_pool():
    pool = AsyncMock()
    conn = AsyncMock()
    pool.acquire.return_value.__aenter__.return_value = conn
    return pool


@pytest.fixture
def mock_llm_provider():
    provider = AsyncMock()
    # Mock regular generate response object
    text_response = MagicMock()
    text_response.text = "This is an insight."
    # Explicitly set attributes to values, not mocks
    text_response.usage = MagicMock()
    text_response.usage.total_tokens = 100
    text_response.cost_usd = 0.001

    provider.generate.return_value = text_response

    # Mock structured generate
    score_response = MagicMock()
    score_response.novelty = 0.8
    score_response.importance = 0.9
    score_response.utility = 0.7
    score_response.confidence = 0.9
    provider.generate_structured.return_value = score_response

    return provider


@pytest.fixture
def mock_ml_client():
    client = AsyncMock()
    client.get_embedding.return_value = [0.1] * 1536
    return client


@pytest.fixture
def mock_reflection_repo():
    return AsyncMock()


@pytest.fixture
def service(
    mock_pool, mock_llm_provider, mock_ml_client, mock_reflection_repo, monkeypatch
):
    # Use monkeypatch for reliable replacement of module-level names

    monkeypatch.setattr(pipeline_module, "reflection_repository", mock_reflection_repo)
    monkeypatch.setattr(pipeline_module, "get_llm_provider", lambda: mock_llm_provider)
    monkeypatch.setattr(pipeline_module, "MLServiceClient", lambda: mock_ml_client)

    svc = ReflectionPipeline(mock_pool)
    # Ensure instance variables are also mocks (though they are set in __init__ using the patched calls/imports)
    # get_llm_provider is called in __init__, so it will use the monkeypatched one.

    # Store repo mock on service for easy access in tests
    svc.mock_reflection_repo = mock_reflection_repo
    return svc


@pytest.mark.asyncio
async def test_generate_reflections_flow(service, mock_pool):
    mem1_id = str(uuid4())
    mem2_id = str(uuid4())
    mem3_id = str(uuid4())

    # 1. Mock Fetch Memories
    mock_pool.fetch.return_value = [
        {
            "id": mem1_id,
            "content": "Memory 1",
            "embedding": [0.1] * 1536,
            "created_at": datetime.now(),
        },
        {
            "id": mem2_id,
            "content": "Memory 2",
            "embedding": [0.1] * 1536,
            "created_at": datetime.now(),
        },
        {
            "id": mem3_id,
            "content": "Memory 3",
            "embedding": [0.1] * 1536,
            "created_at": datetime.now(),
        },
    ]

    # 2. Mock Clustering
    service._cluster_memories = AsyncMock(
        return_value={
            "cluster_0": [
                {"id": mem1_id, "content": "Memory 1"},
                {"id": mem2_id, "content": "Memory 2"},
                {"id": mem3_id, "content": "Memory 3"},
            ]
        }
    )

    # 3. Mock Reflection Creation
    mock_reflection = ReflectionUnit(
        id=uuid4(),
        tenant_id="t-1",
        project_id="p-1",
        content="Generated Insight",
        type=ReflectionType.INSIGHT,  # Explicitly set type
        reflection_type=ReflectionType.INSIGHT,
        priority=3,
        score=0.8,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        last_accessed_at=datetime.now(),
        telemetry=ReflectionTelemetry(
            generation_model="test-model",
            generation_duration_ms=100,
            generation_tokens_used=50,
            generation_cost_usd=0.001,
        ),
    )
    service.mock_reflection_repo.create_reflection.return_value = mock_reflection

    # ...


@pytest.mark.asyncio
async def test_generate_meta_insight(service):

    insights = [
        ReflectionUnit(
            id=uuid4(),
            content="I1",
            tenant_id="t",
            project_id="p",
            type=ReflectionType.INSIGHT,
            reflection_type=ReflectionType.INSIGHT,
            score=0.8,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_accessed_at=datetime.now(),
        ),
        ReflectionUnit(
            id=uuid4(),
            content="I2",
            tenant_id="t",
            project_id="p",
            type=ReflectionType.INSIGHT,
            reflection_type=ReflectionType.INSIGHT,
            score=0.8,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_accessed_at=datetime.now(),
        ),
        ReflectionUnit(
            id=uuid4(),
            content="I3",
            tenant_id="t",
            project_id="p",
            type=ReflectionType.INSIGHT,
            reflection_type=ReflectionType.INSIGHT,
            score=0.8,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            last_accessed_at=datetime.now(),
        ),
    ]

    mock_meta = ReflectionUnit(
        id=uuid4(),
        content="Meta Insight",
        tenant_id="t",
        project_id="p",
        type=ReflectionType.META,  # Explicitly set type
        reflection_type=ReflectionType.META,
        score=0.9,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        last_accessed_at=datetime.now(),
        telemetry=ReflectionTelemetry(
            generation_model="test-model",
            generation_duration_ms=100,
            generation_tokens_used=50,
            generation_cost_usd=0.001,
        ),
    )

    service.mock_reflection_repo.create_reflection.return_value = mock_meta

    meta = await service._generate_meta_insight("t", "p", insights)

    assert meta.content == "Meta Insight"

    assert meta.type == ReflectionType.META

    service.mock_reflection_repo.create_reflection.assert_called_once()


def test_calculate_priority(service):
    scoring = ReflectionScoring(
        novelty_score=0.8, importance_score=0.8, utility_score=0.8, confidence_score=0.8
    )
    priority = service._calculate_priority(20, scoring)
    assert priority == 5

    scoring_low = ReflectionScoring(
        novelty_score=0.2, importance_score=0.2, utility_score=0.2, confidence_score=0.2
    )
    priority_low = service._calculate_priority(2, scoring_low)
    assert priority_low == 1
