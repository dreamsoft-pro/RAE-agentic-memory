# RAE Agentic Memory Engine - TODO List

**Ostatnia aktualizacja:** 2025-11-24
**Status projektu:** Production Ready ✅

Ten plik zawiera uporządkowaną listę zadań do wykonania, pogrupowanych według priorytetów.

---

## 🔥 Priorytet WYSOKI (Critical)

### 1. ✅ ~~Repository Pattern - Direct SQL Elimination~~ DONE
**Status:** ✅ Completed (2025-11-23)
- ✅ Extended GraphRepository with 8 new methods
- ✅ Refactored EntityResolutionService
- ✅ Refactored ReflectionEngine
- ✅ Refactored CommunityDetectionService
- ✅ Created 29 tests (27 passing - 93%)
- ✅ Updated documentation

**Rezultat:** 100% eliminacja direct SQL z service layer

---

### 2. Test Coverage - Increase to 80%+
**Status:** ⚠️ In Progress (Currently: 60%)
**Priority:** HIGH
**Estimated Effort:** 2-3 weeks

**Areas Needing Coverage:**

#### A. API Routes/Endpoints (~25% → Target: 75%+)
- [ ] Memory API routes (`api/v1/memory.py`)
  - [ ] `/v1/memory/store` - POST
  - [ ] `/v1/memory/query` - POST
  - [ ] `/v1/memory/delete` - DELETE
  - [ ] Reflection endpoints
- [ ] Graph API routes (`api/v1/graph.py`)
  - [ ] `/v1/graph/extract` - POST
  - [ ] `/v1/graph/query` - POST
  - [ ] `/v1/graph/stats` - GET
  - [ ] `/v1/graph/nodes` - GET
- [ ] Agent API routes (`api/v1/agent.py`)
  - [ ] `/v1/agent/execute` - POST
- [ ] Governance API routes (`api/v1/governance.py`)
  - [ ] `/v1/governance/overview` - GET
  - [ ] `/v1/governance/tenant/{id}` - GET

#### B. Service Layer (~70% → Target: 90%+)
- [ ] HybridSearchService error scenarios
- [ ] CostController edge cases
- [ ] DriftDetector statistical tests
- [ ] AnalyticsService aggregations

#### C. Repository Layer (~75% → Target: 85%+)
- [ ] GraphRepository error handling
- [ ] MemoryRepository expansion
- [ ] Transaction rollback scenarios

**Action Items:**
```bash
# 1. Generate coverage report
pytest --cov=apps/memory_api --cov-report=html --cov-report=term apps/memory_api/tests/

# 2. Identify gaps
open htmlcov/index.html

# 3. Write missing tests (priority order)
# - API routes (highest impact)
# - Service error paths
# - Repository edge cases
```

---

### 3. Memory Decay - Complete Implementation
**Status:** ⚠️ Partial
**Priority:** HIGH
**Estimated Effort:** 1 week

**Problem:**
- `last_accessed_at` and `usage_count` columns exist in DB
- `_update_memory_access_stats()` exists but has `pass` (not implemented)
- Only importance-based decay is working

**Tasks:**
- [ ] **Implement `_update_memory_access_stats` in `agent.py`**
  ```python
  async def _update_memory_access_stats(self, memory_ids: List[UUID]):
      """Update last_accessed_at and increment usage_count"""
      # Batch update for performance
      await self.memory_repo.update_access_stats(
          memory_ids=memory_ids,
          timestamp=datetime.utcnow()
      )
  ```

- [ ] **Add repository method in `MemoryRepository`**
  ```python
  async def update_access_stats(self, memory_ids: List[UUID], timestamp: datetime):
      """Batch update access statistics"""
      # SQL: UPDATE memories SET
      #      last_accessed_at = $1,
      #      usage_count = usage_count + 1
      #      WHERE id = ANY($2)
  ```

- [ ] **Wire updates in all read paths**
  - Agent API execution
  - Direct memory query endpoints
  - Hybrid search retrieval

- [ ] **Optional: Integrate with ImportanceScoringService**
  ```python
  def calculate_decay(importance, last_accessed_at, usage_count):
      time_decay = calculate_time_decay(last_accessed_at)
      usage_boost = min(1.0, usage_count / 100)
      return importance * time_decay * (1 + usage_boost * 0.2)
  ```

