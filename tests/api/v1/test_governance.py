import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from apps.memory_api.main import app
from datetime import datetime, timezone

client = TestClient(app)


@pytest.mark.asyncio
async def test_governance_overview_success(mock_app_state_pool):
    """Test GET /v1/governance/overview endpoint"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    # Mock aggregate statistics
    mock_conn.fetchrow.return_value = {
        "total_calls": 1000,
        "total_cost_usd": 150.50,
        "total_tokens": 500000,
        "unique_tenants": 5
    }

    # Mock top tenants
    mock_conn.fetch.side_effect = [
        [
            {"tenant_id": "tenant-1", "calls": 500, "cost_usd": 75.25, "tokens": 250000},
            {"tenant_id": "tenant-2", "calls": 300, "cost_usd": 45.15, "tokens": 150000},
        ],
        [
            {"model": "gpt-4", "calls": 600, "cost_usd": 90.30, "tokens": 300000},
            {"model": "claude-3-5-sonnet-20241022", "calls": 400, "cost_usd": 60.20, "tokens": 200000},
        ]
    ]

    response = client.get(
        "/v1/governance/overview?days=30",
        headers={"X-Tenant-Id": "admin"}
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
async def test_governance_overview_with_custom_days(mock_app_state_pool):
    """Test governance overview with custom time period"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    mock_conn.fetchrow.return_value = {
        "total_calls": 200,
        "total_cost_usd": 30.00,
        "total_tokens": 100000,
        "unique_tenants": 2
    }

    mock_conn.fetch.side_effect = [
        [{"tenant_id": "tenant-1", "calls": 200, "cost_usd": 30.00, "tokens": 100000}],
        [{"model": "gpt-4", "calls": 200, "cost_usd": 30.00, "tokens": 100000}]
    ]

    response = client.get(
        "/v1/governance/overview?days=7",
        headers={"X-Tenant-Id": "admin"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_cost_usd"] == 30.00


@pytest.mark.asyncio
async def test_governance_overview_error(mock_app_state_pool):
    """Test governance overview when database fails"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value
    mock_conn.fetchrow.side_effect = Exception("Database error")

    response = client.get(
        "/v1/governance/overview",
        headers={"X-Tenant-Id": "admin"}
    )

    assert response.status_code == 500
    assert "error" in response.json()["detail"].lower() or "Database error" in response.json()["detail"]


@pytest.mark.asyncio
async def test_tenant_governance_stats_success(mock_app_state_pool):
    """Test GET /v1/governance/tenant/{tenant_id} endpoint"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    # Mock tenant statistics
    mock_conn.fetchrow.return_value = {
        "total_calls": 500,
        "total_cost_usd": 75.25,
        "total_tokens": 250000,
        "avg_cost_per_call": 0.15,
        "cache_hit_rate": 0.35,
        "cache_savings": 12.50
    }

    # Mock breakdowns
    mock_conn.fetch.side_effect = [
        [{"project_id": "project-1", "calls": 300, "cost_usd": 45.15, "tokens": 150000}],
        [{"model": "gpt-4", "calls": 500, "cost_usd": 75.25, "tokens": 250000}],
        [{"operation": "query", "calls": 400, "cost_usd": 60.20, "tokens": 200000}]
    ]

    response = client.get(
        "/v1/governance/tenant/test-tenant?days=30",
        headers={"X-Tenant-Id": "test-tenant"}
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
async def test_tenant_governance_stats_no_data(mock_app_state_pool):
    """Test tenant stats when no data exists for tenant"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    mock_conn.fetchrow.return_value = {
        "total_calls": 0,
        "total_cost_usd": 0.0,
        "total_tokens": 0,
        "avg_cost_per_call": 0.0,
        "cache_hit_rate": 0.0,
        "cache_savings": 0.0
    }

    response = client.get(
        "/v1/governance/tenant/nonexistent-tenant",
        headers={"X-Tenant-Id": "admin"}
    )

    assert response.status_code == 404
    assert "No data found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_tenant_governance_stats_with_custom_period(mock_app_state_pool):
    """Test tenant stats with custom time period"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    mock_conn.fetchrow.return_value = {
        "total_calls": 100,
        "total_cost_usd": 15.00,
        "total_tokens": 50000,
        "avg_cost_per_call": 0.15,
        "cache_hit_rate": 0.40,
        "cache_savings": 5.00
    }

    mock_conn.fetch.side_effect = [
        [{"project_id": "project-1", "calls": 100, "cost_usd": 15.00, "tokens": 50000}],
        [{"model": "gpt-4", "calls": 100, "cost_usd": 15.00, "tokens": 50000}],
        [{"operation": "query", "calls": 100, "cost_usd": 15.00, "tokens": 50000}]
    ]

    response = client.get(
        "/v1/governance/tenant/test-tenant?days=7",
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_calls"] == 100


@pytest.mark.asyncio
async def test_tenant_budget_status_success(mock_app_state_pool):
    """Test GET /v1/governance/tenant/{tenant_id}/budget endpoint"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    mock_conn.fetchrow.return_value = {
        "current_cost_usd": 45.50,
        "current_tokens": 150000
    }

    response = client.get(
        "/v1/governance/tenant/test-tenant/budget",
        headers={"X-Tenant-Id": "test-tenant"}
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
async def test_tenant_budget_status_with_alerts(mock_app_state_pool):
    """Test budget status with budget alerts (simulated)"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    # Simulate high usage (would trigger alerts if budget was configured)
    mock_conn.fetchrow.return_value = {
        "current_cost_usd": 950.00,
        "current_tokens": 3000000
    }

    response = client.get(
        "/v1/governance/tenant/test-tenant/budget",
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["current_month_cost_usd"] == 950.00
    # Note: alerts would only be present if budget limits were configured in database


@pytest.mark.asyncio
async def test_tenant_budget_status_zero_usage(mock_app_state_pool):
    """Test budget status with zero usage"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    mock_conn.fetchrow.return_value = {
        "current_cost_usd": 0.0,
        "current_tokens": 0
    }

    response = client.get(
        "/v1/governance/tenant/new-tenant/budget",
        headers={"X-Tenant-Id": "new-tenant"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["current_month_cost_usd"] == 0.0
    assert data["projected_month_end_cost"] == 0.0
    assert data["status"] == "OK"


@pytest.mark.asyncio
async def test_tenant_budget_status_error(mock_app_state_pool):
    """Test budget status when database fails"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value
    mock_conn.fetchrow.side_effect = Exception("Database connection failed")

    response = client.get(
        "/v1/governance/tenant/test-tenant/budget",
        headers={"X-Tenant-Id": "test-tenant"}
    )

    assert response.status_code == 500
    assert "error" in response.json()["detail"].lower() or "Database connection failed" in response.json()["detail"]


@pytest.mark.asyncio
async def test_governance_overview_invalid_days(mock_app_state_pool):
    """Test governance overview with invalid days parameter"""
    response = client.get(
        "/v1/governance/overview?days=400",  # Max is 365
        headers={"X-Tenant-Id": "admin"}
    )

    # FastAPI should validate and return 422 for invalid parameter
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_tenant_governance_stats_invalid_days(mock_app_state_pool):
    """Test tenant stats with invalid days parameter"""
    response = client.get(
        "/v1/governance/tenant/test-tenant?days=0",  # Min is 1
        headers={"X-Tenant-Id": "test-tenant"}
    )

    # FastAPI should validate and return 422 for invalid parameter
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_governance_overview_empty_results(mock_app_state_pool):
    """Test governance overview with no data in system"""
    mock_conn = mock_app_state_pool.acquire.return_value.__aenter__.return_value

    mock_conn.fetchrow.return_value = {
        "total_calls": 0,
        "total_cost_usd": 0.0,
        "total_tokens": 0,
        "unique_tenants": 0
    }

    mock_conn.fetch.side_effect = [[], []]  # Empty top tenants and models

    response = client.get(
        "/v1/governance/overview",
        headers={"X-Tenant-Id": "admin"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["total_calls"] == 0
    assert data["top_tenants"] == []
    assert data["top_models"] == []
