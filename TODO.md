# RAE Agentic Memory - Roadmap & Implementation Plan

**Status as of 2025-12-02:** ✅ **ALL MAJOR BACKEND FUNCTIONALITIES COMPLETED**

This document tracks the implementation status of RAE features and defines the roadmap for quality assurance and future extensions.

## Phase 3: Quality & Reliability (Target: 80% Coverage)

**Current Status:** ~52% Coverage (244 tests passing)
**Target:** 80% Coverage (~400+ tests)

### Iteration 1: Foundation Layer (Repositories & Basic Services) 🎯
**Goal:** Increase coverage to ~60% by securing the data access layer and core utilities.

- [x] **`apps/memory_api/repositories/cost_logs_repository.py`** (Current: ~87%)
    - Implement unit tests for `log_cost` and `get_costs` methods.
    - Mock database pool interactions.
- [x] **`apps/memory_api/repositories/trigger_repository.py`** (Current: ~48%)
    - Increase coverage for `create_trigger`, `update_trigger`, `get_active_triggers`.
    - Test edge cases (invalid inputs, DB errors).
- [x] **`apps/memory_api/services/cost_controller.py`** (Current: ~89%)
    - Test budget calculation logic and thresholds.
    - Verify cache checking logic.
- [x] **`apps/memory_api/services/analytics.py`** (Current: ~95%)
    - Test metrics aggregation logic.

### Iteration 2: Core Logic (Complex Services) 🧠
**Goal:** Increase coverage to ~70% by testing the most critical and complex business logic.

- [x] **`apps/memory_api/services/hybrid_search_service.py`** (Current: ~81%) 🚨 **CRITICAL**
    - Test result fusion logic (weighting).
    - Test reranking integration (mock LLM).
    - Test fallback strategies (vector only, graph only).
- [x] **`apps/memory_api/services/graph_extraction.py`** (Current: ~79%)
    - Test triple extraction parsing.
    - Test graph node/edge creation logic.
- [x] **`apps/memory_api/services/reflection_pipeline.py`** (Current: ~63%)
    - Test reflection cycle execution.
    - Verify recursive insight generation.

### Iteration 3: Microservices & Integrations 🔌
**Goal:** Increase coverage to ~75% by covering isolated services.

- [x] **`apps/ml_service/*`** (Current: 0%)
    - Add integration tests for embedding generation (mocking the actual model to save resources).
    - Test entity resolution endpoints.
- [x] **`apps/reranker-service/*`** (Current: 0%)
    - Test rerank endpoint logic.
- [x] **`integrations/mcp`** (Current: ~50% in isolated suite)
    - Ensure MCP tests are fully integrated into the main CI pipeline reporting.

### Iteration 4: Safety Net (Routes & Dashboard) 🛡️
**Goal:** Reach 80% coverage by testing API controllers and frontend backends.

- [ ] **`apps/memory_api/routes/dashboard.py`** (Current: 0%)
    - Test all dashboard endpoints (happy paths and error handling).
    - Verify data formatting for frontend.
- [ ] **`apps/memory_api/routes/graph_enhanced.py`** (Current: 0%)
    - Test advanced graph endpoints.
- [ ] **E2E/Integration Polish**
    - Add missing integration tests for full flows (Store -> Process -> Query).

---

## Completed in v2.2.0-enterprise (2025-12-02) ✅

*   **✅ Token Savings Tracker:**
    - Implemented `TokenSavingsRepository` and `TokenSavingsService`.
    - Added database migration (`token_savings_log`).
    - Integrated with `HybridSearchService` to track cache hits.
    - Added API endpoints for metrics and visualization.
    - **Verification:** Unit tests passed, manual seed confirmed.

*   **✅ Critical Infrastructure Fixes:**
    - Fixed Qdrant initialization (502 errors).
    - Fixed Alembic migration automation (Docker command).
    - Fixed Dockerfile dependencies (`psycopg2-binary`).
    - Fixed Dashboard configuration persistence.

---

## Completed in v2.0.4-enterprise (2025-11-30) ✅