- [ ] **Update documentation**
  - `docs/configuration.md` - Add `MEMORY_DECAY_RATE` explanation
  - `docs/concepts/architecture.md` - Add "Memory Lifecycle" section
  - `API_DOCUMENTATION.md` - Note about automatic decay

**Files to modify:**
- `apps/memory_api/api/v1/agent.py`
- `apps/memory_api/repositories/memory_repository.py`
- `apps/memory_api/services/importance_scoring.py`
- `docs/configuration.md`
- `docs/concepts/architecture.md`

---

## ⚠️ Priorytet ŚREDNI (Medium)

### 4. API Documentation vs Real Endpoints Alignment
**Status:** ⚠️ Needs Review
**Priority:** MEDIUM
**Estimated Effort:** 1 week

**Problem:**
- `API_DOCUMENTATION.md` describes more APIs than exist
- Some base paths inconsistent (e.g., `/v1/memories` vs `/v1/memory`)
- Agent, Cache, Governance APIs not in "Quick Navigation"

**Tasks:**

#### A. Synchronize "Quick Navigation" with real routers
- [ ] Parse `apps/memory_api/main.py` for all routers
- [ ] Update `API_DOCUMENTATION.md` navigation:
  - [ ] Add **Agent API** (`/v1/agent/*`)
  - [ ] Add **Cache API** (`/v1/cache/*`)
  - [ ] Add **Governance API** (`/v1/governance/*`)
  - [ ] Update **Graph API** (align with GraphRAG)
  - [ ] Add **Health API** (`/health`, `/health/ready`, `/metrics`)

#### B. Decide canonical base path for Memory API
- [ ] **Option A (recommended):** Keep `/v1/memory` as canonical
  - Update all docs to match
- [ ] **Option B:** Add alias `/v1/memories` in code
  - Mark one as preferred in docs

#### C. Update Memory API endpoints to match reality
- [ ] List all endpoints from `apps/memory_api/api/v1/memory.py`
- [ ] Replace outdated endpoint list in `API_DOCUMENTATION.md`
- [ ] Mark missing endpoints (GET /{id}, PUT /{id}) as:
  - "Removed" or "Planned but not implemented"

#### D. Document Agent, Cache, Governance APIs
- [ ] **Agent API:**
  - Document `POST /v1/agent/execute`
  - Inputs, outputs, cost breakdown
- [ ] **Cache API:**
  - Document `POST /v1/cache/rebuild`
- [ ] **Governance API:**
  - Document `/v1/governance/overview`
  - Document `/v1/governance/tenant/{id}`
  - Document `/v1/governance/tenant/{id}/budget`

#### E. Expand Health API documentation
- [ ] Document all health endpoints
- [ ] Explain Kubernetes liveness/readiness probes
- [ ] Explain Prometheus scraping

**Files:**
- `API_DOCUMENTATION.md`
- `apps/memory_api/main.py`
- `apps/memory_api/api/v1/*`

---

### 5. Python SDK - Full Implementation
**Status:** ⚠️ Partial (Basic CRUD only)
**Priority:** MEDIUM
**Estimated Effort:** 1 week

**Problem:**
- SDK provides only `store`, `query`, `delete`
- Stub methods: `evaluate`, `reflect`, `get_tags`
- Docs show methods that don't exist: `hybrid_search`, `extract_knowledge_graph`, etc.

**Tasks:**

#### A. Unify naming and exported classes
- [ ] Decide canonical class name: `RAEClient` and `AsyncRAEClient`
- [ ] Update `client.py` accordingly
- [ ] Ensure `__init__.py` exports canonical names

#### B. Implement or deprecate stub methods
- [ ] **Option A (preferred):** Implement real endpoints
  - `evaluate()` → Call evaluation API
  - `reflect()` → Call reflection API
  - `get_tags()` → Call tags API
- [ ] **Option B:** Mark as `NotImplementedError` with clear docstring

#### C. Add GraphRAG-related methods
- [ ] `extract_knowledge_graph()` → `POST /v1/graph/extract`
- [ ] `query_with_graph()` → `POST /v1/graph/query`
- [ ] `get_graph_stats()` → `GET /v1/graph/stats`
- [ ] `get_graph_nodes()` → `GET /v1/graph/nodes`
- [ ] `get_graph_edges()` → `GET /v1/graph/edges`
- [ ] `get_subgraph()` → `GET /v1/graph/subgraph`

