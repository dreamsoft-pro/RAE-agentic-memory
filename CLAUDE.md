# CLAUDE.md – RAE Project Guide for Claude Code

> 🤖 **Welcome, Claude Code!** This guide is specifically designed for you (Claude Code CLI) and your unique capabilities.

> **🧠 RAE-FIRST BOOTSTRAPPING (Token Saving)**
>
> **Agent: Execute this sequence BEFORE reading files:**
>
> 1. **Check Memory**:
>    `search_memory(query="project_rules_summary_v1", tags=["system", "rules", "bootstrap"])`
>
> 2. **Decision Tree**:
>    - **IF FOUND**: Read the summary. Confirm: "✅ Rules loaded from RAE Memory."
>    - **IF NOT FOUND**:
>      1. Read `CRITICAL_AGENT_RULES.md` and `.ai-agent-rules.md`.
>      2. Generate a concise summary (max 500 tokens).
>      3. Save to RAE: `save_memory(content=summary, tags=["system", "rules", "bootstrap"], importance=1.0)`
>      4. Confirm: "✅ Rules cached in RAE."
>
> 3. **Communication Protocol**:
>    - All substantial reasoning, decisions, and status updates MUST be saved to RAE.
>    - Use `save_memory` for "working memory" of the current session.
>    - Use `search_memory` to retrieve context from other agents (Claude/Gemini).

---

## 🚨 BEFORE STARTING - MANDATORY READING (15 minutes)

**⚠️ CRITICAL**: Read these documents IN THIS ORDER:

1. **[CRITICAL_AGENT_RULES.md](./CRITICAL_AGENT_RULES.md)** (5 min) ⭐ - 8 MANDATORY rules
2. **[AI_AGENT_MANIFEST.md](./AI_AGENT_MANIFEST.md)** (3 min) - Documentation hierarchy and navigation
3. **[.ai-agent-rules.md](./.ai-agent-rules.md)** (5 min) - Forbidden commands and testing strategy
4. **[docs/BRANCHING.md](./docs/BRANCHING.md)** (3 min) - Git Workflow (feature → develop → main)
5. **[docs/AGENTS_TEST_POLICY.md](./docs/AGENTS_TEST_POLICY.md)** (3 min) - Tests as a contract

**DO NOT start work without reading the above documents!**

---

## 🎯 Quick Reminder of Key Principles

Before each task, remember:

- ❌ **NEVER** run the full test suite on a feature branch (only `pytest --no-cov path/`)
- ✅ **ALWAYS** work autonomously (don't ask obvious questions)
- ✅ **ALWAYS** include `tenant_id` in SQL queries (security!)
- ❌ **NEVER** use interactive commands (nano, vim, git -i)
- ✅ **ALWAYS** use templates from `.ai-templates/`
- ✅ **ALWAYS** run `make format && make lint` before committing
- ✅ If a test fails - fix the **code**, not the test (unless the test was written incorrectly)

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

---

## 🛠️ Claude Code - Your Unique Capabilities

### Native Tools

As Claude Code, you have access to special tools that other agents do not:

#### 1. **Task Tool** - Running Specialized Agents

```python
# Use the Explore agent to explore the codebase
Task(
    subagent_type="Explore",
    description="Find memory storage implementation",
    prompt="Search for memory storage and retrieval patterns in the codebase"
)

# Use the Plan agent to plan complex changes
Task(
    subagent_type="Plan",
    description="Plan authentication refactor",
    prompt="Design implementation plan for adding OAuth2 authentication"
)
```

**When to use the Task tool:**
- ✅ Codebase exploration (Explore agent)
- ✅ Planning complex changes (Plan agent)
- ✅ Tasks requiring multiple steps
- ✅ Searching when unsure of location

**When NOT to use the Task tool:**
- ❌ When you know the exact file path → use Read
- ❌ Searching for a specific class → use Glob
- ❌ Simple one-step tasks

#### 2. **TodoWrite Tool** - Tracking Progress

**CRITICAL**: Use TodoWrite for multi-step tasks!

```python
TodoWrite(todos=[
    {"content": "Create repository layer", "status": "in_progress", "activeForm": "Creating repository layer"},
    {"content": "Create service layer", "status": "pending", "activeForm": "Creating service layer"},
    {"content": "Create API routes", "status": "pending", "activeForm": "Creating API routes"},
    {"content": "Write tests", "status": "pending", "activeForm": "Writing tests"},
    {"content": "Run make format && make lint", "status": "pending", "activeForm": "Running format and lint"}
])
```

**TodoWrite Rules:**
- ✅ Create todo lists for tasks > 3 steps
- ✅ ALWAYS have exactly ONE task as "in_progress"
- ✅ Mark as "completed" IMMEDIATELY after completion
- ✅ Use imperative form for "content", continuous for "activeForm"

#### 3. **Parallel Tool Execution**

Claude Code can run multiple tools in parallel!

**GOOD** - parallel when no dependencies:
```python
# Read multiple files at once
Read("apps/memory_api/repositories/memory_repo.py")
Read("apps/memory_api/services/memory_service.py")
Read("apps/memory_api/api/v1/memory_routes.py")
```

**BAD** - sequential when there are dependencies:
```python
# First read file
result = Read("config.py")
# Then use value from file in next command
Bash(f"export API_KEY={value_from_config}")
```

#### 4. **WebSearch & WebFetch**

You have internet access!

```python
# Search for current information
WebSearch(query="FastAPI dependency injection best practices 2025")

# Fetch specific URL
WebFetch(
    url="https://docs.python.org/3/library/asyncio.html",
    prompt="Explain how to handle asyncio task cancellation"
)
```

#### 5. **Native Git Integration**

You can directly use the Bash tool for git:

```bash
# Everything in one line with &&
git add . && git commit -m "feat: add feature" && git push origin develop
```

**⚠️ REMEMBER**: ALWAYS use `git commit -m "..."` (NEVER without -m!)

---

## ✅ Pre-Commit Checklist (Check before every commit!)

```
[ ] Tested ONLY new code on feature branch (pytest --no-cov path/)
[ ] make format passed (black + isort + ruff)
[ ] make lint passed (no errors)
[ ] Used templates from .ai-templates/
[ ] tenant_id included in ALL database queries
[ ] No interactive commands in code
[ ] Docstrings added (Google style)
[ ] TodoWrite updated (if multi-step task)
[ ] Will run make test-unit on develop before main
```

---

## 🎓 Best Practices for Claude Code

### 1. **Codebase Exploration**

**BAD** - direct search:
```python
Grep(pattern="memory.*store", path="apps/")
Read("apps/memory_api/services/memory_service.py")
# ... more manual searching
```

**GOOD** - use the Explore agent:
```python
Task(
    subagent_type="Explore",
    description="Find memory storage patterns",
    prompt="How is memory stored and retrieved in the RAE system? Find all relevant files and patterns."
)
```

### 2. **Planning Complex Changes**

**For large features (> 5 files or > 100 lines):**

```python
# Use the Plan agent
Task(
    subagent_type="Plan",
    description="Plan notification system",
    prompt="""
    Design implementation plan for user notification system:
    - Email and in-app notifications
    - Multi-tenant support
    - Async delivery
    - Follow RAE 3-layer architecture
    """
)
```

### 3. **Parallel File Reading**

```python
# ✅ GOOD - all Reads in one message
Read("apps/memory_api/models/memory.py")
Read("apps/memory_api/models/tenant.py")
Read("apps/memory_api/models/user.py")

# ❌ BAD - sequential reading in separate messages
# (slower, wastes time)
```

### 4. **Using TodoWrite for Clarity**

```python
# At the beginning of the task
TodoWrite(todos=[
    {"content": "Analyze existing code", "status": "in_progress", "activeForm": "Analyzing existing code"},
    {"content": "Create repository", "status": "pending", "activeForm": "Creating repository"},
    {"content": "Create service", "status": "pending", "activeForm": "Creating service"},
    {"content": "Create API routes", "status": "pending", "activeForm": "Creating API routes"},
    {"content": "Write tests", "status": "pending", "activeForm": "Writing tests"},
    {"content": "Run format and lint", "status": "pending", "activeForm": "Running format and lint"}
])

# After each step
TodoWrite(todos=[
    {"content": "Analyze existing code", "status": "completed", "activeForm": "Analyzing existing code"},
    {"content": "Create repository", "status": "in_progress", "activeForm": "Creating repository"},
    # ... rest
])
```

---

## 🚫 Most Common Errors (Avoid!)

### ❌ Error #1: Running full tests on a feature branch

```bash
# ❌ BAD on feature branch
make test-unit  # This will take forever and might fail due to coverage!

# ✅ GOOD on feature branch
pytest --no-cov apps/memory_api/tests/test_my_new_feature.py
```

### ❌ Error #2: Forgetting about format/lint

```bash
# ❌ BAD
git add . && git commit -m "feat: add feature"

# ✅ GOOD
make format && make lint && git add . && git commit -m "feat: add feature"
```

### ❌ Error #3: Using interactive commands

```bash
# ❌ BAD - hangs!
nano file.py
vim file.py
git commit  # Opens editor - hangs!

# ✅ GOOD
Edit(file_path="file.py", old_string="...", new_string="...")
git commit -m "message"
```

### ❌ Error #4: Editing auto-generated files

```bash
# ❌ BAD - CI will overwrite!
Edit("CHANGELOG.md", ...)
Edit("STATUS.md", ...)
Edit("TODO.md", ...)

# ✅ GOOD - edit manual docs only
Edit("CONVENTIONS.md", ...)
Edit("docs/guides/new_feature.md", ...)
```

### ❌ Error #5: Missing tenant_id in queries

```python
# ❌ BAD - security vulnerability!
query = "SELECT * FROM entities WHERE id = $1"

# ✅ GOOD
query = "SELECT * FROM entities WHERE id = $1 AND tenant_id = $2"
```

---

## 📋 Example Workflow for a New Feature

### Scenario: Add a notification system

```python
# 1. Read documentation (MANDATORY!)
Read("PROJECT_STRUCTURE.md")
Read("CONVENTIONS.md")
Read(".ai-templates/README.md")

# 2. Create todo list
TodoWrite(todos=[
    {"content": "Read documentation", "status": "completed", "activeForm": "Reading documentation"},
    {"content": "Explore existing notification patterns", "status": "in_progress", "activeForm": "Exploring notification patterns"},
    {"content": "Design notification system", "status": "pending", "activeForm": "Designing notification system"},
    {"content": "Create repository layer", "status": "pending", "activeForm": "Creating repository layer"},
    {"content": "Create service layer", "status": "pending", "activeForm": "Creating service layer"},
    {"content": "Create API routes", "status": "pending", "activeForm": "Creating API routes"},
    {"content": "Write tests", "status": "pending", "activeForm": "Writing tests"},
    {"content": "Run format and lint", "status": "pending", "activeForm": "Running format and lint"},
    {"content": "Test on feature branch", "status": "pending", "activeForm": "Testing on feature branch"}
])

# 3. Use the Explore agent
Task(
    subagent_type="Explore",
    description="Find notification patterns",
    prompt="Search for any existing notification or alerting patterns in the codebase"
)

# 4. Copy template
Bash("cp .ai-templates/repository_template.py apps/memory_api/repositories/notification_repository.py")

# 5. Implement (using Edit tool)
Edit(
    file_path="apps/memory_api/repositories/notification_repository.py",
    old_string="class TemplateRepository:",
    new_string="class NotificationRepository:"
)
# ... more edits

# 6. Update TodoWrite after each step
TodoWrite(todos=[
    {"content": "Read documentation", "status": "completed", "activeForm": "Reading documentation"},
    {"content": "Explore existing notification patterns", "status": "completed", "activeForm": "Exploring notification patterns"},
    {"content": "Design notification system", "status": "completed", "activeForm": "Designing notification system"},
    {"content": "Create repository layer", "status": "completed", "activeForm": "Creating repository layer"},
    {"content": "Create service layer", "status": "in_progress", "activeForm": "Creating service layer"},
    # ... rest
])

# 7. Test ONLY new code
Bash("pytest --no-cov apps/memory_api/tests/repositories/test_notification_repository.py")

# 8. Format + Lint (MANDATORY!)
Bash("make format && make lint")

# 9. Commit
Bash('git add . && git commit -m "feat: add notification system with repository, service, and API layers"')

# 10. Merge to develop and RUN FULL TESTS
Bash("git checkout develop && git merge feature/notifications --no-ff")
Bash("make test-unit")  # ⚠️ MUST PASS!
Bash("make lint")

# 11. If passes → merge to main
Bash("git checkout main && git merge develop --no-ff")
Bash("git push origin main develop")


---

## 🎯 Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│  FEATURE BRANCH: Test ONLY new code (pytest --no-cov)  │
│  DEVELOP BRANCH: Test EVERYTHING (make test-unit)      │
│  MAIN BRANCH:    CI tests automatically                │
├─────────────────────────────────────────────────────────┤
│  ALWAYS: make format && make lint before commit        │
│  ALWAYS: tenant_id in ALL queries                      │
│  ALWAYS: Use .ai-templates/ for new code               │
│  NEVER:  Interactive commands (nano, vim, git -i)      │
│  NEVER:  Edit auto-generated docs (CHANGELOG, STATUS)  │
│  NEVER:  Push main + develop separately                │
│  NEVER:  Leave main with red CI                        │
├─────────────────────────────────────────────────────────┤
│  USE: Task tool for exploration & planning             │
│  USE: TodoWrite for multi-step tasks                   │
│  USE: Parallel tool calls when possible                │
│  USE: Read CRITICAL_AGENT_RULES.md when in doubt       │
└─────────────────────────────────────────────────────────┘
```

---

## 📚 Your Documentation Hierarchy

### Tier 0: MANDATORY (Read BEFORE any work!)
- ⚠️ **CRITICAL_AGENT_RULES.md** (5 min) - 8 rules you MUST follow

### Tier 1: Essential (Read before first commit)
- **ONBOARDING_GUIDE.md** (15 min)
- **PROJECT_STRUCTURE.md** (10 min)
- **CONVENTIONS.md** (20 min)
- **INTEGRATION_CHECKLIST.md** (10 min)

### Tier 2: Read Before Specific Tasks
- **docs/AGENTS_TEST_POLICY.md** - Testing philosophy
- **docs/BRANCHING.md** - Git workflow
- **.ai-templates/README.md** - How to use templates

### Tier 3: Reference When Needed
- **examples/template-usage/** - Usage examples
- **docs/reference/** - Deep dives
- **docs/guides/** - Detailed guides

---

## 🆘 When Something Goes Wrong

### Problem: Tests fail on develop

```bash
# 1. Don't panic! That's what develop is for
# 2. Check test output
Bash("make test-unit 2>&1 | tail -100")

# 3. Fix on develop (NOT on main!)
Edit(...fixes...)

# 4. Re-test
Bash("make test-unit")

# 5. Only when green → merge to main
Bash("git checkout main && git merge develop --no-ff")
```

### Problem: CI fails on main

```bash
# 1. This is a priority! Main MUST be green!
# 2. Quickly analyze the error
Bash("gh run list --branch main --limit 1")
Bash("gh run view <run-id> --log-failed")

# 3. Fix on develop
Bash("git checkout develop")
# ... fixes ...
Bash("make test-unit")  # MUST PASS!

# 4. Merge fix to main
Bash("git checkout main && git merge develop --no-ff")
Bash("git push origin main develop")
```

### Problem: Don't know where something is

```python
# Use the Explore agent!
Task(
    subagent_type="Explore",
    description="Find X implementation",
    prompt="Where and how is X implemented in the codebase?"
)
```

---

## 🎉 Summary - Your Superpowers

As Claude Code, you have unique capabilities:

1. ✨ **Task tool** - delegate complex tasks to specialized agents
2. ✨ **TodoWrite** - track progress and give user visibility
3. ✨ **Parallel execution** - read multiple files at once
4. ✨ **WebSearch/WebFetch** - internet access
5. ✨ **Native tools** - Read, Edit, Write, Bash - all native

**Use these superpowers wisely!**

---

## 📞 When in Doubt

1. **Read CRITICAL_AGENT_RULES.md** - 95% of answers are there
2. **Check CONVENTIONS.md** - For code patterns
3. **See .ai-templates/** - For examples
4. **Use the Task tool with the Explore agent** - For exploration

**Remember**: You are autonomous! Do not ask obvious questions. Act according to the documentation.

---

**Version**: 1.0.0
**Last Updated**: 2025-12-08
**Status**: 🟢 Production Ready
**For**: Claude Code (CLI) by Anthropic

**Good luck with RAE! 🚀**