*   **✅ Maintenance Workers:** Summarization, Decay, Dreaming (Implementation & Tests).
*   **✅ Event Triggers:** Database storage, CRUD API, execution logging.
*   **✅ Dashboard Metrics:** Time-series database, optimized queries.
*   **✅ A/B Testing & Benchmarking:** Full database implementation.
*   **✅ CI/CD:** All checks passing.

---

## Remaining (Out of Current Scope)

- **Go SDK**
- **Node.js SDK**
- **Memory Replay Tool**

## Technical Debt (Auto-generated from code)
*Last scan: 2025-12-07 19:28*

- [ ] **CHANGELOG.md:133** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:134** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:411** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:412** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:688** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:689** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:965** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:966** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:1241** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:1242** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:1517** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:1518** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:1792** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:1793** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:2067** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:2068** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:2341** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:2342** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:2615** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:2616** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:2888** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:2889** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:3161** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:3162** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:3433** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:3434** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:3705** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:3706** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:3975** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:3976** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:4244** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:4245** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:4513** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:4514** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:4779** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:4780** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5044** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5045** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5308** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5309** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5571** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5572** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5833** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5834** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6095** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6096** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6354** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6355** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6612** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6613** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6868** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6869** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:7122** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:7123** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:7371** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:7372** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:7615** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:7616** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:7857** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:7858** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8098** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8099** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8338** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8339** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8568** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8569** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8790** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8791** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9011** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9012** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9231** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9232** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9450** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9451** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9668** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9669** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9885** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9886** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10101** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10102** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10316** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10317** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10530** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10531** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10743** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10744** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10955** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10956** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11167** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11168** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11375** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11376** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11582** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11583** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11789** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11790** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11995** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11996** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12200** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12201** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12405** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12406** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12599** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12600** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12786** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12787** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12972** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12973** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13158** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13159** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13342** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13343** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13526** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13527** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13709** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13710** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13891** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13892** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14071** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14072** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14251** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14252** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14428** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14429** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14605** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14606** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14781** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14782** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14957** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14958** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15131** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15132** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15305** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15306** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15473** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15474** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15632** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15633** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15787** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15788** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15936** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15937** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16085** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16086** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16232** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16233** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16378** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16379** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16504** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16505** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16628** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16629** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16739** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16740** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16850** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16851** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16957** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16958** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17063** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17064** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17154** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17155** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17236** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17237** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17308** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17309** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17378** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17379** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17451** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17452** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17526** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17527** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17616** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17617** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17692** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17693** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17767** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17768** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CONTRIBUTING.md:148** - Run the documentation automator to update status and TODOs:
- [ ] **CRITICAL_AGENT_RULES.md:305** - - `TODO.md` - Extracted TODOs/FIXMEs from code
- [ ] **README.md:1115** - - ✅ **[TODO List](TODO.md)** - Upcoming features and improvements
- [ ] **AI_AGENT_MANIFEST.md:89** - | `TODO.md` | Extracted TODOs/FIXMEs | Push to develop/main | `.github/workflows/ci.yml` |
- [ ] **AI_AGENT_MANIFEST.md:350** - | **Pending Work** | `TODO.md` | Extracted TODOs from code |
- [ ] **STATUS.md:25** - All missing/incomplete functionalities from TODO.md have been successfully implemented:
- [ ] **STATUS.md:268** - - [Technical Debt](TODO.md)
- [ ] **apps/memory_api/services/hybrid_search.py:318** - connected_components=1,   TODO: compute from graph
- [ ] **apps/memory_api/services/smart_reranker.py:122** - "recency_seconds": 0,   TODO: calc
- [ ] **apps/memory_api/services/context_builder.py:321** - In production, use vector search to get similarity scores
- [ ] **apps/memory_api/services/context_builder.py:467** - Implement profile retrieval
- [ ] **apps/memory_api/routes/event_triggers.py:170** - tenant_id = "default"   TODO: Get from auth context
- [ ] **apps/memory_api/routes/event_triggers.py:197** - tenant_id = "default"   TODO: Get from auth context
- [ ] **apps/memory_api/routes/event_triggers.py:371** - tenant_id = "default"   TODO: Get from auth context
- [ ] **apps/memory_api/core/graph_operator.py:751** - Use embedding similarity for semantic matching with similarity_threshold
- [ ] **apps/memory_api/core/reward.py:278** - Add relevance scoring when available
- [ ] **apps/memory_api/core/action_executor.py:248** - Integrate with actual services
- [ ] **apps/memory_api/core/action_executor.py:275** - Mock action implementations (TODO: Replace with real integrations)
- [ ] **apps/memory_api/workers/memory_maintenance.py:613** - project_id="default",   TODO: Get actual projects
- [ ] **apps/memory_api/repositories/metrics_repository.py:83** - Implement COPY-based bulk insert for better performance
- [ ] **scripts/validate_docs.py:44** - r"\[TODO:.*?\]",
- [ ] **scripts/validate_docs.py:45** - r"\[FIXME:.*?\]",
- [ ] **scripts/metrics_tracker.py:132** - metrics.record_file("TODO.md", "update_todo")
- [ ] **scripts/docs_automator.py:4** - Generates/Updates CHANGELOG.md, TODO.md, STATUS.md, and TESTING_STATUS.md.
- [ ] **scripts/docs_automator.py:18** - _FILE = "TODO.md"
- [ ] **scripts/docs_automator.py:138** - print(f"Updating {TODO_FILE}...")
- [ ] **scripts/docs_automator.py:139** - current_content = get_file_content(TODO_FILE)
- [ ] **scripts/docs_automator.py:141** - Scan for TODOs in code
- [ ] **scripts/docs_automator.py:149** - if file_path == os.path.join(PROJECT_ROOT, TODO_FILE): continue
- [ ] **scripts/docs_automator.py:154** - if "TODO" in line or "FIXME" in line:
- [ ] **scripts/docs_automator.py:156** - clean_line = re.sub(r"^(TODO|FIXME)[:\s]*", "", clean_line)
- [ ] **scripts/docs_automator.py:165** - "\n".join(todos) if todos else "No TODOs found in code."
- [ ] **scripts/docs_automator.py:167** - Inject into TODO.md
- [ ] **scripts/docs_automator.py:178** - write_file_content(TODO_FILE, new_content)
- [ ] **scripts/docs_automator.py:387** - metrics.record_file(TODO_FILE, "update_todo")
- [ ] **scripts/docs_generators/api_docs.py:24** - Implement FastAPI OpenAPI export
- [ ] **scripts/docs_generators/code_metrics.py:37** - Add radon for cyclomatic complexity
- [ ] **scripts/docs_generators/code_metrics.py:38** - Add lizard for code analysis
- [ ] **.github/workflows/ci.yml:740** - echo "  - TODO.md tracks code TODOs"
- [ ] **.github/workflows/ci.yml:752** - echo "  - TODO.md (code TODOs)"
- [ ] **.github/workflows/ci.yml:899** - git add CHANGELOG.md TODO.md STATUS.md docs/TESTING_STATUS.md || true
- [ ] **.github/workflows/docs.yml:53** - file_pattern: 'CHANGELOG.md STATUS.md TODO.md docs/TESTING_STATUS.md docs/.auto-generated/**'
- [ ] **benchmarking/scripts/generate_math_report.py:179** - Implement detailed comparative analysis
- [ ] **benchmarking/math_metrics/controller/reward.py:161** - level_churn = 0.0   TODO: Calculate from decision history
- [ ] **docs/RAE–Docs-vs-Code.md:396** - 11. Priorytetowa lista TODO (szczególnie pod RAE Lite)
- [ ] **docs/CONTRIBUTING_DOCS.md:25** - - **reports/TODO.md** - Extracted TODOs from code
- [ ] **docs/CONTRIBUTING_DOCS.md:300** - file_pattern: 'CHANGELOG.md STATUS.md TODO.md docs/.auto-generated/your-category/your-doc.md'
- [ ] **docs/CONTRIBUTING_DOCS.md:351** - - **TODOs:** Documentation tasks in code
- [ ] **docs/DOCUMENTATION_EXECUTIVE_SUMMARY.md:50** - | **Reports** | CHANGELOG.md, TODO.md | Every CI run |
- [ ] **docs/Self-Documenting Codebase Blueprint.md:11** - 1. Warstwa Źródłowa: Kod, Komentarze TODO, Historia Gita (Commity).
- [ ] **docs/Self-Documenting Codebase Blueprint.md:13** - 3. Warstwa Prezentacji: Pliki Markdown (STATUS.md, CHANGELOG.md, TODO.md).
- [ ] **docs/Self-Documenting Codebase Blueprint.md:29** - B. Komentarze w Kodzie (TODO)
- [ ] **docs/Self-Documenting Codebase Blueprint.md:31** - Format:  TODO: opis zadania lub  TODO: opis zadania.
- [ ] **docs/Self-Documenting Codebase Blueprint.md:46** - 2. Skaner Długu Technicznego (`TODO.md`):
- [ ] **docs/Self-Documenting Codebase Blueprint.md:48** - * Wyciąga linie zawierające TODO.
- [ ] **docs/Self-Documenting Codebase Blueprint.md:70** - * Transparentność: Klient/Manager widzi postępy (CHANGELOG) i problemy (TODO) w prostych plikach tekstowych.
- [ ] **docs/RAE_MATHEMATICAL_REFACTORING_GUIDE.md:2196** - Add relevance scoring when available
- [ ] **docs/RAE_MATHEMATICAL_REFACTORING_GUIDE.md:3935** - Use embedding similarity for semantic matching
- [ ] **docs/.auto-generated/metrics/DASHBOARD.md:39** - | TODO.md | update_todo | 2025-12-06 11:57:03 |
- [ ] **docs/.auto-generated/reports/CHANGELOG.md:40** - - update project status and TODO list after iteration 2 completion ([`49aff83c8`](../../commit/49aff83c8))
- [ ] **docs/.auto-generated/reports/CHANGELOG.md:41** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a98a`](../../commit/934b3a98a))
- [ ] **docs/.auto-generated/reports/CHANGELOG.md:109** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **docs/.auto-generated/reports/CHANGELOG.md:110** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **docs/.auto-generated/reports/CHANGELOG.md:179** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **docs/.auto-generated/reports/CHANGELOG.md:180** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **docs/.auto-generated/reports/CHANGELOG.md:252** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **docs/.auto-generated/reports/CHANGELOG.md:253** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **docs/.auto-generated/reports/CHANGELOG.md:528** - Added - Missing Functionalities from TODO.md Completed 🎯
- [ ] **docs/.auto-generated/reports/CHANGELOG.md:530** - This release completes the implementation of critical functionalities identified in TODO.md that were either missing or partially implemented.
- [ ] **docs/.auto-generated/reports/CHANGELOG.md:762** - - **TODO.md Items** - Completed 5 major categories of missing/incomplete functionalities:
- [ ] **docs/.auto-generated/reports/CHANGELOG.md:771** - - Updated TODO.md to reflect all completed items with detailed completion notes
- [ ] **docs/.auto-generated/reports/CHANGELOG.md:808** - - Technical debt reduction: 5 major TODO.md categories completed
- [ ] **docs/.auto-generated/reports/CHANGELOG.md:1167** - - Resolved TODO comments with detailed implementation notes
- [ ] **docs/.auto-generated/reports/CHANGELOG.md:1182** - - TODO comments resolved with implementation guidance
- [ ] **docs/.auto-generated/status/STATUS.md:25** - All missing/incomplete functionalities from TODO.md have been successfully implemented:
- [ ] **docs/.auto-generated/status/STATUS.md:187** - - [Technical Debt](TODO.md)
- [ ] **docs/reference/llm/RAE–Multi-Model_LLM-Integration-Guide.md:17** - - ✅ Updated documentation (README.md, STATUS.md, TODO.md)
- [ ] **docs/reference/llm/RAE–Multi-Model_LLM-Integration-Guide.md:232** - 8.1. DeepSeek Provider – TODO
- [ ] **docs/reference/llm/RAE–Multi-Model_LLM-Integration-Guide.md:259** - 8.2. Qwen Provider – TODO
- [ ] **docs/reference/llm/RAE–Multi-Model_LLM-Integration-Guide.md:284** - 8.3. Grok Provider – TODO
- [ ] **docs/reference/deployment/observability.md:510** - Future Enhancements (TODO)
- [ ] **docs/project-design/active/DOCUMENTATION_AUTOMATION_PLAN.md:14** - - **docs_automator.py**: Updates 4 files (CHANGELOG, STATUS, TODO, TESTING_STATUS)
- [ ] **docs/project-design/active/DOCUMENTATION_AUTOMATION_PLAN.md:125** - │   │   └── TODO.md            Extracted TODOs
- [ ] **docs/project-design/active/DOCUMENTATION_AUTOMATION_PLAN.md:183** - | `reports/TODO.md` | On push | Every commit | Code scan (TODO/FIXME) |
- [ ] **docs/project-design/completed/enterprise-roadmap/ENTERPRISE-FIX-STATUS.md:331** - - [ ] Remove TODO comments or implement them
- [ ] **docs/project-design/completed/enterprise-roadmap/ENTERPRISE-FIX-STATUS.md:441** - - [ ] 100% of TODO comments resolved
- [ ] **docs/project-design/completed/enterprise-roadmap/ENTERPRISE-FIX-PLAN.md:100** - 2. Implement TODO comments or remove them
- [ ] **docs/project-design/completed/enterprise-roadmap/ENTERPRISE-FIX-PLAN.md:281** - 2. ✅ Implement or remove TODO comments - COMPLETED
- [ ] **docs/project-design/completed/enterprise-roadmap/ENTERPRISE-FIX-PLAN.md:336** - - ✅ All TODO comments resolved
- [ ] **docs/project-design/completed/rae-4layer-design/RAE-–Reflective_Memory_v1-Implementati.md:108** - **TODO:**
- [ ] **docs/project-design/completed/rae-4layer-design/RAE-–Reflective_Memory_v1-Implementati.md:146** - 
- [ ] **docs/project-design/completed/rae-4layer-design/RAE-–Reflective_Memory_v1-Implementati.md:183** - 
- [ ] **docs/project-design/completed/rae-4layer-design/RAE-–Reflective_Memory_v1-Implementati.md:221** - 
- [ ] **docs/project-design/completed/rae-4layer-design/RAE-–Reflective_Memory_v1-Implementati.md:262** - 
- [ ] **docs/project-design/completed/rae-4layer-design/RAE-–Reflective_Memory_v1-Implementati.md:286** - 
- [ ] **docs/project-design/completed/rae-4layer-design/RAE-–Reflective_Memory_v1-Implementati.md:303** - 
- [ ] **docs/project-design/completed/rae-4layer-design/RAE-–Reflective_Memory_v1-Implementati.md:330** - 
- [ ] **docs/project-design/completed/rae-4layer-design/RAE-–Reflective_Memory_v1-Implementati.md:362** - 
- [ ] **docs/project-design/completed/rae-4layer-design/RAE-–Reflective_Memory_v1-Implementati.md:382** - 
- [ ] **docs/project-design/completed/rae-4layer-design/RAE-–Reflective_Memory_v1-Implementati.md:403** - 
- [ ] **docs/project-design/completed/rae-4layer-design/RAE-–Reflective_Memory_v1-Implementati.md:455** - 
- [ ] **docs/project-design/research/RAE-improve_01.md:13** - Implement JWT token verification
- [ ] **docs/project-design/research/RAE-improve_01.md:16** - Implement proper tenant access control
- [ ] **docs/project-design/research/RAE_Code_vs_Docs_Feature_Gaps.md:9** - > - głównym `README.md`, `STATUS.md`, `TESTING_STATUS.md`, `TODO.md`,
- [ ] **docs/guides/administracja/INDEX.md:411** - Zobacz [TODO.md](../../../TODO.md) dla pełnej roadmapy.
- [ ] **docs/guides/developers/INDEX.md:350** - See [TODO.md](../../../TODO.md) for complete roadmap.
- [ ] **docs/guides/rae-lite/RAE-lite.md:10** - Sam projekt deklaruje, że 80%+ coverage to wciąż cel, nie stan – w TODO.md jest to nadal HIGH priority.
- [ ] **docs/templates/README.md:209** - - `CHANGELOG.md`, `STATUS.md`, `TODO.md`