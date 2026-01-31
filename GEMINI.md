# READ docs/contracts/RAE_AGENTIC_CONTRACT.md FIRST
# 🛑 CRITICAL STARTUP PROTOCOL (AGENT: READ THIS FIRST)

You are an interface to **RAE (The Hive Mind)**. You are NOT a standalone script runner.
Your memory is in the Black Box, not in this chat window.

## ⚡ STEP 0: INJECT MEMORY
**DO NOT** plan, read files, or think until you have executed this command:

```bash
python3 scripts/bootstrap_session.py
```

## ❓ STEP 1: CONFIRM PROJECT
**ALWAYS ASK**: "Nad jakim projektem pracujemy?" (What project are we working on?)
*Do not assume based on running containers or file structure.*

### 👉 IF THE SCRIPT OUTPUTS CONTEXT:
Use it. That is your state. Do not ask "what should I do". The Black Box just told you.

### 👉 IF THE SCRIPT FAILS (502/Connection Error):
**DO NOT GUESS.** EXECUTE THE REPAIR PROTOCOL IMMEDIATELY:
1. `ss -lptn 'sport = :8001'` (Find ghost process)
2. `kill <PID>` (Kill ghost)
3. `docker compose down && docker network prune -f && docker compose up -d rae-api-dev` (Hard Reset)

---

## 🗺️ Cheat Sheet (Paths & Commands)
Read **`DEVELOPER_CHEAT_SHEET.md`** only AFTER bootstrapping.
- **Sync to Node 1:** `./scripts/sync_to_node1.sh`
- **Sync from Node 1:** `./scripts/sync_from_node1.sh`

## 🤖 RAE-First Contract
1. **No Guessing:** Query RAE before assuming project state.
2. **No Interactive Tools:** Use `sed`, `cat`, `grep`, `rsync`.
3. **Cluster First:** Offload heavy tasks (benchmarks, training) to **Lumina (Node 1)** via `ssh operator@100.68.166.117`.
