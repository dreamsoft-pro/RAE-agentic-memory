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

## 🚨 NEXT SESSION: Finish Core Migration & Distributed Compute

**Current Status (2025-12-25):**
- **Architecture Migration:** ✅ All services, routes, and background tasks migrated to `RAECoreService`.
- **Distributed Compute:** ✅ Node1 (KUBUS) integration verified and active.
- **Core Stability:** ✅ **908 tests passed** (100% unit Green).
- **Infrastructure:** ✅ RAE-Lite mode supported with in-memory fallbacks.

**Priority Tasks:**

1.  **🏗️ Agnostic Enforcement (CRITICAL)**
    - [x] **Action**: Refactor `EnhancedGraphRepository` to use a generic DB interface instead of `asyncpg.Pool` directly (preparation for RAE-Lite).
    - [x] **Action**: Implement `IEmbeddingProvider` for remote compute nodes to offload embedding generation without leaking node details.

2.  **🚀 Distributed Compute: Expand Cluster**
    - [x] **Action**: Update node1 agent to communicate with the new Control Node API.
    - [x] **Action**: Successfully pull a 'no-op' task from the local module to node1.

3.  **🧠 Heavy Workload Delegation**
    - [x] **Action**: Integrate task delegation into `RAEEngine` for heavy embedding generation and LLM inference.

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
*Last scan: 2025-12-25 14:01*
... (rest of the file)
