{
  "name": "agentic-memory-mcp",
  "version": "0.1.0",
  "tools": [
    {
      "name": "memory_query",
      "endpoint": "/v2/memories/query",
      "method": "POST"
    },
    {
      "name": "memory_add",
      "endpoint": "/memory/add",
      "method": "POST"
    },
    {
      "name": "agent_execute",
      "endpoint": "/agent/execute",
      "method": "POST"
    },
    {
      "name": "memory_timeline",
      "endpoint": "/memory/timeline",
      "method": "GET"
    }
  ],
  "auth": {
    "type": "bearer",
    "header": "Authorization"
  },
  "tenancy_header": "X-Tenant-Id"
}