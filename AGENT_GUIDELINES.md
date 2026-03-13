# GLOBAL AGENT GUIDELINES (CLOUD WORKSPACE)

> **UNIVERSAL PROTOCOL** for all AI Agents operating in the `~/cloud` workspace.
> **MANDATORY**: Read this file immediately upon starting a session.

## 1. 🚨 CRITICAL STARTUP RULE: PROJECT CONFIRMATION

**At the beginning of EVERY session, the Agent MUST:**
1.  **Ask the user:** "Which project are we working on today?" (or similar confirmation).
2.  **Verify the context:** Ensure the current working directory matches the user's intended project.
3.  **Load project-specific rules:** Once the project is confirmed, read the `AGENT_CORE_PROTOCOL.md` (or equivalent) specific to that project (e.g., inside `RAE-agentic-memory/docs/rules/`).

**Why?** The `~/cloud` workspace contains multiple parallel projects (RAE, Screenwatcher, Feniks, etc.). Acting on the wrong project can cause data loss or configuration drift.

## 2. CORE MANDATES (UNIVERSAL)

- **Async-First**: **ALWAYS** use asynchronous connections and operations wherever possible.
- **Autonomy**: Work autonomously but safely. Do NOT ask for permission for standard tasks, but **DO** ask for clarification on ambiguity.
- **Non-Interactive**: **NEVER** use interactive commands (`nano`, `vim`, `git add -i`, `less`). Use `cat`, `sed`, or tool-specific edits.
- **Repository Hygiene**: **NEVER** mix code from other projects. Check `git remote -v` and `git status` constantly.

## 3. WORKFLOW & GIT STRATEGY (4-PHASE)

Strictly follow the flow: `feature/*` → `develop` → `release/*` → `main`.

| Phase | Branch | Action | Protection |
| :--- | :--- | :--- | :--- |
| **1. Dev** | `feature/name` | Create from `develop`. Work here. | Low. Fast iteration. |
| **2. Integ** | `develop` | Merge feature here. **RUN FULL TESTS**. | Medium. Must be stable. |
| **3. QA** | `release/vX` | Create from `develop`. Final QA. | High. 1 Approval. |
| **4. Prod** | `main` | Merge `release` via PR. **HOLY**. | **MAX**. 2 Approvals. |

### STRICT MERGE PROTOCOL (Anti-Data-Loss)
To prevent "lost work" or partial merges, execute this EXACT sequence when finishing a feature:

1. **Update**: `git checkout develop && git pull origin develop`
2. **Merge**: `git merge --no-ff feature/name` (Forces a merge commit for visibility)
3. **Verify (The "Zero-Diff" Check)**:
   - Run: `git log feature/name ^develop` -> **MUST BE EMPTY**
   - Run: `git diff develop...feature/name` -> **MUST BE EMPTY**
   - *If output exists, the merge failed. DO NOT PROCEED.*
4. **Test**: `make lint && make test-unit` (or project equivalent)
5. **Delete**: Only after passing step 3 & 4: `git branch -d feature/name`

## 4. TESTING & QUALITY

- **Zero Warning Policy**: Treat warnings as errors. Fix them immediately.
- **Test First/Test During**: Write tests for new features.
- **Pre-Push Check**: ALWAYS run linters and unit tests locally before pushing to `develop`.

## 5. INFRASTRUCTURE & CLUSTER STRATEGY

- **"Cluster First"**: Offload heavy tasks (benchmarks, training) to dedicated nodes (Lumina, Julia) if available.
- **Node1 (Lumina)**: Primary Compute.
- **Node2 (Julia)**: Secondary Compute.
- **Node3 (Piotrek)**: Inference Engine (LLM/Embeddings).
- **Startup Check**: Run `scripts/connect_cluster.py` (if available in the project) to verify node status.

## 6. DOCUMENTATION

- **Zero Drift**: Keep documentation (`CHANGELOG.md`, `STATUS.md`) synchronized with code changes.
- **Auto-Docs**: Run `make docs` (if available) before pushing.

## 7. RAE-SPECIFIC INTEGRATION

If working on RAE or a project integrated with RAE:
- **RAE-First Communication**: Context exchange should pass through RAE memory.
- **RAE-First Infrastructure**: Use existing Docker containers (`rae-api`, `postgres`) for running tasks.

---
**REMEMBER**: The first step is always **PROJECT CONFIRMATION**.
