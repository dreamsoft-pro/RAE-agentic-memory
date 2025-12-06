from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock

import pytest

from apps.memory_api.config import settings
from apps.memory_api.services.context_builder import ContextBuilder


@pytest.mark.unit
async def test_context_builder_uses_v3_when_enabled():
    # Setup
    pool = MagicMock()
    repo = MagicMock()
    reflection_engine = MagicMock()

    # Mock repository return values
    repo.get_episodic_memories = AsyncMock(
        return_value=[
            {
                "id": "1",
                "content": "test",
                "created_at": datetime(2024, 1, 1, tzinfo=timezone.utc),
                "layer": "episodic",
                "importance": 0.5,
            }
        ]
    )
    repo.get_semantic_memories = AsyncMock(return_value=[])
    reflection_engine.query_reflections = AsyncMock(return_value=[])

    builder = ContextBuilder(pool, repo, reflection_engine)

    # Enable V3 temporarily
    original_flag = settings.ENABLE_MATH_V3
    settings.ENABLE_MATH_V3 = True

    try:
        # Act
        ctx = await builder.build_context(
            tenant_id="t1", project_id="p1", query="test query"
        )

        # Assert
        assert len(ctx.ltm_items) == 1
        # Ideally we check if V3 scoring was used, but since it's internal to _retrieve_ltm
        # and we didn't mock compute_batch_scores_v3, we assume it ran if no error occurred
        # and the flow completed.
        # To be more robust, we could patch compute_batch_scores_v3.

    finally:
        settings.ENABLE_MATH_V3 = original_flag


@pytest.mark.unit
async def test_context_builder_v3_integration_mock():
    """Verify V3 is actually called using patch"""
    from unittest.mock import patch

    pool = MagicMock()
    repo = MagicMock()
    reflection_engine = MagicMock()

    repo.get_episodic_memories = AsyncMock(
        return_value=[
            {"id": "1", "content": "test", "created_at": "2024-01-01T00:00:00Z"}
        ]
    )
    repo.get_semantic_memories = AsyncMock(return_value=[])
    reflection_engine.query_reflections = AsyncMock(return_value=[])

    builder = ContextBuilder(pool, repo, reflection_engine)

    original_flag = settings.ENABLE_MATH_V3
    settings.ENABLE_MATH_V3 = True

    with patch(
        "apps.memory_api.services.context_builder.compute_batch_scores_v3"
    ) as mock_v3:
        # Mock return value to match structure expected by rank_memories_by_score
        mock_res = MagicMock()
        mock_res.final_score = 0.9
        mock_v3.return_value = [mock_res]

        await builder.build_context("t1", "p1", "q")

        mock_v3.assert_called_once()

    settings.ENABLE_MATH_V3 = original_flag
