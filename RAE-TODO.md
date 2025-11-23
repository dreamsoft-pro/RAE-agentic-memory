# RAE – CODE vs DOCS ALIGNMENT PLAN (for Claude)

**Goal:**  
Bring the RAE codebase and documentation into sync so that:

- Every implemented API / feature is documented.
- Every documented feature is either implemented or clearly marked as **planned / deprecated**.
- SDK, configuration, and architecture docs match reality.
- Critical half-implemented mechanisms (e.g. memory decay) are finished.

This file is the **source of truth for the “docs vs code” cleanup**.  
Claude: treat checklist items as concrete tasks; update them incrementally via PRs/commits.

---

## 0. High-Level Priorities

**Global order of work (recommended):**

1. **API Documentation vs Real Endpoints** (API_DOCUMENTATION.md vs apps/memory_api/api/v1/\*).
2. **GraphRAG documentation vs Graph API section**.
3. **Memory Decay mechanism (last_accessed_at / usage_count / importance)**.
4. **Python SDK & examples**.
5. **Configuration docs vs config.py & other services**.
6. **Architecture docs vs docker-compose files**.
7. **Clean up duplications & dead/aspirational docs**.

---

## 1. API Endpoints – Align API_DOCUMENTATION.md with apps/memory_api/api/v1/*

### 1.1. Current Situation (Diagnosis)

- `API_DOCUMENTATION.md`:
  - Describes **more APIs** than exist in `memory_api`:
    - Reflections API
    - Semantic Memory API
    - Hybrid Search API
    - Evaluation API
    - Event Triggers API
    - Dashboard API
  - For “Memories API” it documents:
    - Base path: `/v1/memories`
    - Endpoints such as:
      - `GET /v1/memories/{memory_id}`
      - `PUT /v1/memories/{memory_id}`
- Real code in `apps/memory_api/api/v1/`:
  - Present routers: `agent.py`, `cache.py`, `governance.py`, `graph.py`, `health.py`, `memory.py`.
  - Agent / Cache / Governance APIs exist and are significant, but **not listed** in “Quick Navigation”.
  - `memory.py` base path: `/v1/memory` (not `/v1/memories`).
  - Implemented endpoints differ from documentation (e.g. `/store`, `/query`, `/delete`, reflection endpoints).
  - `graph.py` implements GraphRAG-style endpoints (extract, stats, nodes, edges, query, subgraph, reflection/hierarchical) but **Graph API section** in docs still describes CRUD graph operations that don’t exist.

### 1.2. Objectives

- Make `API_DOCUMENTATION.md` accurately reflect **only**:
  - Implemented endpoints.
  - Implemented base paths.
  - Implemented request/response shapes.
- Clearly mark **planned/not implemented** APIs as such, or move them to a “Future Work / Roadmap” section.
- Bring Agent, Cache, Governance APIs into the official navigation.

### 1.3. Concrete Tasks for Claude

**Files involved:**

- `API_DOCUMENTATION.md`
- `apps/memory_api/main.py`
- `apps/memory_api/api/v1/memory.py`
- `apps/memory_api/api/v1/graph.py`
- `apps/memory_api/api/v1/agent.py`
- `apps/memory_api/api/v1/cache.py`
- `apps/memory_api/api/v1/governance.py`
- `apps/memory_api/api/v1/health.py`

**Checklist:**

- [ ] **Synchronize “Quick Navigation” with real routers**
  - Parse imports and routers in `apps/memory_api/main.py`.
  - In `API_DOCUMENTATION.md`, in the top-level “Quick Navigation”:
    - Add sections for:
      - **Agent API** (`/v1/agent/...`)
      - **Cache API** (`/v1/cache/...`)
      - **Governance API** (`/v1/governance/...`)
      - **Graph API** (aligned with GraphRAG, see section 2)
      - **Health API** (with `/health`, `/health/ready`, `/health/live`, `/metrics`)
    - Ensure existing “Memory API” section refers to `/v1/memory` (or decide to rename the route; see below).

- [ ] **Decide & enforce canonical base path for “Memory API”**
  - Current code: `/v1/memory`.
  - Docs: `/v1/memories`.
  - **Choose one canonical option**:
    - Option A (recommended, low-risk): keep **`/v1/memory`** as canonical, update all docs to match.
    - Option B: introduce alias `/v1/memories` in code (with same handlers) and keep `/v1/memory` as internal/legacy. Document both and mark one as preferred.
  - Update `API_DOCUMENTATION.md` accordingly (all paths, examples, curl snippets).

