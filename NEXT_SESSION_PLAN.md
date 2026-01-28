# Next Session Plan: Cleanup & Stabilization (Post-ONNX)

## 🛑 Status (Session End)
- **Native ONNX**: Implemented and working locally (Code committed).
- **Linting**: 100% Green (Zero Warnings).
- **Tests**: **FAILED**. `make pre-push` blocked by legacy V1 tests and Hard Frames V1 clients.
- **Git**: Local commits ready (ahead of origin), push blocked by test failures.

## 📋 Immediate Tasks (Next Start)
### 1. 🧹 Purge Legacy V1 Tests
- **Objective**: Remove tests that target the deleted API V1.
- **Action**: Delete `tests/api/v1/` directory (Verify functionality exists in `apps/memory_api/tests/` first).
- **Action**: Update or archive `tests/contracts/` to target V2 schemas.

### 2. 🛠️ Fix Hard Frames Tests
- **Objective**: Align Security/Hard Frames tests with API V2.
- **Action**: Update `tests/hard_frames/test_client.py` to use `/v2/agent/execute` instead of `/v1/agent`.
- **Action**: Ensure `test_api_e2e.py` points to correct local ports.

### 3. ✅ Verify & Push
- **Command**: `make test-lite` (Target: 100% Pass).
- **Command**: `git push origin develop` (Only after tests pass).

### 4. 🚀 Cluster Sync
- **Objective**: Deploy validated ONNX code to Node 1.
- **Action**: `rsync` code to Lumina.
- **Action**: Run benchmarks on Node 1 to verify ONNX speedup.