#### D. Add Agent & Governance helpers
- [ ] `execute_agent_task()` → `POST /v1/agent/execute`
- [ ] `get_governance_overview()` → `GET /v1/governance/overview`
- [ ] `get_tenant_governance()` → `GET /v1/governance/tenant/{id}`
- [ ] `get_tenant_budget()` → `GET /v1/governance/tenant/{id}/budget`

#### E. Update SDK README
- [ ] Expand with installation instructions
- [ ] Add basic usage examples (store/query/delete)
- [ ] Add GraphRAG usage examples
- [ ] Add Agent usage examples
- [ ] Add Governance examples

#### F. Align documentation with real SDK
- [ ] Search `docs/` for SDK code snippets
- [ ] Update all examples to match real methods

**Files:**
- `sdk/python/rae_memory_sdk/client.py`
- `sdk/python/rae_memory_sdk/__init__.py`
- `sdk/python/rae_memory_sdk/README.md`
- `docs/graphrag_guide.md`
- `API_DOCUMENTATION.md`

---

### 6. Configuration Documentation
**Status:** ⚠️ Partial
**Priority:** MEDIUM
**Estimated Effort:** 3 days

**Problem:**
- `docs/configuration.md` describes subset of configuration
- Uses outdated patterns (separate `REDIS_HOST`, `REDIS_PORT`)
- ml_service and reranker-service configuration not documented

**Tasks:**

#### A. Generate full configuration table for memory_api
- [ ] Parse `apps/memory_api/config.py`
- [ ] Create table with: Name, Type, Default, Description
- [ ] Replace existing section in `docs/configuration.md`

#### B. Document configuration for ml_service
- [ ] Inspect `apps/ml_service/main.py`
- [ ] Identify env-dependent values
- [ ] Add "ML Service Configuration" subsection

#### C. Document configuration for reranker-service
- [ ] Inspect `apps/reranker-service/main.py`
- [ ] Extract hardcoded model name
- [ ] **Optional:** Refactor to read from env (`RERANKER_MODEL_NAME`)
- [ ] Add "Reranker Service Configuration" subsection