- [ ] **Update “Memories API” to match actual endpoints**
  - Inspect `apps/memory_api/api/v1/memory.py` and list **all** endpoints:
    - `POST /v1/memory/...` (store, query, delete, etc.)
    - Reflection-related endpoints: `rebuild-reflections`, `reflection-stats`, `reflection/hierarchical` (see duplication with `graph.py` in section 7).
  - In `API_DOCUMENTATION.md`:
    - Replace outdated endpoint list with accurate one.
    - Mark **missing endpoints** (e.g. `GET /{memory_id}`, `PUT /{memory_id}`) as:
      - **Removed** (if we don’t want them).
      - Or move them to a “Planned but not implemented” section with an explicit note.

- [ ] **Document Agent, Cache, Governance APIs**
  - For `apps/memory_api/api/v1/agent.py`:
    - Document `POST /v1/agent/execute` in detail:
      - Inputs: tenant_id, task, context, retrieval parameters, cost config, etc.
      - Outputs: LLM result, selected memories, reflection info, cost breakdown (if present).
      - Explain that this is a **central orchestrating endpoint** for agentic workflows.
  - For `apps/memory_api/api/v1/cache.py`:
    - Document `POST /v1/cache/rebuild`:
      - What is rebuilt (context cache).
      - When it should be used (e.g. after bulk imports, migrations, etc.).
  - For `apps/memory_api/api/v1/governance.py`:
    - Document:
      - `GET /v1/governance/overview`
      - `GET /v1/governance/tenant/{tenant_id}`
      - `GET /v1/governance/tenant/{tenant_id}/budget`
    - Describe returned fields (costs, budget, trend metrics).

- [ ] **Expand Health API documentation**
  - In `API_DOCUMENTATION.md`:
    - Under “Health”:
      - Explicitly document:
        - `GET /health`
        - `GET /health/ready`
        - `GET /health/live`
        - `GET /metrics`
      - Explain which endpoints are for:
        - Kubernetes liveness/readiness probes.
        - Prometheus scraping.

- [ ] **Handle “Reflections, Semantic, Hybrid, Evaluation, Event Triggers, Dashboard” sections**
  - In `API_DOCUMENTATION.md`:
    - Identify sections that describe **APIs not present** in `apps/memory_api/api/v1`.
    - For each:
      - If it’s implemented in another service: clearly note **which service** and file implement it (path or “not yet part of this repo”).
      - If not implemented anywhere: move to “Future APIs / Roadmap” with explicit tag: **NOT IMPLEMENTED YET**.
    - Make sure readers cannot confuse planned APIs with actually working endpoints.

---

## 2. GraphRAG vs Graph API Section

### 2.1. Current Situation

- `docs/graphrag_guide.md` + `CHANGELOG_GRAPHRAG.md`:
  - Very detailed and **accurately** describe:
    - Graph extraction.
    - Hybrid search (memory + graph).
    - Graph stats, nodes (with PageRank), edges.
    - Subgraph extraction (BFS, depth limits).
    - `reflection/hierarchical` endpoint under `/v1/graph`.
  - Match real code in `apps/memory_api/api/v1/graph.py` and parts of `memory.py`.
- `API_DOCUMENTATION.md` “Graph API”:
  - Describes **CRUD graph API** (Create Node, Create Edge, Traverse, Shortest Path, etc.).
  - Those endpoints are **not implemented** in `graph.py`.

### 2.2. Objectives

- Make the “Graph API” section in `API_DOCUMENTATION.md` reflect **GraphRAG**, not an old CRUD API.
- Keep `docs/graphrag_guide.md` as the advanced deep-dive, but ensure top-level API docs are consistent.

### 2.3. Tasks for Claude

**Files:**

- `API_DOCUMENTATION.md`
- `docs/graphrag_guide.md`
- `CHANGELOG_GRAPHRAG.md`
- `apps/memory_api/api/v1/graph.py`
- `apps/memory_api/api/v1/memory.py` (for hybrid search / graph options)

**Checklist:**

- [ ] **Rewrite “Graph API” section in API_DOCUMENTATION.md around GraphRAG**
  - Replace old CRUD-style endpoints with:
    - `POST /v1/graph/extract`
    - `POST /v1/graph/query`
    - `POST /v1/graph/reflection/hierarchical`
    - `GET  /v1/graph/stats`
    - `GET  /v1/graph/nodes`
    - `GET  /v1/graph/edges`
    - `GET  /v1/graph/subgraph`
  - For each endpoint, document:
    - Request fields (use actual Pydantic models from `graph.py`).
    - Response fields (nodes, edges, scores, metadata).
    - Example request/response (can be short).

