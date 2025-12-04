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

## 🔴 RULE #2: WORK AUTONOMOUSLY - DON'T ASK FOR PERMISSION

### ❌ DON'T ASK:
- "Should I create a new file?" → **Just create it** (follow PROJECT_STRUCTURE.md)
- "Should I add tests?" → **Yes, always add tests**
- "Should I commit now?" → **Yes, commit when feature is complete**
- "Should I use this pattern?" → **Follow templates in .ai-templates/**
- "Can I proceed with implementation?" → **Yes, if you have a design**

### ✅ DO ASK ONLY WHEN:
- Multiple valid architectural approaches exist
- Breaking changes are needed
- Requirements are genuinely unclear
- User must make a business decision

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
Agent: "I'll implement user notifications using our 3-layer architecture:

Design:
- NotificationRepository (data access)
- NotificationService (business logic)
- NotificationRoutes (API endpoints)
- Comprehensive tests for all layers

[Shows design document]

Implementing now..."
[Agent completes entire feature autonomously]
Agent: "✅ Feature complete. Tests pass. Ready for review."
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

### 🤖 Automated Documentation:

```bash
# Run before commit (if repo has docs automation)
make docs

# This updates:
# - CHANGELOG.md (from commits)
# - STATUS.md (from test results)
# - Coverage reports
```

---

## 🎯 Quick Reference Card

Print this and keep visible:

```
┌─────────────────────────────────────────────────────────┐
│  FEATURE BRANCH: Test ONLY new code (--no-cov)         │
│  DEVELOP BRANCH: Test EVERYTHING (make test-unit)      │
│  MAIN BRANCH:    CI tests automatically                │
├─────────────────────────────────────────────────────────┤
│  NEVER ask permission for standard tasks               │
│  ALWAYS follow templates (.ai-templates/)              │
│  ALWAYS include tenant_id in queries                   │
│  NEVER use interactive commands (nano, vim, etc.)      │
│  ALWAYS fix code when tests fail (not tests!)          │
│  ALWAYS push main + develop together                   │
│  NEVER leave main with red CI                          │
└─────────────────────────────────────────────────────────┘
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

- **This file**: CRITICAL_AGENT_RULES.md (you are here)
- **Onboarding**: ONBOARDING_GUIDE.md
- **Structure**: PROJECT_STRUCTURE.md
- **Patterns**: CONVENTIONS.md
- **Testing**: docs/AGENTS_TEST_POLICY.md
- **Git Workflow**: docs/BRANCHING.md
- **Integration**: INTEGRATION_CHECKLIST.md
- **Complete Rules**: .cursorrules

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
