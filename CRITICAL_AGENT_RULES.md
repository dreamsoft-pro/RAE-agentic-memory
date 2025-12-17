# 🚨 CRITICAL RULES FOR AI AGENTS - READ FIRST! 🚨

> **⚠️ ATTENTION**: These rules are MANDATORY. Violating them will break the workflow and block other developers.

## 🔴 RULE #1: NEVER RUN FULL TEST SUITE ON FEATURE BRANCHES

### ❌ FORBIDDEN ON FEATURE BRANCHES:
```bash
# ❌ NEVER DO THIS ON FEATURE BRANCH:
pytest                              # FORBIDDEN - runs ALL tests
pytest --cov                        # FORBIDDEN - full coverage check
make test                           # FORBIDDEN - full test suite
make test-cov                       # FORBIDDEN - full coverage
make test-unit                      # FORBIDDEN - only on develop!
pytest apps/memory_api/tests/       # FORBIDDEN - too broad
```

### ✅ ALLOWED ON FEATURE BRANCHES:
```bash
# ✅ CORRECT - Test ONLY your new feature:
pytest --no-cov apps/memory_api/tests/services/test_my_new_feature.py
make test-focus FILE=apps/memory_api/tests/services/test_my_new_feature.py

# ✅ CORRECT - Test just the files you changed:
pytest --no-cov apps/memory_api/tests/services/test_service1.py apps/memory_api/tests/services/test_service2.py
```

### 📋 WHY THIS RULE EXISTS:

1. **Speed**: Full test suite takes 10-15 minutes
2. **CI Costs**: Feature branches run on every push
3. **Token Usage**: Each test run costs API tokens
4. **Workflow**: Full tests run automatically on develop/main

### 🎯 WHEN TO RUN FULL TESTS:

```
Feature Branch:  Test ONLY new code ✅
      ↓
   Develop:      Run FULL test suite ✅ (MANDATORY!)
      ↓
     Main:       CI runs full tests automatically ✅
```

---

## 🔴 RULE #2: WORK AUTONOMOUSLY - NO CONFIRMATIONS, NO VERBOSE MESSAGES

