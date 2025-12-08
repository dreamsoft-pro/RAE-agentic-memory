# 🤖 AI Agent Manifest - RAE Project

> **Start Here**: Complete navigation guide for all AI agents working on RAE
>
> **Version**: 1.0.0
> **Last Updated**: 2025-12-06
> **Status**: 🟢 ACTIVE - Universal baseline for all AI agents

---

## 🚨 CRITICAL - READ FIRST (15 minutes)

> ⚠️ **MANDATORY**: These documents contain rules that CANNOT be violated.

### Must-Read Documents (in order):

| # | Document | Time | Purpose |
|---|----------|------|---------|
| 1 | **CRITICAL_AGENT_RULES.md** | 5 min | ⭐ 8 MANDATORY rules (testing, workflow, security) |
| 2 | **This Manifest** | 3 min | Navigation guide & documentation hierarchy |
| 3 | **.ai-agent-rules.md** | 5 min | Forbidden commands & hybrid testing strategy |
| 4 | **docs/BRANCHING.md** | 3 min | Git workflow (feature → develop → main) |
| 5 | **docs/CI_WORKFLOW.md** | 5 min | CI/CD workflow (local → develop → main) |
| 6 | **docs/AGENTS_TEST_POLICY.md** | 3 min | Tests as contracts philosophy |

**Total Time**: ~20-25 minutes to read critical documentation before starting any work.

---

## 📚 Complete Documentation Hierarchy

### 🔴 Tier 1: Critical (Read BEFORE any work)

Must read before touching ANY code:

- **CRITICAL_AGENT_RULES.md** - 8 mandatory rules that cannot be violated
- **.ai-agent-rules.md** - Forbidden interactive commands, hybrid testing strategy
- **docs/BRANCHING.md** - Git workflow (feature/develop/main branches)
- **docs/CI_WORKFLOW.md** - CI/CD workflow (local tests → develop → main)
- **docs/AGENTS_TEST_POLICY.md** - Tests are contracts, not snapshots

**Key Rules from Tier 1 (All 8 Critical Rules):**
1. ❌ **RULE #1**: NEVER run full test suite on feature branches (only `pytest --no-cov`)
2. ✅ **RULE #2**: ALWAYS work autonomously (don't ask obvious questions)
3. ✅ **RULE #3**: Follow 3-phase workflow (Feature → Develop → Main)
   - Feature: test ONLY new code
   - Develop: `make test-unit` MANDATORY before main!
   - Main: CI tests automatically
4. ✅ **RULE #4**: ALWAYS include `tenant_id` in database queries (security!)
5. ✅ **RULE #5**: ALWAYS use templates from `.ai-templates/`
6. ❌ **RULE #6**: NEVER use interactive commands (nano, vim, git -i)
7. ✅ **RULE #7**: Tests are contracts - fix CODE, not tests (when tests fail correctly)
8. ✅ **RULE #8**: Documentation updates
   - DON'T EDIT: Auto-generated files (`CHANGELOG.md`, `STATUS.md`, `TODO.md`, `docs/.auto-generated/`)
   - DO EDIT: Manual files (`CONVENTIONS.md`, `PROJECT_STRUCTURE.md`, `docs/guides/`)

### 🟡 Tier 2: Essential (Read before first commit)

Read before making your first changes:

