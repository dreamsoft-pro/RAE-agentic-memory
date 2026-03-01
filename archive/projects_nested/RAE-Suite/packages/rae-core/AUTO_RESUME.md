# 🛑 STOP! READ THIS BEFORE STARTING THE SESSION

## 🛠 Project Context: RAE Silicon Oracle
Building the **Silicon Oracle** (System 86.0). Deterministic, tiered retrieval.

## 📍 Infrastructure Procedures (Tailscale Active Required):
1. **Waking Lumina (Node 1):** 
   If Node 1 is offline, run: `./scripts/wake_lumina.sh` (This uses VAIO @ 100.78.171.96 as a jump-host).
2. **Syncing Code:**
   Push local changes to Node 1 via: `./scripts/sync_to_node1.sh`.
   Note: Node 1 IP is `100.68.166.117`.
3. **Execution Node:**
   Always run heavy benchmarks on Node 1 (Lumina) via SSH.

## 📍 Critical Code Locations:
- **Core Math:** `rae-core/rae_core/math/logic_gateway.py` (Current: 86.0)
- **Dataset:** `benchmarking/sets/industrial_10k.yaml` (NOW UNIQUE - DO NOT REGENERATE WITHOUT SNIPER LOGIC).
- **API Dev:** Port 8001.

## 🚀 Current Metrics (MRR @ 10k Unique):
- **0.8583** (Record high).
- **Target:** 1.0 (requires Graph Reasoning).

## ⚡ Mandatory Startup:
```bash
python3 scripts/bootstrap_session.py
```

## ⚠️ API v2 Compatibility:
Pydantic validation was relaxed to support MCP tools. DO NOT RESTRICT without testing.