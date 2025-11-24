"""
Memory Dashboard Models - Real-time Monitoring and Visualization

This module defines models for the interactive dashboard including:
- Real-time metrics and statistics
- Visualization data structures
- WebSocket event messages
- System health indicators
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Field

# ============================================================================
# Enums
# ============================================================================


class DashboardEventType(str, Enum):
    """Types of dashboard events pushed via WebSocket"""

    MEMORY_CREATED = "memory_created"
    MEMORY_UPDATED = "memory_updated"
    MEMORY_DELETED = "memory_deleted"

    REFLECTION_GENERATED = "reflection_generated"
    SEMANTIC_NODE_CREATED = "semantic_node_created"

    SEARCH_EXECUTED = "search_executed"
    QUALITY_ALERT = "quality_alert"
    DRIFT_DETECTED = "drift_detected"

    TRIGGER_FIRED = "trigger_fired"
    ACTION_COMPLETED = "action_completed"

    METRICS_UPDATED = "metrics_updated"
    HEALTH_CHANGED = "health_changed"


class VisualizationType(str, Enum):
    """Types of visualizations"""

    REFLECTION_TREE = "reflection_tree"
    SEMANTIC_GRAPH = "semantic_graph"
    MEMORY_TIMELINE = "memory_timeline"
    QUALITY_TREND = "quality_trend"
    SEARCH_HEATMAP = "search_heatmap"
    CLUSTER_MAP = "cluster_map"


class HealthStatus(str, Enum):
    """System health status levels"""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    WARNING = "warning"
    CRITICAL = "critical"
    DOWN = "down"


class MetricPeriod(str, Enum):
    """Time periods for metrics"""

    LAST_HOUR = "last_hour"
    LAST_24H = "last_24h"
    LAST_7D = "last_7d"
    LAST_30D = "last_30d"
    CUSTOM = "custom"


# ============================================================================
# Real-time Metrics Models
# ============================================================================


class SystemMetrics(BaseModel):
    """
    Real-time system metrics for dashboard.

    Provides overview of system activity and health.
    """

    # Memory metrics
    total_memories: int = Field(0, ge=0)
    memories_last_24h: int = Field(0, ge=0)
    avg_memory_importance: float = Field(0.0, ge=0.0, le=1.0)

    # Reflection metrics
    total_reflections: int = Field(0, ge=0)
    reflections_last_24h: int = Field(0, ge=0)
    avg_reflection_score: float = Field(0.0, ge=0.0, le=1.0)

    # Semantic metrics
    total_semantic_nodes: int = Field(0, ge=0)
    semantic_nodes_last_24h: int = Field(0, ge=0)
    degraded_nodes_count: int = Field(0, ge=0)

    # Search metrics
    searches_last_24h: int = Field(0, ge=0)
    avg_search_quality_mrr: float = Field(0.0, ge=0.0, le=1.0)
    avg_search_latency_ms: float = Field(0.0, ge=0.0)

    # Graph metrics
    total_graph_nodes: int = Field(0, ge=0)
    total_graph_edges: int = Field(0, ge=0)
    avg_node_degree: float = Field(0.0, ge=0.0)

    # Trigger metrics
    active_triggers: int = Field(0, ge=0)
    trigger_executions_last_24h: int = Field(0, ge=0)
    trigger_success_rate: float = Field(0.0, ge=0.0, le=1.0)

    # System health
    health_status: HealthStatus = HealthStatus.HEALTHY
    error_rate_last_hour: float = Field(0.0, ge=0.0, le=1.0)

    # Timestamps
    collected_at: datetime = Field(default_factory=datetime.utcnow)
    period: MetricPeriod = MetricPeriod.LAST_24H


class TimeSeriesPoint(BaseModel):
    """Single point in time series data"""

    timestamp: datetime
    value: float
    label: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TimeSeriesMetric(BaseModel):
    """
    Time series metric for trend visualization.

    Used for charts showing metrics over time.
    """

    metric_name: str
    metric_label: str
    unit: Optional[str] = None

    data_points: List[TimeSeriesPoint] = Field(default_factory=list)

    # Statistics
    current_value: Optional[float] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    avg_value: Optional[float] = None

    # Trend
    trend_direction: Optional[str] = Field(
        None, description="'up', 'down', or 'stable'"
    )
    percent_change: Optional[float] = None

    period_start: datetime
    period_end: datetime


class ActivityLog(BaseModel):
    """
    Activity log entry for recent events.

    Displayed in dashboard activity feed.
    """

    log_id: UUID
    event_type: DashboardEventType

    title: str
    description: Optional[str] = None

    # Context
    tenant_id: str
    project_id: str

    # Related entities
    memory_id: Optional[UUID] = None
    reflection_id: Optional[UUID] = None
    semantic_node_id: Optional[UUID] = None
    trigger_id: Optional[UUID] = None

    # Severity for alerts
    severity: Optional[str] = Field(
        None, description="'info', 'warning', 'error', 'critical'"
    )

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # Timestamp
    occurred_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Visualization Data Models
# ============================================================================


class ReflectionTreeNode(BaseModel):
    """
    Node in reflection hierarchy tree.

    Used for tree visualization of hierarchical reflections.
    """

    reflection_id: UUID
    content: str
    type: str
    score: float = Field(ge=0.0, le=1.0)
    depth_level: int = Field(ge=0)

    # Parent-child relationships
    parent_id: Optional[UUID] = None
    children: List["ReflectionTreeNode"] = Field(default_factory=list)

    # Metadata for visualization
    cluster_id: Optional[str] = None
    source_memory_count: int = Field(0, ge=0)

    # Display properties
    color: Optional[str] = None
    size: Optional[float] = None

    created_at: datetime


# Allow recursive type
ReflectionTreeNode.model_rebuild()


class SemanticGraphNode(BaseModel):
    """
    Node in semantic knowledge graph.

    Used for graph visualization of semantic relationships.
    """

    node_id: UUID
    label: str
    node_type: str
    canonical_form: str

    # Node properties
    importance_score: float = Field(ge=0.0, le=1.0)
    reinforcement_count: int = Field(0, ge=0)
    is_degraded: bool = False

    # Visualization properties
    x: Optional[float] = None  # Position (if pre-calculated)
    y: Optional[float] = None
    color: Optional[str] = None
    size: float = 10.0


class SemanticGraphEdge(BaseModel):
    """
    Edge in semantic knowledge graph.

    Represents relationship between semantic nodes.
    """

    source_node_id: UUID
    target_node_id: UUID
    relation_type: str

    # Edge properties
    weight: float = Field(1.0, ge=0.0, le=1.0)
    confidence: float = Field(0.8, ge=0.0, le=1.0)

    # Visualization properties
    color: Optional[str] = None
    width: Optional[float] = None
    dashed: bool = False


class SemanticGraph(BaseModel):
    """
    Complete semantic graph for visualization.

    Contains nodes and edges with layout information.
    """

    nodes: List[SemanticGraphNode]
    edges: List[SemanticGraphEdge]

    # Graph statistics
    node_count: int
    edge_count: int
    avg_degree: float

    # Layout algorithm used
    layout_algorithm: Optional[str] = Field(
        None, description="'force', 'hierarchical', 'circular'"
    )

    # Timestamp
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class MemoryTimelineEvent(BaseModel):
    """
    Event on memory timeline.

    Represents a memory creation or significant event.
    """

    event_id: UUID
    event_type: str  # 'memory_created', 'reflection_generated', etc.

    title: str
    description: Optional[str] = None

    # Related entities
    memory_id: Optional[UUID] = None
    reflection_id: Optional[UUID] = None

    # Importance for sizing
    importance: float = Field(0.5, ge=0.0, le=1.0)

    # Visualization
    color: Optional[str] = None
    icon: Optional[str] = None

    occurred_at: datetime


class MemoryTimeline(BaseModel):
    """
    Timeline of memory events.

    Displays chronological view of memory creation and processing.
    """

    events: List[MemoryTimelineEvent]

    # Time range
    start_time: datetime
    end_time: datetime

    # Statistics
    total_events: int
    event_density: float = Field(0.0, description="Events per day")


class QualityTrend(BaseModel):
    """
    Quality metrics trend over time.

    Shows how system quality evolves.
    """

    metric_name: str  # 'mrr', 'ndcg', 'precision', etc.

    # Time series
    time_points: List[datetime]
    values: List[float]

    # Trend analysis
    trend_direction: str  # 'improving', 'declining', 'stable'
    percent_change: float

    # Thresholds
    warning_threshold: Optional[float] = None
    critical_threshold: Optional[float] = None

    # Current status
    current_value: float
    is_healthy: bool


class SearchHeatmap(BaseModel):
    """
    Heatmap of search activity.

    Shows search patterns by time and query type.
    """

    # Grid data
    time_buckets: List[datetime]  # X-axis
    query_types: List[str]  # Y-axis
    heat_values: List[List[float]]  # 2D array of intensities

    # Statistics
    total_searches: int
    peak_time: datetime
    peak_query_type: str


class ClusterMapNode(BaseModel):
    """
    Node in cluster visualization.

    Represents a cluster of similar memories.
    """

    cluster_id: str
    cluster_label: Optional[str] = None

    # Cluster properties
    member_count: int = Field(ge=0)
    avg_importance: float = Field(ge=0.0, le=1.0)

    # Centroid (for positioning)
    centroid_x: float
    centroid_y: float

    # Visualization
    color: Optional[str] = None
    size: float = 10.0

    # Representative memories
    top_memories: List[UUID] = Field(default_factory=list)


class ClusterMap(BaseModel):
    """
    Map of memory clusters.

    Shows how memories are grouped by similarity.
    """

    clusters: List[ClusterMapNode]

    # Statistics
    total_clusters: int
    total_memories: int
    avg_cluster_size: float

    # Dimensionality reduction method
    reduction_method: str = Field("umap", description="'umap', 'tsne', 'pca'")


# ============================================================================
# WebSocket Message Models
# ============================================================================


class WebSocketMessage(BaseModel):
    """
    Base WebSocket message.

    All WebSocket messages follow this structure.
    """

    message_id: UUID = Field(default_factory=lambda: __import__("uuid").uuid4())
    event_type: DashboardEventType

    # Payload
    payload: Dict[str, Any] = Field(default_factory=dict)

    # Context
    tenant_id: str
    project_id: str

    # Timestamp
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MetricsUpdateMessage(WebSocketMessage):
    """
    Metrics update message.

    Pushed when system metrics change significantly.
    """

    event_type: DashboardEventType = DashboardEventType.METRICS_UPDATED
    metrics: SystemMetrics


class HealthChangeMessage(WebSocketMessage):
    """
    Health status change message.

    Pushed when system health status changes.
    """

    event_type: DashboardEventType = DashboardEventType.HEALTH_CHANGED
    old_status: HealthStatus
    new_status: HealthStatus
    reason: str
    details: Optional[Dict[str, Any]] = None


class AlertMessage(WebSocketMessage):
    """
    Alert notification message.

    Pushed for quality degradation, drift detection, etc.
    """

    event_type: Union[DashboardEventType, str]

    alert_id: UUID = Field(default_factory=lambda: __import__("uuid").uuid4())
    severity: str  # 'warning', 'error', 'critical'
    title: str
    description: str

    # Recommended actions
    actions: List[str] = Field(default_factory=list)

    # Related entities
    related_ids: Dict[str, UUID] = Field(default_factory=dict)


# ============================================================================
# System Health Models
# ============================================================================


class ComponentHealth(BaseModel):
    """
    Health status of a system component.
    """

    component_name: str
    status: HealthStatus

    # Metrics
    response_time_ms: Optional[float] = None
    error_rate: Optional[float] = None
    throughput: Optional[float] = None

    # Details
    message: Optional[str] = None
    last_check: datetime = Field(default_factory=datetime.utcnow)

    # Sub-components
    sub_components: List["ComponentHealth"] = Field(default_factory=list)


# Allow recursive type
ComponentHealth.model_rebuild()


class SystemHealth(BaseModel):
    """
    Overall system health status.

    Aggregates health from all components.
    """

    overall_status: HealthStatus

    # Component statuses
    components: List[ComponentHealth] = Field(default_factory=list)

    # System metrics
    uptime_seconds: float = Field(0.0, ge=0.0)
    total_requests_last_hour: int = Field(0, ge=0)
    avg_response_time_ms: float = Field(0.0, ge=0.0)
    error_rate: float = Field(0.0, ge=0.0, le=1.0)

    # Resource usage
    cpu_usage_percent: Optional[float] = Field(None, ge=0.0, le=100.0)
    memory_usage_percent: Optional[float] = Field(None, ge=0.0, le=100.0)
    disk_usage_percent: Optional[float] = Field(None, ge=0.0, le=100.0)

    # Database
    db_connection_pool_usage: Optional[float] = Field(None, ge=0.0, le=1.0)
    db_query_avg_ms: Optional[float] = None

    # Active issues
    active_alerts: int = Field(0, ge=0)
    degraded_components: int = Field(0, ge=0)

    # Timestamp
    checked_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Request/Response Models
# ============================================================================


class GetDashboardMetricsRequest(BaseModel):
    """Request to get dashboard metrics"""

    tenant_id: str
    project_id: str
    period: MetricPeriod = MetricPeriod.LAST_24H
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class GetDashboardMetricsResponse(BaseModel):
    """Response with dashboard metrics"""

    system_metrics: SystemMetrics
    time_series_metrics: List[TimeSeriesMetric] = Field(default_factory=list)
    recent_activity: List[ActivityLog] = Field(default_factory=list)
    message: str = "Dashboard metrics retrieved successfully"


class GetVisualizationRequest(BaseModel):
    """Request to get visualization data"""

    tenant_id: str
    project_id: str
    visualization_type: VisualizationType

    # Type-specific parameters
    root_reflection_id: Optional[UUID] = None  # For reflection tree
    max_depth: int = Field(5, ge=1, le=10)
    limit: int = Field(100, ge=10, le=1000)

    # Time range
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class GetVisualizationResponse(BaseModel):
    """Response with visualization data"""

    visualization_type: VisualizationType

    # Polymorphic data - one of these will be populated
    reflection_tree: Optional[ReflectionTreeNode] = None
    semantic_graph: Optional[SemanticGraph] = None
    memory_timeline: Optional[MemoryTimeline] = None
    quality_trend: Optional[QualityTrend] = None
    search_heatmap: Optional[SearchHeatmap] = None
    cluster_map: Optional[ClusterMap] = None

    # Metadata
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    cache_valid_until: Optional[datetime] = None
    message: str = "Visualization data generated successfully"


class GetSystemHealthRequest(BaseModel):
    """Request to get system health"""

    tenant_id: str
    project_id: str
    include_sub_components: bool = True


class GetSystemHealthResponse(BaseModel):
    """Response with system health"""

    system_health: SystemHealth
    recommendations: List[str] = Field(default_factory=list)
    message: str = "System health retrieved successfully"


class SubscribeWebSocketRequest(BaseModel):
    """Request to subscribe to WebSocket events"""

    tenant_id: str
    project_id: str

    # Event filters
    event_types: List[DashboardEventType] = Field(
        default_factory=lambda: list(DashboardEventType)
    )

    # Update frequency
    metrics_update_interval_seconds: int = Field(5, ge=1, le=60)


class WebSocketSubscription(BaseModel):
    """WebSocket subscription confirmation"""

    subscription_id: UUID = Field(default_factory=lambda: __import__("uuid").uuid4())
    tenant_id: str
    project_id: str

    subscribed_events: List[DashboardEventType]
    update_interval_seconds: int

    connected_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
