# RAE API Documentation

Complete API reference for RAE Memory Engine v2.0

**Base URL:** `http://localhost:8000` (default)
**Format:** REST API, JSON
**Authentication:** API Key (Bearer token) or X-Tenant-ID header

---

## Quick Navigation

| Module | Endpoints | Description |
|--------|-----------|-------------|
| [Memories](#memories-api) | 15+ | Core memory CRUD operations |
| [Reflections](#reflections-api) | 8 | Hierarchical reflection generation |
| [Semantic Memory](#semantic-memory-api) | 6 | Knowledge extraction and search |
| [Graph Operations](#graph-api) | 18 | Knowledge graph management |
| [Hybrid Search](#hybrid-search-api) | 10 | Multi-strategy search |
| [Evaluation](#evaluation-api) | 15 | Metrics and drift detection |
| [Event Triggers](#event-triggers-api) | 15 | Automation and rules |
| [Dashboard](#dashboard-api) | 12 | Real-time monitoring |

**Total:** 100+ endpoints

---

## Authentication

All requests require authentication via one of:

### API Key (Recommended)
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     http://localhost:8000/v1/memories
```

### Tenant Header
```bash
curl -H "X-Tenant-ID: your-tenant-id" \
     -H "X-Project-ID: your-project-id" \
     http://localhost:8000/v1/memories
```

---

## Memories API

Base path: `/v1/memories`

### Create Memory
```http
POST /v1/memories
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project": "project-1",
  "content": "User prefers dark mode",
  "importance": 0.8,
  "tags": ["preference", "ui"],
  "metadata": {}
}
```

**Response:**
```json
{
  "id": "uuid",
  "created_at": "2025-11-22T10:00:00Z",
  "message": "Memory created successfully"
}
```

### Search Memories
```http
POST /v1/memories/search
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project": "project-1",
  "query": "user preferences",
  "top_k": 10,
  "filters": {
    "tags": ["preference"]
  }
}
```

### Get Memory by ID
```http
GET /v1/memories/{memory_id}
```

### Update Memory
```http
PUT /v1/memories/{memory_id}
```

### Delete Memory
```http
DELETE /v1/memories/{memory_id}
```

---

## Reflections API

Base path: `/v1/reflections`

### Generate Reflection
```http
POST /v1/reflections/generate
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "memory_ids": ["uuid1", "uuid2"],
  "reflection_type": "insight",
  "created_by": "user-1"
}
```

**Reflection Types:**
- `insight` - Basic reflection from memories
- `analysis` - Deep analytical reflection
- `pattern` - Pattern detection
- `meta` - Meta-insight from other reflections
- `synthesis` - High-level knowledge synthesis

### Generate with Clustering
```http
POST /v1/reflections/generate-clustered
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "min_cluster_size": 3,
  "algorithm": "hdbscan",
  "reflection_type": "pattern"
}
```

### Get Reflection
```http
GET /v1/reflections/{reflection_id}
```

### List Reflections
```http
GET /v1/reflections?tenant_id=X&project_id=Y&limit=100
```

### Get Reflection Hierarchy
```http
GET /v1/reflections/{reflection_id}/hierarchy?max_depth=5
```

### Generate Meta-Insight
```http
POST /v1/reflections/meta-insight
Content-Type: application/json

{
  "reflection_ids": ["uuid1", "uuid2", "uuid3"],
  "tenant_id": "tenant-1",
  "project_id": "project-1"
}
```

---

## Semantic Memory API

Base path: `/v1/semantic`

### Extract Semantic Nodes
```http
POST /v1/semantic/extract
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "memory_id": "uuid"
}
```

**Response:**
```json
{
  "nodes_created": 5,
  "nodes": [
    {
      "label": "machine learning",
      "type": "concept",
      "canonical_form": "machine learning",
      "importance_score": 0.85
    }
  ]
}
```

### Semantic Search (3-Stage)
```http
POST /v1/semantic/search
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "query": "artificial intelligence",
  "k": 10
}
```

**Stages:**
1. Topic Identification → Vector search
2. Term Normalization → Canonicalization
3. Semantic Re-ranking → LLM scoring

### Reinforce Node
```http
POST /v1/semantic/nodes/{node_id}/reinforce
```

### Get Node Details
```http
GET /v1/semantic/nodes/{node_id}
```

### List Semantic Nodes
```http
GET /v1/semantic/nodes?tenant_id=X&project_id=Y&limit=100
```

---

## Graph API

Base path: `/v1/graph`

### Create Node
```http
POST /v1/graph/nodes
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "node_id": "ml-1",
  "label": "Machine Learning",
  "node_type": "concept",
  "properties": {}
}
```

### Create Edge
```http
POST /v1/graph/edges
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "source_node_id": "ml-1",
  "target_node_id": "ai-1",
  "relation_type": "is_part_of",
  "edge_weight": 0.9,
  "confidence": 0.85
}
```

### Traverse Graph
```http
POST /v1/graph/traverse
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "start_node_id": "ml-1",
  "algorithm": "bfs",
  "max_depth": 3
}
```

**Algorithms:**
- `bfs` - Breadth-First Search
- `dfs` - Depth-First Search
- `dijkstra` - Shortest path (weighted)

### Temporal Traversal
```http
POST /v1/graph/traverse/temporal
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "start_node_id": "ml-1",
  "at_timestamp": "2025-11-22T10:00:00Z",
  "max_depth": 3
}
```

### Find Shortest Path
```http
POST /v1/graph/shortest-path
Content-Type: application/json

