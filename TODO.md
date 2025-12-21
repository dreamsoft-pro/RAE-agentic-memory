# RAE Agentic Memory - Roadmap & Implementation Plan

## 🚨 NEXT SESSION: Restore rae-core Tests & Complete Linter Cleanup

**Current Status (2025-12-21):**
- **Unit Tests:** ✅ **885 passing** (Restored stability).
- **Graph API:** ✅ Fully implemented `apps/memory_api/api/v1/graph.py` using `EnhancedGraphRepository`.
- **Linter Errors Remaining:** **169** (down from 420).
- **Core Discovery:** `rae-core/tests` are missing from `pytest.ini` `testpaths`, explaining the drop from >900 to 885 tests.

**Priority Tasks:**

1.  **🚨 CRITICAL: Restore Core Test Coverage**
    - [ ] **Action**: Add `rae-core/tests` to `pytest.ini` testpaths.
    - [ ] **Goal**: Verify core logic and restore 100% core coverage.
    - [ ] **Command**: `make test-unit` (expect >900 tests).

2.  **🚨 CRITICAL: Finish Linter Errors (Zero Warning Policy)**
    - [ ] **Remaining B008/B904**: Clean up remaining manual fixes.
    - [ ] **Goal**: CI must pass `make lint`.

3.  **Mypy Cleanup**
    - [ ] **Current Status**: ~462 errors remaining.
    - [ ] **Task**: `.venv/bin/mypy apps/ sdk/ | grep "has no attribute"`

4.  **Documentation Sync**
    - [ ] Update `CONVENTIONS.md` with the "No Absolute Paths" rule verified this session.

---

## Phase 3: Quality & Reliability (Target: 80% Coverage)

### Iteration 1: Foundation Layer (Repositories & Basic Services) ✅
- [x] **`apps/memory_api/repositories/cost_logs_repository.py`**
- [x] **`apps/memory_api/repositories/trigger_repository.py`**
- [x] **`apps/memory_api/services/cost_controller.py`**
- [x] **`apps/memory_api/services/analytics.py`**

### Iteration 2: Core Logic (Complex Services) ✅
- [x] **`apps/memory_api/services/hybrid_search_service.py`** 
- [x] **`apps/memory_api/services/graph_extraction.py`**
- [x] **`apps/memory_api/services/reflection_pipeline.py`**

### Iteration 3: Knowledge Graph API Restoration ✅
- [x] **`apps/memory_api/api/v1/graph.py`** (Fully functional & tested)

### Iteration 4: Safety Net (Routes & Dashboard) 🛡️
- [ ] **`apps/memory_api/routes/dashboard.py`** (Current: 0%)
- [ ] **`apps/memory_api/routes/graph_enhanced.py`** (Current: 0%)
- [ ] **E2E/Integration Polish**