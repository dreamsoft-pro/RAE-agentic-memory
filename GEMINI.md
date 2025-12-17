# GEMINI.md – RAE-agentic-memory Code & Tests Assistant

> 🤖 **GEMINI CLI: This file is for you!**
>
> This document contains all the rules and procedures for working on the RAE project.

---

## 🚀 STARTUP PROCEDURE (RAE-First Bootstrapping)

**Gemini CLI: Przy każdej nowej sesji wykonaj to AUTOMATYCZNIE:**

1. **Check Memory**:
   `search_memory(query="project_rules_summary_v1", tags=["system", "rules", "bootstrap"])`

2. **Decision**:
   - **IF FOUND**: Read the summary. Confirm: "✅ Rules loaded from RAE Memory."
   - **IF NOT FOUND**:
     1. Read `CRITICAL_AGENT_RULES.md` and `.ai-agent-rules.md`.
     2. Generate a concise summary (max 500 tokens).
     3. Save to RAE: `save_memory(content=summary, tags=["system", "rules", "bootstrap"], importance=1.0)`
     4. Confirm: "✅ Rules cached in RAE."

3. **Communication Protocol**:
   - **Treat RAE as the primary communication channel.**
   - Before responding to complex tasks, check if another agent has context: `search_memory(query="task_context", tags=["handoff", "status"])`
   - Save your final status updates to RAE: `save_memory(content="Task complete...", tags=["status", "handoff"])`

4. **Confirm Rules**:
   "I have read and understood the rules via RAE/Files. I will follow:
   - 3-phase testing workflow (--no-cov on feature, make test-unit on develop)
   - No interactive commands (nano, vim, git -i)
   - Always include tenant_id in SQL queries
   - Fix code, not tests (unless tests are wrong)
   - Use .ai-templates/ for new code"

Then check if I'm connected to RAE via MCP.

**User: After Gemini has read the above prompt, continue with the normal task.**

---

## 🧠 RAE Multi-Agent Memory

**Gemini: You are connected to RAE via MCP!**

Available tools:
- `save_memory` - Save decision, progress, problem to shared memory
- `search_memory` - Search what other agents (Claude, other Gemini) have done
- `get_related_context` - Get context about a file

**Use this whenever:**
- ✅ You complete a workflow step (save progress)
- ✅ You fix a bug (save what and why)
- ✅ You make a decision (save reasoning)
- ✅ You find something important (save for others)

**Tenant**: `meta-development`
**Project**: `gemini-rae-collaboration`

Przykład:
```
save_memory(
  content="Fixed critical bug in qdrant.py: implemented missing abstract methods",
  source="gemini-cli-bugfix",
  layer="episodic",
  tags=["bug-fix", "qdrant", "critical"],
  importance=0.9
)
```

---

## 🚨 MANDATORY READING (Read after startup!)

**⚠️ These documents contain critical rules!**

1. **[CRITICAL_AGENT_RULES.md](./CRITICAL_AGENT_RULES.md)** (5 min) ⭐ - 8 MANDATORY rules
2. **[AI_AGENT_MANIFEST.md](./AI_AGENT_MANIFEST.md)** (3 min) - Documentation hierarchy and navigation
3. **[.ai-agent-rules.md](./.ai-agent-rules.md)** (5 min) - Forbidden commands and testing strategy
4. **[docs/BRANCHING.md](./docs/BRANCHING.md)** (3 min) - Git Workflow (feature → develop → main)
5. **[docs/AGENTS_TEST_POLICY.md](./docs/AGENTS_TEST_POLICY.md)** (3 min) - Tests as a contract

**Without reading = workflow violation = blocking other developers!**

---

## 🎯 Quick Reminders of Key Principles

Before each task, remember:

- ❌ **NEVER** run the full test suite on a feature branch (only `--no-cov`)
- ✅ **ALWAYS** work autonomously (don't ask obvious questions)
- ✅ **ALWAYS** include `tenant_id` in SQL queries (security!)
- ❌ **NEVER** use interactive commands (nano, vim, git -i)
- ✅ **ALWAYS** use templates from `.ai-templates/`
- ✅ If a test fails - fix the **code**, not the test (unless the test was written incorrectly)
- ❌ **STRICTLY FORBIDDEN**: Mixing repositories! Do not commit code from other projects to the current repository. Check `git status` before every commit.

**Details**: See [CRITICAL_AGENT_RULES.md](./CRITICAL_AGENT_RULES.md)

---

## 🔄 3-Phase Testing Workflow (CRITICAL!)

**MOST IMPORTANT RULE**: Different phases = different testing levels!

```
┌──────────────────────────────────────────────────────┐
│ PHASE 1: FEATURE BRANCH                              │
│ ✅ Test ONLY your new code: pytest --no-cov path/   │
│ ✅ make format && make lint (MANDATORY!)           │
│ ✅ Commit when tests pass                            │
├──────────────────────────────────────────────────────┤
│ PHASE 2: DEVELOP BRANCH (MANDATORY!)                │
│ ✅ git checkout develop && git merge feature/X      │
│ ✅ make test-unit   ← MANDATORY before main!       │
│ ✅ make lint                                         │
│ ❌ NEVER proceed to main if tests fail!             │
├──────────────────────────────────────────────────────┤
│ PHASE 3: MAIN BRANCH                                │
│ ✅ git checkout main && git merge develop           │
│ ✅ git push origin main develop                     │
│ ✅ CI tests automatically                           │
│ ❌ NEVER leave main with red CI!                    │
└──────────────────────────────────────────────────────┘
```

### Why 3 phases?

1. **Feature branch** (`--no-cov`):
   - Fast feedback (seconds instead of minutes)
   - Test only your code
   - Save CI credits

2. **Develop branch** (`make test-unit` MANDATORY):
   - Full validation before production
   - Detects conflicts with other code
   - Last chance to fix before main

3. **Main branch** (CI automatic):
   - Production code
   - CI runs everything automatically
   - MUST always be green

**⚠️ GEMINI: This is the most critical rule! Do not skip `make test-unit` on develop!**

---

## ✅ Checklist Before Every Commit

Before you `git commit`, check:

```
[ ] Tested ONLY my new code on feature branch (pytest --no-cov)
[ ] make format passed (black + isort + ruff)
[ ] make lint passed (no errors)
[ ] Used templates from .ai-templates/
[ ] tenant_id included in ALL database queries
[ ] No interactive commands in code (nano, vim, git -i)
[ ] Docstrings added (Google style)
[ ] Will run make test-unit on develop before main
```

**If even one point is NO, then do NOT commit!**

---

## 📝 Documentation: Auto vs Manual (RULE #8)

### ❌ DO NOT EDIT (CI updates automatically):
- `CHANGELOG.md` - Git commit history
- `STATUS.md` - Live project metrics
- `TODO.md` - Extracted TODOs/FIXMEs
- `docs/TESTING_STATUS.md` - Test results
- `docs/.auto-generated/` - All auto-generated files

### ✅ EDIT (Your responsibility):
- `CONVENTIONS.md` - New patterns/conventions
- `PROJECT_STRUCTURE.md` - New file locations
- `docs/guides/` - Feature guides
- `.ai-templates/README.md` - Template changes

**⚠️ If you edit an auto-generated file, your changes will be overwritten!**

---

## 0. Project Context

You are working on the **RAE-agentic-memory** repository.

Main assumptions:
- Python code (backend, memory layers, API, etc.).
- Tests in `pytest`.
- The project has:
  - unit, integration, and e2e tests,
  - architectural and contract tests,
  - an extensive directory structure (API, core, memory services, etc.).
- The goal is to **gradually improve code quality and test coverage**, while maintaining:
  - stable CI,
  - reasonable test execution time,
  - compliance with the existing architecture.

---

## 1. Main Assistant Goal

Your task is to:

1. **Improve test and code quality**:
   - increase test coverage in the most critical modules,
   - improve code readability, consistency, and testability,
   - maintain existing architecture (no revolutions).

2. **Avoid loops and unnecessary operations**:
   - do not repeatedly execute the same commands,
   - do not repeatedly touch files that are already "DONE" for a given task.

3. **Respect the existing ecosystem**:
   - do not modify code in `.venv/` or dependency directories,
   - do not "fix the world" – focus on this repository and the specific goal.

---

## 2. General Operating Strategy (Workflow)

Execute each task in four steps:

1. **PLAN**
   - Read the files related to the task.
   - Create a short plan (max 5 points):
     - what you want to change,
     - which files you will touch,
     - which tests you will run.

2. **EDITS**
   - Make changes in **small increments**.
   - After each major change:
     - perform a check like `pytest path/to/tests_for_that_module` instead of a full `pytest` on the entire repo.

3. **TESTS**
   - At the end of the task, run **exactly one full**:
     - `pytest` or `pytest` with appropriate markers (e.g., without `slow`, if configured this way).
   - If full tests have already passed and you are not changing anything else – **do not run them again**.

4. **SUMMARY**
   - List:
     - what has been changed (list of files),
     - which tests were run and with what result,
     - what is the effect on coverage / quality.

---

## 3. ANTI-LOOP Rules

Avoid loops according to the following rules:

1. **Do not repeat without changes**  
   - Do not run the same `pytest` command a second time in a row if, since the previous run:
     - you have not changed any code files,
     - you have not changed any test files.

2. **No tinkering in `.venv` and dependencies**
   - Never modify:
     - files in `.venv/`,
     - dependency code (`site-packages`, vendor, etc.).
   - If you see warnings (`DeprecationWarning`, etc.) from libraries:
     - at most, you can propose adding `filterwarnings` in `pytest.ini` or a short note in the documentation,
     - but do not change library code.

3. **Files marked "done" are untouchable**  
   - If the user or task states that a test/code file is already "DONE" (e.g., `tests/api/v1/test_memory.py` has 100% coverage):
     - **do not edit it** in this task,
     - do not specifically run tests only for it,
     - you can at most read it as an example.

4. **Attempt limit per task**
   - If:
     - three times in a row you make changes and still do not achieve the desired effect, or
     - three times in a row the full tests pass, and you still want to improve something "just in case",
   - then **stop** and:
     - describe what you have already done,
     - describe what is blocking you,
     - suggest what the user should clarify.

5. **Monitor your own behavior**
   - If you notice that:
     - you are reading the same files over and over,
     - you are running the same commands over and over,
   - treat this as a sign of a loop and **end the task with a short report** instead of continuing.

---

## 4. Test and Coverage Strategies

### 4.1. Priorities

Instead of "raising global coverage at all costs", prefer:

1. **Critical modules**:
   - memory (store/retrieve),
   - API that is public to users / other systems,
   - logic related to security, access control, data validation.

2. **Fast tests > slow tests**:
   - prefer unit tests over integrations,
   - prefer integrations over full e2e.

### 4.2. Workflow for one module

For a selected module (e.g., `apps/.../memory.py` and its corresponding `tests/.../test_memory.py`):

1. Read the module code and current tests.
2. Identify **uncovered or poorly covered paths**:
   - rare `if` branches,
   - unusual errors/exceptions,
   - edge cases.
3. Write tests that:
   - are **small** and **do not depend on external services**, if possible,
   - use fixtures and parameters instead of duplicating logic.
4. Run:
   - `pytest path/to/tests_for_that_module`.
5. If tests pass:
   - run full `pytest` **once** at the end of the task.

---

## 5. Warning Handling

1. **Warnings from project code (Your modules)**:
   - treat as a design error,
   - fix code/configuration to remove them, if the change is safe.

2. **Warnings from tests**:
   - if the test is written incorrectly (e.g., unused fixture, non-awaited coroutine),
     - fix the tests.

3. **Warnings from external libraries**:
   - **do not change** library code.
   - if the user wishes:
     - propose adding appropriate `filterwarnings` in `pytest.ini`
       with a clear comment about the origin of the warning and why it is being ignored.

---

## 6. Boundaries and Things You DO NOT Do

- Do not:
  - change code in `.venv/`, `site-packages`, etc.
  - disable tests without a clear reason (and without a comment).
  - modify CI configuration (e.g., GitHub Actions) unless explicitly requested by the user and with a clear purpose.
  - rearrange project architecture (e.g., changing directory structure, main modules) – your role is **evolutionary refactoring**, not revolutionary.

- You may:
  - improve styles/typing/minor errors in files where you are working on tests,
  - propose minor refactors (e.g., extracting functions) if they clearly improve testability.

---

## 7. Task Completion Conditions

Consider the task complete if:

1. The scope defined by the user (e.g., "module X + tests") is:
   - covered by a reasonable number of tests,
   - tests pass locally.

2. Full tests:
   - have been run **once at the end**,
   - have passed (or you clearly describe which ones failed and why – if it's outside the scope of the task).

3. You list:
   - modified files,
   - new tests/scenarios,
   - a brief description of the impact on quality (coverage / stability),
   - TODOs for the future, if you noticed something that goes beyond the current goal.

After these conditions are met, **do not make further changes** – finish the work and await further user instructions.
