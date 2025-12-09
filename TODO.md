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
*Last scan: 2025-12-08 23:29*

- [ ] **CHANGELOG.md:183** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:184** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:530** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:531** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:860** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:861** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:1189** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:1190** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:1517** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:1518** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:1844** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:1845** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:2169** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:2170** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:2492** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:2493** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:2814** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:2815** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:3135** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:3136** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:3456** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:3457** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:3776** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:3777** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:4096** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:4097** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:4415** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:4416** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:4734** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:4735** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5052** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5053** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5370** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5371** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5662** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5663** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:5953** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:5954** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6242** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6243** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6531** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6532** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:6819** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:6820** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:7107** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:7108** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:7394** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:7395** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:7681** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:7682** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:7967** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:7968** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8252** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8253** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8535** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8536** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:8817** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:8818** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9098** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9099** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9379** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9380** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9659** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9660** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:9939** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:9940** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10218** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10219** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10497** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10498** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:10775** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:10776** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11053** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11054** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11330** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11331** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11607** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11608** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:11883** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:11884** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12159** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12160** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12434** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12435** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12709** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12710** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:12983** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:12984** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13257** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13258** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13530** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13531** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:13803** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:13804** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14075** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14076** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14347** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14348** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14617** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14618** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:14886** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:14887** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15155** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15156** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15421** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15422** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15686** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15687** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:15950** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:15951** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16213** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16214** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16475** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16476** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16737** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16738** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:16996** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:16997** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17254** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17255** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17510** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17511** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:17764** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:17765** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18013** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18014** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18257** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18258** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18499** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18500** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18740** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18741** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:18980** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:18981** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19210** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19211** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19432** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19433** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19653** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19654** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:19873** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:19874** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:20092** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:20093** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:20310** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:20311** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:20527** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:20528** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:20743** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:20744** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:20958** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:20959** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:21172** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:21173** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:21385** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:21386** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:21597** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:21598** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:21809** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:21810** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:22017** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:22018** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:22224** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:22225** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:22431** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:22432** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:22637** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:22638** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:22842** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:22843** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:23047** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:23048** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:23241** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:23242** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:23428** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:23429** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:23614** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:23615** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:23800** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:23801** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:23984** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:23985** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:24168** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:24169** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:24351** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:24352** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:24533** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:24534** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:24713** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:24714** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:24893** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:24894** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25070** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25071** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25247** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25248** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25423** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25424** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25599** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25600** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25773** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25774** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:25947** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:25948** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26115** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26116** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26274** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26275** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26429** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26430** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26578** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26579** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26727** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26728** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:26874** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:26875** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27020** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27021** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27146** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27147** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27270** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27271** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27381** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27382** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27492** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27493** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27599** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27600** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27705** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27706** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27796** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27797** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27878** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27879** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:27950** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:27951** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28020** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28021** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28093** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28094** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28168** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28169** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28258** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28259** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28334** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28335** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
- [ ] **CHANGELOG.md:28409** - - update project status and TODO list after iteration 2 completion ([`49aff83`](../../commit/49aff83))
- [ ] **CHANGELOG.md:28410** - - Update TODO with Test Coverage Roadmap (Phase 3) ([`934b3a9`](../../commit/934b3a9))
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
- [ ] **STATUS.md:303** - - [Technical Debt](TODO.md)
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