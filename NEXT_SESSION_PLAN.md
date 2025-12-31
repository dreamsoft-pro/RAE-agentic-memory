# Plan for Next Session: Telemetry Implementation Audit

## Objective
Verify 100% compliance of the codebase with `docs/specs/TELEMETRY_IMPLEMENTATION_PLAN.md` (Phases 1-4).

## Role: Quality Assurance & Node1 Delegate

## Instructions
1. **Delegate to Node1 (`codebase_investigator`)**:
   - Task: "Deep audit of Telemetry & Sync implementation."
   - Checkpoints:
     - **Phase 1 (Ops):** Is `otel-collector` removed from `docker-compose.yml`? Are `rae_uptime_seconds` and `rae_memory_count_total` registered in `metrics.py`?
     - **Phase 2 (Cognitive):** Does `MemoryItem` in `rae-core` have `provenance` and `sync_metadata`? Does `ReflectionEngine` use them?
     - **Phase 3 (Sync):** Is `SyncManager` implemented in `rae-core`? Are `/system/sync` endpoints exposed in `rae-api`?
     - **Phase 4 (Research):** Does `run_research_mode.sh` exist? Is `httpx` instrumented in `opentelemetry_config.py`?

2. **Auto-Fix Protocol**:
   - If ANY file is missing or code is divergent from the plan, **fix it immediately** without asking for permission.
   - Run tests: `make test-unit` (focus on `test_sync_manager.py` and `test_reflection_simple.py`).

3. **Final Report**:
   - Generate `AUDIT_REPORT_TELEMETRY.md` with status of each phase (Pass/Fail -> Fixed).
