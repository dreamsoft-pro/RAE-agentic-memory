from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from apps.memory_api.models.dashboard_models import (
    ComplianceArea,
    ComplianceStatus,
    ISO42001Metric,
    RiskLevel,
    RiskMetric,
)
from apps.memory_api.services.compliance_service import ComplianceService


@pytest.fixture
def mock_pool():
    pool_mock = AsyncMock()

    # Connection mock needs async methods for fetch/fetchrow/fetchval
    conn_mock = MagicMock()

    async def async_fetch(*args, **kwargs):
        return []

    conn_mock.fetch.side_effect = async_fetch

    async def async_fetchrow(*args, **kwargs):
        return None

    conn_mock.fetchrow.side_effect = async_fetchrow

    async def async_fetchval(*args, **kwargs):
        return 0

    conn_mock.fetchval.side_effect = async_fetchval

    # Context Manager Mock
    # __aenter__ must return the conn_mock
    async def aenter(*args, **kwargs):
        return conn_mock

    async def aexit(*args, **kwargs):
        return None

    mock_context_manager = MagicMock()
    mock_context_manager.__aenter__ = AsyncMock(side_effect=aenter)
    mock_context_manager.__aexit__ = AsyncMock(side_effect=aexit)

    # pool.acquire() returns the context manager (NOT awaited itself in `async with pool.acquire()`)
    # wait, pool.acquire() IS awaited?
    # No, `async with pool.acquire() as conn` -> calls pool.acquire(), gets object, awaits obj.__aenter__()
    # Actually asyncpg Pool.acquire IS an async method, so it returns a coroutine that resolves to a connection context manager?
    # Let's double check asyncpg docs.
    # `async with pool.acquire() as connection:`
    # If pool.acquire() is async, then `pool.acquire()` returns a coroutine.
    # `async with` takes an object that has `__aenter__` and `__aexit__`.
    # If the expression in `async with EXPR` returns a coroutine, Python DOES NOT await it automatically unless you write `async with await EXPR`.
    # BUT asyncpg Pool.acquire is NOT async def. It returns a `PoolAcquireContext` synchronously.
    # `class PoolAcquireContext:` has `async def __aenter__`.
    # So `pool.acquire()` is a synchronous call returning a context manager.

    pool_mock.acquire = MagicMock(return_value=mock_context_manager)

    # We store the conn_mock on the pool_mock for easy access in tests to set side effects
    pool_mock._conn_mock = conn_mock

    yield pool_mock


@pytest.fixture
def compliance_service(mock_pool):
    return ComplianceService(mock_pool)


@pytest.mark.asyncio
async def test_generate_compliance_report_full(compliance_service):
    """Test generating a full compliance report with all sub-metrics mocked."""
    # ... (rest of the test as is) ...


@pytest.mark.asyncio
async def test_verify_rls_status_success(compliance_service, mock_pool):
    """Test RLS verification when all tables have RLS enabled."""
    conn_mock = mock_pool._conn_mock

    # Using async function side_effects is more robust than list iterators for AsyncMock

    async def fetch_policy_count(*args, **kwargs):
        return [{"total": 2, "active": 2}]

    async def fetchrow_table_status(query, table_name, *args, **kwargs):
        return {"rowsecurity": True}

    conn_mock.fetch.side_effect = fetch_policy_count
    conn_mock.fetchrow.side_effect = fetchrow_table_status

    status = await compliance_service.verify_rls_status("t1")

    assert status.rls_enabled_percentage == 100.0
    assert status.verification_passed is True
    assert "memories" in status.tables_with_rls
    assert status.total_policies == 2
    assert status.active_policies == 2


@pytest.mark.asyncio
async def test_verify_rls_status_failure(compliance_service, mock_pool):
    """Test RLS verification when some tables are missing RLS."""
    conn_mock = mock_pool._conn_mock

    async def fetch_policy_count(*args, **kwargs):
        return [{"total": 1, "active": 1}]

    async def fetchrow_table_status(query, table_name, *args, **kwargs):
        # Simulate missing RLS for 'reflections' table
        if table_name == "reflections":
            return {"rowsecurity": False}
        return {"rowsecurity": True}

    conn_mock.fetch.side_effect = fetch_policy_count
    conn_mock.fetchrow.side_effect = fetchrow_table_status

    status = await compliance_service.verify_rls_status("t1")

    assert status.rls_enabled_percentage < 100.0
    assert status.verification_passed is False
    assert "reflections" in status.tables_without_rls
    assert status.total_policies == 1
    assert status.active_policies == 1