{
  "source_node_id": "ml-1",
  "target_node_id": "ai-1",
  "algorithm": "dijkstra"
}
```

### Detect Cycles
```http
POST /v1/graph/detect-cycle
Content-Type: application/json

{
  "source_node_id": "ml-1",
  "target_node_id": "ai-1"
}
```

### Create Snapshot
```http
POST /v1/graph/snapshots
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "snapshot_name": "Q4-2025",
  "description": "End of quarter snapshot"
}
```

---

## Hybrid Search API

Base path: `/v1/search`

### Hybrid Multi-Strategy Search
```http
POST /v1/search/hybrid
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "query": "machine learning optimization",
  "k": 20,
  "weight_profile": "quality_focused",
  "enable_strategies": {
    "vector": true,
    "semantic": true,
    "graph": true,
    "fulltext": false
  },
  "enable_reranking": true
}
```

**Weight Profiles:**
- `balanced` - Equal weights (default)
- `quality_focused` - Emphasize semantic + graph
- `speed_focused` - Emphasize vector
- `comprehensive` - All strategies enabled
- `exploratory` - High graph traversal depth

### Analyze Query Intent
```http
POST /v1/search/analyze
Content-Type: application/json

{
  "query": "how does gradient descent work?",
  "context": ["machine learning", "optimization"]
}
```

**Response:**
```json
{
  "intent": "question_how",
  "confidence": 0.92,
  "key_entities": ["gradient descent", "optimization"],
  "recommended_strategies": ["semantic", "graph"],
  "strategy_weights": {
    "vector": 0.3,
    "semantic": 0.4,
    "graph": 0.3
  }
}
```

**Intent Types:**
- `factual_lookup` - Simple fact retrieval
- `conceptual_search` - Understanding concepts
- `question_how` - Process/mechanism questions
- `question_why` - Reasoning/causation
- `comparison` - Comparing concepts
- `exploratory` - Open-ended exploration

### Get Weight Profiles
```http
GET /v1/search/weight-profiles
```

### Set Custom Weights
```http
POST /v1/search/custom-weights
Content-Type: application/json

