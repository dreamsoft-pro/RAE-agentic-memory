# RAE Connection & Lumina Wake-up Guide

> **Status:** Verified working as of 2026-01-18.
> **Context:** Phase 5 Infrastructure.

## 1. RAE MCP Configuration (Local)

To connect tools (like `search_memory`) to the local RAE instance:

*   **Config File:** `.claude/mcp.json` (or `.gemini/settings.json`)
*   **URL:** `http://localhost:8001`
*   **Prerequisites:**
    *   Docker container `rae-api-dev` must be running and healthy.
    *   Port 8001 must not be blocked by ghost processes (check `ss -lptn 'sport = :8001'`).
    *   If DNS errors occur (`Temporary failure in name resolution`), restart Docker network:
        ```bash
        docker compose down && docker network prune -f && docker compose up -d rae-api-dev
        ```

## 2. RAE MCP Configuration (Lumina / Node 1)

Lumina is the primary compute node.

*   **IP Address:** `100.68.166.117`
*   **API URL:** `http://100.68.166.117:8001`
*   **SSH Access:** `ssh operator@100.68.166.117`
*   **Working Directory:** `~/rae-node-agent`

### Connecting MCP to Lumina
If local Docker is unstable, you can point MCP directly to Lumina in `.claude/mcp.json`:
```json
"RAE_API_URL": "http://100.68.166.117:8001"
```
*Note: Requires restart of the Agent/IDE to apply config changes.*

## 3. How to Wake Up / Fix Lumina

If `curl 100.68.166.117:8001/health` fails or SSH is refused:

### A. Soft Reset (Services)
If SSH works but API is down:
```bash
ssh operator@100.68.166.117 "cd ~/rae-node-agent && docker compose restart rae-api-dev"
```

### B. Hard Reset (Containers)
If services are stuck or network is broken:
```bash
ssh operator@100.68.166.117 "cd ~/rae-node-agent && docker compose down && docker network prune -f && docker compose up -d"
```

### C. Wake-on-LAN (Physical Wake)
If the machine is powered off (SSH timeout), use Wake-on-LAN from a device on the same local network (e.g., this laptop):
```bash
# Verify MAC address first (usually stored in config/cluster.yaml or known inventory)
# Example command (replace <MAC_ADDRESS> with actual Lumina MAC):
wakeonlan <MAC_ADDRESS>
```
*(Note: Current verified IP is Tailscale IP `100.68.166.117`. WoL requires physical LAN access or a relay).*

## 4. Synchronization Protocol
To push local code changes to Lumina before running benchmarks:
```bash
rsync -avz --no-perms --no-owner --group --exclude '.venv' --exclude '.git' --exclude '__pycache__' --exclude '*.pyc' --exclude 'tmp_node1_sync' ./ operator@100.68.166.117:~/rae-node-agent/
```
