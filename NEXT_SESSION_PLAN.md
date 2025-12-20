# Next Session Plan: Mypy "Zero Warnings" Completion

## Status
- **Progress:** Reduced Mypy errors from 1290 to 466.
- **Fixed:** Pydantic models (plugins, constr replacement), logging (structlog migration), and Implicit Optional in key services.
- **Branch:** feature/mypy-fixes (if applicable, otherwise current).

## Priority: Fix Remaining 466 Mypy Errors

### 1. Fix Dependency Injection in Background Tasks
**Errors:** `Missing positional argument "rae_service"` in `apps/memory_api/tasks/background_tasks.py`.
**Action:**
- Update constructor calls for `ReflectionEngine`, `GraphExtractionService`, and `DreamingWorker` in `background_tasks.py`.
- Ensure they all receive the required `rae_service`.

### 2. Fix Test Suite Type Errors
**Errors:** Large number of `Missing named argument` and `Incompatible type` in `apps/memory_api/tests/`.
**Action:**
- Update test cases to match the refined Pydantic models (adding missing required fields in mocks).
- Fix fixture types in `conftest.py` if necessary.

### 3. Fix Attribute Errors in Services
**Errors:** `BaseModel has no attribute "topics"` (and others) in `semantic_extractor.py` and `reflection_pipeline.py`.
**Action:**
- Use `cast(SemanticExtractionResult, result)` after `generate_structured` calls.
- Verify that `LLMResult` or `LLMResponse` models actually have the attributes being accessed (e.g., `cost_usd`).

### 4. Final Verification
- Run `.venv/bin/mypy apps/ sdk/`.
- Run `make lint`.
- Goal: **Success: no issues found in 279 source files.**

## Start Command
To pick up from where we left off, run:
```bash
.venv/bin/mypy apps/ sdk/
```