{
  "vector": 0.4,
  "semantic": 0.3,
  "graph": 0.2,
  "fulltext": 0.1
}
```

---

## Evaluation API

Base path: `/v1/evaluation`

### Evaluate Search Results
```http
POST /v1/evaluation/search
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "relevance_judgments": {
    "query1": {"doc1": 1.0, "doc2": 0.5}
  },
  "search_results": {
    "query1": [
      {"document_id": "doc1", "rank": 1, "score": 0.95}
    ]
  },
  "metrics_to_compute": ["mrr", "ndcg", "precision", "recall"]
}
```

**Metrics:**
- `mrr` - Mean Reciprocal Rank
- `ndcg` - Normalized Discounted Cumulative Gain
- `precision` - Precision@K
- `recall` - Recall@K
- `map` - Mean Average Precision

### Detect Drift
```http
POST /v1/evaluation/drift/detect
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "metric_name": "search_score",
  "drift_type": "data_drift",
  "baseline_start": "2025-10-01T00:00:00Z",
  "baseline_end": "2025-10-31T23:59:59Z",
  "current_start": "2025-11-01T00:00:00Z",
  "current_end": "2025-11-30T23:59:59Z",
  "statistical_test": "ks_test"
}
```

**Drift Types:**
- `data_drift` - Input distribution changed
- `concept_drift` - Input-output relationship changed
- `prediction_drift` - Output distribution changed

**Statistical Tests:**
- `ks_test` - Kolmogorov-Smirnov test
- `psi` - Population Stability Index
- `chi_square` - Chi-square test

### Create A/B Test
```http
POST /v1/evaluation/ab-test/create
Content-Type: application/json

{
  "test_name": "New Search Algorithm",
  "variants": [
    {"name": "control", "traffic_percentage": 50.0},
    {"name": "treatment", "traffic_percentage": 50.0}
  ],
  "metrics": ["mrr", "ndcg"],
  "duration_days": 7
}
```

### Get Quality Metrics
```http
POST /v1/evaluation/quality/metrics
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "period_start": "2025-11-01T00:00:00Z",
  "period_end": "2025-11-30T23:59:59Z"
}
```

---

## Event Triggers API

Base path: `/v1/triggers`

### Create Trigger
```http
POST /v1/triggers/create
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "rule_name": "Auto Reflection on 50 Memories",
  "condition": {
    "event_types": ["memory_created"],
    "condition_group": {
      "operator": "AND",
      "conditions": [
        {
          "field": "payload.memory_count",
          "operator": "greater_equal",
          "value": 50
        }
      ]
    },
    "cooldown_seconds": 3600,
    "max_executions_per_hour": 5
  },
  "actions": [
    {
      "action_type": "generate_reflection",
      "config": {"reflection_type": "synthesis"},
      "retry_on_failure": true,
      "max_retries": 3
    }
  ],
  "priority": 7,
  "created_by": "user-1"
}
```

**Condition Operators (12 total):**
- `equals`, `not_equals`
- `greater_than`, `less_than`, `greater_equal`, `less_equal`
- `contains`, `not_contains`
- `in`, `not_in`
- `matches_regex`
- `is_null`, `is_not_null`

**Action Types (12 total):**
- `send_notification`, `send_email`, `send_webhook`
- `create_memory`, `update_memory`, `delete_memory`
- `generate_reflection`, `extract_semantics`
- `apply_decay`, `reinforce_node`
- `create_snapshot`, `run_evaluation`

### Emit Event
```http
POST /v1/triggers/events/emit
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "event_type": "quality_degraded",
  "payload": {
    "quality_score": 0.65,
    "threshold": 0.70,
    "metric": "mrr"
  },
  "tags": ["quality", "alert"]
}
```

### List Triggers
```http
GET /v1/triggers/list?tenant_id=X&project_id=Y&status_filter=active
```

### Get Trigger Execution History
```http
POST /v1/triggers/executions
Content-Type: application/json

{
  "trigger_id": "uuid",
  "limit": 100,
  "status_filter": "completed"
}
```

### Create Workflow
```http
POST /v1/triggers/workflows/create
Content-Type: application/json