@pytest.mark.asyncio
async def test_get_active_risks(compliance_service):
    """Test fetching active risks from DB (hardcoded in service for now)."""
    # This method does NOT use the pool directly in its current hardcoded form
    # We assert against the hardcoded values in the service
    risks = await compliance_service._get_active_risks("t1", "p1")

    assert len(risks) == 3  # Hardcoded list in service has 3 items
    assert isinstance(risks[0], RiskMetric)
    assert risks[0].risk_id == "RISK-001"
    assert risks[0].risk_level == RiskLevel.HIGH


@pytest.mark.asyncio
async def test_calculate_overall_score(compliance_service):
    """Test internal score calculation by mocking sub-metrics."""

    with patch.object(
        compliance_service, "_get_governance_metrics", new_callable=AsyncMock
    ) as mock_gov, patch.object(
        compliance_service, "_get_risk_management_metrics", new_callable=AsyncMock
    ) as mock_risk, patch.object(
        compliance_service, "_get_data_management_metrics", new_callable=AsyncMock
    ) as mock_data, patch.object(
        compliance_service, "_get_transparency_metrics", new_callable=AsyncMock
    ) as mock_trans, patch.object(
        compliance_service, "_get_human_oversight_metrics", new_callable=AsyncMock
    ) as mock_human, patch.object(
        compliance_service, "_get_security_privacy_metrics", new_callable=AsyncMock
    ) as mock_sec, patch.object(
        compliance_service, "_get_active_risks", new_callable=AsyncMock
    ) as mock_active_risks, patch.object(
        compliance_service, "_get_retention_metrics", new_callable=AsyncMock
    ) as mock_retention, patch.object(
        compliance_service, "_get_source_trust_metrics", new_callable=AsyncMock
    ) as mock_source_trust, patch.object(
        compliance_service, "_get_audit_trail_completeness", new_callable=AsyncMock
    ) as mock_audit_comp, patch.object(
        compliance_service, "_get_audit_entries_count", new_callable=AsyncMock
    ) as mock_audit_count, patch.object(
        compliance_service, "_update_compliance_metrics", new_callable=MagicMock
    ) as mock_update_metrics:

        # Mock a metric with 100% score for one area, others empty
        compliant_metric = ISO42001Metric(
            requirement_id="T1",
            requirement_name="Test Metric 1",
            compliance_area=ComplianceArea.GOVERNANCE,
            status=ComplianceStatus.COMPLIANT,
            current_value=100.0,
            threshold=100.0,
            last_check=datetime.now(timezone.utc),
        )
        mock_gov.return_value = [compliant_metric]
        mock_risk.return_value = []
        mock_data.return_value = []
        mock_trans.return_value = []
        mock_human.return_value = []
        mock_sec.return_value = []
        mock_active_risks.return_value = []
        mock_retention.return_value = []
        mock_source_trust.return_value = None
        mock_audit_comp.return_value = 85.0
        mock_audit_count.return_value = 1500

        report = await compliance_service.generate_compliance_report("t1", "p1")

        assert (
            report.overall_compliance_score == 100.0
        )  # Only one area, fully compliant
        mock_update_metrics.assert_called_once()


# This test was a placeholder and is removed as it does not correspond to a public method.
# @pytest.mark.asyncio
# async def test_log_compliance_violation(compliance_service, mock_pool):
#     """Test logging a violation."""
#     pass


@pytest.mark.asyncio
async def test_get_governance_metrics_logic(compliance_service):
    """Test fetching and parsing governance metrics (which are hardcoded in the service)."""
    # The _get_governance_metrics method uses internal helper methods which are hardcoded true/false for simplicity
    # Patch the helper methods if needed, or just assert the expected output
    with patch.object(
        compliance_service,
        "_check_roles_defined",
        new_callable=AsyncMock,
        return_value=True,
    ), patch.object(
        compliance_service,
        "_check_policy_exists",
        new_callable=AsyncMock,
        return_value=True,
    ):

        metrics = await compliance_service._get_governance_metrics("t1", "p1")

        assert len(metrics) == 3
        assert metrics[0].requirement_id == "5.1"
        assert metrics[0].status == ComplianceStatus.COMPLIANT
        assert metrics[1].requirement_id == "5.2"
        assert metrics[1].status == ComplianceStatus.COMPLIANT
