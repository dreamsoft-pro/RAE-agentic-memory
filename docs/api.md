# RAE - Agentic Memory API v1 Reference

This document provides a reference for the RESTful API of the RAE (Reasonging Agentic-memory Engine).

## Common
All API endpoints are prefixed with `/v1`.
All requests must include the `X-Tenant-Id` header, which identifies the client/tenant.

## Error Format
All API calls that result in an error will return a JSON object with the following structure:
```json
{
  "error": {
    "code": "...",
    "message": "...",
    "details": "..."
  }
}
```

## Memory Endpoints
Endpoints for managing and querying memories.
File: `apps/memory-api/api/v1/memory.py`

### Store Memory
- **Endpoint:** `POST /v1/memory/store`
- **Description:** Stores a new memory record in the database and vector store.
- **Request Body:** `StoreMemoryRequest`
```json
{
  "content": "string (max 8192 chars)",
  "source": "string (optional, max 255 chars)",
  "importance": "float (optional, 0.0 to 1.0)",
  "layer": "string (optional, 'stm', 'ltm', 'rm', 'em')",
  "tags": ["string", "list", "optional"],
  "timestamp": "datetime (optional)",
  "project": "string (optional, max 255 chars)"
}
```
- **Response:** `StoreMemoryResponse`
```json
{
  "id": "string (uuid)",
  "message": "Memory stored successfully."
}
```

### Query Memory
- **Endpoint:** `POST /v1/memory/query`
- **Description:** Queries memories based on a text query.
- **Request Body:** `QueryMemoryRequest`
```json
{
  "query_text": "string (max 1024 chars)",
  "k": "integer (optional, default 10, 1-100)",
  "filters": { "key": "value" }
}
```
- **Response:** `QueryMemoryResponse`
```json
{
  "results": [
    {
      "id": "string (uuid)",
      "content": "string",
      "source": "string",
      "importance": "float",
      "layer": "string",
      "tags": ["string", "list"],
      "timestamp": "datetime",
      "last_accessed_at": "datetime",
      "usage_count": "integer",
      "project": "string",
      "score": "float"
    }
  ]
}
```

### Delete Memory
- **Endpoint:** `DELETE /v1/memory/delete?memory_id=...`
- **Description:** Deletes a memory record.
- **Query Parameter:** `memory_id` (string, required)
- **Response:** `DeleteMemoryResponse`
```json
{
  "message": "Memory <memory_id> deleted successfully."
}
```

## Agent Endpoint
Endpoint for interacting with the agent.
File: `apps/memory-api/api/v1/agent.py`

### Execute Agent Task
- **Endpoint:** `POST /v1/agent/execute`
- **Description:** Executes a task with the agent, which can leverage its memory.
- **Request Body:** `AgentExecuteRequest`
```json
{
  "tenant_id": "string (max 255 chars)",
  "project": "string (max 255 chars)",
  "prompt": "string (max 8192 chars)",
  "tools_allowed": ["string", "list", "optional"],
  "budget_tokens": "integer (optional, default 20000, 1-100000)"
}
```
- **Response:** `AgentExecuteResponse`
```json
{
  "answer": "string",
  "used_memories": { ... },
  "cost": {
    "input_tokens": "integer",
    "output_tokens": "integer",
    "total_estimate": "float"
  }
}
```
