# Next Session Plan

## Priority 1: ContextBuilder Consolidation
- **Goal:** Eliminate logic duplication between `apps/memory_api/services/context_builder.py` and `rae-core/rae_core/context/builder.py`.
- **Task:** Refactor the `apps` service to delegate the final context assembly and token management to the `rae-core` utility.

## Priority 2: Data Hygiene (Ghost Columns)
- **Goal:** Activate `session_id` to support ISO 42001 provenance.
- **Task:** Update `verify_mcp.py` and `screenwatcher` integration to explicitly pass `session_id`.
- **Task:** Create a migration to drop the legacy `ttl` column (if confirmed unused).

## Priority 3: Verification
- **Goal:** Ensure Dashboard fix didn't introduce latency.
- **Task:** Run `make test-lite` and check `/metrics` endpoint latency.