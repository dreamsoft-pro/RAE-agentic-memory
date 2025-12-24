from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from apps.memory_api.main import app
from apps.memory_api.security.dependencies import (
    get_and_verify_tenant_id,
    require_admin,
    verify_tenant_access,
)


@pytest.fixture
def client_with_auth(mock_app_state_pool):
    """Create TestClient with mocked lifespan and auth"""
    # mock_app_state_pool already sets app.state.pool, so we just need to ensure
    # it has a close method for lifespan shutdown
    if not hasattr(mock_app_state_pool, "close"):
        mock_app_state_pool.close = AsyncMock()

    # Override auth to prevent 401 errors
    app.dependency_overrides[get_and_verify_tenant_id] = lambda: "test-tenant"
    app.dependency_overrides[require_admin] = lambda: True
    app.dependency_overrides[verify_tenant_access] = lambda tenant_id: True

    # Mock lifespan dependencies (use the same pool from mock_app_state_pool)
    with (
        patch(
            "apps.memory_api.main.asyncpg.create_pool",
            new=AsyncMock(return_value=mock_app_state_pool),
        ),
        patch("apps.memory_api.main.rebuild_full_cache", new=AsyncMock()),
    ):
        with TestClient(app) as client:
            yield client

    # Cleanup
    app.dependency_overrides = {}


