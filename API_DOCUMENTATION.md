# RAE API Documentation

Complete API reference for RAE Memory Engine v2.0 Enterprise

**Base URL:** `http://localhost:8000` (default)
**Format:** REST API, JSON
**Authentication:** API Key (Bearer token) or X-Tenant-ID header

---

## Quick Navigation

| Module | Endpoints | Description |
|--------|-----------|-------------|
| [Memory API](#memory-api) | 6 | Core memory storage and retrieval operations |
| [Agent API](#agent-api) | 1 | Agent orchestration and execution |
| [Graph API](#graph-api) | 7 | Knowledge graph operations (GraphRAG) |
| [Cache API](#cache-api) | 1 | Context cache management |
| [Governance API](#governance-api) | 3 | Cost tracking and budget management |
| [Health API](#health-api) | 4 | Health checks and system metrics |

**Total:** 22 enterprise-ready endpoints

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

## Memory API

Base path: `/v1/memory`

The Memory API provides core memory storage, retrieval, and management operations. It supports hybrid search combining vector similarity with knowledge graph traversal.

**Memory Lifecycle & Decay:**

All memory retrievals automatically track access statistics:
- **`last_accessed_at`**: Updated to current UTC timestamp on every retrieval
- **`usage_count`**: Incremented on every retrieval

These statistics power the **importance scoring system**, which calculates dynamic importance based on:
- Recency (when created)
- Access frequency (how often used)
- Graph centrality (knowledge graph position)
- Semantic relevance (similarity to recent queries)
- User ratings, consolidation status, and manual adjustments

**Temporal Decay:**
- Memories decay over time based on access patterns
- Recently accessed memories (< 7 days): Decay slower
- Normal memories (7-30 days): Standard decay rate
- Stale memories (30+ days): Accelerated decay

For configuration and implementation details, see:
- [Configuration Guide](docs/configuration.md#memory-decay--importance-scoring)
- [Architecture Documentation](docs/architecture.md#memory-lifecycle--governance)

---

### Store Memory

Store a new memory record in the system.

```http
POST /v1/memory/store
Content-Type: application/json
X-Tenant-Id: tenant-1

{
  "content": "User prefers dark mode in the application",
  "source": "user_preference",
  "importance": 0.8,
  "layer": "em",
  "tags": ["preference", "ui"],
  "project": "project-1",
  "timestamp": "2025-11-22T10:00:00Z"
}
```

**Memory Layers:**
- `em` - Episodic Memory (events, interactions)
- `sm` - Semantic Memory (facts, knowledge)
- `rm` - Reflective Memory (insights, patterns)

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

### Query Memory

Query memories using vector search or hybrid search with graph traversal (GraphRAG).

**Standard Vector Search:**
```http
POST /v1/memory/query
Content-Type: application/json
X-Tenant-Id: tenant-1

{
  "query_text": "user interface preferences",
  "k": 10,
  "project": "project-1",
  "use_graph": false,
  "filters": {
    "tags": ["preference"]
  }
}
```

**Hybrid Search with GraphRAG:**

When `use_graph: true` is specified, the query endpoint performs **hybrid search** combining vector similarity with knowledge graph traversal. This provides richer, more contextual results by:

1. Performing vector search to find semantically similar memories
2. Mapping results to knowledge graph entities
3. Traversing the graph to discover related entities and relationships
4. Synthesizing comprehensive context from all sources

```http
POST /v1/memory/query
Content-Type: application/json
X-Tenant-Id: tenant-1

{
  "query_text": "machine learning concepts",
  "k": 5,
  "project": "project-1",
  "use_graph": true,
  "graph_depth": 2
}
```

**GraphRAG Parameters:**
- `use_graph` (default: false) - Enable hybrid search with graph traversal
- `graph_depth` (default: 2, max: 5) - Maximum depth for graph traversal
- `project` (required when use_graph=true) - Project identifier for graph context

**Note:** For advanced graph operations (extraction, statistics, subgraph queries), see the [Graph API](#graph-api) section below.

**Response:**
```json
{
  "results": [
    {
      "id": "uuid",
      "score": 0.92,
      "content": "User prefers dark mode",
      "source": "user_preference",
      "importance": 0.8,
      "layer": "em",
      "tags": ["preference", "ui"],
      "timestamp": "2025-11-22T10:00:00Z",
      "last_accessed_at": "2025-11-23T14:30:00Z",
      "usage_count": 5,
      "project": "project-1"
    }
  ],
  "synthesized_context": "Context from graph traversal...",
  "graph_statistics": {
    "nodes_traversed": 15,
    "edges_traversed": 20
  }
}
```

---

### Delete Memory

Delete a memory record by ID.

```http
DELETE /v1/memory/delete?memory_id={memory_id}
X-Tenant-Id: tenant-1
```

**Response:**
```json
{
  "message": "Memory 550e8400-e29b-41d4-a716-446655440000 deleted successfully."
}
```

---

### Rebuild Reflections

Trigger background task to rebuild reflective memories for a project.

```http
POST /v1/memory/rebuild-reflections
Content-Type: application/json

{
  "tenant_id": "tenant-1",
  "project": "project-1"
}
```

**Response (202 Accepted):**
```json
{
  "message": "Reflection rebuild task dispatched for project project-1."
}
```

---

### Get Reflection Statistics

Get statistics about reflective memories in a project.

```http
GET /v1/memory/reflection-stats?project=project-1
X-Tenant-Id: tenant-1
```

**Response:**
```json
{
  "reflective_memory_count": 42,
  "average_strength": 0.75
}
```

---

### Generate Hierarchical Reflection

Generate hierarchical (map-reduce) summarization of episodic memories.

This enterprise endpoint handles large numbers of episodes by recursively summarizing them using a map-reduce pattern, scaling to thousands of episodes without hitting context limits.

```http
POST /v1/memory/reflection/hierarchical?project=project-1&bucket_size=10
X-Tenant-Id: tenant-1
```

**Query Parameters:**
- `project` (required) - Project identifier
- `bucket_size` (optional, default: 10) - Number of episodes per bucket
- `max_episodes` (optional) - Maximum episodes to process

**Response:**
```json
{
  "summary": "Comprehensive hierarchical summary of all episodes...",
  "statistics": {
    "project": "project-1",
    "tenant_id": "tenant-1",
    "episode_count": 150,
    "bucket_size": 10,
    "max_episodes_processed": 150,
    "summary_length": 2500
  }
}
```

---

## Agent API

Base path: `/v1/agent`

The Agent API provides orchestrated AI agent execution with memory retrieval, context caching, reranking, and cost tracking.

### Execute Agent Task

Execute an AI agent task with full memory retrieval and context management.

This enterprise endpoint orchestrates:
1. Retrieval of pre-built semantic & reflective context from cache
2. Vector search for episodic memories
3. Reranking of retrieved memories
4. LLM inference with full context
5. Automatic reflection generation
6. Cost tracking and governance

```http
POST /v1/agent/execute
Content-Type: application/json
X-Tenant-Id: tenant-1

{
  "tenant_id": "tenant-1",
  "project": "project-1",
  "prompt": "What are the user's preferences for the dashboard layout?"
}
```

**Response:**
```json
{
  "answer": "Based on the user's interactions, they prefer a dark mode interface with a minimalist layout...",
  "used_memories": {
    "results": [
      {
        "id": "uuid",
        "score": 0.95,
        "content": "User prefers dark mode",
        "source": "user_preference",
        "importance": 0.8,
        "layer": "em",
        "tags": ["preference", "ui"],
        "timestamp": "2025-11-22T10:00:00Z",
        "last_accessed_at": "2025-11-23T14:30:00Z",
        "usage_count": 5,
        "project": "project-1"
      }
    ]
  },
  "cost": {
    "input_tokens": 1250,
    "output_tokens": 180,
    "total_estimate": 0.0245
  }
}
```

**Features:**
- **Context Caching:** Leverages pre-built semantic and reflective context for cost savings
- **Hybrid Retrieval:** Combines vector search with reranking for optimal results
- **Automatic Reflection:** Stores agent interactions as reflective memories
- **Cost Tracking:** Full token and cost breakdown per request
- **Governance:** Budget enforcement and cost guard middleware

---

## Graph API

Base path: `/v1/graph`

The Graph API provides GraphRAG (Graph-Augmented Retrieval) capabilities for knowledge graph extraction, querying, and analysis. It automatically builds knowledge graphs from episodic memories and enables advanced graph-based retrieval.

**Note:** For full conceptual guide, see `docs/graphrag_guide.md`

### Extract Knowledge Graph

Extract knowledge graph from episodic memories using LLM-powered entity and relationship extraction.

```http
POST /v1/graph/extract
Content-Type: application/json
X-Tenant-Id: tenant-1

{
  "project_id": "project-1",
  "limit": 50,
  "min_confidence": 0.5,
  "auto_store": true
}
```

**Response:**
```json
{
  "triples": [
    {
      "subject": "User",
      "predicate": "prefers",
      "object": "dark mode",
      "confidence": 0.92,
      "source_memory_id": "uuid"
    }
  ],
  "entities": ["User", "dark mode", "interface"],
  "statistics": {
    "memories_processed": 50,
    "triples_extracted": 35,
    "unique_entities": 18
  }
}
```

---

### Generate Hierarchical Reflection

Generate hierarchical (map-reduce) reflection from large episode collections.

```http
POST /v1/graph/reflection/hierarchical
Content-Type: application/json
X-Tenant-Id: tenant-1

{
  "project_id": "project-1",
  "bucket_size": 10,
  "max_episodes": 100
}
```

**Response:**
```json
{
  "project_id": "project-1",
  "summary": "Comprehensive hierarchical summary...",
  "episodes_processed": 100
}
```

---

### Get Graph Statistics

Get comprehensive statistics about the knowledge graph.

```http
GET /v1/graph/stats?project_id=project-1
X-Tenant-Id: tenant-1
```

**Response:**
```json
{
  "project_id": "project-1",
  "tenant_id": "tenant-1",
  "total_nodes": 247,
  "total_edges": 412,
  "unique_relations": ["prefers", "relates_to", "is_part_of", "depends_on"],
  "statistics": {
    "avg_edges_per_node": 1.67,
    "total_relation_types": 4
  }
}
```

---

### Get Graph Nodes

Retrieve graph nodes with optional PageRank filtering for large graphs.

```http
GET /v1/graph/nodes?project_id=project-1&limit=100&use_pagerank=true&min_pagerank_score=0.01
X-Tenant-Id: tenant-1
```

**Query Parameters:**
- `project_id` (required) - Project identifier
- `limit` (default: 100) - Maximum nodes to return
- `use_pagerank` (default: false) - Enable PageRank filtering
- `min_pagerank_score` (default: 0.0) - Minimum PageRank threshold

**Response:**
```json
[
  {
    "id": "uuid",
    "node_id": "entity_123",
    "label": "Machine Learning",
    "properties": {
      "pagerank_score": 0.045,
      "type": "concept"
    },
    "created_at": "2025-11-22T10:00:00Z"
  }
]
```

---

### Get Graph Edges

Retrieve graph edges with optional filtering by relation type.

```http
GET /v1/graph/edges?project_id=project-1&limit=100&relation=prefers
X-Tenant-Id: tenant-1
```

**Query Parameters:**
- `project_id` (required) - Project identifier
- `limit` (default: 100) - Maximum edges to return
- `relation` (optional) - Filter by relation type

**Response:**
```json
[
  {
    "id": "uuid",
    "source_node_id": "uuid1",
    "target_node_id": "uuid2",
    "relation": "prefers",
    "properties": {
      "confidence": 0.92
    },
    "created_at": "2025-11-22T10:00:00Z"
  }
]
```

---

### Query Knowledge Graph

Advanced hybrid search combining vector retrieval with graph traversal.

```http
POST /v1/graph/query
Content-Type: application/json
X-Tenant-Id: tenant-1

{
  "query": "machine learning optimization techniques",
  "project_id": "project-1",
  "top_k_vector": 5,
  "graph_depth": 2,
  "traversal_strategy": "bfs"
}
```

**Traversal Strategies:**
- `bfs` - Breadth-First Search (explores nearby entities first)
- `dfs` - Depth-First Search (explores deep relationships)

**Response:**
```json
{
  "vector_matches": [
    {
      "id": "uuid",
      "score": 0.92,
      "content": "Gradient descent optimization...",
      "layer": "em"
    }
  ],
  "graph_nodes": [
    {
      "id": "uuid",
      "label": "gradient descent"
    }
  ],
  "graph_edges": [
    {
      "source_id": "uuid1",
      "target_id": "uuid2",
      "relation": "optimizes"
    }
  ],
  "synthesized_context": "Based on the retrieved memories and graph traversal...",
  "statistics": {
    "vector_results": 5,
    "nodes_traversed": 15,
    "edges_traversed": 22,
    "traversal_depth_reached": 2
  }
}
```

---

### Get Subgraph

Retrieve a subgraph starting from specific nodes.

```http
GET /v1/graph/subgraph?project_id=project-1&node_ids=uuid1,uuid2&depth=2
X-Tenant-Id: tenant-1
```

**Query Parameters:**
- `project_id` (required) - Project identifier
- `node_ids` (required) - Comma-separated node IDs
- `depth` (default: 1) - Maximum traversal depth

**Response:**
```json
{
  "nodes": [
    {
      "id": "uuid",
      "node_id": "entity_123",
      "label": "Machine Learning",
      "properties": {},
      "created_at": "2025-11-22T10:00:00Z"
    }
  ],
  "edges": [
    {
      "id": "uuid",
      "source_node_id": "uuid1",
      "target_node_id": "uuid2",
      "relation": "relates_to",
      "properties": {},
      "created_at": "2025-11-22T10:00:00Z"
    }
  ],
  "statistics": {
    "start_nodes": 2,
    "depth": 2,
    "nodes_found": 15,
    "edges_found": 22
  }
}
```

---

## Cache API

Base path: `/v1/cache`

The Cache API manages the context cache system, which pre-builds and stores semantic and reflective memory contexts for cost optimization in agent execution.

### Rebuild Context Cache

Trigger a background task to rebuild the entire context cache.

This operation:
- Scans all tenants and projects
- Rebuilds semantic memory contexts
- Rebuilds reflective memory contexts
- Updates Redis cache entries

Use this after:
- Bulk memory imports
- Database migrations
- Major schema changes
- Cache corruption

```http
POST /v1/cache/rebuild
```

**Response (202 Accepted):**
```json
{
  "message": "Cache rebuild task dispatched."
}
```

**Note:** This is an asynchronous operation. The cache will be rebuilt in the background via Celery worker. Monitor logs or use metrics endpoints to track progress.

---

## Governance API

Base path: `/v1/governance`

The Governance API provides enterprise-grade cost tracking, budget management, and usage analytics for multi-tenant deployments.

### Get System Overview

Get system-wide cost overview across all tenants (admin only).

```http
GET /v1/governance/overview?days=30
```

**Query Parameters:**
- `days` (default: 30) - Number of days to analyze

**Response:**
```json
{
  "total_cost_usd": 1247.50,
  "total_calls": 15420,
  "total_tokens": 8925000,
  "unique_tenants": 12,
  "period_start": "2025-10-23T00:00:00Z",
  "period_end": "2025-11-23T00:00:00Z",
  "top_tenants": [
    {
      "tenant_id": "tenant-1",
      "calls": 5240,
      "cost_usd": 425.30,
      "tokens": 2850000
    }
  ],
  "top_models": [
    {
      "model": "claude-3-5-sonnet-20241022",
      "calls": 8920,
      "cost_usd": 892.40,
      "tokens": 5420000
    }
  ]
}
```

---

### Get Tenant Statistics

Get comprehensive governance statistics for a specific tenant.

```http
GET /v1/governance/tenant/{tenant_id}?days=30
```

**Query Parameters:**
- `days` (default: 30) - Number of days to analyze

**Response:**
```json
{
  "tenant_id": "tenant-1",
  "total_cost_usd": 425.30,
  "total_calls": 5240,
  "total_tokens": 2850000,
  "average_cost_per_call": 0.081,
  "cache_hit_rate": 0.35,
  "cache_savings_usd": 148.85,
  "period_start": "2025-10-23T00:00:00Z",
  "period_end": "2025-11-23T00:00:00Z",
  "by_project": [
    {
      "project_id": "project-1",
      "calls": 3200,
      "cost_usd": 258.40,
      "tokens": 1740000
    }
  ],
  "by_model": [
    {
      "model": "claude-3-5-sonnet-20241022",
      "calls": 4100,
      "cost_usd": 328.00,
      "tokens": 2100000
    }
  ],
  "by_operation": [
    {
      "operation": "agent_execute",
      "calls": 4200,
      "cost_usd": 360.50,
      "tokens": 2400000
    }
  ]
}
```

**Key Metrics:**
- **cache_hit_rate:** Percentage of requests using cached context (0.0 - 1.0)
- **cache_savings_usd:** Estimated cost savings from context caching
- **by_project:** Cost breakdown by project
- **by_model:** Usage breakdown by LLM model
- **by_operation:** Cost breakdown by operation type

---

### Get Tenant Budget Status

Get current budget status and projections for a tenant.

```http
GET /v1/governance/tenant/{tenant_id}/budget
```

**Response:**
```json
{
  "tenant_id": "tenant-1",
  "budget_usd_monthly": 500.00,
  "budget_tokens_monthly": 5000000,
  "current_month_cost_usd": 425.30,
  "current_month_tokens": 2850000,
  "budget_used_percent": 85.06,
  "days_remaining": 7,
  "projected_month_end_cost": 512.85,
  "alerts": [
    "Warning: 75% of budget used ($425.30 / $500.00)",
    "Projected to exceed budget: $512.85 estimated by month end"
  ],
  "status": "WARNING"
}
```

**Status Levels:**
- **OK:** Under 75% of budget
- **WARNING:** 75-90% of budget used, or projected to exceed
- **CRITICAL:** 90-100% of budget used
- **EXCEEDED:** Budget limit reached

**Features:**
- Real-time budget monitoring
- Projection based on daily average spend
- Multi-level alert system
- Token and cost budget tracking

---

## Health API

The Health API provides comprehensive health checks for all system components, designed for Kubernetes probes, monitoring systems, and observability.

### Health Check

Comprehensive health check of all system components.

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-23T14:30:00Z",
  "version": "1.0.0",
  "components": {
    "database": {
      "status": "healthy",
      "response_time_ms": 12.5,
      "message": "Database connection successful"
    },
    "redis": {
      "status": "healthy",
      "response_time_ms": 3.2,
      "message": "Redis connection successful",
      "details": {
        "version": "7.0.12",
        "used_memory_mb": 245.8,
        "connected_clients": 5
      }
    },
    "vector_store": {
      "status": "healthy",
      "response_time_ms": 8.7,
      "message": "Vector store connection successful",
      "details": {
        "version": "1.7.0",
        "title": "qdrant"
      }
    }
  }
}
```

**Overall Status:**
- **healthy:** All components working normally
- **degraded:** Some non-critical components have issues
- **unhealthy:** Critical components are failing

---

### Readiness Probe

Kubernetes readiness probe endpoint.

```http
GET /health/ready
```

**Response (200 OK):**
```json
{
  "status": "ready"
}
```

**Use Case:** Kubernetes readiness probes to determine if the service can accept traffic.

---

### Liveness Probe

Kubernetes liveness probe endpoint.

```http
GET /health/live
```

**Response (200 OK):**
```json
{
  "status": "alive",
  "timestamp": "2025-11-23T14:30:00Z"
}
```

**Use Case:** Kubernetes liveness probes to detect if the service needs to be restarted.

---

### System Metrics

Get detailed system metrics for monitoring and observability.

```http
GET /metrics
```

**Response:**
```json
{
  "timestamp": "2025-11-23T14:30:00Z",
  "uptime_seconds": 345620.5,
  "memory_usage_mb": 512.4,
  "database": {},
  "redis": {
    "used_memory_mb": 245.8,
    "connected_clients": 5,
    "total_commands": 1547920
  },
  "vector_store": {}
}
```

**Note:** This endpoint also exposes Prometheus metrics at `/metrics` in Prometheus format for scraping.

---

## Future / Planned APIs

The following APIs are described in this documentation but **NOT YET IMPLEMENTED** in the current release. They represent the target design for future versions.

### Not Currently Available

- **Standalone Reflections API** (`/v1/reflections`) - Reflection generation is currently integrated into Memory API and Graph API
- **Semantic Memory API** (`/v1/semantic`) - Planned for entity extraction and semantic search
- **Standalone Hybrid Search API** (`/v1/search`) - Hybrid search is currently integrated into Memory API query endpoint
- **Evaluation API** (`/v1/evaluation`) - Metrics, drift detection, A/B testing
- **Event Triggers API** (`/v1/triggers`) - Automation, rules, and workflows
- **Dashboard API** (`/v1/dashboard`) - Real-time monitoring and WebSocket events

**Implementation Status:** These APIs are part of the product roadmap and may be added in future releases. For current capabilities, use the implemented endpoints documented above.

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

# Store a memory
memory_id = await client.store(
    content="User prefers dark mode",
    importance=0.8,
    layer="em",
    tags=["preference", "ui"]
)

# Query memories (vector search)
results = await client.query(
    query_text="user preferences",
    k=10
)

# Query with graph traversal (hybrid search)
results = await client.query(
    query_text="machine learning concepts",
    k=5,
    use_graph=True,
    graph_depth=2
)

# Delete a memory
await client.delete(memory_id=memory_id)
```

**Available SDK Methods:**
- `store()` / `store_async()` - Store memories
- `query()` / `query_async()` - Query memories (supports hybrid search)
- `delete()` / `delete_async()` - Delete memories

**Note:** GraphRAG and Agent execution methods are planned for future SDK releases. Currently, use direct API calls for these features.

See [sdk/python/rae_memory_sdk/README.md](sdk/python/rae_memory_sdk/README.md) for full SDK documentation.

---

## Examples

Complete examples in [apps/memory_api/clients/examples.py](apps/memory_api/clients/examples.py)

---

**API Version:** v2.0 Enterprise
**Last Updated:** 2025-11-23
**Implemented Endpoints:** 22
**Status:** Production Ready ✅

---

## Summary of Changes

This documentation now accurately reflects the **implemented** RAE Memory API endpoints:

### ✅ Implemented APIs (22 endpoints)
- **Memory API** (6 endpoints) - `/v1/memory/*`
- **Agent API** (1 endpoint) - `/v1/agent/execute`
- **Graph API** (7 endpoints) - `/v1/graph/*` (GraphRAG)
- **Cache API** (1 endpoint) - `/v1/cache/rebuild`
- **Governance API** (3 endpoints) - `/v1/governance/*`
- **Health API** (4 endpoints) - `/health*`, `/metrics`

### 🔮 Planned APIs (Future Releases)
- Standalone Reflections API
- Semantic Memory API
- Standalone Hybrid Search API
- Evaluation API
- Event Triggers API
- Dashboard API

### 🔧 Enterprise Features
- **GraphRAG** - Knowledge graph extraction and traversal
- **Context Caching** - Cost optimization through cached contexts
- **Governance** - Cost tracking, budget management, usage analytics
- **Agent Orchestration** - Full agent execution pipeline with automatic reflection
- **Health Monitoring** - Kubernetes-ready health probes and metrics

For questions or support, visit: https://github.com/dreamsoft-pro/RAE-agentic-memory
