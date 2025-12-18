# Next Session Plan

## Priority: Fix Unit Test Failures (Migration Cleanup)

The migration of `MemoryRepository` to `RAE-Core` is code-complete, but unit tests are failing due to environment configuration and mismatched signatures.

### 1. Disable DB Validation in Tests
**Error:** `RuntimeError: Database schema validation failed: 1 violations found.`
**Cause:** The application startup validator runs against mock database pools in tests.
**Action:**
- Modify `apps/memory_api/tests/conftest.py`.
- In the `mock_env` or `app` fixture, ensure `RAE_DB_MODE` environment variable is set to `"ignore"`.

### 2. Fix `tests/api/v1/test_memory.py`
**Error:** `fixture 'mock_pool' not found`
**Action:**
- Add `mock_pool` fixture to `tests/api/v1/test_memory.py` (copy from `apps/memory_api/tests/conftest.py` or import it).

### 3. Fix ReflectionEngineV2 Tests
**Error:** `AttributeError: 'ReflectionEngineV2' object has no attribute 'generate_reflection'`
**Action:**
- Inspect `apps/memory_api/services/reflection_engine_v2.py`.
- Determine the correct method name (likely `store_reflection` or `generate_reflection_v2`).
- Update `apps/memory_api/tests/services/test_reflection_engine_v2.py` to use the correct method.

### 4. Fix Worker Tests (Dependency Injection)
**Error:** `TypeError: SummarizationWorker.__init__() got an unexpected keyword argument 'memory_repository'`
**Action:**
- Update `apps/memory_api/tests/test_workers.py` and `apps/memory_api/tests/test_summarization_worker.py`.
- Replace `memory_repository` mock with `rae_service` mock in worker instantiation.

### 5. Final Verification
- Run `make test-unit`.
- Ensure 0 errors, 0 warnings (per policy).