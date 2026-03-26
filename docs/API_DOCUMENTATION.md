# RAE API Documentation (v2.0 Silicon Oracle)

Complete API reference for RAE Memory Engine v2.0 Enterprise.

**Base URL:** `http://localhost:8001` (Standard/Dev)
**Format:** REST API, JSON
**Authentication:** X-Tenant-ID header (Mandatory)

---

## Quick Navigation

| Module | Base Path | Endpoints | Description |
|--------|-----------|-----------|-------------|
| [Memory](#memory-api) | `/v2/memories` | 9 | Core memory storage and retrieval |
| [Agent](#agent-api) | `/v2/agent` | 1 | Agent orchestration and execution |
| [Mesh](#mesh-api) | `/v2/mesh` | 5 | Federated memory synchronization |
| [Bridge](#bridge-api) | `/v2/bridge` | 2 | External event ingestion |
| [Compliance](#compliance-api) | `/v2/compliance` | 3 | ISO 42001 governance and approvals |
| [Health](#health-api) | `/health` | 4 | System status and metrics |

---

## Authentication

RAE uses a multi-tenant architecture. Every request **MUST** include the `X-Tenant-Id` header.

```bash
curl -H "X-Tenant-Id: your-tenant-uuid" \
     http://localhost:8001/v2/memories/
```

---

## Memory API

Base path: `/v2/memories`

### Store Memory
```http
POST /v2/memories/
```
Stores a new memory. Automatic PII scrubbing and audit logging applied.

**Payload:**
```json
{
  "content": "Meeting summary...",
  "project": "project-alpha",
  "layer": "episodic",
  "human_label": "Project Kickoff",
  "author": "agent-007",
  "metadata": {"importance": 0.9}
}
```

### Query Memory (Search)
```http
POST /v2/memories/query
```
Performs hybrid semantic search across layers.

**Payload:**
```json
{
  "query": "What was discussed?",
  "project": "project-alpha",
  "layers": ["episodic", "semantic"],
  "top_k": 5
}
```

---

## Mesh API (Federation)

Base path: `/v2/mesh`

### Invite Peer
```http
POST /v2/mesh/invite
```
Generates an invitation for another RAE instance.

### Join Mesh
```http
POST /v2/mesh/join
```
Accepts an invitation and establishes a secure memory bridge.

---

## Bridge API

Base path: `/v2/bridge`

### Interact
```http
POST /v2/bridge/interact
```
Emits events to the RAE event bus for trigger evaluation.

---

## Compliance API

Base path: `/v2/compliance`

### Request Approval
```http
POST /v2/compliance/approvals
```
Submits a high-risk operation for human review.