{
  "workflow_name": "Quality Recovery Workflow",
  "steps": [
    {
      "step_id": "step1",
      "step_name": "Run Evaluation",
      "action": {
        "action_type": "run_evaluation",
        "config": {}
      },
      "order": 1
    },
    {
      "step_id": "step2",
      "step_name": "Send Alert",
      "action": {
        "action_type": "send_notification",
        "config": {}
      },
      "depends_on": ["step1"],
      "order": 2
    }
  ],
  "stop_on_failure": true
}
```

### Get Trigger Templates
```http
GET /v1/triggers/templates
```

### Instantiate Template
```http
POST /v1/triggers/templates/{template_id}/instantiate
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "rule_name": "My Auto Reflection",
  "parameters": {
    "memory_threshold": 50
  }
}
```

---

## Dashboard API

Base path: `/v1/dashboard`

### WebSocket Connection
```javascript
const ws = new WebSocket(
  'ws://localhost:8000/v1/dashboard/ws?tenant_id=X&project_id=Y&event_types=memory_created,quality_alert'
);

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Dashboard event:', message);
};
```

**Event Types:**
- `memory_created`, `memory_updated`, `memory_deleted`
- `reflection_generated`, `semantic_node_created`
- `quality_alert`, `drift_detected`
- `trigger_fired`, `action_completed`
- `metrics_updated`, `health_changed`

### Get Dashboard Metrics
```http
POST /v1/dashboard/metrics
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "period": "last_24h"
}
```

**Response:**
```json
{
  "system_metrics": {
    "total_memories": 1000,
    "memories_last_24h": 50,
    "total_reflections": 100,
    "active_triggers": 5,
    "health_status": "healthy"
  },
  "time_series_metrics": [...],
  "recent_activity": [...]
}
```

### Get Visualization Data
```http
POST /v1/dashboard/visualizations
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "visualization_type": "reflection_tree",
  "root_reflection_id": "uuid",
  "max_depth": 5
}
```

**Visualization Types:**
- `reflection_tree` - Hierarchical reflection tree
- `semantic_graph` - Knowledge graph visualization
- `memory_timeline` - Chronological memory events
- `quality_trend` - Quality metrics over time
- `search_heatmap` - Search activity patterns
- `cluster_map` - Memory cluster visualization

### Get System Health
```http
POST /v1/dashboard/health
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project_id": "project-1",
  "include_sub_components": true
}
```

### Get Activity Log
```http
GET /v1/dashboard/activity?tenant_id=X&project_id=Y&limit=100
```

---

## Error Responses

All endpoints follow a consistent error format:

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "2025-11-22T10:00:00Z",
  "request_id": "uuid"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `429` - Too Many Requests (rate limited)
- `500` - Internal Server Error
- `503` - Service Unavailable

---

## Rate Limiting

Default rate limits:
- **Anonymous:** 100 requests/hour
- **Authenticated:** 1000 requests/hour
- **Enterprise:** 10000 requests/hour

Headers returned:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1701000000
```

---

## Pagination

List endpoints support pagination:

```http
GET /v1/memories?limit=50&offset=100
```

Response includes pagination metadata:
```json
{
  "results": [...],
  "total_count": 1000,
  "limit": 50,
  "offset": 100,
  "has_more": true
}
```

---

## Interactive Documentation

**Swagger UI:** http://localhost:8000/docs
**ReDoc:** http://localhost:8000/redoc

---

## SDK Usage

### Python SDK

```python
from rae_memory_sdk import RAEClient

client = RAEClient(
    api_url="http://localhost:8000",
    api_key="your-api-key",
    tenant_id="tenant-1",
    project_id="project-1"
)

# All API methods available
memory = await client.create_memory(
    content="Test memory",
    importance=0.8
)

results = await client.hybrid_search(
    query="machine learning",
    k=10
)
```

See [apps/memory_api/clients/README.md](apps/memory_api/clients/README.md) for full SDK documentation.

---

## Examples

Complete examples in [apps/memory_api/clients/examples.py](apps/memory_api/clients/examples.py)

---

**API Version:** v2.0
**Last Updated:** 2025-11-22
**Endpoints:** 100+
**Status:** Production Ready ✅
