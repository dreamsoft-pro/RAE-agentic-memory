# API Endpoints Reference

**Auto-Generated** from OpenAPI specification

**Last Updated:** 2025-12-06
**API Version:** 2.1.1

## Core Memory Endpoints

### POST /v2/memories/create
Create a new memory entry.

**Request Body:**
```json
{
  "content": "string",
  "layer": "episodic|semantic|ltm|rm",
  "tags": ["string"],
  "metadata": {}
}
```

### POST /v2/memory/query
Query memories with hybrid search.

### POST /v2/memory/reflection
Generate reflection from memories.

## GraphRAG Endpoints

### POST /v2/graph/entities
Extract entities from text.

### GET /v2/graph/traverse
Traverse knowledge graph.

## Enterprise Endpoints

### POST /v2/triggers/create
Create event trigger rule.

### GET /v2/cost/usage
Get cost tracking data.

---

**Note:** Full API documentation will be auto-generated from FastAPI app in future iteration.
See interactive docs at: http://localhost:8000/docs
