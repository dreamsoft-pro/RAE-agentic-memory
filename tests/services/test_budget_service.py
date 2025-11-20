import pytest
# POPRAWKA: Dodano MagicMock do importów
from unittest.mock import AsyncMock, MagicMock 
from datetime import datetime
from apps.memory_api.services import budget_service
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_check_budget():
    mock_pool = MagicMock()
    mock_pool.fetchrow = AsyncMock()
    
    mock_pool.fetchrow.return_value = {
        "id": "b1", "tenant_id": "t1", "project_id": "p1",
        "monthly_limit": 10.0, "monthly_usage": 5.0,
        "daily_limit": 1.0, "daily_usage": 0.5,
        "last_usage_at": datetime.now()
    }

    await budget_service.check_budget(mock_pool, "t1", "p1", 0.1)

@pytest.mark.asyncio
async def test_check_budget_fail():
    mock_pool = MagicMock()
    mock_pool.fetchrow = AsyncMock()
    
    mock_pool.fetchrow.return_value = {
        "id": "b1", "tenant_id": "t1", "project_id": "p1",
        "monthly_limit": 10.0, "monthly_usage": 5.0,
        "daily_limit": 1.0, "daily_usage": 0.9,
        "last_usage_at": datetime.now()
    }

    with pytest.raises(HTTPException) as exc:
        await budget_service.check_budget(mock_pool, "t1", "p1", 0.2)
    assert exc.value.status_code == 402