# 🛑 CRITICAL STARTUP PROTOCOL (AGENT: READ THIS FIRST)

You are in the **CLOUD ROOT** directory. You are managing multiple projects (Dreamsoft Pro, ScreenWatcher, Billboard Splitter).

## ⚡ STEP 0: INJECT SESSION CONTEXT
**DO NOT** plan or read files until you have executed this command:

```bash
python3 scripts/bootstrap_cloud.py
```

### 👉 IF THE SCRIPT OUTPUTS A PLAN:
Follow it. It contains the current state of infrastructure (Lumina vs Laptop), port mappings, and the "Operacja Lustro" roadmap.

### 👉 CURRENT FOCUS:
Modernization of Dreamsoft Pro 2.0 (Next.js + PHP API).
- Baza danych zsynchronizowana na Node 1 (Lumina).
- Frontend Next.js na porcie 3005 (Laptop).
- Stary system na porcie 8081 (Laptop).

## 🔐 INFRASTRUCTURE & AUTH
- **GitHub Auth:** ALWAYS use SSH keys. Use `GIT_SSH_COMMAND="ssh -o BatchMode=yes"` to avoid interactive passphrase prompts.
- **Node 1 (Lumina):** DO NOT connect unless explicitly requested.
- **Persistence:** Use Bind Mounts for local data to ensure memory survives code changes.