#### D. Unify Redis & Celery configuration docs
- [ ] Document `REDIS_URL`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`
- [ ] Remove outdated `REDIS_HOST`, `REDIS_PORT`, `REDIS_DB` recommendations

#### E. Highlight security & rate limiting settings
- [ ] Add "Security & Rate Limiting" subsection
- [ ] Document: `API_KEY`, `ENABLE_API_KEY_AUTH`, `ENABLE_JWT_AUTH`, `SECRET_KEY`
- [ ] Document: `ENABLE_RATE_LIMITING`, `RATE_LIMIT_REQUESTS`, `RATE_LIMIT_WINDOW`

#### F. Document decay & logging
- [ ] Add bullets for `MEMORY_DECAY_RATE`
- [ ] Document logging levels (`LOG_LEVEL`, `RAE_APP_LOG_LEVEL`)

**Files:**
- `docs/configuration.md`
- `apps/memory_api/config.py`
- `apps/ml_service/main.py`
- `apps/reranker-service/main.py`

---

### 7. OpenTelemetry - Distributed Tracing
**Status:** ⚠️ Partial (Basic tracing only)
**Priority:** MEDIUM
**Estimated Effort:** 1-2 weeks

**Current State:**
- Basic OpenTelemetry setup exists
- Celery tracing NOT implemented
- ML service tracing NOT implemented

**Tasks:**
- [ ] **Celery Worker Tracing**
  ```python
  from opentelemetry.instrumentation.celery import CeleryInstrumentor
  CeleryInstrumentor().instrument()
  ```

- [ ] **ML Service Tracing**
  - Add OTEL instrumentation to `apps/ml_service/main.py`
  - Trace embedding generation
  - Trace model inference

- [ ] **Jaeger Exporter**
  ```python
  from opentelemetry.exporter.jaeger.thrift import JaegerExporter
  jaeger_exporter = JaegerExporter(
      agent_host_name="jaeger",
      agent_port=6831,
  )
  ```

- [ ] **DB Query Spans**
  ```python
  from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
  AsyncPGInstrumentor().instrument()
  ```

- [ ] **Update docker-compose.yml**
  - Add Jaeger service
  ```yaml
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"  # Jaeger UI
      - "6831:6831/udp"  # Jaeger agent
  ```

- [ ] **Update documentation**
  - Add "Distributed Tracing" section to monitoring docs

**Files:**
- `apps/memory_api/observability.py`
- `apps/ml_service/main.py`
- `apps/memory_api/background_tasks.py`
- `docker-compose.yml`
- `docs/concepts/monitoring.md`

---

### 8. Rate Limiting - Per-Tenant Dynamic Limits
**Status:** ⚠️ Basic implementation only
**Priority:** MEDIUM
**Estimated Effort:** 1 week

**Current State:**
- Basic rate limiting exists
- No per-tenant configuration
- No sliding window
- No dashboard metrics

**Tasks:**
- [ ] **Per-tenant limits configuration**
  ```python
  # Store in Redis or PostgreSQL
  tenant_limits = {
      "tenant1": {"requests": 1000, "window": 60},
      "tenant2": {"requests": 5000, "window": 60},
  }
  ```

- [ ] **Sliding window algorithm**
  ```python
  from redis import Redis
  async def check_rate_limit(tenant_id: str) -> bool:
      key = f"rate_limit:{tenant_id}:{window_start}"
      count = await redis.incr(key)
      await redis.expire(key, window_size)
      return count <= limit
  ```

- [ ] **Dashboard metrics**
  - Add rate limit metrics to Prometheus
  - Add Grafana dashboard panel

- [ ] **Admin API for rate limit management**
  ```python
  @router.put("/admin/rate-limits/{tenant_id}")
  async def update_rate_limit(tenant_id: str, limits: RateLimitConfig):
      # Update tenant-specific limits
  ```

**Files:**
- `apps/memory_api/middleware/rate_limiter.py`
- `apps/memory_api/api/v1/admin.py` (new)
- `docs/concepts/rate-limiting.md` (new)

---

## 📊 Priorytet NISKI (Low)

### 9. GraphRAG Documentation Alignment
**Status:** ⚠️ Needs minor updates
**Priority:** LOW
**Estimated Effort:** 2 days

**Tasks:**
- [ ] Rewrite "Graph API" section in `API_DOCUMENTATION.md` around GraphRAG
  - Replace old CRUD-style endpoints
  - Document actual GraphRAG endpoints
- [ ] Clarify relationship between `/v1/memory/query` and GraphRAG
  - Explain `use_graph`, `graph_depth`, `max_graph_hops` options
- [ ] Mark old CRUD Graph API as deprecated/never implemented
- [ ] Cross-link docs
  - `API_DOCUMENTATION.md` → `docs/graphrag_guide.md`
  - `docs/graphrag_guide.md` → `API_DOCUMENTATION.md`

**Files:**
- `API_DOCUMENTATION.md`
- `docs/graphrag_guide.md`

---

### 10. Architecture Documentation - Services Mapping
**Status:** ⚠️ Partial
**Priority:** LOW
**Estimated Effort:** 2 days

**Tasks:**
- [ ] Add "Deployed Services" table
  - Service Name, Container, Role, Dependencies
  - memory-api, ml-service, reranker, workers, etc.
- [ ] Clarify ml-service vs reranker-service deployment
  - Document which is used in dev vs production
- [ ] Map logical components to services
  - LLMService, VectorStore, ContextCache → physical services
- [ ] Describe observability stack concretely
  - Prometheus scraping, redis-exporter, Grafana dashboards
- [ ] Describe async processing & workers
  - Celery worker, Celery beat, scheduled jobs

**Files:**
- `docs/concepts/architecture.md`
- `docker-compose.yml`
- `infra/docker-compose.yml`

---

### 11. Cleanup - Duplications & Dead Code
**Status:** ⚠️ Minor issues
**Priority:** LOW
**Estimated Effort:** 1 day

**Tasks:**
- [ ] **Choose canonical home for `POST /reflection/hierarchical`**
  - Recommended: Keep under Graph API (`/v1/graph/reflection/hierarchical`)
  - Remove duplicate from `memory.py` OR make it a proxy
  - Update `API_DOCUMENTATION.md` to document only one endpoint

- [ ] **Mark aspirational APIs explicitly**
  - Move unimplemented APIs to "Future / Planned APIs" section
  - Add "Implementation Status" table

- [ ] **Align comments with real behavior**
  - Search for comments about `last_accessed_at` auto-updates
  - Remove/update misleading comments

**Files:**
- `apps/memory_api/api/v1/memory.py`
- `apps/memory_api/api/v1/graph.py`
- `API_DOCUMENTATION.md`

---

### 12. Graph Snapshots - API Endpoints
**Status:** ⚠️ Partial (SQL exists, API missing)
**Priority:** LOW
**Estimated Effort:** 3 days

**Current State:**
- SQL for snapshots exists in repository
- No API endpoints for snapshot create/restore

**Tasks:**
- [ ] **Add snapshot endpoints**
  ```python
  @router.post("/v1/graph/snapshot")
  async def create_graph_snapshot(tenant_id: str, project_id: str):
      # Create snapshot

  @router.get("/v1/graph/snapshots")
  async def list_graph_snapshots(tenant_id: str, project_id: str):
      # List snapshots

  @router.post("/v1/graph/snapshot/{id}/restore")
  async def restore_graph_snapshot(id: UUID):
      # Restore from snapshot
  ```

- [ ] **Add repository methods**
  ```python
  async def create_snapshot(tenant_id, project_id, description) -> UUID:
      # Store snapshot metadata + graph state

  async def restore_snapshot(snapshot_id: UUID):
      # Restore graph from snapshot
  ```

- [ ] **Update documentation**
  - Add "Graph Snapshots" section to GraphRAG guide

**Files:**
- `apps/memory_api/api/v1/graph.py`
- `apps/memory_api/repositories/graph_repository.py`
- `docs/graphrag_guide.md`

---

## ❌ Nie Planowane (Out of Scope)

Te funkcje są poza obecnym scope projektu i są planowane na przyszłe wersje:

### v2.1
- [ ] MCP API Client Integration
- [ ] Advanced Retry Logic (Circuit Breaker improvements)

### v2.2
- [ ] Advanced Action Orchestration (Complex workflow dependencies)
- [ ] LLM-based Action Orchestration

### v2.3
- [ ] Query Suggestions (ML-based)
- [ ] Semantic Memory TTL/LTM Decay (Advanced model)

### v3.0
- [ ] Real-time Collaboration (Multi-user features)
- [ ] Advanced Dashboard (Real-time updates, complex visualizations)

---

## 📋 Acceptance Criteria

Projekt można uznać za "complete" gdy:

### Critical (Must Have)
- [x] ~~Repository Pattern implemented (100% eliminacja direct SQL)~~
- [ ] Test Coverage ≥ 80%
- [ ] Memory Decay fully implemented (`last_accessed_at`, `usage_count`)

### Important (Should Have)
- [ ] API Documentation aligned with real endpoints
- [ ] Python SDK complete (GraphRAG methods, Agent methods)
- [ ] Configuration fully documented (all services)

### Nice to Have
- [ ] OpenTelemetry - Celery + ML service tracing
- [ ] Rate Limiting - Per-tenant dynamic limits
- [ ] GraphRAG docs alignment
- [ ] Architecture docs - Services mapping
- [ ] Cleanup - Duplications removed

---

## 📊 Progress Tracking

### Overall Progress: ~75% Complete

| Kategoria | Status | Progress |
|-----------|--------|----------|
| **Core Features** | ✅ Complete | 100% |
| **Infrastructure** | ✅ Complete | 100% |
| **Repository Pattern** | ✅ Complete | 100% |
| **Tests** | ⚠️ In Progress | 60% |
| **Documentation** | ⚠️ In Progress | 95% |
| **SDK** | ⚠️ Partial | 40% |
| **Observability** | ⚠️ Partial | 60% |

---

## 🔗 Related Documents

- [Project Status](STATUS.md) - Aktualny stan projektu
- [Testing Guide](TESTING.md) - Status testów i instrukcje
- [Contributing](CONTRIBUTING.md) - Jak kontrybuować
- [Architecture](docs/concepts/architecture.md) - Architektura systemu

---

## 📝 Update History

### 2025-11-24
- ✅ CI Pipeline Fixes - COMPLETED
  - Fixed syntax errors in integrations/mcp-server/main.py
  - Applied black & isort formatting (145+ files)
  - Created root-level Dockerfile
  - Added missing test dependencies
  - Updated CI workflow for ML dependencies
- 📝 Documentation updated (CHANGELOG, STATUS, TODO)

### 2025-11-23
- ✅ Repository Pattern - COMPLETED
- ✅ Reorganized TODO structure by priority
- ✅ Added detailed task breakdowns
- ✅ Updated progress tracking

### 2025-11-22
- ✅ GraphRAG implementation - COMPLETED
- ✅ Hybrid Cache - COMPLETED
- ✅ Kubernetes Helm charts - COMPLETED
- ✅ 220+ pages documentation - COMPLETED

---

**Last Updated:** 2025-11-24
**Maintainer:** RAE Team