- [ ] **Clarify relationship between `/v1/memory/query` and GraphRAG**
  - In the “Memories API” section:
    - Explain options `use_graph`, `graph_depth`, `max_graph_hops`, etc. (whatever is really implemented).
    - Show minimal example of hybrid query using GraphRAG.

- [ ] **Mark old CRUD Graph API as deprecated/never implemented**
  - Add a small “Deprecated / Not Implemented” subsection:
    - List old conceptual endpoints.
    - State explicitly that the “low-level graph CRUD API” was **never implemented** in `memory_api` and has been replaced by GraphRAG.

- [ ] **Cross-link docs**
  - At top of “Graph API” section in `API_DOCUMENTATION.md`, add a note:
    - “For a full conceptual guide see `docs/graphrag_guide.md`.”
  - Ensure `docs/graphrag_guide.md` references `API_DOCUMENTATION.md` as the “official API reference”.

---

## 3. Memory Decay – last_accessed_at, usage_count, importance

### 3.1. Current Situation

- DB & models:
  - `last_accessed_at`, `usage_count`, `importance` columns exist.
- Implementation:
  - `ImportanceScoringService` is **fully implemented** and used in many places.
  - `last_accessed_at` / `usage_count`:
    - `_update_memory_access_stats` in `apps/memory_api/api/v1/agent.py` exists but has **`pass`**.
    - Comments in other places (e.g. old reflections routes) mention automatic updates that are not active.
  - Result: **time-based decay is not working**, only importance-based logic is active.

### 3.2. Objectives

- Finish implementation of `last_accessed_at` / `usage_count` updates on read paths.
- Optionally integrate both temporal and importance-based decay into a coherent model.
- Make docs honest: explain what actually decays and how.

### 3.3. Tasks for Claude

**Files:**

- `apps/memory_api/api/v1/agent.py`
- `apps/memory_api/repositories/memory_repository.py` (or equivalent DB access layer)
- `apps/memory_api/services/importance_scoring.py`
- `docs/configuration.md`
- `docs/architecture.md`
- `API_DOCUMENTATION.md` (short note)

**Checklist:**

- [ ] **Implement `_update_memory_access_stats`**
  - Locate DB repository method that retrieves memories (used in agent execution).
  - Implement logic in `_update_memory_access_stats` to:
    - Increment `usage_count` for accessed memory IDs.
    - Set `last_accessed_at = now()` in UTC.
  - Make the implementation **batch-friendly** (bulk update) to avoid N DB round-trips.

- [ ] **Wire `_update_memory_access_stats` in all relevant read flows**
  - Confirm where it is currently called (agent’s retrieval flow).
  - If other core read paths bypass Agent API (e.g. via direct memory endpoints), ensure they also call a common helper or service that updates stats.

- [ ] **Optional: integrate temporal decay with ImportanceScoringService**
  - In `services/importance_scoring.py`:
    - Review `decay_importance` / `auto_archive_low_importance`.
    - Optionally incorporate `last_accessed_at` and `usage_count` into the decay formula:
      - Example: more aggressive decay for items not accessed in a long time.
  - Ensure any scheduled tasks (Celery beat) that call decay functions are aware of new logic.

- [ ] **Document decay behaviour**
  - In `docs/configuration.md`:
    - Document `MEMORY_DECAY_RATE` and any other decay-related settings.
    - Explain how `last_accessed_at`, `usage_count`, and `importance` interact.
  - In `docs/architecture.md`:
    - Add a small subsection under “Memory Lifecycle / Governance”.
  - In `API_DOCUMENTATION.md`:
    - Add a short note in “Memories API” describing the existence of decay (no deep algorithmic details, just behavior).

---

## 4. Python SDK – sdk/python/rae_memory_sdk vs docs

### 4.1. Current Situation

- SDK implementation (`sdk/python/rae_memory_sdk/client.py`):
  - Provides:
    - `store` / `store_async`
    - `query` / `query_async`
    - `delete` / `delete_async`
  - Provides **stub** methods:
    - `evaluate`
    - `reflect`
    - `get_tags`
  - Class name: `MemoryClient` (not `RAEClient`).
