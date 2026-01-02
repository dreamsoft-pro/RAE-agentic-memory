# Plan for Next Session: Audit, Tech Debt & Modernization

**Status:** Ready for execution
**Target Branch:** `feature/maintenance-deps-and-audit` (create from `develop`)

## 1. Telemetry Implementation Audit (High Priority)
**Objective:** Verify 100% compliance with `docs/specs/TELEMETRY_IMPLEMENTATION_PLAN.md`.

- [x] **Phase 1 (Ops):** Verify `otel-collector` is removed from `docker-compose.yml`. Check `metrics.py` for `rae_uptime_seconds`.
- [x] **Phase 2 (Cognitive):** Verify `MemoryItem` in `rae-core` has `provenance` and `sync_metadata`.
- [x] **Phase 3 (Sync):** Verify `SyncManager` structure in `rae-core` and endpoints in `rae-api`.
- [x] **Phase 4 (Research):** Verify `run_research_mode.sh` exists and `httpx` instrumentation is active in `opentelemetry_config.py`.
- [x] **Deliverable:** Create `AUDIT_REPORT_TELEMETRY.md` with Pass/Fail status.

## 2. Fix FastAPI Deprecation Warnings
**Objective:** Eliminate noise in logs to maintain "Zero Warning Policy".

- [x] **Search:** grep for `HTTP_422_UNPROCESSABLE_ENTITY` (deprecated in newer Starlette/FastAPI versions).
- [x] **Replace:** Update to use `fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY` or integer `422`.
- [x] **Pydantic V2:** Check for any remaining Pydantic V1 patterns that cause warnings (e.g., `dict()` -> `model_dump()`, `parse_obj()` -> `model_validate()`).

## 3. Dependency Modernization (Critical)
**Objective:** Update outdated libraries to ensure security and performance.

- [x] **Audit:** Run `pip list --outdated` inside the container/venv.
- [x] **Update:**
    - `apps/memory_api/requirements.txt`: Focus on `fastapi`, `uvicorn`, `pydantic`, `langchain`, `qdrant-client`.
    - `requirements-dev.txt`: Focus on `pytest`, `ruff`, `mypy`, `black`.
- [x] **Constraint:** Update strictly **one major library at a time** and run tests to isolate breaking changes.
- [x] **Lock:** Regenerate any lock files if present (or just ensure `requirements.txt` versions are pinned).

## 4. Full Verification
**Objective:** Ensure no regression after dependency updates.

- [ ] **Unit Tests:** `make test-lite` (Fast check).
- [ ] **Integration Tests:** `make test-int` (Verify DB/API contracts with new libs).
- [ ] **Sanity Check:** Run `make lint` to ensure new linter versions don't introduce new rules that fail.

## 5. Final Polish
- [ ] Update `CHANGELOG.md` with "Maintenance: Dependencies updated & Telemetry Audited".
- [ ] Merge to `develop`.