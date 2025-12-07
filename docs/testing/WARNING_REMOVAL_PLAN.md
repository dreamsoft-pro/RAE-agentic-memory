# Test Warning Removal Plan

**Generated:** 2025-12-07
**Test Run Summary:**
- Total Tests: 860 passed, 24 skipped
- Total Warnings: 237 warning instances (73 unique warnings)
- Test Execution Time: 24.08s

## Executive Summary

This document provides an iterative, priority-based plan to eliminate all test warnings while maintaining system stability. Warnings are categorized by severity with specific action items for each.

### Warning Distribution by Severity

| Severity | Count | Impact |
|----------|-------|--------|
| **CRITICAL** | 2 | Python 3.14 compatibility blockers |
| **HIGH** | 65 | Scheduled for removal in 2025-2026 |
| **MEDIUM** | 1 | Framework-level deprecations |
| **LOW** | 5 | Environment/informational warnings |
| **TOTAL** | 73 | |

---

## Phase 1: CRITICAL Priority (Immediate Action Required)

### ⚠️ CRITICAL-1: google._upb._message Deprecation (Python 3.14 Blocker)

**Warning Count:** 2 occurrences
**Impact:** Will cause failures in Python 3.14
**Source:** Third-party dependency (protobuf via OpenTelemetry)

**Warning Message:**
```
DeprecationWarning: Type google._upb._message.MessageMapContainer uses PyType_Spec
with a metaclass that has custom tp_new. This is deprecated and will no longer be
allowed in Python 3.14.
```

**Location:**
- `<frozen importlib._bootstrap>:488`

**Root Cause:**
Using outdated version of protobuf/grpcio packages that are incompatible with Python 3.14.

**Solution Strategy:**
1. **Immediate Action (Non-breaking):**
   ```bash
   # Check current versions
   pip list | grep -E "protobuf|grpcio"

   # Upgrade to compatible versions
   pip install --upgrade protobuf>=4.25.0 grpcio>=1.60.0
   ```

2. **Verification:**
   ```bash
   PYTHONPATH=. pytest apps/memory_api/tests/observability/ -W error::DeprecationWarning
   ```

3. **Rollback Plan:**
   - Document current versions in `requirements.txt` before upgrade
   - Test OpenTelemetry functionality after upgrade
   - If issues arise, pin to latest compatible version

**Estimated Effort:** 30 minutes
**Risk Level:** Low (dependency upgrade only)
**Success Criteria:** Zero google._upb warnings in test output

---

## Phase 2: HIGH Priority (Scheduled for Removal)

### 🔴 HIGH-1: datetime.utcnow() Deprecation (40 occurrences)

**Warning Count:** 40 occurrences across 9 files
**Impact:** Will be removed in a future Python version
**Scheduled Removal:** Python 3.12+ (deprecated), removal TBD

**Warning Message:**
```
DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for
removal in a future version. Use timezone-aware objects to represent datetimes
in UTC: datetime.datetime.now(datetime.UTC).
```

**Affected Files:**
1. `apps/memory_api/services/compliance_service.py` (7 occurrences)
2. `apps/memory_api/services/policy_versioning_service.py` (4 occurrences)
3. `apps/memory_api/services/human_approval_service.py` (6 occurrences)
4. `apps/memory_api/services/retention_service.py` (4 occurrences)
5. `apps/memory_api/utils/circuit_breaker.py` (4 occurrences)
6. `apps/memory_api/models/reflection_v2_models.py` (1 occurrence)
7. `apps/memory_api/tests/services/test_semantic_search_v2.py` (5 occurrences)
8. `apps/memory_api/tests/test_human_approval_service.py` (8 occurrences)
9. `.venv/lib/python3.12/site-packages/pydantic/main.py` (1 occurrence - third party)

**Solution Strategy:**

**Step 1:** Create utility helper (apps/memory_api/utils/datetime_utils.py)
```python
from datetime import datetime, timezone

def utc_now() -> datetime:
    """Get current UTC datetime with timezone awareness."""
    return datetime.now(timezone.utc)

# Backward-compatible alias if needed
utcnow = utc_now
```

**Step 2:** Replace in production code (service files first)
```python
# OLD
from datetime import datetime
timestamp = datetime.utcnow()

# NEW
from datetime import datetime, timezone
timestamp = datetime.now(timezone.utc)

# OR with helper
from apps.memory_api.utils.datetime_utils import utc_now
timestamp = utc_now()
```

**Step 3:** Update test files
- Tests can use the same pattern
- Ensure test fixtures use timezone-aware datetimes

