# NEXT SESSION PLAN: GPU Acceleration & External Integration (v3.5.0-dev)

## 🎯 Strategic Goals
1.  **Hardware Acceleration**: Enable CUDA support for Native ONNX in the `standard` (Full) profile.
2.  **External Connectivity**: Implement API and MCP backends for Embeddings and Reranking.
3.  **Config Consolidation**: Move all hardcoded engine parameters to `config/math_controller.yaml`.

---

## 🛠️ Task Breakdown

### 1. CUDA & GPU Support (Standard Profile)
- **Library Upgrade**: Switch from `onnxruntime` to `onnxruntime-gpu` in `requirements.txt` for the Full image.
- **Provider Logic**: Update `NativeEmbeddingProvider` to detect CUDA and automatically select `CUDAExecutionProvider` if `RAE_USE_GPU=True`.
- **Docker Integration**: Update `docker-compose.yml` to include `deploy.resources.reservations.devices` for NVIDIA GPU access.

### 2. External Embedding & Reranking (API/MCP)
- **Backend Expansion**: Extend `RAE_EMBEDDING_BACKEND` to support `api` (OpenAI/LiteLLM compatible) and `mcp` (Model Context Protocol tool calls).
- **Reranking Plugability**: Refactor `HybridSearchEngine` to allow `external_reranker` via MCP tools or remote API endpoints.
- **Protocol Discovery**: Implement automatic tool discovery for MCP-based embedding providers.

### 3. Configuration Externalization
- **Engine Parameters**: Move `limit=100` (candidate window), `resonance_threshold`, and `szubar_induction_energy` from `engine.py` to `config/math_controller.yaml`.
- **Environment Toggles**: Add `.env` flags for:
    - `RAE_USE_GPU`: (bool) Enable/disable CUDA.
    - `RAE_RERANKER_BACKEND`: (`local`, `api`, `mcp`).
    - `RAE_MCP_EMBEDDING_TOOL`: Tool name for MCP embeddings.

---

## 🚀 Initialization Commands
`python3 scripts/bootstrap_session.py`
`docker compose --profile dev up -d`

---

## 📝 Memory Snapshot (RAE-RM)
- Current State: **System 3.4 (Silicon Oracle)** stable at 100k mems (MRR 0.85).
- Constraint: Maintain **Zero Warning Policy** and **RAE-First** communication.
- Focus: Transition from "Local-Only" to **"Hardware-Optimized & Mesh-Connected"**.