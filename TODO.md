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
*Last scan: 2025-12-09 08:18*

- [ ] **CHANGELOG.md:185** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:186** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:539** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:540** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:891** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:892** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:1238** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:1239** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:1568** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:1569** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:1897** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:1898** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:2225** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:2226** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:2552** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:2553** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:2877** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:2878** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:3200** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:3201** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:3522** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:3523** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:3843** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:3844** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:4164** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:4165** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:4484** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:4485** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:4804** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:4805** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5123** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5124** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5442** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5443** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5760** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5761** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6078** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6079** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6370** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6371** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6661** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6662** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6950** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6951** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:7239** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:7240** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:7527** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:7528** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:7815** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:7816** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8102** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8103** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8389** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8390** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8675** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8676** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8960** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8961** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9243** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9244** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9525** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9526** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9806** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9807** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10087** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10088** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10367** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10368** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10647** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10648** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10926** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10927** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11205** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11206** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11483** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11484** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11761** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11762** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12038** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12039** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12315** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12316** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12591** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12592** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12867** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12868** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13142** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13143** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13417** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13418** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13691** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13692** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13965** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13966** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14238** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14239** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14511** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14512** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14783** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14784** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15055** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15056** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15325** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15326** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15594** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15595** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15863** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15864** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16129** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16130** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16394** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16395** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16658** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16659** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16921** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16922** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17183** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17184** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17445** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17446** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17704** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17705** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17962** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17963** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18218** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18219** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18472** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18473** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18721** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18722** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18965** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18966** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19207** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19208** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19448** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19449** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19688** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19689** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19918** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19919** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:20140** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:20141** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:20361** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:20362** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:20581** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:20582** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:20800** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:20801** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:21018** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:21019** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:21235** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:21236** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:21451** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:21452** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:21666** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:21667** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:21880** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:21881** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:22093** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:22094** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:22305** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:22306** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:22517** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:22518** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:22725** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:22726** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:22932** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:22933** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:23139** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:23140** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:23345** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:23346** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:23550** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:23551** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:23755** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:23756** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:23949** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:23950** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:24136** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:24137** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:24322** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:24323** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:24508** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:24509** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:24692** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:24693** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:24876** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:24877** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25059** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25060** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25241** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25242** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25421** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25422** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25601** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25602** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25778** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25779** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25955** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25956** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26131** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26132** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26307** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26308** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26481** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26482** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26655** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26656** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26823** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26824** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26982** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26983** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27137** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27138** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27286** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27287** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27435** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27436** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27582** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27583** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27728** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27729** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27854** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27855** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27978** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27979** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28089** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28090** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28200** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28201** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28307** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28308** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28413** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28414** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28504** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28505** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28586** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28587** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28658** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28659** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28728** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28729** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28801** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28802** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28876** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28877** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28966** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28967** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:29042** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:29043** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:29117** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:29118** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
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