- SDK docs:
  - `sdk/python/rae_memory_sdk/README.md` – very basic, mentions `AsyncRAEClient`.
  - `API_DOCUMENTATION.md` and `docs/graphrag_guide.md` show **richer SDK usage**, e.g.:
    - `client.hybrid_search(...)`
    - `client.extract_knowledge_graph(...)`
    - `client.query_with_graph(...)`
  - These methods **do not exist** in SDK.

### 4.2. Objectives

- Provide a **coherent, usable SDK** that matches examples.
- Or: simplify docs so examples match the minimal SDK (but this would reduce UX; better to upgrade SDK).

### 4.3. Tasks for Claude

**Files:**

- `sdk/python/rae_memory_sdk/client.py`
- `sdk/python/rae_memory_sdk/README.md`
- `docs/graphrag_guide.md`
- `API_DOCUMENTATION.md`

**Checklist:**

- [ ] **Unify naming and exported classes**
  - Decide canonical class name:
    - Recommended: `RAEClient` (sync) and `AsyncRAEClient` (async), or:
    - Single `RAEClient` with both sync and async methods clearly documented.
  - Update `client.py` accordingly:
    - Create `RAEClient` as a thin wrapper around existing `MemoryClient` or rename.
  - Ensure `__init__.py` exports the canonical class names used in docs.

- [ ] **Fully implement existing stub methods OR clearly deprecate them**
  - For `evaluate`, `reflect`, `get_tags`:
    - Option A (preferred): implement real calls to corresponding endpoints in `memory.py` (or other appropriate routers).
    - Option B: if endpoints are not stable, mark methods as:
      - `DeprecatedWarning` or `NotImplementedError` with clear docstring, and remove them from README.

- [ ] **Add GraphRAG-related methods to SDK**
  - Expose wrappers for:
    - `extract_knowledge_graph` → `POST /v1/graph/extract`
    - `query_with_graph` (or similar) → `POST /v1/graph/query`
    - `get_graph_stats` → `GET /v1/graph/stats`
    - `get_graph_nodes` → `GET /v1/graph/nodes`
    - `get_graph_edges` → `GET /v1/graph/edges`
    - `get_subgraph` → `GET /v1/graph/subgraph`
  - Ensure method signatures mirror the Pydantic models and typical usage from `docs/graphrag_guide.md`.

- [ ] **Add Agent & Governance helpers (optional but desirable)**
  - SDK helpers for:
    - `execute_agent_task(...)` → `POST /v1/agent/execute`
    - `get_governance_overview()`
    - `get_tenant_governance(tenant_id)`
    - `get_tenant_budget(tenant_id)`

- [ ] **Update SDK README**
  - Expand `sdk/python/rae_memory_sdk/README.md` to cover:
    - Installation.
    - Basic usage (store/query/delete).
    - GraphRAG usage (extract/query).
    - Agent usage.
    - Short governance example.
  - Ensure all cited methods actually exist in `client.py`.

- [ ] **Align other docs with real SDK**
  - Search `docs/` and `API_DOCUMENTATION.md` for SDK code snippets.
  - Update all examples to match:
    - Class names and method names.
    - Parameters and return shapes.

---

## 5. Configuration – docs/configuration.md vs real config

### 5.1. Current Situation

- `docs/configuration.md`:
  - Describes a **subset** of configuration, mainly for `memory_api`.
  - Uses some outdated patterns (e.g. separate `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB`).
