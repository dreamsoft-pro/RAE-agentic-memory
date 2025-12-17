# 🚀 SESSION START - AI Agent Session Start Guide

> **⏱️ Time: 15 minutes** | **🔴 Status: MANDATORY - REQUIRED BEFORE EVERY SESSION**

---

## 📖 STEP 1: Read Critical Documents (10 minutes)

Read these documents in this **EXACT** order:

| # | Document | Time | Priority | Content |
|---|----------|------|----------|---------|
| 1 | **CRITICAL_AGENT_RULES.md** | 5 min | 🔴 CRITICAL | 10 mandatory rules that CANNOT be broken |
| 2 | **AI_AGENT_MANIFEST.md** | 3 min | 🔴 CRITICAL | Universal documentation navigation and hierarchy |
| 3 | **AUTONOMOUS_OPERATIONS.md** | 2 min | 🔴 CRITICAL | List of operations you perform WITHOUT asking |

### Why this order?

1. **CRITICAL_AGENT_RULES.md** - Basic safety and workflow rules
2. **AI_AGENT_MANIFEST.md** - Map of all documentation and how to navigate
3. **AUTONOMOUS_OPERATIONS.md** - How to work AUTONOMOUSLY without blocking the user

---

## 🔍 STEP 2: Check Project Status (3 minutes)

Run these commands to understand the context:

```bash
# 1. Branch status
git status
git branch -a

# 2. Last changes (10 commits)
git log --oneline -10

# 3. CI/CD status (last 5 runs)
gh run list --limit 5

# 4. Current location
pwd
ls -la
```

### Understand the context:

- **Which branch are you on?** (feature/develop/release/main)
- **Are there uncommitted changes?**
- **Is CI green or red?**
- **What was the last commit?**

---

## 🎯 STEP 3: Identify Task Type (2 minutes)

Determine what type of work you will be performing:

| Task Type | Branch | Testing | Example |
|-----------|--------|---------|---------|
| **New Feature** | `feature/*` | ONLY new code (--no-cov) | Add cache service |
| **Bug Fix** | `feature/*` or `hotfix/*` | ONLY changed code | Fix null pointer |
| **Refactoring** | `feature/*` | Full tests locally | Move to repo pattern |
| **Documentation** | `feature/*` | SKIP tests (lint only) | Update README |
| **Release** | `release/*` | Full tests + integration | Stabilize v1.2.0 |

---

## ⚡ STEP 4: Start Work AUTONOMOUSLY

After reading the documents and understanding the context:

### ✅ DO NOT ask about:

- Can I create a file/directory?
- Should I add tests?
- Which pattern should I use? (use templates from `.ai-templates/`)
- Can I commit?
- Can I push to a feature branch?
- Can I merge feature → develop?

### ❓ ASK ONLY about:

- **Architecture**: Multiple equally good approaches
- **Breaking changes**: API breaking changes
- **Business**: Unclear requirements or product decisions
- **Risk**: Force push, data deletion, prod changes

### 🔄 Standard Workflow (Autonomous):

```
1. Receive task from user
2. [SILENCE - do not ask permission for standard things]
3. Read necessary files (PROJECT_STRUCTURE.md, CONVENTIONS.md)
4. For non-trivial features: Create design document
5. Implement using templates from .ai-templates/
6. Test according to branch and change type
7. Format + lint: make format && make lint
8. Commit with conventional message
9. Push (if feature branch)
10. REPORT result to user
11. DO NOT ask "can I continue?" - just continue
```

---

## 🗺️ QUICK REFERENCE CARD

