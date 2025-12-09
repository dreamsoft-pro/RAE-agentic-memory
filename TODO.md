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
*Last scan: 2025-12-09 10:37*

- [ ] **CHANGELOG.md:185** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:186** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:540** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:541** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:892** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:893** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:1239** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:1240** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:1569** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:1570** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:1898** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:1899** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:2226** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:2227** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:2553** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:2554** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:2878** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:2879** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:3201** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:3202** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:3523** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:3524** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:3844** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:3845** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:4165** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:4166** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:4485** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:4486** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:4805** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:4806** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5124** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5125** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5443** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5444** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5761** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5762** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6079** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6080** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6371** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6372** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6662** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6663** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6951** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6952** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:7240** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:7241** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:7528** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:7529** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:7816** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:7817** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8103** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8104** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8390** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8391** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8676** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8677** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8961** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8962** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9244** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9245** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9526** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9527** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9807** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9808** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10088** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10089** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10368** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10369** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10648** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10649** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10927** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10928** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11206** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11207** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11484** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11485** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11762** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11763** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12039** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12040** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12316** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12317** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12592** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12593** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12868** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12869** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13143** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13144** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13418** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13419** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13692** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13693** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13966** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13967** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14239** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14240** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14512** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14513** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14784** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14785** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15056** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15057** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15326** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15327** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15595** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15596** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15864** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15865** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16130** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16131** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16395** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16396** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16659** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16660** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16922** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16923** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17184** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17185** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17446** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17447** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17705** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17706** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17963** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17964** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18219** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18220** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18473** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18474** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18722** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18723** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18966** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18967** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19208** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19209** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19449** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19450** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19689** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19690** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19919** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19920** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:20141** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:20142** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:20362** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:20363** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:20582** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:20583** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:20801** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:20802** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:21019** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:21020** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:21236** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:21237** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:21452** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:21453** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:21667** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:21668** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:21881** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:21882** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:22094** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:22095** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:22306** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:22307** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:22518** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:22519** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:22726** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:22727** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:22933** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:22934** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:23140** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:23141** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:23346** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:23347** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:23551** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:23552** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:23756** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:23757** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:23950** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:23951** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:24137** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:24138** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:24323** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:24324** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:24509** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:24510** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:24693** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:24694** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:24877** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:24878** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25060** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25061** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25242** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25243** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25422** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25423** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25602** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25603** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25779** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25780** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25956** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25957** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26132** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26133** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26308** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26309** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26482** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26483** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26656** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26657** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26824** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26825** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26983** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26984** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27138** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27139** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27287** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27288** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27436** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27437** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27583** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27584** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27729** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27730** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27855** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27856** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27979** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27980** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28090** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28091** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28201** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28202** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28308** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28309** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28414** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28415** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28505** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28506** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28587** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28588** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28659** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28660** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28729** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28730** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28802** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28803** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28877** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28878** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28967** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28968** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:29043** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:29044** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:29118** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:29119** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **INTEGRATION_CHECKLIST.md:51** - - [ ] Did NOT edit `TODO.md` (CI extracts from code comments)
- [ ] **CONTRIBUTING.md:148** - Run the documentation automator to update status and TODOs:
- [ ] **CLAUDE_CODE.md:298** - Edit("TODO.md", ...)
- [ ] **CRITICAL_AGENT_RULES.md:305** - - `TODO.md` - Extracted TODOs/FIXMEs from code
- [ ] **README.md:1403** - - ✅ **[TODO List](TODO.md)** - Upcoming features and improvements
- [ ] **ONBOARDING_GUIDE.md:366** - - ❌ DON'T: Edit `CHANGELOG.md`, `STATUS.md`, `TODO.md`, `docs/.auto-generated/`
- [ ] **ONBOARDING_GUIDE.md:375** - - `TODO.md` - Extracted TODOs/FIXMEs
- [ ] **PROJECT_STRUCTURE.md:375** - 9. **Auto-generated docs** (DON'T EDIT): `CHANGELOG.md`, `STATUS.md`, `TODO.md`, `docs/.auto-generated/`
- [ ] **AI_AGENT_MANIFEST.md:54** - - DON'T EDIT: Auto-generated files (`CHANGELOG.md`, `STATUS.md`, `TODO.md`, `docs/.auto-generated/`)
- [ ] **AI_AGENT_MANIFEST.md:96** - | `TODO.md` | Extracted TODOs/FIXMEs | Push to develop/main | `.github/workflows/ci.yml` |
- [ ] **AI_AGENT_MANIFEST.md:357** - | **Pending Work** | `TODO.md` | Extracted TODOs from code |
- [ ] **STATUS.md:25** - All missing/incomplete functionalities from TODO.md have been successfully implemented:
- [ ] **STATUS.md:305** - - [Technical Debt](TODO.md)
- [ ] **AGENT_QUALITY_SYSTEM.md:275** - - ❌ `TODO.md` - Extracted TODOs/FIXMEs
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
- [ ] **.github/workflows/ci.yml:745** - echo "  - TODO.md tracks code TODOs"
- [ ] **.github/workflows/ci.yml:757** - echo "  - TODO.md (code TODOs)"
- [ ] **.github/workflows/ci.yml:904** - git add CHANGELOG.md TODO.md STATUS.md docs/TESTING_STATUS.md || true
- [ ] **.github/workflows/docs.yml:53** - file_pattern: 'CHANGELOG.md STATUS.md TODO.md docs/TESTING_STATUS.md docs/.auto-generated/**'
- [ ] **rae_core/rae_core/core/graph_operator.py:749** - Use embedding similarity for semantic matching with similarity_threshold
- [ ] **rae_core/rae_core/core/reward.py:276** - Add relevance scoring when available
- [ ] **rae_core/rae_core/core/action_executor.py:248** - Integrate with actual services
- [ ] **rae_core/rae_core/core/action_executor.py:275** - Mock action implementations (TODO: Replace with real integrations)
- [ ] **benchmarking/scripts/generate_math_report.py:179** - Implement detailed comparative analysis
- [ ] **benchmarking/math_metrics/controller/reward.py:161** - level_churn = 0.0   TODO: Calculate from decision history
- [ ] **docs/RAE–Docs-vs-Code.md:396** - 11. Priorytetowa lista TODO (szczególnie pod RAE Lite)
- [ ] **docs/RAE_DOCUMENTATION_OVERHAUL_IMPLEMENTATION_PLAN.md:608** - 3. **Set up tracking** in TODO.md or project management tool
- [ ] **docs/RAE_CORE_REFACTOR_PLAN.md:332** - - **TODO list** w każdej iteracji (TodoWrite!)
- [ ] **docs/CONTRIBUTING_DOCS.md:25** - - **reports/TODO.md** - Extracted TODOs from code
- [ ] **docs/CONTRIBUTING_DOCS.md:300** - file_pattern: 'CHANGELOG.md STATUS.md TODO.md docs/.auto-generated/your-category/your-doc.md'
- [ ] **docs/CONTRIBUTING_DOCS.md:351** - - **TODOs:** Documentation tasks in code
- [ ] **docs/STYLE_GUIDE.md:482** - .md
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
- [ ] **docs/autodoc/autodoc_checker.py:9** - - API endpoint consistency (TODO)
- [ ] **docs/autodoc/autodoc_checker.py:82** - Implement fragment injection
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
- [ ] **docs/testing/AUTO_HEALING_GUIDE.md:617** - Implement cost tracking to database
- [ ] **docs/guides/administracja/INDEX.md:411** - Zobacz [TODO.md](../../../TODO.md) dla pełnej roadmapy.
- [ ] **docs/guides/developers/INDEX.md:350** - See [TODO.md](../../../TODO.md) for complete roadmap.
- [ ] **docs/guides/rae-lite/RAE-lite.md:10** - Sam projekt deklaruje, że 80%+ coverage to wciąż cel, nie stan – w TODO.md jest to nadal HIGH priority.
- [ ] **docs/templates/README.md:209** - - `CHANGELOG.md`, `STATUS.md`, `TODO.md`