### ❌ NEVER ASK FOR CONFIRMATION:
- "Should I create a new file?" → **Just create it** (follow PROJECT_STRUCTURE.md)
- "Should I add tests?" → **Yes, always add tests**
- "Should I commit now?" → **Yes, commit when feature is complete**
- "Should I use this pattern?" → **Follow templates in .ai-templates/**
- "Can I proceed with implementation?" → **Yes, if you have a design**
- "Do you want to proceed?" → **NEVER show this - just execute**

### ❌ NO INTERACTIVE COMMANDS:
```bash
# ❌ FORBIDDEN - require user input:
nano, vim, vi, less, more
git add -i
git rebase -i
git commit -i
any command with interactive prompts
```

### ❌ NO VERBOSE DESCRIPTIONS IN COMMITS:
```bash
# ❌ WRONG - marketing speak, verbose:
git commit -m "feat: Complete amazing Phase 1!

✅ Implemented incredible features:
- Super cool feature X
- Awesome component Y

Phase 1 Milestone M1 completed! 🎉
Next: Phase 2 will be even better!"

# ✅ CORRECT - technical, concise:
git commit -m "feat(rae-core): implement 4-layer memory architecture

- sensory, working, longterm, reflective layers
- hybrid search with RRF/weighted fusion
- reflection engine for pattern detection
- comprehensive test coverage"
```

### ❌ NO VERBOSE PROGRESS MESSAGES:
```
# ❌ WRONG:
"Great! Now I'll implement the amazing feature X which will revolutionize..."
"Perfect! Let me create this incredible component..."
"Excellent! The tests are passing beautifully..."

# ✅ CORRECT:
[Just do the work silently, show results when done]
```

### ✅ DO ASK ONLY WHEN:
- Multiple valid architectural approaches exist
- Breaking changes are needed
- Requirements are genuinely unclear
- User must make a business decision (NOT technical)

### 📖 Example - Autonomous Work:

```
❌ WRONG CONVERSATION:
User: "Add user notifications"
Agent: "Should I create a new file for this?"
User: "Yes"
Agent: "Should I add tests?"
User: "Yes"
Agent: "Should I use the repository pattern?"
User: "Yes"
[10 minutes wasted on obvious questions]

✅ CORRECT CONVERSATION:
User: "Add user notifications"
Agent: [silently implements: NotificationRepository, NotificationService, routes, tests]
Agent: "Implemented notifications (3-layer arch). Tests pass."
```

---

## 🔴 RULE #3: FOLLOW THE EXACT WORKFLOW - NO SHORTCUTS

### 📋 Mandatory Workflow for Every Feature:

```bash
# ═══════════════════════════════════════════════════════════
# PHASE 1: FEATURE BRANCH (your code ONLY)
# ═══════════════════════════════════════════════════════════

git checkout develop
git pull origin develop
git checkout -b feature/my-feature

# 1. Design (mandatory for non-trivial features)
# Write design document, get approval if needed

# 2. Implement using templates
cp .ai-templates/repository_template.py apps/memory_api/repositories/my_repo.py
# ... implement ...

# 3. Test ONLY your new code
pytest --no-cov apps/memory_api/tests/repositories/test_my_repo.py
# OR
make test-focus FILE=apps/memory_api/tests/repositories/test_my_repo.py

# 4. Format & lint
make format && make lint

# 5. Commit
git add .
git commit -m "feat: add my feature"

# 6. Push feature branch
git push origin feature/my-feature

# ═══════════════════════════════════════════════════════════
# PHASE 2: DEVELOP BRANCH (full validation)
# ═══════════════════════════════════════════════════════════

git checkout develop
git merge feature/my-feature --no-ff

# 🚨 CRITICAL: Run FULL test suite on develop!
make test-unit           # This must pass!
make lint                # This must pass!

# If anything fails → fix it on develop
# If everything passes → proceed to main

# ═══════════════════════════════════════════════════════════
# PHASE 3: MAIN BRANCH (production ready)
# ═══════════════════════════════════════════════════════════

git checkout main
git merge develop --no-ff

# Push both branches together
git push origin main develop

# Verify CI is green
gh run watch

# If CI fails → FIX IMMEDIATELY and push again
# NEVER leave main with red CI!
```

### ⚠️ CRITICAL CHECKPOINTS:

| Checkpoint | Action | If Fails |
|------------|--------|----------|
| Feature branch tests | Test ONLY new code | Fix your code |
| Develop full tests | Run ALL tests | Fix on develop, don't proceed to main |
| Main CI | Automatic in GitHub Actions | Fix immediately, push again |

---

## 🔴 RULE #4: ALWAYS INCLUDE tenant_id IN DATABASE QUERIES

### ❌ SECURITY VIOLATION:
```python
# ❌ FORBIDDEN - Missing tenant_id (SECURITY HOLE!)
query = "SELECT * FROM memories WHERE id = $1"
result = await conn.fetchrow(query, memory_id)
```

### ✅ SECURITY CORRECT:
```python
# ✅ CORRECT - Includes tenant_id
query = "SELECT * FROM memories WHERE id = $1 AND tenant_id = $2"
result = await conn.fetchrow(query, memory_id, tenant_id)
```

### 🔍 CI Checks This Automatically:

The quality-gate job in CI will warn about queries without tenant_id.

**Why**: Multi-tenancy security. Without tenant_id, users could access other tenants' data!

---

## 🔴 RULE #5: USE TEMPLATES FOR ALL NEW CODE

### ❌ DON'T:
- Write code from scratch
- Copy from other projects
- "I'll just quickly write this..."

### ✅ DO:
```bash
# 1. Copy appropriate template
cp .ai-templates/repository_template.py apps/memory_api/repositories/my_repo.py

# 2. Replace entity names
# Entity → MyEntity
# entities → my_entities

# 3. Customize logic
# Keep structure, change specifics

# 4. Keep patterns intact
# Dependency injection, error handling, logging
```

### 📚 Templates Available:
- `repository_template.py` - Data access layer
- `service_template.py` - Business logic layer
- `route_template.py` - API endpoints
- `test_template.py` - All testing patterns

---

## 🔴 RULE #6: NO INTERACTIVE COMMANDS IN CODE

### ❌ FORBIDDEN COMMANDS:
```bash
nano file.py          # ❌ Interactive editor
vim file.py           # ❌ Interactive editor
vi file.py            # ❌ Interactive editor
less file.py          # ❌ Interactive pager
git add -i            # ❌ Interactive git
git rebase -i         # ❌ Interactive rebase
```

### ✅ USE INSTEAD:
```bash
cat file.py           # ✅ View file
head -n 50 file.py    # ✅ View first 50 lines
# Use Edit/Write tools  ✅ Edit files
git add .             # ✅ Non-interactive git
```

**Why**: Interactive commands block CI/CD and automation.

---

## 🔴 RULE #7: TESTS ARE CONTRACTS, NOT SNAPSHOTS

### ❌ WRONG APPROACH:
```
Test fails → "Let me change the test to make it pass"
```

### ✅ CORRECT APPROACH:
```
Test fails → "Why did it fail? Is the test correct?"
  ↓
If test correctly describes expected behavior:
  → FIX THE CODE

If test was testing implementation details:
  → IMPROVE THE TEST (test behavior, not implementation)
```

### 📖 Example:

```python
# ❌ BAD TEST - Tests implementation
def test_service_calls_repository_with_exact_params():
    service.do_work(data)
    mock_repo.insert.assert_called_once_with(
        exact_internal_params  # ❌ Tests implementation details
    )

# ✅ GOOD TEST - Tests behavior
def test_service_creates_entity_with_valid_data():
    result = service.do_work(data)
    assert result.id is not None  # ✅ Tests behavior
    assert result.status == "active"
```

See `docs/AGENTS_TEST_POLICY.md` for complete philosophy.

---

## 🔴 RULE #8: UPDATE DOCUMENTATION AUTOMATICALLY

### 📝 When Documentation Must Be Updated:

| Change | Documentation to Update |
|--------|------------------------|
| New API endpoint | OpenAPI docs (automatic), API guides |
| New pattern/convention | CONVENTIONS.md |
| New file location | PROJECT_STRUCTURE.md |
| New template | .ai-templates/README.md |
| Breaking change | CHANGELOG.md, migration guide |

### 🤖 Automated Documentation (CI Handles This):

**Files auto-updated by GitHub Actions (DO NOT manually edit):**
- `CHANGELOG.md` - Git commit history (last 50 commits)
- `STATUS.md` - Live project metrics (coverage, tests, branch)
- `TODO.md` - Extracted TODOs/FIXMEs from code
- `docs/TESTING_STATUS.md` - Test results and coverage
- `docs/.auto-generated/api/` - OpenAPI specs and endpoints
- `docs/.auto-generated/metrics/` - Code metrics, automation health

**Automatic workflow:**
1. Every push to `develop`/`main` triggers `.github/workflows/docs.yml`
2. Runs `python scripts/docs_automator.py` (integrated with metrics)
3. Auto-commits updated files with `[skip ci]` tag
4. Metrics saved to `docs/.auto-generated/metrics/automation-health.json`

**Dashboard:** [docs/.auto-generated/metrics/DASHBOARD.md](docs/.auto-generated/metrics/DASHBOARD.md)

**Test locally (optional, CI will run automatically):**
```bash
make docs  # or: python scripts/docs_automator.py
```

**Metrics tracked:**
- Execution time, files generated, errors, warnings
- Success rate (100% = healthy)
- Historical trends (last 50 runs)

### 📝 Manual Documentation (Your Responsibility):

When you add new features, **manually update** these files (CI does NOT handle these):
- `CONVENTIONS.md` - New patterns or conventions
- `PROJECT_STRUCTURE.md` - New file locations
- `docs/guides/` - Feature guides and tutorials
- `docs/reference/` - Technical specifications
- `.ai-templates/README.md` - New templates

---

---

## 🔴 RULE #9: START EVERY SESSION WITH REQUIRED READING

### 📖 MANDATORY - Read These First (15 minutes)

Before ANY work, read these documents in this EXACT order:

| # | Document | Time | What |
|---|----------|------|------|
| 1 | **SESSION_START.md** | 5 min | How to start a session properly |
| 2 | **AUTONOMOUS_OPERATIONS.md** | 5 min | What to do WITHOUT asking |
| 3 | **BRANCH_STRATEGY.md** | 5 min | 4-phase workflow (feature→develop→release→main) |

### 🎯 Why This Rule Exists

1. **Prevents Questions**: Reading first prevents 20+ obvious questions
2. **Saves Time**: 15 minutes reading saves hours of back-and-forth
3. **Consistency**: All agents start with the same baseline knowledge
4. **Autonomy**: Understanding autonomy rules upfront = no blocking user

### ❌ DON'T:
```
User: "Add cache service"
Agent: "Should I create a file?"           # You didn't read docs!
Agent: "Which pattern to use?"             # Read AUTONOMOUS_OPERATIONS.md!
Agent: "Can I commit?"                     # Read SESSION_START.md!
```

### ✅ DO:
```
User: "Add cache service"
Agent: [Silently reads SESSION_START.md, AUTONOMOUS_OPERATIONS.md]
Agent: [Implements autonomously using templates]
Agent: "Done. Cache service implemented with 12 tests. Ready for merge."
```

**See**: `SESSION_START.md` for complete checklist

---

## 🔴 RULE #10: RESPECT 4-PHASE WORKFLOW WITH RELEASE BRANCH

### 🌳 NEW: Release Branch as Production Gate

```
feature/* → develop → release → main
  (dev)     (integ)   (QA)     (HOLY)
```

**Critical Change**: Main is now ONLY accessed through release branch!

### 📋 Rules for Each Branch

| Branch | Testing | Merge How | Protection |
|--------|---------|-----------|------------|
| feature/* | ONLY new code (--no-cov) | Local or PR to develop | None |
| develop | FULL tests (make test-unit) | Local or PR | Basic CI |
| release | Full + integration | PR to main (1 approval) | High |
| main | CI automatic | ONLY from release PR (2 approvals) | MAXIMUM |

### ❌ FORBIDDEN:
```bash
# Direct merge to main
git checkout main
git merge develop        # ❌ WRONG!
git push origin main     # ❌ FORBIDDEN!
```

### ✅ CORRECT:
```bash
# Create release branch
git checkout -b release/v1.2.0 develop
git push origin release/v1.2.0

# Create PR to main (ONLY way)
gh pr create --base main --head release/v1.2.0 \
  --title "Release v1.2.0"

# Wait for:
# - 2 approvals
# - All CI checks pass
# - Merge through GitHub UI
```

### 🎯 Why Release Branch Exists

1. **Stabilization**: Final QA before production
2. **Protection**: No accidental pushes to main
3. **Review**: Formal approval process (2 maintainers)
4. **Rollback**: Easy to identify release points
5. **Safety**: Main is HOLY - always working code

**See**: `BRANCH_STRATEGY.md` for complete 4-phase workflow

---

## 🔴 RULE #11: STRICT REPOSITORY SEPARATION - NO MIXING

### ❌ ABSOLUTELY FORBIDDEN:
- Mixing code from different projects (e.g., `ProjectA` code in `ProjectB` repo)
- Committing files meant for `repo-A` into `repo-B`
- "Just testing" code from another project in the current working directory
- Copy-pasting unrelated modules without explicit architectural decision

### ✅ CORRECT BEHAVIOR:
- **Isolate contexts**: If working on `ProjectA`, switch directory/repo entirely.
- **Verify destination**: Check `git remote -v` before pushing.
- **Clean workspace**: Don't leave unrelated files in the project root.
- **Git Hygiene**: `git status` before EVERY add/commit to ensure only relevant files are staged.

### 📋 Why This Rule Exists:
1. **Pollution**: Unrelated code bloats the repo and confuses dependencies.
2. **Security**: Leaking proprietary/private code to public/wrong repos.
3. **CI/CD Failure**: Build scripts for one project (e.g., Windows .exe) break CI for another (e.g., Linux Docker).

---

## 🎯 Quick Reference Card (Updated)

Print this and keep visible:

```
┌─────────────────────────────────────────────────────────────┐
│  SESSION START: Read docs first (15 min) - MANDATORY       │
├─────────────────────────────────────────────────────────────┤
│  4-PHASE WORKFLOW:                                          │
│    feature/* → develop → release → main                     │
│                                                             │
│  FEATURE BRANCH: Test ONLY new code (--no-cov)             │
│  DEVELOP BRANCH: Test EVERYTHING (make test-unit)          │
│  RELEASE BRANCH: Full + integration + 1 approval           │
│  MAIN BRANCH:    HOLY - only from release (2 approvals)    │
├─────────────────────────────────────────────────────────────┤
│  AUTONOMY:                                                  │
│    NEVER ask permission for standard tasks                 │
│    ALWAYS follow templates (.ai-templates/)                │
│    ALWAYS work autonomously (read AUTONOMOUS_OPERATIONS.md)│
├─────────────────────────────────────────────────────────────┤
│  SECURITY:                                                  │
│    ALWAYS include tenant_id in queries                     │
│    NEVER use interactive commands (nano, vim, etc.)        │
│    NEVER force push to main/release                        │
├─────────────────────────────────────────────────────────────┤
│  TESTING:                                                   │
│    ALWAYS fix code when tests fail (not tests!)            │
│    NEVER leave main with red CI                            │
│    READ SESSION_START.md before EVERY session              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚨 Consequences of Rule Violations

| Violation | Consequence |
|-----------|-------------|
| Run full tests on feature branch | Wastes 10+ minutes, burns CI credits |
| Skip tests on develop | Breaks main, blocks team |
| Ask unnecessary questions | Wastes user time, delays work |
| Missing tenant_id | Security vulnerability! |
| Skip templates | Inconsistent code, needs refactoring |
| Interactive commands | Blocks CI, fails automation |
| Change tests instead of code | Tests become useless |
| Leave main with red CI | Blocks deployments, breaks team |

---

## 📚 Complete Rule Set Links

### 🔴 Tier 1 - CRITICAL (Read EVERY session)

- **This file**: CRITICAL_AGENT_RULES.md (you are here - 10 rules)
- **Session Start**: SESSION_START.md (how to start properly)
- **Autonomy**: AUTONOMOUS_OPERATIONS.md (what to do WITHOUT asking)
- **Branch Strategy**: BRANCH_STRATEGY.md (4-phase workflow)

### 🟡 Tier 2 - ESSENTIAL (Read before first commit)

- **Structure**: PROJECT_STRUCTURE.md (where to put files)
- **Patterns**: CONVENTIONS.md (how to write code)
- **Testing Policy**: docs/AGENTS_TEST_POLICY.md (tests as contracts)
- **Testing Optimization**: TESTING_OPTIMIZATION.md (smart testing)
- **Git Workflow**: docs/BRANCHING.md (git commands)
- **Onboarding**: ONBOARDING_GUIDE.md (complete guide)

### 🟢 Tier 3 - REFERENCE (As needed)

- **Branch Protection**: BRANCH_PROTECTION.md (GitHub rules)
- **Public Repo**: PUBLIC_REPO_STRATEGY.md (for external contributions)
- **Integration**: INTEGRATION_CHECKLIST.md (pre-commit checks)
- **Complete Rules**: .cursorrules (all rules for Cursor)
- **Manifest**: AI_AGENT_MANIFEST.md (universal navigation)

---

## ✅ Checklist Before Every Commit

```
[ ] Tested ONLY my new code on feature branch
[ ] Used templates from .ai-templates/
[ ] Included tenant_id in all queries
[ ] No interactive commands in code
[ ] Followed autonomous work pattern (didn't ask obvious questions)
[ ] Will run full tests on develop before merging to main
[ ] Documentation updated if needed
[ ] Ready to fix immediately if CI fails on main
```

---

**Remember**: These rules exist to maintain quality and velocity. Follow them strictly!

**Version**: 1.0.0
**Last Updated**: 2025-12-04
**Status**: 🔴 MANDATORY - NO EXCEPTIONS
