# RAE - Agentic Memory API Reference

Complete API reference for the RAE (Reflective Agentic Memory Engine).

## Overview

RAE Memory API provides a comprehensive cognitive memory system for AI agents with:
- **Memory Management**: Store and query memories across different layers
- **Knowledge Graphs**: Build and query GraphRAG knowledge graphs
- **Reflections**: Generate hierarchical insights from memories
- **Automation**: Event-driven triggers and workflows
- **Search**: Multi-strategy hybrid search
- **Analytics**: Quality metrics and drift detection
- **Governance**: Cost tracking and budget management

## Base URL

```
http://localhost:8000
```

## Authentication

All API endpoints (except health checks) require authentication via API key or JWT token.

### API Key Authentication

Include API key in request headers:
```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/v2/v2/memories/query
```

### JWT Authentication

Include JWT token in Authorization header:
```bash
curl -H "Authorization: Bearer your-jwt-token" http://localhost:8000/v2/v2/memories/query
```

## Common Headers

| Header | Required | Description |
|--------|----------|-------------|
| `X-API-Key` | Yes* | API authentication key |
| `Authorization` | Yes* | Bearer token (alternative to API key) |
| `X-Tenant-ID` | Yes | Tenant identifier for multi-tenancy |
| `X-Project-ID` | No | Project identifier within tenant |
| `Content-Type` | Yes | application/json |

*One of X-API-Key or Authorization required

## API Endpoints

### Health & Monitoring

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/health` | Comprehensive health check | No |
| GET | `/health/ready` | Kubernetes readiness probe | No |
| GET | `/health/live` | Kubernetes liveness probe | No |
| GET | `/metrics` | Prometheus metrics | No |

### Memory Operations

Base path: `/v2/memory`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v2/memory/store` | Store new memory |
| POST | `/v2/v2/memories/query` | Query memories with vector search |
| DELETE | `/v2/memory/delete` | Delete memory by ID |
| POST | `/v2/memory/rebuild-reflections` | Trigger reflection rebuild |
| GET | `/v2/memory/reflection-stats` | Get reflection statistics |

### Agent Operations

Base path: `/v2/agent`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v2/agent/execute` | Execute agent task with memory context |

### Cache Operations

Base path: `/v2/cache`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v2/cache/rebuild` | Rebuild context cache |

### Knowledge Graph (GraphRAG)

Base path: `/v2/graph`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v2/graph/extract` | Extract knowledge graph from memories |
| POST | `/v2/graph/reflection/hierarchical` | Generate hierarchical reflection |
| GET | `/v2/graph/stats` | Get graph statistics |
| GET | `/v2/graph/nodes` | Retrieve graph nodes |
| GET | `/v2/graph/edges` | Retrieve graph edges |
| POST | `/v2/graph/query` | Query knowledge graph |
| GET | `/v2/graph/subgraph` | Get subgraph from starting nodes |

### Governance & Cost Tracking

Base path: `/v2/governance`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v2/governance/overview` | System-wide cost overview |
| GET | `/v2/governance/tenant/{tenant_id}` | Tenant governance stats |
| GET | `/v2/governance/tenant/{tenant_id}/budget` | Budget status and projections |

---

## Enterprise Features

### Event Triggers & Automation

Base path: `/v2/triggers`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v2/triggers/create` | Create trigger rule |
| GET | `/v2/triggers/{trigger_id}` | Get trigger by ID |
| PUT | `/v2/triggers/{trigger_id}` | Update trigger |
| DELETE | `/v2/triggers/{trigger_id}` | Delete trigger |
| POST | `/v2/triggers/{trigger_id}/enable` | Enable trigger |
| POST | `/v2/triggers/{trigger_id}/disable` | Disable trigger |
| GET | `/v2/triggers/list` | List all triggers |
| POST | `/v2/triggers/events/emit` | Manually emit event |
| GET | `/v2/triggers/events/types` | Get available event types |
| POST | `/v2/triggers/executions` | Get trigger execution history |
| POST | `/v2/triggers/workflows/create` | Create workflow |
| GET | `/v2/triggers/workflows/{workflow_id}` | Get workflow |
| GET | `/v2/triggers/workflows` | List workflows |
| GET | `/v2/triggers/templates` | Get trigger templates |
| GET | `/v2/triggers/templates/{template_id}` | Get specific template |
| POST | `/v2/triggers/templates/{template_id}/instantiate` | Create trigger from template |
| GET | `/v2/triggers/health` | Triggers service health |
| GET | `/v2/triggers/info` | Triggers service info |

### Reflections

Base path: `/v2/reflections`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v2/reflections/generate` | Generate reflections with clustering |
| POST | `/v2/reflections/query` | Query reflections semantically |
| GET | `/v2/reflections/{reflection_id}` | Get single reflection |
| GET | `/v2/reflections/{reflection_id}/children` | Get child reflections |
| POST | `/v2/reflections/graph` | Get reflection relationship graph |
| POST | `/v2/reflections/relationships` | Create reflection relationship |
| GET | `/v2/reflections/statistics/{tenant_id}/{project}` | Get reflection stats |
| DELETE | `/v2/reflections/batch` | Batch delete reflections |

### Hybrid Search