**Step 4:** Add pre-commit hook or linting rule
```yaml
# .pre-commit-config.yaml addition
- id: check-datetime-utcnow
  name: Check for datetime.utcnow() usage
  entry: bash -c 'grep -rn "datetime\.utcnow()" apps/ && exit 1 || exit 0'
  language: system
  pass_filenames: false
```

**Implementation Order:**
1. Create datetime_utils.py helper (5 min)
2. Fix apps/memory_api/services/compliance_service.py (15 min)
3. Fix apps/memory_api/services/policy_versioning_service.py (10 min)
4. Fix apps/memory_api/services/human_approval_service.py (15 min)
5. Fix apps/memory_api/services/retention_service.py (10 min)
6. Fix apps/memory_api/utils/circuit_breaker.py (10 min)
7. Fix apps/memory_api/models/reflection_v2_models.py (5 min)
8. Fix test files (20 min)
9. Run full test suite to verify (5 min)
10. Add pre-commit hook (5 min)

**Estimated Effort:** 2 hours
**Risk Level:** Low (straightforward replacement)
**Success Criteria:** Zero datetime.utcnow warnings, all tests pass

---

### 🔴 HIGH-2: Pydantic V2 Deprecations (24 occurrences)

**Warning Count:** 24 occurrences across 7 files
**Impact:** Will be removed in Pydantic V3.0
**Scheduled Removal:** Pydantic V3.0 (estimated 2025-2026)

**Warning Types:**
1. Class-based `config` deprecation (2 files)
2. `.copy()` method deprecation (1 test file, 16 occurrences)
3. `.dict()` method deprecation (4 files, 6 occurrences)

#### HIGH-2A: Class-based Config → ConfigDict

**Affected Files:**
- `apps/memory_api/core/state.py:241`
- `apps/memory_api/core/actions.py:80`

**Current Pattern:**
```python
class RAEState(BaseModel):
    class Config:
        arbitrary_types_allowed = True
```

**New Pattern:**
```python
from pydantic import ConfigDict

class RAEState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
```

**Action Steps:**
1. Update `apps/memory_api/core/state.py:241`
2. Update `apps/memory_api/core/actions.py:80`
3. Search for other class Config patterns: `grep -rn "class Config:" apps/`
4. Run tests to verify model behavior unchanged

**Estimated Effort:** 20 minutes
**Risk Level:** Low (Pydantic V2 migration guide is comprehensive)

#### HIGH-2B: .copy() → .model_copy()

**Affected Files:**
- `apps/memory_api/tests/core/test_reward.py` (16 occurrences)

**Current Pattern:**
```python
state_copy = state.copy(update={"budget": BudgetState(...)})
```

**New Pattern:**
```python
state_copy = state.model_copy(update={"budget": BudgetState(...)})
```

**Action Steps:**
1. Find all `.copy()` calls in test files
2. Replace with `.model_copy()`
3. Verify `update`, `deep`, `include`, `exclude` parameters work identically

**Estimated Effort:** 15 minutes
**Risk Level:** Very Low (test-only changes)

#### HIGH-2C: .dict() → .model_dump()

**Affected Files:**
- `apps/memory_api/services/hybrid_search_service.py:351`
- `apps/memory_api/services/rules_engine.py:599`
- `apps/memory_api/api/v1/agent.py:243`
- `apps/memory_api/routes/dashboard.py:335, 526`

**Current Pattern:**
```python
result_dict = model.dict()
result_dict = model.dict(exclude={'password'})
```

**New Pattern:**
```python
result_dict = model.model_dump()
result_dict = model.model_dump(exclude={'password'})
```

**Action Steps:**
1. Search: `grep -rn "\.dict()" apps/ --include="*.py"`
2. Replace each instance with `.model_dump()`
3. Test affected endpoints (especially dashboard and agent APIs)
4. Verify JSON serialization still works correctly

**Estimated Effort:** 30 minutes
**Risk Level:** Medium (affects API responses - needs thorough testing)

---

### 🔴 HIGH-3: pkg_resources Deprecation (2 occurrences)

**Warning Count:** 2 occurrences
**Impact:** Scheduled for removal 2025-11-30
**Source:** Third-party dependency (OpenTelemetry)

**Affected Files:**
- `.venv/lib/python3.12/site-packages/opentelemetry/instrumentation/dependencies.py:4`
- `.venv/lib/python3.12/site-packages/pkg_resources/__init__.py:3146`

**Root Cause:**
OpenTelemetry instrumentation uses deprecated `pkg_resources` API.

**Solution Strategy:**
1. **Check OpenTelemetry version:**
   ```bash
   pip list | grep opentelemetry
   ```

2. **Upgrade to latest versions:**
   ```bash
   pip install --upgrade \
     opentelemetry-api \
     opentelemetry-sdk \
     opentelemetry-instrumentation \
     opentelemetry-exporter-otlp
   ```