Print and keep visible during work:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    RAE AGENT QUICK REFERENCE                         │
├─────────────────────────────────────────────────────────────────────┤
│  GIT WORKFLOW (4-phase):                                            │
│    feature/* → develop → release → main                             │
│                                                                      │
│  TESTING:                                                            │
│    Feature:  Test ONLY new code (pytest --no-cov)                  │
│    Develop:  Test EVERYTHING (make test-unit) - MANDATORY!         │
│    Release:  Full tests + integration + approval                    │
│    Main:     HOLY - merge only from release via PR                 │
│                                                                      │
│  AUTONOMY:                                                          │
│    ✅ Create files/directories without asking                      │
│    ✅ Use templates from .ai-templates/                             │
│    ✅ Commit and push to feature/develop                           │
│    ✅ Format/lint before every commit                              │
│    ❌ DO NOT ask obvious questions                                 │
│                                                                      │
│  SECURITY:                                                           │
│    ⚠️  ALWAYS tenant_id in SQL queries                              │
│    ⚠️  NEVER nano/vim/less/git -i (interactive commands)            │
│    ⚠️  NEVER force push to main/release                             │
│                                                                      │
│  TESTS AS CONTRACT:                                                  │
│    ❌ Test fails → Fix CODE, not test                               │
│    ✅ Test correctly describes expected behavior                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📚 Additional Documents (As Needed)

After reading the mandatory ones, read as needed:

| Situation | Document | When to read |
|-----------|----------|--------------|
| Adding a new feature | `PROJECT_STRUCTURE.md` | Where to place files |
| | `CONVENTIONS.md` | How to write code |
| | `.ai-templates/README.md` | Which template to use |
| Modifying tests | `docs/AGENTS_TEST_POLICY.md` | Testing philosophy |
| Working with git | `BRANCH_STRATEGY.md` | Workflow details |
| | `docs/BRANCHING.md` | Git commands |
| Creating a PR | `CONTRIBUTING.md` | Contribution process |
| Public PR | `PUBLIC_REPO_STRATEGY.md` | Rules for external PRs |

---

## 🎓 Example - Correct Session Start

```
User: "Add cache service with Redis"

Agent: [SILENCE - reads documents]
       1. ✅ Read CRITICAL_AGENT_RULES.md (5 min)
       2. ✅ Read AI_AGENT_MANIFEST.md (3 min)
       3. ✅ Read AUTONOMOUS_OPERATIONS.md (2 min)
       4. ✅ Checked git status: branch develop, clean
       5. ✅ Checked CI: last run PASSED
       6. ✅ Read PROJECT_STRUCTURE.md - where to place service
       7. ✅ Read CONVENTIONS.md - Service Layer pattern

Agent: [Starts working AUTONOMOUSLY - WITHOUT asking]
       1. ✅ git checkout -b feature/add-cache-service
       2. ✅ cp .ai-templates/service_template.py services/cache_service.py
       3. ✅ [Implementation of cache service with DI]
       4. ✅ cp .ai-templates/test_template.py tests/services/test_cache_service.py
       5. ✅ [Implementation of tests]
       6. ✅ pytest --no-cov tests/services/test_cache_service.py
       7. ✅ make format && make lint
       8. ✅ git add .
       9. ✅ git commit -m "feat(services): add Redis cache service with DI"
       10. ✅ git push origin feature/add-cache-service

Agent: "Implemented cache service with full test coverage.

        Results:
        - ✅ CacheService in services/cache_service.py
        - ✅ 12 tests in tests/services/test_cache_service.py (12/12 PASSED)
        - ✅ Dependency Injection pattern
        - ✅ Lint: PASSED
        - ✅ Format: PASSED
        - ✅ Pushed to feature/add-cache-service

        Ready for merge to develop."
```

---

## 🚫 Example - INCORRECT Session Start

```
User: "Add cache service"

Agent: "Should I create a new file?"              # ❌ BAD!
User: "Yes"
Agent: "Where should I put it?"                       # ❌ BAD! Read PROJECT_STRUCTURE.md
User: "In services/"
Agent: "Should I add tests?"                     # ❌ BAD! Always add tests
User: "Yes"
Agent: "Which pattern to use?"                     # ❌ BAD! Use templates
User: "Repository pattern"
Agent: "Can I commit now?"               # ❌ BAD! Commit autonomously
User: "Yes"

[15 minutes wasted on questions about obvious things]
```

---

## ⏱️ Timeline Summary

```
┌────────────────┬──────────────────────────────────────────┐
│ Time           │ Action                                   │
├────────────────┼──────────────────────────────────────────┤
│ 0:00 - 0:05    │ Read CRITICAL_AGENT_RULES.md             │
│ 0:05 - 0:08    │ Read AI_AGENT_MANIFEST.md                │
│ 0:08 - 0:10    │ Read AUTONOMOUS_OPERATIONS.md            │
│ 0:10 - 0:13    │ Check git status, CI, context            │
│ 0:13 - 0:15    │ Identify task type                       │
│ 0:15+          │ START WORK AUTONOMOUSLY                  │
└────────────────┴──────────────────────────────────────────┘
```

---

## ✅ Checklist - Ready to Work

Before starting implementation, confirm:

- [ ] ✅ I have read CRITICAL_AGENT_RULES.md (10 rules)
- [ ] ✅ I have read AI_AGENT_MANIFEST.md (navigation)
- [ ] ✅ I have read AUTONOMOUS_OPERATIONS.md (what to do without asking)
- [ ] ✅ I have checked git status and CI
- [ ] ✅ I have identified the task type (feature/bugfix/docs/release)
- [ ] ✅ I know which branch I am working on
- [ ] ✅ I understand that I DO NOT ask about standard operations
- [ ] ✅ Ready to work AUTONOMOUSLY

---

## 🆘 What to Do When...

| Situation | Action |
|-----------|--------|
| Don't know where to put a file | Read `PROJECT_STRUCTURE.md` - DO NOT ask |
| Don't know which pattern to use | Read `CONVENTIONS.md` + use `.ai-templates/` - DO NOT ask |
| Tests fail | Fix CODE, not test (unless the test is wrong) |
| CI is red on develop | Fix on develop, DO NOT merge to main |
| Need approval | Only for release→main and main merges |
| Really don't know what to do | NOW you can ask the user |

---

## 🎯 Success Metrics

You know you started the session well when:

- ✅ You spent 15 minutes reading documentation
- ✅ You DID NOT ask any "obvious" questions
- ✅ You started with `git checkout -b feature/...`
- ✅ You used templates from `.ai-templates/`
- ✅ You tested according to the branch
- ✅ You committed with a conventional message
- ✅ You reported the result, did not ask "can I continue?"

---

**Version**: 1.0.0
**Date**: 2025-12-10
**Status**: 🔴 MANDATORY - Required before every session
**Last Updated**: 2025-12-10

**Remember**: These 15 minutes of reading will save hours of asking questions and fixing!
