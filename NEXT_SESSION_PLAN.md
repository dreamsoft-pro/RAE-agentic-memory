# Next Session Plan

## Priority: High
1. **Dashboard Stabilization**
   - Address any remaining issues with the Dashboard functionality.
   - Ensure the Dashboard correctly visualizes memory stats and graph data.

2. **Benchmark Verification**
   - Execute `benchmarking/scripts/run_benchmark.py` (Academic Lite/Extended).
   - Verify that the "Math-only" changes in Lite profile didn't negatively impact core metrics.
   - Run `check_nodes.py` to ensure cluster readiness for heavy benchmarks.

3. **Documentation Sync**
   - Update `STATUS.md` to reflect the "Green" state of all tests.
   - Update `TODO.md` to remove completed items (Governance 422, Core Coverage).

## Startup Protocol
1. **Read `DEVELOPER_CHEAT_SHEET.md`**.
2. **Check Cluster**: `python scripts/check_nodes.py`.
3. **Verify MCP**: `curl -s http://localhost:8001/health`.
