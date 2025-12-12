# Next Session Plan - Test Fixing Continuation

**Date:** 2025-12-11
**Session Goal:** Fix remaining 39 test failures + verify agnosticism + commit

---

## ✅ Completed in Previous Session (2 tests fixed)

**Fixed Files:**
- `apps/memory_api/tests/test_reflective_flags.py`
  - ✅ `test_reflective_memory_disabled_no_reflections` - added mock_reflection_engine
  - ✅ `test_dreaming_enabled_runs_dreaming` - fixed async context manager with @asynccontextmanager

**Current Status:**
- Tests passing: 870 (was 868)
- Tests failing: 39 (was 41)
- Total: 958 tests

---

## 🎯 Remaining Work - 39 Tests to Fix

### PRIORITY 1: Contract Tests (4 failures) ⚡ QUICK WINS

**File:** `tests/contracts/test_api_contracts.py`

**Issue:** Response format changed from `{"detail": "..."}` to `{"error": {"code": "...", "message": "...", "details": [...]}}`

**Failing Tests:**
1. `test_store_memory_response_schema` - expects old format
2. `test_delete_memory_response_schema` - expects old format
3. `test_health_response_schema` - mock issues with pool.acquire
4. `test_400_error_schema` - expects `detail` field, got `error` object

**Fix Strategy:**
- Update schema expectations to match new error format
- Fix async mock for health check (pool.acquire context manager)

---

### PRIORITY 2: Integration Tests - Decay Worker (6 failures)

**File:** `tests/integration/test_decay_worker.py`

**Failing Tests:**
1. `test_decay_worker_basic_cycle`
2. `test_decay_worker_with_access_stats`
3. `test_decay_worker_multiple_tenants`
4. `test_decay_worker_importance_floor`
5. `test_decay_worker_get_all_tenants`
6. `test_decay_worker_preserves_metadata`

**Likely Issue:** Async mock setup for pool/connection (similar to dreaming worker fix)

---

### PRIORITY 3: Integration Tests - Dreaming Worker (4 failures)

**File:** `tests/integration/test_dreaming_worker.py`

**Failing Tests:**
1. `test_dreaming_worker_basic_cycle`
2. `test_dreaming_worker_lookback_window`
3. `test_dreaming_worker_importance_filter`
4. `test_dreaming_worker_max_samples_limit`

**Fix Strategy:** Apply same pattern as `test_reflective_flags.py` fix (asynccontextmanager)

---

### PRIORITY 4: Integration Tests - Lite Profile (7 errors/failures)

**File:** `tests/integration/test_lite_profile.py`

**Failing Tests:**
1. `test_lite_profile_health_check` - ERROR
2. `test_lite_profile_api_docs` - ERROR
3. `test_lite_profile_store_memory` - ERROR
4. `test_lite_profile_query_memory` - ERROR
5. `test_lite_profile_postgres_accessible` - FAILED
6. `test_lite_profile_qdrant_accessible` - FAILED
7. `test_lite_profile_redis_accessible` - FAILED

**Issue:** subprocess errors, service availability checks

---

### PRIORITY 5: Integration Tests - GraphRAG (5 errors)

**File:** `tests/integration/test_graphrag.py`

**Failing Tests:**
1. `test_graph_extraction_basic` - socket.gaierror
2. `test_graph_storage` - socket.gaierror
3. `test_hybrid_search` - socket.gaierror
4. `test_graph_traversal_depth` - socket.gaierror
5. `test_hierarchical_reflection` - socket.gaierror

**Issue:** Service connection errors - may need Docker services running or better mocks

---

### PRIORITY 6: Integration Tests - Reflection Flow (5 errors)

**File:** `tests/integration/test_reflection_flow.py`

**Failing Tests:**
1. `test_generate_reflection_from_failure`
2. `test_generate_reflection_from_success`
3. `test_reflection_retrieval_in_context`
4. `test_inject_reflections_into_prompt`
5. `test_end_to_end_reflection_flow`

**Issue:** subprocess errors

---

### PRIORITY 7: LLM Tests (8 failures)

**File:** `tests/llm/test_llm_provider_contract.py`

**Failing Tests:**
1. `test_basic_completion`
2. `test_json_mode`
3. `test_streaming`
4. `test_token_usage`
5. `test_temperature_control`
6. `test_max_tokens`
7. `test_provider_contract_hello_world[openai-gpt-3.5-turbo]`
8. `test_provider_contract_hello_world[anthropic-claude-3-haiku-20240307]`

**Issue:** Require LLM API keys OR need better mocking

---

## 🔍 After Tests: Verify Agnosticism

### 1. Verify rae-core agnosticism (database independence)
- Check that rae-core doesn't depend on specific database implementations
- Test with different storage backends

### 2. Verify cache agnosticism
- Ensure cache layer works with different backends (Redis, in-memory, etc.)

### 3. Verify storage agnosticism
- Ensure storage layer works with different backends (PostgreSQL, SQLite, etc.)

---

## ✅ Final Steps

1. **Run full test suite:** `python -m pytest --override-ini="addopts="`
   - Target: 958 tests passing
   - Goal: **0 errors, 0 warnings**

2. **Run format & lint:**
   ```bash
   cd rae-core
   black . && isort . && ruff check .
   ```

3. **Commit changes:**
   ```bash
   git add .
   git commit -m "fix: resolve 41 test failures and verify system agnosticism

   - Fixed reflective flags tests (2)
   - Fixed contract tests (4)
   - Fixed integration tests (27)
   - Fixed LLM tests (8)
   - Verified rae-core, cache, and storage agnosticism
   - All 958 tests passing with 0 errors, 0 warnings

   🤖 Generated with Claude Code"
   ```

4. **Push to GitHub:**
   ```bash
   git push origin develop
   ```

---

## 📋 Commands for Next Session Start

```bash
# 1. Activate venv
cd /home/grzegorz/cloud/Dockerized/RAE-agentic-memory
source .venv/bin/activate

# 2. Check current test status
python -m pytest --override-ini="addopts=" --co -q 2>&1 | tail -5

# 3. Run specific failing tests to verify
python -m pytest tests/contracts/test_api_contracts.py -v --tb=short --no-cov --override-ini="addopts="

# 4. Start fixing from Priority 1 (contract tests)
```

---

## 🎯 Session Strategy

**Policy:** 0 ERRORS, 0 WARNINGS (mandatory)
**Approach:** Fix category by category (contract → integration → LLM → agnosticism)
**Infrastructure:** Docker services are running
**Branch:** develop

---

## 📊 Progress Tracking

- [x] Reflective flags tests (2/2) ✅
- [ ] Contract tests (0/4)
- [ ] Integration - Decay worker (0/6)
- [ ] Integration - Dreaming worker (0/4)
- [ ] Integration - Lite profile (0/7)
- [ ] Integration - GraphRAG (0/5)
- [ ] Integration - Reflection flow (0/5)
- [ ] LLM tests (0/8)
- [ ] Verify agnosticism (0/3)
- [ ] Final test run (0/1)
- [ ] Commit & push (0/1)

**Total Progress:** 2/56 tasks (4%)
