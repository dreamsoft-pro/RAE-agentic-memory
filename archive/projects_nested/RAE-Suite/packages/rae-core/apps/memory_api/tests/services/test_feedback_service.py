from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from apps.memory_api.config import settings
from apps.memory_api.services.feedback_service import FeedbackService


@pytest.mark.asyncio
async def test_process_feedback_positive():
    mock_rae = MagicMock()
    mock_rae.adjust_importance = AsyncMock(return_value=0.7)
    mock_rae.db = AsyncMock()

    service = FeedbackService(rae_service=mock_rae)
    settings.FEEDBACK_POSITIVE_DELTA = 0.1

    mem_id = str(uuid4())
    result = await service.process_feedback(
        tenant_id="t1", memory_id=mem_id, feedback_type="positive"
    )

    assert result is True
    mock_rae.adjust_importance.assert_called_once_with(
        memory_id=mem_id, tenant_id="t1", delta=0.1
    )


@pytest.mark.asyncio
async def test_process_feedback_negative():
    mock_rae = MagicMock()
    mock_rae.adjust_importance = AsyncMock(return_value=0.4)
    mock_rae.db = AsyncMock()

    service = FeedbackService(rae_service=mock_rae)
    settings.FEEDBACK_NEGATIVE_DELTA = 0.2

    mem_id = str(uuid4())
    result = await service.process_feedback(
        tenant_id="t1", memory_id=mem_id, feedback_type="negative"
    )

    assert result is True
    mock_rae.adjust_importance.assert_called_once_with(
        memory_id=mem_id, tenant_id="t1", delta=-0.2
    )


@pytest.mark.asyncio
async def test_process_feedback_db_error():
    mock_rae = MagicMock()
    mock_rae.adjust_importance = AsyncMock()
    # Mock DB failure
    mock_rae.db = MagicMock()
    mock_rae.db.execute = AsyncMock(side_effect=Exception("DB Error"))

    service = FeedbackService(rae_service=mock_rae)

    mem_id = str(uuid4())
    result = await service.process_feedback(
        tenant_id="t1", memory_id=mem_id, feedback_type="positive"
    )

    assert result is False
