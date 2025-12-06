from unittest.mock import AsyncMock, MagicMock

import pytest

from apps.memory_api.config import settings
from apps.memory_api.services.feedback_service import FeedbackService


@pytest.mark.asyncio
async def test_process_feedback_positive():
    mock_repo = MagicMock()
    mock_repo.update_importance = AsyncMock(return_value=0.7)

    service = FeedbackService(mock_repo)

    settings.ENABLE_FEEDBACK_LOOP = True
    settings.FEEDBACK_POSITIVE_DELTA = 0.1

    result = await service.process_feedback(
        tenant_id="t1", memory_id="m1", feedback_type="positive"
    )

    assert result is True
    mock_repo.update_importance.assert_called_once_with(
        memory_id="m1", tenant_id="t1", delta=0.1
    )


@pytest.mark.asyncio
async def test_process_feedback_negative():
    mock_repo = MagicMock()
    mock_repo.update_importance = AsyncMock(return_value=0.4)

    service = FeedbackService(mock_repo)

    settings.ENABLE_FEEDBACK_LOOP = True
    settings.FEEDBACK_NEGATIVE_DELTA = 0.2

    result = await service.process_feedback(
        tenant_id="t1", memory_id="m1", feedback_type="negative"
    )

    assert result is True
    mock_repo.update_importance.assert_called_once_with(
        memory_id="m1", tenant_id="t1", delta=-0.2
    )


@pytest.mark.asyncio
async def test_process_feedback_disabled():
    mock_repo = MagicMock()
    service = FeedbackService(mock_repo)

    settings.ENABLE_FEEDBACK_LOOP = False

    result = await service.process_feedback("t1", "m1", "positive")

    assert result is False
    mock_repo.update_importance.assert_not_called()
