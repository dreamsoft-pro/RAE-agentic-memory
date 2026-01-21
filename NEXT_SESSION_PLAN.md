# RAE SESSION PLAN

## 🚀 PRIORITY: 100k Memory Hard Frames Stress Test (CLUSTER)

**Context:** Local tests for "Hard Frames" passed (Physical/Protocol/Semantic containment). Now we must test **System Degradation** at scale (100k memories) on Node 1 (Lumina).

### 📋 Checklist for Lumina Session:
1.  **Sync Code:**
    ```bash
    rsync -avz --exclude '.git' --exclude '__pycache__' ./ operator@100.68.166.117:~/rae-node-agent/
    ```
2.  **Remote Startup (Lumina):**
    *   SSH into Lumina.
    *   Build the secure agent:
        ```bash
        docker compose -f docker-compose.secure.yml -p hard_frames up -d --build
        ```
3.  **Execute Stress Test:**
    *   We need to verify if the Agent degrades safely when flooded with 100k memories.
    *   Run the degradation test suite in a loop:
        ```bash
        .venv/bin/pytest tests/hard_frames/test_degradation_stability.py
        ```
    *   *Note:* Real 100k injection might require connecting the `rae-kernel` to the real Qdrant on Lumina (edit `docker-compose.secure.yml` on remote to point to `rae-qdrant`).

## 🛠️ Pending Tasks
- [ ] Refactor `rae-sdk` to be fully compliant with the new Thin Client protocol.
- [ ] Merge "Hard Frames" into `develop` once 100k test passes.
