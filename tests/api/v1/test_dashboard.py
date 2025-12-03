import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from datetime import datetime, timezone
from fastapi import Request, WebSocket, WebSocketDisconnect
from apps.memory_api.routes.dashboard import router
from apps.memory_api.models.dashboard_models import (
    HealthStatus, SystemHealth, GetSystemHealthRequest, 
    GetDashboardMetricsRequest, MetricPeriod, DashboardEventType
)

# --- Fixtures & Mocks ---

@pytest.fixture
def mock_websocket_service():
    with patch("apps.memory_api.routes.dashboard.get_websocket_service") as mock_get:
        service_mock = MagicMock()
        mock_get.return_value = service_mock
        yield service_mock

@pytest.fixture
def mock_metrics_repo():
    with patch("apps.memory_api.routes.dashboard.get_metrics_repo") as mock_get:
        repo_mock = AsyncMock()
        mock_get.return_value = repo_mock
        yield repo_mock

@pytest.fixture
def mock_compliance_service():
    with patch("apps.memory_api.routes.dashboard.get_compliance_service") as mock_get:
        service_mock = AsyncMock()
        mock_get.return_value = service_mock
        yield service_mock

@pytest.fixture
def mock_pool():
    pool = AsyncMock()
    pool.fetchval.return_value = 1
    pool.fetch.return_value = []
    pool.fetchrow.return_value = None
    return pool

@pytest.fixture
def mock_request(mock_pool):
    req = MagicMock(spec=Request)
    req.app.state.pool = mock_pool
    return req

# --- Tests ---

@pytest.mark.asyncio
async def test_get_system_health(mock_request, mock_websocket_service, mock_pool):
    from apps.memory_api.routes.dashboard import get_system_health
    
    # Setup mock return
    mock_websocket_service._check_system_health = AsyncMock(return_value=SystemHealth(
        overall_status=HealthStatus.HEALTHY,
        component_statuses={"db": "healthy"},
        last_check_time=datetime.now(timezone.utc),
        error_rate=0.0,
        latency_ms=10.0,
        active_connections=5,
        degraded_components=0
    ))
    
    request_data = GetSystemHealthRequest(
        tenant_id="test-tenant",
        project_id="test-project",
        include_sub_components=True
    )
    
    response = await get_system_health(request_data, mock_pool)
    
    assert response.system_health.overall_status == HealthStatus.HEALTHY
    assert response.recommendations == []
    mock_websocket_service._check_system_health.assert_called_once()

@pytest.mark.asyncio
async def test_get_dashboard_metrics(mock_request, mock_websocket_service, mock_pool):
    from apps.memory_api.routes.dashboard import get_dashboard_metrics
    from apps.memory_api.models.dashboard_models import SystemMetrics
    
    mock_websocket_service._collect_system_metrics = AsyncMock(return_value=SystemMetrics(
        total_memories=100
    ))
    
    request_data = GetDashboardMetricsRequest(
        tenant_id="test-tenant",
        project_id="test-project",
        period=MetricPeriod.LAST_24H
    )
    
    response = await get_dashboard_metrics(request_data, mock_pool)
    
    assert response.system_metrics.total_memories == 100
    # Since pool.fetch returns [], recent_activity should be empty
    assert response.recent_activity == []

@pytest.mark.asyncio
async def test_get_activity_log(mock_pool):
    from apps.memory_api.routes.dashboard import get_activity_log
    
    # Mock DB responses for memories and reflections
    mock_pool.fetch.side_effect = [
        [ # Memories
            {"id": uuid4(), "content": "Test Memory", "importance": 0.8, "created_at": datetime.now(timezone.utc)}
        ],
        [ # Reflections
            {"id": uuid4(), "content": "Test Reflection", "score": 0.9, "created_at": datetime.now(timezone.utc)}
        ]
    ]
    
    response = await get_activity_log(
        tenant_id="t1", 
        project_id="p1", 
        limit=10,
        event_types=None,
        pool=mock_pool
    )
    
    assert response["total_count"] == 2
    assert len(response["activity_logs"]) == 2
    assert response["activity_logs"][0]["event_type"] in [DashboardEventType.MEMORY_CREATED, DashboardEventType.REFLECTION_GENERATED]

@pytest.mark.asyncio
async def test_websocket_endpoint(mock_websocket_service):
    from apps.memory_api.routes.dashboard import websocket_endpoint
    
    mock_ws = AsyncMock(spec=WebSocket)
    mock_ws.receive_text.side_effect = ["ping", WebSocketDisconnect()]
    
    mock_websocket_service.handle_connection = AsyncMock(return_value="conn-123")
    
    await websocket_endpoint(
        websocket=mock_ws,
        tenant_id="t1",
        project_id="p1",
        event_types="memory_created,reflection_generated"
    )
    
    mock_websocket_service.handle_connection.assert_called_once()
    mock_ws.send_text.assert_called_with("pong")
    mock_websocket_service.handle_disconnection.assert_called_with("conn-123")

@pytest.mark.asyncio
async def test_compliance_report(mock_compliance_service):
    from apps.memory_api.routes.dashboard import get_compliance_report
    from apps.memory_api.models.dashboard_models import GetComplianceReportRequest, ComplianceReport, ComplianceStatus
    
    mock_report = ComplianceReport(
        tenant_id="t1",
        project_id="p1",
        overall_compliance_score=95.0,
        overall_status=ComplianceStatus.COMPLIANT
    )
    mock_compliance_service.generate_compliance_report.return_value = mock_report
    
    req = GetComplianceReportRequest(
        tenant_id="t1",
        project_id="p1",
        report_type="full",
        include_audit_trail=False 
    )
    
    response = await get_compliance_report(req, mock_compliance_service)
    
    assert response.compliance_report.overall_compliance_score == 95.0
    mock_compliance_service.generate_compliance_report.assert_called_once()

@pytest.mark.asyncio
async def test_risk_register(mock_compliance_service):
    from apps.memory_api.routes.dashboard import get_risk_register, GetRiskRegisterRequest, RiskLevel
    from apps.memory_api.models.dashboard_models import RiskMetric
    
    mock_risk = RiskMetric(
        risk_id="r1",
        risk_description="desc",
        category="cat",
        probability=0.5,
        impact=0.5,
        risk_score=0.25,
        risk_level=RiskLevel.HIGH,
        status="open",
        identified_at=datetime.now(timezone.utc),
        last_reviewed_at=datetime.now(timezone.utc)
    )
    
    mock_compliance_service._get_active_risks.return_value = [mock_risk]
    
    req = GetRiskRegisterRequest(
        tenant_id="t1",
        project_id="p1",
        risk_level=RiskLevel.HIGH
    )
    
    response = await get_risk_register(req, mock_compliance_service)
    
    assert response.high_priority_count == 1
    assert len(response.risks) == 1