3. **Alternative: Suppress if needed (temporary):**
   ```python
   # In conftest.py or test configuration
   import warnings
   warnings.filterwarnings("ignore", category=UserWarning, module="pkg_resources")
   ```

4. **Long-term: Wait for OpenTelemetry fix**
   - Track issue: https://github.com/open-telemetry/opentelemetry-python-contrib/issues
   - This is a known issue in the OpenTelemetry ecosystem

**Estimated Effort:** 30 minutes (mostly waiting for upstream fix)
**Risk Level:** Very Low (third-party dependency)
**Success Criteria:** Either warnings eliminated or documented as waiting on upstream

---

## Phase 3: MEDIUM Priority (Framework Deprecations)

### 🟡 MEDIUM-1: FastAPI Duplicate Operation ID (1 occurrence)

**Warning Count:** 1 occurrence
**Impact:** May cause OpenAPI spec conflicts

**Warning Message:**
```
UserWarning: Duplicate Operation ID metrics_metrics_get for function metrics
at /home/grzegorz/cloud/Dockerized/RAE-agentic-memory/apps/memory_api/api/v1/health.py
```

**Affected Files:**
- `apps/memory_api/api/v1/health.py`

**Root Cause:**
Multiple endpoints with the same function name `metrics()` causing OpenAPI operation ID collision.

**Solution Strategy:**
1. **Find duplicate function:**
   ```bash
   grep -n "def metrics" apps/memory_api/api/v1/health.py
   ```

2. **Option A: Rename function**
   ```python
   # OLD
   @router.get("/metrics")
   def metrics():
       ...

   # NEW
   @router.get("/metrics")
   def get_health_metrics():  # More descriptive name
       ...
   ```

3. **Option B: Set explicit operation_id**
   ```python
   @router.get("/metrics", operation_id="health_metrics_endpoint")
   def metrics():
       ...
   ```

**Estimated Effort:** 10 minutes
**Risk Level:** Very Low (internal naming only)
**Success Criteria:** No duplicate operation ID warnings

---

## Phase 4: LOW Priority (Informational/Environment)

### 🟢 LOW-1: NVML Initialization Warning (2 occurrences)

**Warning Count:** 2 occurrences
**Impact:** Informational - CUDA/GPU not available

**Warning Message:**
```
UserWarning: Can't initialize NVML
```

**Location:**
- `torch/cuda/__init__.py:827`

**Root Cause:**
PyTorch attempting to initialize NVIDIA Management Library (NVML) when no GPU is available.

**Solution Strategy:**
1. **Option A: Suppress in test configuration (Recommended)**
   ```python
   # conftest.py
   import warnings
   warnings.filterwarnings("ignore", message="Can't initialize NVML")
   ```

2. **Option B: Set environment variable**
   ```bash
   export CUDA_VISIBLE_DEVICES=""
   ```

3. **Option C: Install CPU-only PyTorch**
   - Only if GPU support is not needed at all
   - Reduces package size significantly

**Estimated Effort:** 5 minutes
**Risk Level:** None (does not affect functionality)
**Success Criteria:** Warning suppressed in test output

---

### 🟢 LOW-2: ResourceWarning (2 occurrences)

**Warning Count:** 2 occurrences
**Impact:** Unclosed resources (file handles, sockets, etc.)

**Solution Strategy:**
1. **Enable ResourceWarning tracking:**
   ```bash
   PYTHONPATH=. pytest -W default::ResourceWarning -v
   ```

2. **Common patterns to check:**
   - Files opened without context manager
   - Database connections not properly closed
   - HTTP sessions not closed

3. **Fix pattern:**
   ```python
   # BAD
   f = open('file.txt')
   data = f.read()

   # GOOD
   with open('file.txt') as f:
       data = f.read()
   ```

**Estimated Effort:** 30 minutes (investigation + fixes)
**Risk Level:** Low (cleanup task)
**Success Criteria:** Zero ResourceWarning in tests

---

### 🟢 LOW-3: Click Parser Deprecation (1 occurrence - third party)

**Warning Count:** 1 occurrence
**Impact:** Third-party deprecation (spaCy)

**Location:**
- `spacy/cli/_util.py:23`

**Solution Strategy:**
- **Wait for spaCy update** - this is in their code, not ours
- **Suppress warning:**
  ```python
  warnings.filterwarnings("ignore", module="spacy.cli._util")
  ```

**Estimated Effort:** 2 minutes
**Risk Level:** None
**Success Criteria:** Warning suppressed

---

## Implementation Timeline

