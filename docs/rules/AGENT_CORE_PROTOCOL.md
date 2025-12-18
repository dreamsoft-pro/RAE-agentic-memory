# AGENT CORE PROTOCOL (v2.0)

> **SINGLE SOURCE OF TRUTH** for all AI Agents (Gemini, Claude, etc.) working on RAE.
> **MANDATORY**: Read this before every session.

## 1. CORE MANDATES

- **Autonomy**: Work autonomously. Do NOT ask for permission to create files, add tests, or commit standard work.
- **Security**: **ALWAYS** include `tenant_id` in SQL queries. This is a multi-tenant system.
- **Non-Interactive**: **NEVER** use interactive commands (`nano`, `vim`, `git add -i`, `less`). Use `cat`, `sed`, or tool-specific edits.
- **Templates**: **ALWAYS** start with templates from `.ai-templates/` (Repo, Service, Route, Test). Do NOT write from scratch.
- **Repository Hygiene**: **NEVER** mix code from other projects. Check `git remote -v` and `git status` constantly.

## 2. WORKFLOW & GIT STRATEGY (4-PHASE)

Strictly follow the flow: `feature/*` → `develop` → `release/*` → `main`.

| Phase | Branch | Action | Protection |
| :--- | :--- | :--- | :--- |
| **1. Dev** | `feature/name` | Create from `develop`. Work here. | Low. Fast iteration. |
| **2. Integ** | `develop` | Merge feature here. **RUN FULL TESTS**. | Medium. Must be stable. |
| **3. QA** | `release/vX` | Create from `develop`. Final QA. | High. 1 Approval. |
| **4. Prod** | `main` | Merge `release` via PR. **HOLY**. | **MAX**. 2 Approvals. |

**Crucial**:
- **NEVER** push directly to `main` or `release` (except PRs).
- **NEVER** leave `main` or `develop` with red CI.

## 3. TESTING PROTOCOL

Different branches = Different testing levels.

### Phase 1: Feature Branch (`feature/*`)
- **Goal**: Speed & Focus.
- **Command**: `pytest --no-cov path/to/new_test.py`
- **Rule**: Test **ONLY** your new code. Do NOT run full suite.

### Phase 2: Develop Branch (`develop`)
- **Goal**: Integrity & Regression.
- **Command**: `make test-unit` (and `make lint`)
- **Rule**: **MANDATORY** before proceeding to Release/Main. Fix ALL failures here.

### Phase 3: Main/Release
- **Goal**: Production Guarantee.
- **Command**: CI (GitHub Actions).
- **Rule**: If CI fails, fix immediately on `develop` and propagate up.

## 4. DOCUMENTATION STRATEGY

- **Auto-Generated (DO NOT EDIT)**: `CHANGELOG.md`, `STATUS.md`, `TODO.md`, `docs/.auto-generated/`.
- **Manual (EDIT THESE)**: `CONVENTIONS.md`, `PROJECT_STRUCTURE.md`, `docs/guides/`, `.ai-templates/`.

## 5. SESSION STARTUP ROUTINE

1. **Read Protocol**: Read this file (`docs/rules/AGENT_CORE_PROTOCOL.md`).
2. **Check Context**: Use `search_memory` (if available) for recent agent activity.
3. **Plan**: Create a plan/todo list before editing code.

## 6. HIGH STANDARDS & QUALITY GATES

- **Zero Warning Policy**: Treat warnings as errors. Fix them immediately. Do not ignore them.
- **No Drift**: Ensure architectural decisions are persistent. Do not re-introduce fixed bugs or deprecated patterns.
- **Best Practices**:
  - **Clean Code**: Follow SOLID, DRY, and KISS principles.
  - **Type Safety**: strict `mypy` compliance.
  - **Documentation**: Keep docs in sync with code (especially `CONVENTIONS.md`).
- **Definition of Done**:
  - Tests passed (Green).
  - Linter passed (No warnings).
  - Documentation updated.
  - PR ready for review.

---
**Violation Consequences**:
- Blocking other devs (broken develop/main).
- Security leaks (missing `tenant_id`).
- Wasted CI credits (full tests on feature branches).

## 7. RESOURCE & COMMUNICATION EFFICIENCY

- **RAE First**: **ALWAYS** consult RAE (memory/context) first. Input/Output MUST flow through RAE to minimize token usage.
- **Model Economy**: Use cheaper/lighter models for simple tasks (formatting, basic logic). Reserve SOTA models for complex reasoning.
- **Rate Limits (CLI)**: **STRICTLY** adhere to Requests Per Minute (RPM) limits. This applies especially to Gemini CLI.
- **Quality Over Speed**: Do not rush. "Done Well" > "Done Fast". Take time to verify. Correctness is paramount.
