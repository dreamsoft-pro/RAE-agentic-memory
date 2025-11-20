# REST API Reference

Complete API reference for RAE Memory API.

## Base URL
```
http://localhost:8000
```

## Authentication

Include API key in headers:
```bash
curl -H "X-API-Key: your-api-key"
```

Or use Bearer token:
```bash
curl -H "Authorization: Bearer your-token"
```

## Endpoints

### Store Memory

**POST** `/v1/memory/store`

```bash
curl -X POST http://localhost:8000/v1/memory/store \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: demo-tenant" \
  -d '{
    "content": "User prefers dark mode",
    "layer": "episodic",
    "tags": ["preference", "ui"],
    "metadata": {"source": "user_settings"}
  }'
```

**Response:**
```json
{
  "id": "mem_abc123",
  "status": "stored",
  "layer": "episodic",
  "timestamp": "2025-01-20T10:30:00Z"
}
```

### Query Memory

**POST** `/v1/memory/query`

```bash
curl -X POST http://localhost:8000/v1/memory/query \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: demo-tenant" \
  -d '{
    "query": "What are user preferences?",
    "top_k": 10,
    "layers": ["episodic", "semantic"]
  }'
```

**Response:**
```json
{
  "results": [
    {
      "id": "mem_abc123",
      "content": "User prefers dark mode",
      "score": 0.92,
      "layer": "episodic",
      "tags": ["preference", "ui"]
    }
  ],
  "total": 1
}
```

### Hybrid Search (GraphRAG)

**POST** `/v1/memory/hybrid-search`

```bash
curl -X POST http://localhost:8000/v1/memory/hybrid-search \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: demo-tenant" \
  -d '{
    "query": "authentication issues",
    "use_graph": true,
    "graph_depth": 2,
    "top_k": 10
  }'
```

**Response:**
```json
{
  "vector_matches": [...],
  "graph_nodes": [...],
  "graph_edges": [...],
  "synthesized_context": "..."
}
```

### Generate Reflection

**POST** `/v1/agent/reflect`

```bash
curl -X POST http://localhost:8000/v1/agent/reflect \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: demo-tenant" \
  -d '{
    "memory_limit": 50,
    "min_confidence": 0.7
  }'
```

### Health Check

**GET** `/health`

```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "components": {
    "database": {"status": "healthy", "response_time_ms": 5.2},
    "redis": {"status": "healthy", "response_time_ms": 1.3},
    "vector_store": {"status": "healthy", "response_time_ms": 8.7}
  },
  "version": "1.0.0"
}
```

## Request Headers

| Header | Required | Description |
|--------|----------|-------------|
| `X-API-Key` | Yes* | API authentication key |
| `Authorization` | Yes* | Bearer token (alternative to API key) |
| `X-Tenant-ID` | Yes | Tenant identifier |
| `X-Project-ID` | No | Project identifier |
| `Content-Type` | Yes | application/json |

*One of X-API-Key or Authorization required

## Error Responses

```json
{
  "error": {
    "code": "400",
    "message": "Invalid request",
    "details": {...}
  }
}
```

**Status Codes:**
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 429: Rate Limit Exceeded
- 500: Internal Server Error

## Rate Limiting

Default: 100 requests per 60 seconds

**Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1735603200
```

## Interactive Docs

Visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

See [Python SDK](python-sdk.md) for easier API usage.
