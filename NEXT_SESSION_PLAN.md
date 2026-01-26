# Next Session Plan - 2026-01-27

## 1. Final Core Stability (Priority 1)
- [ ] Fix `test_szubar_strategy_failure_injection`:
    - Analyze `search_memories_sql` debug logs from the previous session.
    - Resolve the mismatch between stored governance JSONB and the search filter.
    - Standardize `agent_id` vs `project` handling once and for all in the Postgres adapter.
- [ ] Verify 36/36 green tests.

## 2. Benchmark Optimization (Spectacular Results)
- [ ] Re-run `Industrial Large` on **Node 1 (Lumina)**:
    - Use a larger model (e.g., `nomic-embed-text` 768d or `text-embedding-3-small` 1536d).
    - Aim for MRR > 0.90 using the new **ConfidenceWeightedFusion** (ORB 2.0).
- [ ] Fix `Math-Only` precision:
    - Investigate why `plainto_tsquery` is less effective than ILIKE for technical failures.
    - Implement a more aggressive heuristic expansion for technical terms.

## 3. Self-Tuning Intelligence (ORB 4.0)
- [ ] Integrate entropy-based confidence analysis into `ConfidenceWeightedFusion`.
- [ ] Activate `Graph Centrality Boost` using real edge data from benchmarks.

## 4. Documentation & Cleanup
- [ ] Remove temporary diagnostic logs from `rae_adapters/postgres.py`.
- [ ] Update `DEVELOPER_CHEAT_SHEET.md` with new fusion strategy commands.
