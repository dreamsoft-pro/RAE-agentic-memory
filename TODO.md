# RAE Agentic Memory - Roadmap & Implementation Plan

## 🛠️ Critical Engineering Remediation (PLAN_REPAIR_001)

**Source:** [PLAN_REPAIR_001.md](docs/plans/PLAN_REPAIR_001.md)
**Goal:** Fix architectural risks identified in Cold Review.

- [x] **Phase 1: Stabilization** - Offload `HDBSCAN`/`KMeans` to thread pool to prevent Event Loop Starvation.
- [x] **Phase 2: Data Integrity** - Implement `ConsistencyService` to remove orphaned Qdrant embeddings.
- [x] **Phase 3: Architecture** - Decouple Storage Adapters and fix naming drift.
    - [x] Create abstract interfaces in `rae-core`.
    - [x] Refactor high-level services (`MemoryConsolidation`, `Analytics`, `HybridSearch`, etc.) to use `RAECoreService`.
    - [x] Update Dependency Injection in `apps/memory_api/dependencies.py`.
    - [x] Migrate background workers and tasks to use `RAECoreService`.
- [x] Migrate `apps/memory_api/routes/graph_enhanced.py` to `RAECoreService`.

## 🚀 IRON RAE Optimization (MATH Layer Refactor)

**Source:** [IRON_RAE_OPTIMIZATION_PLAN.md](docs/plans/IRON_RAE_OPTIMIZATION_PLAN.md)
**Goal:** Enhance mathematical core for stability and multi-vector support.

- [x] **Phase 1: MATH-2 – Multi-Vector Fusion**
    - [x] Implement Reciprocal Rank Fusion (RRF) in `rae-core`.
    - [x] Update `QdrantStore` for named vectors (OpenAI/Ollama).
    - [x] Update `HybridSearchService` for concurrent multi-model search.
- [x] **Phase 2: MATH-1 – Deterministic Topological Logic**
    - [x] Implement `GraphTopologyEngine` (NetworkX based).
    - [x] Add path proving and centrality analysis.
- [x] **Phase 3: MATH-3 – Dynamics Control**
    - [x] Implement PID Controller and Kalman Filter in `rae-core`.
- [x] **Infrastructure**: Fix Gemini Auth (Token/ADC fallback).
- [x] **Quality**: Zero Warning Policy enforcement.

## 🚨 NEXT SESSION: Full Benchmark Suite Execution

**Current Status (2026-01-02):**
- **Tests:** ✅ 972 passed, 0 failed.
- **Linting:** ✅ Zero warnings.
- **Features:** ✅ IRON RAE implemented.

**Priority Tasks:**

1.  **📊 Benchmarking (Verification)**
    - [ ] Run `make benchmark-full`.
    - [ ] Verify LECT > 0.9999.
    - [ ] Verify GRDT > 0.8.

---

### Iteration 1: Foundation Layer ✅
- [x] **`apps/memory_api/repositories/cost_logs_repository.py`**
- [x] **`apps/memory_api/repositories/trigger_repository.py`**
- [x] **`apps/memory_api/services/cost_controller.py`**
- [x] **`apps/memory_api/services/analytics.py`** (Refactored to RAECoreService)

### Iteration 2: Core Logic ✅
- [x] **`apps/memory_api/services/hybrid_search_service.py`** (Refactored to RAECoreService)
- [x] **`apps/memory_api/services/graph_extraction.py`**
- [x] **`apps/memory_api/services/reflection_pipeline.py`** (Refactored to RAECoreService)

### Iteration 3: Knowledge Graph API Restoration ✅
- [x] **`apps/memory_api/api/v1/graph.py`** (Updated to new architecture)

### Iteration 4: Safety Net (Routes & Dashboard) ✅
- [x] **`apps/memory_api/routes/dashboard.py`** (Refactored to RAECoreService & IDatabaseProvider)
- [x] **`apps/memory_api/routes/graph_enhanced.py`** (Refactored to RAECoreService & IDatabaseProvider)
- [x] **E2E/Integration Polish** (Verified with 908 passing unit tests)

## Technical Debt (Auto-generated from code)
*Last scan: 2026-01-01 03:04*

- [ ] **CHANGELOG.md:1116** - - resolve conflict in TODO.md ([`c3694b8`](../../commit/c3694b8))