### Sprint 1: Critical & High-1 (Week 1)
- [ ] Day 1: Fix CRITICAL-1 (google._upb - dependency upgrade)
- [ ] Day 2-3: Fix HIGH-1 (datetime.utcnow in service files)
- [ ] Day 4: Fix HIGH-1 (datetime.utcnow in test files)
- [ ] Day 5: Code review and regression testing

**Deliverable:** 42 warnings eliminated (57% reduction)

### Sprint 2: High-2 & High-3 (Week 2)
- [ ] Day 1: Fix HIGH-2A (Pydantic Config → ConfigDict)
- [ ] Day 2: Fix HIGH-2B (Pydantic .copy() → .model_copy())
- [ ] Day 3: Fix HIGH-2C (Pydantic .dict() → .model_dump())
- [ ] Day 4: Fix HIGH-3 (pkg_resources - dependency upgrade)
- [ ] Day 5: Integration testing and verification

**Deliverable:** 23 additional warnings eliminated (89% reduction)

### Sprint 3: Medium & Low (Week 3)
- [ ] Day 1: Fix MEDIUM-1 (FastAPI duplicate operation ID)
- [ ] Day 2: Fix LOW priorities (NVML, ResourceWarning, Click)
- [ ] Day 3: Add pre-commit hooks and linting rules
- [ ] Day 4-5: Documentation and team training

**Deliverable:** All warnings eliminated (100% clean)

---

## Verification Strategy

### After Each Phase

```bash
# Run full test suite with warnings as errors
PYTHONPATH=. pytest apps/memory_api/tests/ tests/ \
  -W error::DeprecationWarning \
  -W error::PydanticDeprecatedSince20 \
  --maxfail=1

# Generate warning report
PYTHONPATH=. pytest apps/memory_api/tests/ tests/ \
  -W default \
  --tb=short \
  -v \
  2>&1 | tee warning_report.log

# Count remaining warnings
grep -c "DeprecationWarning\|UserWarning\|PydanticDeprecatedSince20" warning_report.log
```

### Success Metrics

| Phase | Target | Metric |
|-------|--------|--------|
| After Phase 1 | ≤71 warnings | CRITICAL eliminated |
| After Phase 2 | ≤8 warnings | HIGH eliminated |
| After Phase 3 | ≤7 warnings | MEDIUM eliminated |
| After Phase 4 | 0 warnings | Complete cleanup |

---

## Risk Mitigation

### General Principles
1. **Never skip tests** - All changes must pass existing test suite
2. **Review API contracts** - Ensure external APIs remain unchanged
3. **Test in staging** - Deploy to staging environment before production
4. **Incremental commits** - One warning type per commit for easy rollback
5. **Pair review** - Have another developer review Pydantic changes

### Rollback Strategy
```bash
# If issues arise, revert specific commits
git revert <commit-hash>

# Or rollback entire phase
git checkout <pre-phase-tag>
```

### Known Risks

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Pydantic behavior change | Low | Extensive test coverage, gradual rollout |
| Dependency conflicts | Medium | Document versions, test in isolation |
| API response format change | Low | Integration tests for all endpoints |
| Production datetime issues | Low | Thorough timezone testing |

---

## Monitoring & Validation

### Post-Deployment Checklist

- [ ] All 860 tests pass
- [ ] No new warnings introduced
- [ ] API response formats unchanged (compare before/after)
- [ ] Database timestamps still UTC
- [ ] OpenTelemetry traces still functional
- [ ] Dashboard WebSocket connections stable
- [ ] Health check endpoints responding correctly

### Continuous Monitoring

```yaml
# Add to CI/CD pipeline (.github/workflows/tests.yml)
- name: Check for test warnings
  run: |
    PYTHONPATH=. pytest apps/memory_api/tests/ tests/ -W default 2>&1 | tee warnings.log
    WARNING_COUNT=$(grep -c "Warning" warnings.log || true)
    if [ $WARNING_COUNT -gt 0 ]; then
      echo "⚠️ Found $WARNING_COUNT warnings in test suite"
      exit 1
    fi
```

---

## Additional Resources

### Documentation References
- [Python datetime migration guide](https://docs.python.org/3/library/datetime.html#datetime.datetime.now)
- [Pydantic V2 migration guide](https://docs.pydantic.dev/latest/migration/)
- [OpenTelemetry Python instrumentation](https://opentelemetry.io/docs/languages/python/)

### Related Files
- `pytest.ini` - Test configuration
- `.github/workflows/test.yml` - CI/CD pipeline
- `requirements.txt` - Python dependencies
- `docs/TESTING_STATUS.md` - Current test status

---

## Contact & Support

**Document Owner:** RAE Development Team
**Last Updated:** 2025-12-07
**Next Review:** After Phase 1 completion

For questions or issues during implementation, create an issue with label `testing/warnings`.
