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
*Last scan: 2025-12-07 22:41*

- [ ] **CHANGELOG.md:136** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:137** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:417** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:418** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:697** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:698** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:977** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:978** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:1256** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:1257** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:1535** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:1536** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:1813** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:1814** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:2091** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:2092** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:2368** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:2369** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:2645** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:2646** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:2921** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:2922** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:3197** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:3198** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:3472** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:3473** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:3747** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:3748** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:4021** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:4022** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:4295** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:4296** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:4568** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:4569** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:4841** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:4842** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5113** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5114** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5385** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5386** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5655** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5656** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5924** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5925** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6193** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6194** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6459** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6460** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6724** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6725** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6988** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6989** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:7251** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:7252** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:7513** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:7514** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:7775** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:7776** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8034** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8035** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8292** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8293** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8548** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8549** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8802** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8803** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9051** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9052** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9295** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9296** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9537** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9538** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9778** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9779** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10018** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10019** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10248** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10249** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10470** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10471** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10691** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10692** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10911** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10912** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11130** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11131** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11348** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11349** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11565** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11566** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11781** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11782** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11996** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11997** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12210** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12211** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12423** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12424** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12635** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12636** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12847** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12848** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13055** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13056** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13262** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13263** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13469** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13470** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13675** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13676** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13880** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13881** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14085** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14086** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14279** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14280** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14466** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14467** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14652** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14653** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14838** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14839** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15022** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15023** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15206** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15207** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15389** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15390** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15571** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15572** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15751** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15752** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15931** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15932** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16108** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16109** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16285** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16286** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16461** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16462** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16637** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16638** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16811** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16812** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16985** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16986** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17153** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17154** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17312** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17313** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17467** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17468** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17616** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17617** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17765** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17766** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17912** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17913** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18058** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18059** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18184** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18185** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18308** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18309** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18419** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18420** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18530** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18531** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18637** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18638** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18743** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18744** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18834** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18835** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18916** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18917** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18988** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18989** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19058** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19059** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19131** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19132** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19206** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19207** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19296** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19297** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19372** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19373** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19447** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19448** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CONTRIBUTING.md:148** - Run the documentation automator to update status and TODOs:
- [ ] **CRITICAL_AGENT_RULES.md:305** - - `TODO.md` - Extracted TODOs/FIXMEs from code
- [ ] **README.md:1329** - - ✅ **[TODO List](TODO.md)** - Upcoming features and improvements
- [ ] **AI_AGENT_MANIFEST.md:89** - | `TODO.md` | Extracted TODOs/FIXMEs | Push to develop/main | `.github/workflows/ci.yml` |
- [ ] **AI_AGENT_MANIFEST.md:350** - | **Pending Work** | `TODO.md` | Extracted TODOs from code |
- [ ] **STATUS.md:25** - All missing/incomplete functionalities from TODO.md have been successfully implemented:
- [ ] **STATUS.md:274** - - [Technical Debt](TODO.md)
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