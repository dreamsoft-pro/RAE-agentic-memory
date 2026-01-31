# Session State - 2026-01-29

## Current Goal
Stabilize all unit tests (1079+) to ensure GitHub Actions CI passes.

## Progress
- [x] Removed heavy ML dependency skips in tests.
- [x] Fixed PII Scrubber to use regex fallback (no Presidio dependency).
- [x] Fixed Qdrant adapter tests (UUID strings and 'episodic' layer).
- [x] Fixed Vector Store tests (partially).

## Blockers
- **Pydantic Validation**: 60+ occurrences of `"layer": "em"` remain in test fixtures and mocks. These must be changed to `"layer": "episodic"` to match the strict `LayerEnum` in `MemoryRecord`.
- **RAE MCP Tool**: `rae-memory__save_memory` returned 404 (pointing to V1 API).

## Next Steps
1. Run `grep -r '"layer": "em"' .` to identify all targets.
2. Replace `"em"` with `"episodic"` in all identified test files.
3. Run `RAE_API_URL="" make test-fast` until green.

## Resuming Work
Execute:
```bash
python3 scripts/bootstrap_session.py
```
Then confirm we are working on "Stabilizacja testów RAE".