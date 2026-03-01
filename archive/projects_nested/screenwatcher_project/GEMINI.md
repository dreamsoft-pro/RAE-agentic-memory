# Gemini Agent Rules for RAE Project

## 🚀 SESSION STARTUP PROTOCOL (EXECUTE FIRST)

**Step 1: Connect via RAE-First (MCP Wrapper)**
> **MANDATORY**: Execute the bridge script to connect to the Hive Mind.
> ```bash
> python3 scripts/connect_rae_mcp.py
> ```
> This script uses `docker exec` to bypass host limitations and communicates with RAE via the `rae-api-dev` container.

**Step 2: Read the Map**
> Read **`DEVELOPER_CHEAT_SHEET.md`** (if available) or check `scripts/` for available tools.

---

This document contains key operational rules for AI agents working on the RAE (Robotic Agent Emulation) project.

## 🚨 Critical Rules - MUST FOLLOW

### 1. **No Interactive Commands**
- **NEVER** use interactive commands (`nano`, `vim`, `git add -i`).
- **ALLOWED**: `cat`, `grep`, `sed`, `git add .`.

### 2. **RAE & Communication**
- **ALWAYS** use `scripts/connect_rae_mcp.py` to fetch context and log session starts.
- Do NOT rely on host-level python packages for RAE communication.

### 3. **Docker Development Workflows**
- **Use Profiles**: Employ `dev`, `standard`, `lite` profiles.
- **MCP Port**: RAE listens on port `8001` (host) / `8000` (container internal).