# 🧠 RAE Memory Engine: API Reference V2
> **Version:** 4.16 Silicon Oracle (Neural Polyglot)  
> **Environment:** Enterprise / Mission Critical  
> **Standards:** ISO 27001, ISO 42001 (Auditable AI)

---

## 🚦 System Overview

| Status | Module | Base Path | Function |
| :--- | :--- | :--- | :--- |
| 🟢 **Active** | **[RAE Bridge](#-rae-bridge-api)** | `/v2/bridge` | Intelligent Event Ingestion & Implicit Capture |
| 🟢 **Active** | **[Hybrid Search](#-hybrid-search-api)** | `/v2/search` | Neural Polyglot (Multi-Vector & Multi-Layer) |
| 🟢 **Active** | **[Core Memory](#-core-memory-api)** | `/v2/memories` | Persistent Storage (CRUD) |
| 🟡 **Beta** | **[Reflection](#-reflections-api)** | `/v2/reflections` | Hierarchical Insight Generation |
| 🔵 **Sync** | **[Mesh API](#-mesh-api)** | `/v2/mesh` | Federated Memory Synchronization |

---

## 🔐 Authentication & Headers

RAE requires strict identity enforcement for auditability.

| Header | Required | Description |
| :--- | :--- | :--- |
| `X-Tenant-Id` | **Yes** | UUID of the organization (Default: `0000...0000`) |
| `X-Project-Id` | No* | Project ID. *If missing, Bridge auto-detects it via payload keywords.* |
| `Content-Type` | Yes | `application/json` |

---

## 🌉 RAE Bridge API
`POST /v2/bridge/interact`

The primary entrance for all agentic events. Implements **Implicit Capture** – every interaction is automatically saved to memory.

### ⚡ Quick Interaction
`按钮: Execute` `颜色: #4CAF50`

```bash
curl -X POST http://localhost:8001/v2/bridge/interact \
-H "Content-Type: application/json" \
-d '{
  "payload": {
    "action": "component_modernization",
    "component": "OrderDetails.tsx",
    "details": "Migrated from AngularJS to Next.js 14"
  },
  "source_agent": "qwen-writer",
  "target_agent": "deepseek-auditor"
}'
```

**Intelligence Features:**
- 🔍 **Auto-Project:** Detects `dreamsoft_modernization` based on "modernization" keyword.
- 🏷️ **Human Label:** Automatically generates *"Component Modernization (qwen-writer -> deepseek-auditor)"*.

---

## 🔍 Hybrid Search API
`POST /v2/search/hybrid`

Powered by **System 96.0 (Neural Polyglot)**. Concurrent exploration of multiple vector spaces and reflection layers.

### 🌐 Cross-Layer Query
`按钮: Search` `颜色: #2196F3`

```bash
curl -X POST http://localhost:8001/v2/search/hybrid \
-H "Content-Type: application/json" \
-d '{
  "query": "How did we handle AngularJS migrations?",
  "limit": 5,
  "tenant_id": "00000000-0000-0000-0000-000000000000"
}'
```

**Polyglot Features:**
- ⚡ **Concurrency:** Simultaneously queries `episodic`, `semantic`, and `reflective` layers.
- 📐 **Dimensional Independence:** Supports OpenAI (1536d), Nomic (768d), and MiniLM (384d) without data loss.
- 🧮 **RRF Fusion:** Uses Exponential Rank Sharpening to find the best consensus across all models.

---

## 🛡️ Enterprise Guard (Programmatic API)
`rae_core.utils.enterprise_guard`

For Python-based systems requiring **ISO 27001 Compliance**.

### 📦 Usage Example
Use the `@audited_operation` decorator to wrap any critical function. RAE will handle the rest.

```python
from rae_core.utils.enterprise_guard import audited_operation

@audited_operation(operation_name="database_migration", impact_level="high")
async def run_migration():
    # Your complex logic here...
    return "Success"
```

**Automatic Capture:**
- ⏱️ `duration_s`: Measured automatically.
- 💾 `mem_delta_mb`: RAM usage tracked.
- 📈 `impact`: Categorized for the Dashboard.
- 🕵️ `traceability`: Linked to `human_label`.

---

## 📊 Dashboard & Monitoring
`GET /v2/dashboard/metrics`

Real-time health and performance metrics for the entire RAE cluster.

### 📈 Fetch Stats
`按钮: Get Metrics` `颜色: #FF9800`

```bash
curl -X GET "http://localhost:8001/v2/dashboard/metrics?period=last_24h" \
-H "X-Tenant-Id: 00000000-0000-0000-0000-000000000000"
```

---

## 📂 Core Memory (CRUD)
Standard operations for manual memory management.

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/v2/memories/` | List all memories for tenant |
| `GET` | `/v2/memories/{id}` | Get specific memory details |
| `DELETE`| `/v2/memories/{id}` | Permanently remove memory (requires auth) |
| `POST` | `/v2/memories/` | Manual memory store (use Bridge instead for A2A) |

---

## 🔌 Ecosystem & Integrations

RAE is designed to be the central memory core for any AI framework.

### 🦜 LangChain & LlamaIndex
Seamlessly plug RAE into your existing agent pipelines.
- **LangChain:** `integrations/langchain/rae_langchain_retriever.py`
- **LlamaIndex:** `integrations/llama_index/rae_llamaindex_store.py`

### 🤖 Model Context Protocol (MCP)
The native language of modern AI agents.
- **Claude/Cline/Cursor:** Use the server in `integrations/mcp/`.
- **Gemini:** Specialized support in `integrations/gemini-mcp/`.

### 🛠️ Official SDKs
- **Python SDK:** Standard client with `@audited_operation` support.
- **Secure SDK:** Advanced encryption and data classification layers.

### 📊 Visualization Tools
Access your cognitive data through specialized dashboards:
- **Timeline & Graph:** Comprehensive Streamlit app in `tools/memory-dashboard/`.
- **Lightweight UI:** NiceGUI implementation in `tools/memory-dashboard-nicegui/`.

---
*© 2026 RAE Project - Silicon Oracle Documentation. Audited by RAE-Feniks.*
