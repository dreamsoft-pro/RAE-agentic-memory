import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4, UUID
from datetime import datetime, timezone
from fastapi import HTTPException

from apps.memory_api.routes.graph_enhanced import (
    create_node, create_edge, get_node_metrics, traverse_graph,
    detect_cycle, find_shortest_path, create_snapshot
)
from apps.memory_api.models.graph_enhanced_models import (
    CreateGraphNodeRequest, CreateGraphEdgeRequest, TraverseGraphRequest,
    DetectCycleRequest, FindPathRequest, CreateSnapshotRequest, 
    TraversalAlgorithm, EnhancedGraphNode, EnhancedGraphEdge,
    NodeDegreeMetrics, CycleDetectionResult, GraphPath, GraphSnapshot
)

# --- Fixtures ---

@pytest.fixture
def mock_repo():
    with patch("apps.memory_api.routes.graph_enhanced.EnhancedGraphRepository") as mock:
        repo_instance = AsyncMock()
        mock.return_value = repo_instance
        yield repo_instance

@pytest.fixture
def mock_pool():
    return AsyncMock()

# --- Tests ---

@pytest.mark.asyncio
async def test_create_node(mock_repo, mock_pool):
    node_uuid = uuid4()
    req = CreateGraphNodeRequest(
        tenant_id="t1",
        project_id="p1",
        node_id=str(node_uuid),
        label="Test Node",
        properties={"key": "value"}
    )
    
    mock_node = EnhancedGraphNode(
        id=node_uuid,
        tenant_id="t1",
        project_id="p1",
        node_id=str(node_uuid),
        label="Test Node",
        created_at=datetime.now(timezone.utc)
    )
    mock_repo.create_node.return_value = mock_node
    
    response = await create_node(req, mock_pool)
    
    assert str(response.id) == str(node_uuid)
    assert response.label == "Test Node"
    mock_repo.create_node.assert_called_once()

@pytest.mark.asyncio
async def test_create_edge_success(mock_repo, mock_pool):
    req = CreateGraphEdgeRequest(
        tenant_id="t1",
        project_id="p1",
        source_node_id=str(uuid4()),
        target_node_id=str(uuid4()),
        relation="RELATES_TO"
    )
    
    # Mock no cycle detected
    mock_repo.detect_cycle.return_value = MagicMock(has_cycle=False)
    
    mock_edge = EnhancedGraphEdge(
        id=uuid4(),
        tenant_id="t1",
        project_id="p1",
        source_node_id=req.source_node_id,
        target_node_id=req.target_node_id,
        relation="RELATES_TO",
        valid_from=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    mock_repo.create_edge.return_value = mock_edge
    
    response = await create_edge(req, mock_pool)
    
    assert response.relation == "RELATES_TO"
    mock_repo.create_edge.assert_called_once()
    mock_repo.detect_cycle.assert_called_once()

@pytest.mark.asyncio
async def test_get_node_metrics(mock_repo, mock_pool):
    node_id = uuid4()
    mock_metrics = NodeDegreeMetrics(
        node_id=node_id,
        in_degree=2,
        out_degree=3,
        total_degree=5
    )
    mock_repo.get_node_metrics.return_value = mock_metrics
    
    response = await get_node_metrics("t1", "p1", str(node_id), mock_pool)
    
    assert response.metrics.total_degree == 5
    assert str(response.node_id) == str(node_id)

@pytest.mark.asyncio
async def test_traverse_graph(mock_repo, mock_pool):
    req = TraverseGraphRequest(
        tenant_id="t1",
        project_id="p1",
        start_node_id=str(uuid4()),
        algorithm=TraversalAlgorithm.BFS,
        max_depth=2
    )
    
    mock_node = EnhancedGraphNode(
        id=uuid4(), tenant_id="t1", project_id="p1", 
        node_id="n1", label="Node 1", 
        created_at=datetime.now(timezone.utc)
    )
    mock_edge = EnhancedGraphEdge(
        id=uuid4(), tenant_id="t1", project_id="p1",
        source_node_id=uuid4(), target_node_id=uuid4(), relation="rel",
        valid_from=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    mock_repo.traverse_temporal.return_value = ([mock_node], [mock_edge])
    
    response = await traverse_graph(req, mock_pool)
    
    assert response.total_nodes == 1
    assert response.total_edges == 1
    assert response.algorithm_used == TraversalAlgorithm.BFS

@pytest.mark.asyncio
async def test_detect_cycle(mock_repo, mock_pool):
    req = DetectCycleRequest(
        tenant_id="t1",
        project_id="p1",
        source_node_id=str(uuid4()),
        target_node_id=str(uuid4())
    )
    
    mock_res = CycleDetectionResult(
        has_cycle=True, 
        cycle_length=3,
        source_node_id=req.source_node_id,
        target_node_id=req.target_node_id
    )
    mock_repo.detect_cycle.return_value = mock_res
    
    response = await detect_cycle(req, mock_pool)
    
    assert response.result.has_cycle is True
    assert "Cycle detected" in response.message

@pytest.mark.asyncio
async def test_find_shortest_path(mock_repo, mock_pool):
    req = FindPathRequest(
        tenant_id="t1",
        project_id="p1",
        start_node_id=str(uuid4()),
        end_node_id=str(uuid4())
    )
    
    mock_path = GraphPath(
        nodes=[uuid4(), uuid4()],
        length=3, 
        total_weight=1.5
    )
    mock_repo.find_shortest_path.return_value = mock_path
    
    response = await find_shortest_path(req, mock_pool)
    
    assert response.path_found is True
    assert response.path.length == 3

@pytest.mark.asyncio
async def test_create_snapshot(mock_repo, mock_pool):
    req = CreateSnapshotRequest(
        tenant_id="t1",
        project_id="p1",
        snapshot_name="Backup 1"
    )
    
    snap_id = uuid4()
    mock_repo.create_snapshot.return_value = snap_id
    
    mock_snapshot = GraphSnapshot(
        id=snap_id, tenant_id="t1", project_id="p1",
        snapshot_name="Backup 1",
        node_count=10, edge_count=15,
        snapshot_size_bytes=1024,
        created_at=datetime.now(timezone.utc)
    )
    mock_repo.get_snapshot.return_value = mock_snapshot
    
    response = await create_snapshot(req, mock_pool)
    
    assert response.snapshot_id == snap_id
    assert response.node_count == 10
    mock_repo.create_snapshot.assert_called_once()

@pytest.mark.asyncio
async def test_create_edge_failure(mock_repo, mock_pool):
    req = CreateGraphEdgeRequest(
        tenant_id="t1",
        project_id="p1",
        source_node_id=str(uuid4()),
        target_node_id=str(uuid4()),
        relation="RELATES_TO"
    )
    
    mock_repo.detect_cycle.side_effect = Exception("DB Error")
    
    with pytest.raises(HTTPException) as exc:
        await create_edge(req, mock_pool)
    
    assert exc.value.status_code == 400
