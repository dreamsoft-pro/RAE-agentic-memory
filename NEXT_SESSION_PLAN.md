# Next Session Plan - Mypy & Maintenance

## Status
- **Mypy Errors:** 388 (down from 462).
- **Recent Fixes:** Corrected signatures in `PostgresStorage` and `InMemoryStorage`, added `TypedDict` for `ReflectionEngine`, and fixed type annotations in 5+ services.

## To Do
1. **Finish `apps/memory_api/services/graph_algorithms.py`**: Fix `related` list type (currently `List[str]`, should be `List[Dict[str, Any]]`).
2. **Fix `apps/memory_api/repositories/`**:
    - `trigger_repository.py`: Resolve `no-any-return` (lines 278, 389, 644).
    - `reflection_repository.py`: Fix 10+ `arg-type` errors (lines 237-510) where lists/ints are appended to list of strings.
3. **FastAPI Deprecation Warnings**: Fix 2 warnings for `HTTP_422_UNPROCESSABLE_ENTITY`.
4. **Unit Tests**: Investigate 22 skipped tests in `make test-unit`.

## Command to Continue
```bash
.venv/bin/mypy apps/ sdk/ | head -n 20
```