Base path: `/v2/search`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v2/search/hybrid` | Multi-strategy hybrid search |
| POST | `/v2/search/analyze` | Analyze query intent |
| POST | `/v2/search/analyze/explain` | Explain query analysis |
| GET | `/v2/search/weights/profiles` | Get weight profiles |
| GET | `/v2/search/weights/profiles/{profile_name}` | Get specific profile |
| POST | `/v2/search/weights/calculate` | Calculate weights for query |
| POST | `/v2/search/compare` | Compare search strategies |
| POST | `/v2/search/test/weights` | Test custom weights |
| GET | `/v2/search/health` | Search service health |
| GET | `/v2/search/info` | Search service info |

### Evaluation & Quality Metrics

Base path: `/v2/evaluation`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v2/evaluation/search` | Evaluate search results |
| GET | `/v2/evaluation/metrics/supported` | Get supported metrics |
| POST | `/v2/evaluation/drift/detect` | Detect semantic drift |
| GET | `/v2/evaluation/drift/severity-levels` | Get drift severity levels |
| POST | `/v2/evaluation/ab-test/create` | Create A/B test |
| POST | `/v2/evaluation/ab-test/{test_id}/compare` | Compare A/B variants |
| POST | `/v2/evaluation/quality/metrics` | Get quality metrics |
| GET | `/v2/evaluation/quality/thresholds` | Get quality thresholds |
| POST | `/v2/evaluation/benchmark/run` | Run benchmark suite |
| GET | `/v2/evaluation/benchmark/suites` | List benchmark suites |
| GET | `/v2/evaluation/health` | Evaluation service health |
| GET | `/v2/evaluation/info` | Evaluation service info |

### Dashboard & Real-time Monitoring

Base path: `/v2/dashboard`

| Method | Endpoint | Description |
|--------|----------|-------------|
| WS | `/v2/dashboard/ws` | WebSocket for real-time updates |
| POST | `/v2/dashboard/metrics` | Get dashboard metrics |
| GET | `/v2/dashboard/metrics/timeseries/{metric_name}` | Get metric time series |
| POST | `/v2/dashboard/visualizations` | Get visualization data |
| POST | `/v2/dashboard/health` | Get system health |
| GET | `/v2/dashboard/health/simple` | Simple health check |
| GET | `/v2/dashboard/activity` | Get activity log |
| GET | `/v2/dashboard/info` | Dashboard info |

### Advanced Graph Management

Base path: `/v2/graph-management`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v2/graph-management/nodes` | Create graph node |
| GET | `/v2/graph-management/nodes/{node_id}/metrics` | Get node metrics |
| POST | `/v2/graph-management/nodes/connected` | Find connected nodes |
| POST | `/v2/graph-management/edges` | Create graph edge |
| PUT | `/v2/graph-management/edges/{edge_id}/weight` | Update edge weight |
| POST | `/v2/graph-management/edges/{edge_id}/deactivate` | Deactivate edge |
| POST | `/v2/graph-management/edges/{edge_id}/activate` | Activate edge |
| PUT | `/v2/graph-management/edges/{edge_id}/temporal` | Set temporal validity |
| POST | `/v2/graph-management/traverse` | Traverse graph (BFS/DFS) |
| POST | `/v2/graph-management/path/shortest` | Find shortest path |
| POST | `/v2/graph-management/cycles/detect` | Detect cycles |
| POST | `/v2/graph-management/snapshots` | Create graph snapshot |
| GET | `/v2/graph-management/snapshots/{snapshot_id}` | Get snapshot |
| GET | `/v2/graph-management/snapshots` | List snapshots |
| POST | `/v2/graph-management/snapshots/{snapshot_id}/restore` | Restore snapshot |
| POST | `/v2/graph-management/statistics` | Get graph statistics |
| POST | `/v2/graph-management/nodes/batch` | Batch create nodes |
| POST | `/v2/graph-management/edges/batch` | Batch create edges |
| GET | `/v2/graph-management/health` | Graph service health |

---

## Error Handling

All API calls return errors in a consistent format:

```json
{
  "error": {
    "code": "400",
    "message": "Validation Error",
    "details": {...}
  }
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 202 | Accepted (async operation) |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 429 | Rate Limit Exceeded |
| 500 | Internal Server Error |

## Rate Limiting

Default limits: 100 requests per 60 seconds per tenant.

**Response Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1735603200
```

## Interactive Documentation

RAE API provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Spec**: http://localhost:8000/openapi.json

## SDKs & Integration

- **Python SDK**: See [Python SDK Documentation](python-sdk.md)
- **MCP Server**: See [MCP Server Documentation](mcp-server.md)
- **REST Examples**: See [REST API Examples](rest-api.md)

## Further Reading

- [Architecture Overview](../concepts/architecture.md)
- [Memory Layers](../concepts/FULL_SPEC.md#1-memory-hierarchy)
- [GraphRAG Guide](../concepts/graphrag.md)
- [Cost Controller](../concepts/cost-controller.md)
- [Hybrid Search](../services/HYBRID_SEARCH.md)
- [Rules Engine](../services/RULES_ENGINE.md)
- [Evaluation Service](../services/EVALUATION_SERVICE.md)
