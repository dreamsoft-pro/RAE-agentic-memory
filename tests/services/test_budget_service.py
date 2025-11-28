from datetime import datetime

# POPRAWKA: Dodano MagicMock do importów
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from apps.memory_api.services import budget_service


@pytest.mark.asyncio
async def test_check_budget():
    mock_pool = MagicMock()
    mock_pool.fetchrow = AsyncMock()

    mock_pool.fetchrow.return_value = {
        "id": "b1",
        "tenant_id": "t1",
        "project_id": "p1",
        "monthly_limit_usd": 10.0,
        "monthly_usage_usd": 5.0,
        "daily_limit_usd": 1.0,
        "daily_usage_usd": 0.5,
        "monthly_tokens_limit": None,
        "monthly_tokens_used": 0,
        "daily_tokens_limit": None,
        "daily_tokens_used": 0,
        "created_at": datetime.now(),
        "last_usage_at": datetime.now(),
        "last_token_update_at": datetime.now(),
        "last_daily_reset": datetime.now(),
        "last_monthly_reset": datetime.now(),
    }

    await budget_service.check_budget(mock_pool, "t1", "p1", 0.1, 100)


@pytest.mark.asyncio
async def test_check_budget_fail():
    mock_pool = MagicMock()
    mock_pool.fetchrow = AsyncMock()

    mock_pool.fetchrow.return_value = {
        "id": "b1",
        "tenant_id": "t1",
        "project_id": "p1",
        "monthly_limit_usd": 10.0,
        "monthly_usage_usd": 5.0,
        "daily_limit_usd": 1.0,
        "daily_usage_usd": 0.9,
        "monthly_tokens_limit": None,
        "monthly_tokens_used": 0,
        "daily_tokens_limit": None,
        "daily_tokens_used": 0,
        "created_at": datetime.now(),
        "last_usage_at": datetime.now(),
        "last_token_update_at": datetime.now(),
        "last_daily_reset": datetime.now(),
        "last_monthly_reset": datetime.now(),
    }

    with pytest.raises(HTTPException) as exc:
        await budget_service.check_budget(mock_pool, "t1", "p1", 0.2, 200)
    assert exc.value.status_code == 402