- **PROJECT_STRUCTURE.md** - Where to place files (repositories, services, routes)
- **CONVENTIONS.md** - Code patterns with WHY explanations
- **.ai-templates/** - Repository, Service, Route, Test templates
- **INTEGRATION_CHECKLIST.md** - Pre-commit verification checklist

**Key Knowledge from Tier 2:**
- Repository Pattern for data access
- Service Layer for business logic
- 3-layer architecture (API → Service → Repository)
- Dependency injection patterns
- Testing patterns and fixtures

### 🟢 Tier 3: Reference (Consult as needed)

Use when you need specific information:

- **ONBOARDING_GUIDE.md** - Complete 15-minute onboarding
- **TESTING.md** - Comprehensive testing guide
- **CONTRIBUTING.md** - Contribution workflow
- **docs/guides/developers/** - Developer guides and best practices
- **docs/reference/** - Technical specifications and deep dives
- **examples/** - Working code examples

---

## 🔍 Workflow & Automation Status

### ✅ Automated in CI/CD (DO NOT manually edit these):

GitHub Actions automatically handles:

| File | What | When | Workflow |
|------|------|------|----------|
| `CHANGELOG.md` | Git commit history (last 50) | Push to develop/main | `.github/workflows/ci.yml` |
| `STATUS.md` | Live metrics (coverage, tests) | Push to develop/main | `.github/workflows/ci.yml` |
| `TODO.md` | Extracted TODOs/FIXMEs | Push to develop/main | `.github/workflows/ci.yml` |
| `docs/TESTING_STATUS.md` | Test results & coverage | After CI run | `.github/workflows/docs.yml` |
| `docs/.auto-generated/` | API specs, metrics | After CI run | `.github/workflows/docs.yml` |

**How it works:**
1. You push to `develop` or `main`
2. CI runs tests and quality gates
3. If successful, `docs-update` job runs `scripts/docs_automator.py`
4. Changes auto-committed with `[skip ci]` tag
5. Metrics tracked in `docs/.auto-generated/metrics/automation-health.json`

**View automation status:** [docs/.auto-generated/metrics/DASHBOARD.md](docs/.auto-generated/metrics/DASHBOARD.md)

### 📝 Manual Updates Required (Your responsibility):

You MUST manually update these when adding features:

| File | When to Update | Example |
|------|---------------|---------|
| `CONVENTIONS.md` | New pattern/convention | Added caching pattern |
| `PROJECT_STRUCTURE.md` | New directory/location | Added new repository type |
| `docs/guides/` | New feature guide | User authentication guide |
| `docs/reference/` | Technical spec change | Updated API schema |
| `.ai-templates/README.md` | New template | Added webhook template |

---

## 🎯 Quick Decision Tree

Fast answers to common questions:

```
❓ "Should I..."

├─ ...run full test suite on feature branch?
│  └─ ❌ NO! (Rule #1) - Only test YOUR new code with --no-cov
│
├─ ...run full tests on develop branch?
│  └─ ✅ YES! (MANDATORY) - make test-unit before merging to main
│
├─ ...ask permission to create a file?
│  └─ ❌ NO! (Rule #2) - Work autonomously, follow PROJECT_STRUCTURE.md
│
├─ ...ask permission to add tests?
│  └─ ❌ NO! - ALWAYS add comprehensive tests
│
├─ ...ask which pattern to use?
│  └─ ❌ NO! - Use templates from .ai-templates/
│
├─ ...include tenant_id in SQL query?
│  └─ ✅ YES! (Rule #4) - ALWAYS for security
│
├─ ...use nano/vim to edit files?
│  └─ ❌ NO! (Rule #6) - Use Edit/Write tools
│
├─ ...change test to make it pass?
│  └─ ⚠️ DEPENDS - If test is correct, fix CODE not test (Rule #7)
│
├─ ...update CHANGELOG.md manually?
│  └─ ❌ NO! (Rule #8) - CI auto-updates it
│
└─ ...update CONVENTIONS.md?
   └─ ✅ YES! - Manual documentation is your responsibility
```

---

## 🔄 Standard Workflow (Every Feature)

Copy-paste this workflow for every feature:

```bash
# ═══════════════════════════════════════════════════════════
# PHASE 1: FEATURE BRANCH (Test ONLY your new code)
# ═══════════════════════════════════════════════════════════

# 1. Create feature branch
git checkout develop
git pull origin develop
git checkout -b feature/my-feature

# 2. Design (for non-trivial features)
#    Write design document, get approval if uncertain

# 3. Implement using templates
cp .ai-templates/repository_template.py apps/memory_api/repositories/my_repo.py
# ... implement following template patterns ...

# 4. Test ONLY your new code (NOT full suite!)
pytest --no-cov apps/memory_api/tests/repositories/test_my_repo.py
# OR
make test-focus FILE=apps/memory_api/tests/repositories/test_my_repo.py

# 5. Format & lint
make format && make lint

# 6. Commit
git add .
git commit -m "feat: add my feature"

# 7. Push feature branch
git push origin feature/my-feature

# ═══════════════════════════════════════════════════════════
# PHASE 2: DEVELOP BRANCH (Full validation - MANDATORY!)
# ═══════════════════════════════════════════════════════════

# 8. Merge to develop
git checkout develop
git merge feature/my-feature --no-ff

# 9. 🚨 CRITICAL: Run FULL test suite on develop
make test-unit           # Must pass!
make lint                # Must pass!
make security-scan       # Must pass!

# If ANYTHING fails → FIX on develop, do NOT proceed to main
# If EVERYTHING passes → proceed to phase 3

# ═══════════════════════════════════════════════════════════
# PHASE 3: MAIN BRANCH (Production ready)
# ═══════════════════════════════════════════════════════════

# 10. Merge to main
git checkout main
git merge develop --no-ff

# 11. Push both branches together (keeps them in sync)
git push origin main develop

# 12. Verify CI is green
gh run watch

# If CI fails on main:
# - FIX IMMEDIATELY
# - Push fix to main AND develop
# - NEVER leave main with red CI
```

---

## 📋 Agent-Specific Configuration Files

Different AI agents read different config files:

| Agent | Primary Config | Secondary Configs | Notes |
|-------|---------------|-------------------|-------|
| **Claude Code** | `.clauderc` | This manifest | JSON format, now includes all rules |
| **Cursor AI** | `.cursorrules` | This manifest | Most complete rules file |
| **Google Gemini** | `GEMINI.md` | This manifest | Now includes manifest reference |
| **GitHub Copilot** | `.github/copilot-instructions.md` | This manifest | (If created) |
| **Any AI Agent** | **This file first** | Then specific config | Universal baseline |

**Recommendation**: All agents should read this manifest FIRST for baseline understanding, then consult their agent-specific files for customizations.

---

## ✅ Pre-Commit Checklist

Before EVERY commit, verify:

```
Checklist - Feature Branch:
[ ] Tested ONLY my new code (pytest --no-cov [my test file])
[ ] Used templates from .ai-templates/
[ ] Included tenant_id in all database queries
[ ] No interactive commands in code (no nano, vim, git -i)
[ ] Followed autonomous work (didn't ask obvious questions)
[ ] Code formatted: make format
[ ] Linted: make lint
[ ] Conventional commit message: feat/fix/docs/test/refactor

Checklist - Before Merging to Main:
[ ] Feature merged to develop
[ ] Full test suite passed on develop: make test-unit
[ ] Lint passed: make lint
[ ] Security scan passed: make security-scan
[ ] Manual documentation updated (if needed)
[ ] Ready to fix immediately if CI fails on main
[ ] Will push main + develop together
```

---

## 🚨 Common Mistakes & Solutions

| Mistake | Why It's Wrong | Solution |
|---------|---------------|----------|
| Running `pytest` on feature branch | Wastes 10+ mins, burns CI credits | Use `pytest --no-cov [your file]` |
| Asking "Should I create a file?" | Wastes time, blocks progress | Just create it (follow PROJECT_STRUCTURE.md) |
| Missing `tenant_id` in query | Security vulnerability! | Always include in WHERE clause |
| Using `nano` or `vim` in script | Blocks CI/automation | Use Edit/Write tools or `cat`/`sed` |
| Changing test to make it pass | Makes tests useless | Fix code if test is correct |
| Manually editing CHANGELOG.md | Conflicts with automation | Only edit manual docs |
| Leaving main with red CI | Blocks team, breaks deployments | Fix immediately and push again |
| Not testing on develop | Breaks main, blocks team | ALWAYS run full tests on develop first |

---

## 📞 Getting Help

When you're stuck:

1. **Check Decision Tree** (above) - Answers 90% of questions
2. **Read Tier 1 Docs** - Critical rules and workflow
3. **Search examples/** - Working code samples
4. **Check templates** - `.ai-templates/` for patterns
5. **Ask User** - Only for genuine ambiguity (architecture choices, business decisions)

**When to ask user:**
- Multiple valid architectural approaches exist
- Breaking changes required
- Requirements genuinely unclear
- Business/product decision needed

**When NOT to ask:**
- File locations (check PROJECT_STRUCTURE.md)
- Code patterns (check CONVENTIONS.md)
- Should I add tests? (Always yes)
- Should I create this file? (Just do it)

---

## 🎓 Learning Path

**New to RAE?** Follow this learning path:

### Day 1: Foundation (1 hour)
1. Read CRITICAL_AGENT_RULES.md (5 min)
2. Read this manifest (10 min)
3. Read .ai-agent-rules.md (10 min)
4. Read docs/BRANCHING.md (10 min)
5. Read docs/AGENTS_TEST_POLICY.md (10 min)
6. Skim PROJECT_STRUCTURE.md (10 min)
7. Review .ai-templates/ (10 min)

### Day 2: First Contribution (2 hours)
1. Read CONVENTIONS.md (30 min)
2. Study templates in .ai-templates/ (30 min)
3. Read ONBOARDING_GUIDE.md (15 min)
4. Make first small contribution (45 min)

### Week 1: Mastery (5 hours)
1. Read TESTING.md (30 min)
2. Study examples/ directory (1 hour)
3. Read docs/guides/developers/ (2 hours)
4. Make 3-5 contributions (1.5 hours)

---

## 📊 Project Health Indicators

Check these to understand project status:

| Indicator | File | What It Shows |
|-----------|------|---------------|
| **Test Coverage** | `STATUS.md` | Current: 57%, Target: 75-80% |
| **Test Count** | `STATUS.md` | Current: 461 tests total |
| **CI Status** | GitHub Actions | Must be 🟢 green on main |
| **Documentation Status** | `docs/.auto-generated/metrics/` | Automation health |
| **Recent Changes** | `CHANGELOG.md` | Last 50 commits |
| **Pending Work** | `TODO.md` | Extracted TODOs from code |

---

## 🔐 Security Reminders

CRITICAL security practices:

1. **Multi-tenancy**: ALWAYS include `tenant_id` in queries
2. **Secrets**: NEVER hardcode API keys (use `.env`)
3. **Input Validation**: Validate at system boundaries
4. **SQL Injection**: Use parameterized queries only
5. **Authentication**: Respect `TENANCY_ENABLED` config

See `docs/guides/security-best-practices.md` for complete guide.

---

## 🎯 Success Metrics

You're succeeding when:

- ✅ CI stays green on main (100% of time)
- ✅ Tests pass on first try (after develop validation)
- ✅ Code follows templates (consistent patterns)
- ✅ No questions about obvious tasks (autonomous work)
- ✅ Security checks pass (tenant_id everywhere)
- ✅ Documentation stays current (manual docs updated)
- ✅ Fast iterations (quick tests on feature branches)

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-06 | Initial unified manifest for all AI agents |

---

## 🔗 Quick Links

**Core Rules:**
- [CRITICAL_AGENT_RULES.md](./CRITICAL_AGENT_RULES.md) - 8 mandatory rules
- [.ai-agent-rules.md](./.ai-agent-rules.md) - Forbidden commands & testing
- [docs/BRANCHING.md](./docs/BRANCHING.md) - Git workflow
- [docs/CI_WORKFLOW.md](./docs/CI_WORKFLOW.md) - CI/CD workflow
- [docs/AGENTS_TEST_POLICY.md](./docs/AGENTS_TEST_POLICY.md) - Testing philosophy

**Structure & Patterns:**
- [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) - File locations
- [CONVENTIONS.md](./CONVENTIONS.md) - Code patterns
- [.ai-templates/](./.ai-templates/) - Code templates
- [INTEGRATION_CHECKLIST.md](./INTEGRATION_CHECKLIST.md) - Pre-commit checks

**Guides:**
- [ONBOARDING_GUIDE.md](./ONBOARDING_GUIDE.md) - Complete onboarding
- [TESTING.md](./TESTING.md) - Testing guide
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Contribution guide

**Agent Configs:**
- [.cursorrules](./.cursorrules) - Cursor AI config
- [GEMINI.md](./GEMINI.md) - Google Gemini config
- [.clauderc](./.clauderc) - Claude Code config

---

**Remember**: This manifest is your universal baseline. Read it first, then consult agent-specific configs for customizations.

**Status**: 🟢 ACTIVE
**Maintenance**: Updated by team as project evolves
**Feedback**: Open issues for manifest improvements