- Real code:
  - `apps/memory_api/config.py`:
    - Many more settings:
      - `RERANKER_API_URL`, `MEMORY_API_URL`
      - `REDIS_URL`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`
      - `LLM_MODEL`, `EXTRACTION_MODEL`, `SYNTHESIS_MODEL`
      - `API_KEY`, `ENABLE_API_KEY_AUTH`, `ENABLE_JWT_AUTH`, `SECRET_KEY`
      - `ENABLE_RATE_LIMITING`, `RATE_LIMIT_REQUESTS`, `RATE_LIMIT_WINDOW`
      - `MEMORY_DECAY_RATE`
      - `LOG_LEVEL`, `RAE_APP_LOG_LEVEL`
  - `apps/ml_service/main.py`:
    - Configuration via env or defaults, docs ignore it.
  - `apps/reranker-service/main.py`:
    - Model is **hardcoded**.

### 5.2. Objectives

- Make `docs/configuration.md` a single, **complete reference** for all services.
- Remove outdated patterns and reflect real configuration keys and defaults.
- Highlight security-relevant options.

### 5.3. Tasks for Claude

**Files:**

- `docs/configuration.md`
- `apps/memory_api/config.py`
- `apps/ml_service/main.py`
- `apps/reranker-service/main.py`
- (optionally) any `.env.example`

**Checklist:**

- [ ] **Generate a full configuration table for memory_api**
  - Parse `apps/memory_api/config.py`:
    - For each `Settings` field:
      - Name (env var).
      - Type.
      - Default.
      - Short description.
  - Replace or expand the existing `docs/configuration.md` memory_api section with this table.

- [ ] **Document configuration for ml_service**
  - Inspect `apps/ml_service/main.py`:
    - Identify env-dependent values (e.g. model name, external URLs).
  - Add a dedicated subsection “ML Service Configuration” to `docs/configuration.md`:
    - List relevant env vars, defaults, and purpose.

- [ ] **Document configuration for reranker-service**
  - Inspect `apps/reranker-service/main.py`:
    - Extract the hardcoded model name and any potential env usage.
  - Add subsection “Reranker Service Configuration”:
    - Document current hardcoded model.
    - If possible, **refactor** reranker to read model name from env (e.g. `RERANKER_MODEL_NAME`), then document it.

- [ ] **Unify Redis & Celery configuration docs**
  - In `docs/configuration.md`:
    - Stop recommending `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB` if the code uses `REDIS_URL`.
    - Document:
      - `REDIS_URL`
      - `CELERY_BROKER_URL`
      - `CELERY_RESULT_BACKEND`

- [ ] **Highlight security & rate limiting settings**
  - Add dedicated subsection “Security & Rate Limiting”:
    - `API_KEY`, `ENABLE_API_KEY_AUTH`
    - `ENABLE_JWT_AUTH`, `SECRET_KEY`
    - `ENABLE_RATE_LIMITING`, `RATE_LIMIT_REQUESTS`, `RATE_LIMIT_WINDOW`
  - Explain recommended production defaults (do **not** put secrets in docs; describe behavior only).

- [ ] **Document decay & logging**
  - Add short bullets for:
    - `MEMORY_DECAY_RATE`
    - Logging levels (`LOG_LEVEL`, `RAE_APP_LOG_LEVEL`).

---

## 6. Architecture – docs/architecture.md vs docker-compose.yml

### 6.1. Current Situation

- `docs/architecture.md`:
  - Describes **logical components**:
    - LLMService, VectorStore, ContextCache, BudgetService, CostController, ReflectionEngine.
  - Mentions observability in general and a Grafana dashboard.
  - Does **not** fully enumerate microservices or workers.
- docker configs:
  - `docker-compose.yml`:
    - `rae-api` (memory_api)
    - `ml-service`
    - `postgres`, `redis`, `qdrant`
    - `celery-worker`, `celery-beat`
    - `rae-dashboard`
  - `infra/docker-compose.yml`:
    - `memory-api`, `memory-api-worker`
    - `postgres`, `redis`, `qdrant`
    - `reranker`
    - `prometheus`, `grafana`, `redis-exporter`

### 6.2. Objectives

- Make `docs/architecture.md` clearly describe:
  - **Physical services** (containers/microservices).
  - **Logical components** mapped to those services.
  - Observability stack.
- Clarify the role and deployment status of `ml-service` and `reranker`.

### 6.3. Tasks for Claude

**Files:**

- `docs/architecture.md`
- `docker-compose.yml`
- `infra/docker-compose.yml`

**Checklist:**

- [ ] **Add a “Deployed Services” table**
  - In `docs/architecture.md`, add a section “Services & Containers” with a table:
    - Columns: Service Name, Container, Role, Critical Dependencies.
    - Rows at minimum:
      - `memory-api` / `rae-api`
      - `ml-service` (if still part of deployment strategy)
      - `reranker`
      - `memory-api-worker` or `celery-worker`/`celery-beat`
      - `rae-dashboard`
      - `postgres`, `redis`, `qdrant`
      - `prometheus`, `grafana`, `redis-exporter`
  - Indicate where `docker-compose.yml` vs `infra/docker-compose.yml` are used (local dev vs infra).

- [ ] **Clarify ml-service vs reranker-service deployment**
  - Based on docker files:
    - Document whether **both** are used, or only one in production profile.
  - In `docs/architecture.md`, add a note under the relevant section:
    - If `ml-service` is used only in dev: mark that explicitly.
    - If `reranker` is the canonical production reranker: say so.

- [ ] **Map logical components to services**
  - For each conceptual component:
    - LLMService
    - VectorStore
    - ContextCache
    - BudgetService & CostController
    - ReflectionEngine
  - Add a small table or bullet list mapping:
    - “Implemented in: `apps/memory_api/...` (and dependent services: ml-service, reranker, qdrant, etc.)”.

- [ ] **Describe observability stack concretely**
  - Expand “Observability” section to explicitly mention:
    - `prometheus` scraping `/metrics` from memory-api.
    - `redis-exporter`.
    - `grafana` with preconfigured dashboards (if present).
  - Include a short high-level diagram description (textual is enough) describing data flow for metrics.

- [ ] **Describe async processing & workers**
  - Add subsection “Asynchronous Tasks & Scheduling”:
    - Explain role of `celery-worker` / `memory-api-worker`.
    - Mention Celery beat / scheduled jobs (decay, cache rebuild, reflection, etc. if applicable).

---

## 7. Cleanup – Duplications, Aspirational Docs, Dead Code

### 7.1. Current Situation

- Duplicate endpoint: `POST /reflection/hierarchical` in both `memory.py` and `graph.py`.
- Several API sections in `API_DOCUMENTATION.md` describe features not implemented in `memory_api`.
- Some comments elsewhere mention behaviors (e.g. auto increment `usage_count`) that are not active.

### 7.2. Objectives

- Remove or consolidate duplicate endpoints.
- Make it impossible for a reader to think an unimplemented feature is available.
- Keep aspirational ideas, but in **clearly separated sections**.

### 7.3. Tasks for Claude

**Files:**

- `apps/memory_api/api/v1/memory.py`
- `apps/memory_api/api/v1/graph.py`
- `API_DOCUMENTATION.md`
- Any other routes mentioning features not present in `main.py`

**Checklist:**

- [ ] **Choose canonical home for `POST /reflection/hierarchical`**
  - Recommended: keep it under **Graph API** (`/v1/graph/reflection/hierarchical`) because it is tightly coupled to GraphRAG.
  - Steps:
    - If `memory.py` has a duplicate implementation:
      - Remove it **or** make it a thin proxy that calls the Graph API internally and mark it as deprecated.
    - Ensure `API_DOCUMENTATION.md` documents **only one** canonical endpoint.

- [ ] **Mark aspirational APIs explicitly**
  - In `API_DOCUMENTATION.md`, for:
    - Reflections API, Semantic Memory API, Hybrid Search API (if separate), Evaluation, Event Triggers, Dashboard (if not implemented):
      - Move them under a “Future / Planned APIs” header.
      - Preface with: “The following APIs are **not yet implemented** in this service. They describe the target design.”
  - Optionally include a short “Implementation Status” table summarizing what exists vs planned.

- [ ] **Align comments and docstrings with real behavior**
  - Search for comments referring to:
    - automatic updates of `last_accessed_at` and `usage_count`.
    - old Graph CRUD or other APIs that do not exist.
  - Update or remove these comments to avoid misleading future contributors.

---

## 8. Acceptance Criteria

The alignment work can be considered “good enough” when:

- [ ] **API_DOCUMENTATION.md**:
  - Lists only endpoints that exist OR clearly labeled planned ones.
  - Paths, payloads, and sample requests for Memory, Graph, Agent, Cache, Governance, and Health APIs reflect actual code.
- [ ] **GraphRAG docs**:
  - `API_DOCUMENTATION.md` + `docs/graphrag_guide.md` are mutually consistent.
- [ ] **Memory Decay**:
  - `last_accessed_at` and `usage_count` are updated on real read paths.
  - `MEMORY_DECAY_RATE` and decay behavior are documented.
- [ ] **Python SDK**:
  - Exported classes and methods match all examples in SDK README and main docs.
  - No stub method is advertised as fully working.
- [ ] **Configuration docs**:
  - `docs/configuration.md` lists all important env vars for memory_api, ml_service, reranker-service.
  - Redis/Celery and security settings are correctly described.
- [ ] **Architecture docs**:
  - `docs/architecture.md` includes a clear list of deployed services (from docker-compose files).
  - Observability stack and workers are documented.
- [ ] **Duplications**:
  - Single canonical location for `reflection/hierarchical`.
  - Aspirational APIs are demarcated as such.

When implementing these changes, keep commits logically grouped by area (API docs, SDK, configuration, architecture, decay), to make review straightforward.