@pytest.mark.asyncio
async def test_governance_overview_success(client_with_auth, mock_app_state_pool):
    """Test GET /v1/governance/overview endpoint"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    # Mock aggregate statistics
    mock_conn.fetchrow.return_value = {
        "total_calls": 1000,
        "total_cost_usd": 150.50,
        "total_tokens": 500000,
        "unique_tenants": 5,
    }

    # Mock top tenants
    mock_conn.fetch.side_effect = [
        [
            {
                "tenant_id": "tenant-1",
                "calls": 500,
                "cost_usd": 75.25,
                "tokens": 250000,
            },
            {
                "tenant_id": "tenant-2",
                "calls": 300,
                "cost_usd": 45.15,
                "tokens": 150000,
            },
        ],
        [
            {"model": "gpt-4", "calls": 600, "cost_usd": 90.30, "tokens": 300000},
            {
                "model": "claude-3-5-sonnet-20241022",
                "calls": 400,
                "cost_usd": 60.20,
                "tokens": 200000,
            },
        ],
    ]

    response = client_with_auth.get(
        "/v1/governance/overview?days=30", headers={"X-Tenant-Id": "admin"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_cost_usd"] == 150.50
    assert data["total_calls"] == 1000
    assert data["total_tokens"] == 500000
    assert data["unique_tenants"] == 5
    assert "top_tenants" in data
    assert "top_models" in data


@pytest.mark.asyncio
async def test_governance_overview_with_custom_days(
    client_with_auth, mock_app_state_pool
):
    """Test governance overview with custom time period"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    mock_conn.fetchrow.return_value = {
        "total_calls": 200,
        "total_cost_usd": 30.00,
        "total_tokens": 100000,
        "unique_tenants": 2,
    }

    mock_conn.fetch.side_effect = [
        [{"tenant_id": "tenant-1", "calls": 200, "cost_usd": 30.00, "tokens": 100000}],
        [{"model": "gpt-4", "calls": 200, "cost_usd": 30.00, "tokens": 100000}],
    ]

    response = client_with_auth.get(
        "/v1/governance/overview?days=7", headers={"X-Tenant-Id": "admin"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_cost_usd"] == 30.00


@pytest.mark.asyncio
async def test_governance_overview_error(client_with_auth, mock_app_state_pool):
    """Test governance overview when database fails"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value
    mock_conn.fetchrow.side_effect = Exception("Database error")

    response = client_with_auth.get(
        "/v1/governance/overview", headers={"X-Tenant-Id": "admin"}
    )

    assert response.status_code == 500
    # Our generic exception handler returns: {"error": {"code": "500", "message": "Internal Server Error"}}
    # But for TestClient, we might get direct exception or the handler's response.
    # The traceback showed unhandled exception causing 500.
    # The custom generic_exception_handler returns:
    # content={"error": {"code": "500", "message": "Internal Server Error"}}

    # Wait, the failure in previous run was `KeyError: 'detail'`.
    # This means response.json() does not have 'detail' key.
    # It likely has 'error' key based on generic_exception_handler.

    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "500"


@pytest.mark.asyncio
async def test_tenant_governance_stats_success(client_with_auth, mock_app_state_pool):
    """Test GET /v1/governance/tenant/{tenant_id} endpoint"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    # Mock tenant statistics
    mock_conn.fetchrow.return_value = {
        "total_calls": 500,
        "total_cost_usd": 75.25,
        "total_tokens": 250000,
        "avg_cost_per_call": 0.15,
        "cache_hit_rate": 0.35,
        "cache_savings": 12.50,
    }

    # Mock breakdowns
    mock_conn.fetch.side_effect = [
        [
            {
                "project_id": "project-1",
                "calls": 300,
                "cost_usd": 45.15,
                "tokens": 150000,
            }
        ],
        [{"model": "gpt-4", "calls": 500, "cost_usd": 75.25, "tokens": 250000}],
        [{"operation": "query", "calls": 400, "cost_usd": 60.20, "tokens": 200000}],
    ]

    response = client_with_auth.get(
        "/v1/governance/tenant/test-tenant?days=30",
        headers={"X-Tenant-Id": "test-tenant"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["tenant_id"] == "test-tenant"
    assert data["total_cost_usd"] == 75.25
    assert data["total_calls"] == 500
    assert data["cache_hit_rate"] == 0.35
    assert "by_project" in data
    assert "by_model" in data
    assert "by_operation" in data


@pytest.mark.asyncio
async def test_tenant_governance_stats_no_data(client_with_auth, mock_app_state_pool):
    """Test tenant stats when no data exists for tenant"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    mock_conn.fetchrow.return_value = {
        "total_calls": 0,
        "total_cost_usd": 0.0,
        "total_tokens": 0,
        "avg_cost_per_call": 0.0,
        "cache_hit_rate": 0.0,
        "cache_savings": 0.0,
    }

    response = client_with_auth.get(
        "/v1/governance/tenant/nonexistent-tenant", headers={"X-Tenant-Id": "admin"}
    )

    assert response.status_code == 404
    # The error handler for HTTPException returns:
    # content={"error": {"code": str(exc.status_code), "message": exc.detail}}
    data = response.json()
    assert "error" in data
    assert "No data found" in data["error"]["message"]


@pytest.mark.asyncio
async def test_tenant_governance_stats_with_custom_period(
    client_with_auth, mock_app_state_pool
):
    """Test tenant stats with custom time period"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    mock_conn.fetchrow.return_value = {
        "total_calls": 100,
        "total_cost_usd": 15.00,
        "total_tokens": 50000,
        "avg_cost_per_call": 0.15,
        "cache_hit_rate": 0.40,
        "cache_savings": 5.00,
    }

    mock_conn.fetch.side_effect = [
        [{"project_id": "project-1", "calls": 100, "cost_usd": 15.00, "tokens": 50000}],
        [{"model": "gpt-4", "calls": 100, "cost_usd": 15.00, "tokens": 50000}],
        [{"operation": "query", "calls": 100, "cost_usd": 15.00, "tokens": 50000}],
    ]

    response = client_with_auth.get(
        "/v1/governance/tenant/test-tenant?days=7",
        headers={"X-Tenant-Id": "test-tenant"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_calls"] == 100


@pytest.mark.asyncio
async def test_tenant_budget_status_success(client_with_auth, mock_app_state_pool):
    """Test GET /v1/governance/tenant/{tenant_id}/budget endpoint"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    mock_conn.fetchrow.return_value = {
        "current_cost_usd": 45.50,
        "current_tokens": 150000,
    }

    response = client_with_auth.get(
        "/v1/governance/tenant/test-tenant/budget",
        headers={"X-Tenant-Id": "test-tenant"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["tenant_id"] == "test-tenant"
    assert data["current_month_cost_usd"] == 45.50
    assert data["current_month_tokens"] == 150000
    assert "projected_month_end_cost" in data
    assert "days_remaining" in data
    assert data["status"] == "OK"


@pytest.mark.asyncio
async def test_tenant_budget_status_with_alerts(client_with_auth, mock_app_state_pool):
    """Test budget status with budget alerts (simulated)"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    # Simulate high usage (would trigger alerts if budget was configured)
    mock_conn.fetchrow.return_value = {
        "current_cost_usd": 950.00,
        "current_tokens": 3000000,
    }

    response = client_with_auth.get(
        "/v1/governance/tenant/test-tenant/budget",
        headers={"X-Tenant-Id": "test-tenant"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["current_month_cost_usd"] == 950.00
    # Note: alerts would only be present if budget limits were configured in database


@pytest.mark.asyncio
async def test_tenant_budget_status_zero_usage(client_with_auth, mock_app_state_pool):
    """Test budget status with zero usage"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    mock_conn.fetchrow.return_value = {"current_cost_usd": 0.0, "current_tokens": 0}

    response = client_with_auth.get(
        "/v1/governance/tenant/new-tenant/budget", headers={"X-Tenant-Id": "new-tenant"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["current_month_cost_usd"] == 0.0
    assert data["projected_month_end_cost"] == 0.0
    assert data["status"] == "OK"


@pytest.mark.asyncio
async def test_tenant_budget_status_error(client_with_auth, mock_app_state_pool):
    """Test budget status when database fails"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value
    mock_conn.fetchrow.side_effect = Exception("Database connection failed")

    response = client_with_auth.get(
        "/v1/governance/tenant/test-tenant/budget",
        headers={"X-Tenant-Id": "test-tenant"},
    )

    assert response.status_code == 500
    # The generic exception handler returns:
    # content={"error": {"code": "500", "message": "Internal Server Error"}}
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "500"


@pytest.mark.asyncio
async def test_governance_overview_invalid_days(client_with_auth, mock_app_state_pool):
    """Test governance overview with invalid days parameter"""
    response = client_with_auth.get(
        "/v1/governance/overview?days=400",  # Max is 365
        headers={"X-Tenant-Id": "admin"},
    )

    # FastAPI should validate and return 422 for invalid parameter
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tenant_governance_stats_invalid_days(
    client_with_auth, mock_app_state_pool
):
    """Test tenant stats with invalid days parameter"""
    response = client_with_auth.get(
        "/v1/governance/tenant/test-tenant?days=0",  # Min is 1
        headers={"X-Tenant-Id": "test-tenant"},
    )

    # FastAPI should validate and return 422 for invalid parameter
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_governance_overview_empty_results(client_with_auth, mock_app_state_pool):
    """Test governance overview with no data in system"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    mock_conn.fetchrow.return_value = {
        "total_calls": 0,
        "total_cost_usd": 0.0,
        "total_tokens": 0,
        "unique_tenants": 0,
    }

    mock_conn.fetch.side_effect = [[], []]  # Empty top tenants and models

    response = client_with_auth.get(
        "/v1/governance/overview", headers={"X-Tenant-Id": "admin"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_calls"] == 0
    assert data["top_tenants"] == []
    assert data["top_models"] == []
