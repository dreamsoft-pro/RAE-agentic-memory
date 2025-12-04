# 🤖 AI Agent Onboarding Guide - RAE Project

> **Welcome!** This guide will get you productive on the RAE project in 15 minutes.

## 🎯 Quick Start (5 Minutes)

### Step 1: Read These Files First (In Order)

1. **THIS FILE** (you're here!) - Overview and first steps
2. **PROJECT_STRUCTURE.md** - Where to find/add code
3. **CONVENTIONS.md** - How to write code (with WHY explanations)
4. **.cursorrules** - Complete rules and protocols

**⏰ Time: 10 minutes of reading = Hours saved later**

### Step 2: Understand the System

RAE uses a **3-layer architecture**:

```
API Layer (routes)
    ↓
Service Layer (business logic)
    ↓
Repository Layer (database)
```

**Key Principle**: Never skip layers! Always go API → Service → Repository.

### Step 3: Know Your Templates

Located in `.ai-templates/`:
- `repository_template.py` - Data access layer
- `service_template.py` - Business logic layer
- `route_template.py` - API endpoints
- `test_template.py` - All types of tests

**Use these templates for EVERY new code!**

## 📚 Essential Documentation

### Documentation Hierarchy (Read in This Order)

#### Level 1: Must Read Before Any Work
- ✅ `PROJECT_STRUCTURE.md` - File locations, import patterns
- ✅ `CONVENTIONS.md` - Architectural patterns with WHY
- ✅ `.cursorrules` - Complete rules including Design-First Protocol

#### Level 2: Read Before Specific Tasks
- 📝 `docs/AGENTS_TEST_POLICY.md` - Testing philosophy (tests = contracts)
- 📝 `docs/BRANCHING.md` - Git workflow (hybrid strategy)
- 📝 `.ai-templates/README.md` - How to use templates

#### Level 3: Reference When Needed
- 📖 `docs/reference/architecture/` - Deep architectural docs
- 📖 `docs/guides/developers/` - Developer guides
- 📖 `Makefile` - Available commands

## 🎓 Your First Task - Step by Step

Let's walk through adding a simple feature: **User preferences management**

### Phase 1: Design First (MANDATORY!)

**❌ DON'T**: Start coding immediately
**✅ DO**: Follow Design-First Protocol

#### 1.1 Read Documentation (5 minutes)
```bash
# Read these before starting:
cat PROJECT_STRUCTURE.md
cat CONVENTIONS.md
cat .ai-templates/README.md
```

#### 1.2 Create Design Document

Write this in your response to the user:

```markdown
# Design: User Preferences Management

## Problem Statement
Users need to store and retrieve preferences (theme, language, notification settings)
with proper tenant isolation.

## Proposed Solution
Implement 3-layer architecture:
- PreferenceRepository (CRUD operations)
- PreferenceService (validation, business rules)
- API endpoints at /api/v1/users/preferences

## Architecture Impact
- Layers affected: Repository, Service, API
- New files:
  - apps/memory_api/repositories/preference_repository.py
  - apps/memory_api/services/preference_service.py
  - apps/memory_api/api/v1/preferences.py
  - apps/memory_api/models/preference.py
- Modified files:
  - apps/memory_api/api/v1/__init__.py (register router)
- Dependencies: None (uses existing asyncpg, Pydantic)

## Implementation Plan
1. Create Pydantic models (PreferenceInput, PreferenceOutput)
2. Create PreferenceRepository (get, insert, update, delete)
3. Create PreferenceService (validation, business logic)
4. Add API endpoints (GET, POST, PATCH, DELETE)
5. Add tests for all 3 layers
6. Update router registration

## Code Structure
Repository: apps/memory_api/repositories/preference_repository.py
Service: apps/memory_api/services/preference_service.py
API: apps/memory_api/api/v1/preferences.py
Models: apps/memory_api/models/preference.py
Tests:
  - apps/memory_api/tests/repositories/test_preference_repository.py
  - apps/memory_api/tests/services/test_preference_service.py
  - apps/memory_api/tests/api/v1/test_preferences.py

## Testing Strategy
- Unit tests: PreferenceService (mock repository)
- Integration tests: PreferenceRepository (real DB)
- API tests: Endpoints (TestClient)
- Expected coverage: 80%+

## Risks/Concerns
None - follows established patterns
```

#### 1.3 Wait for Approval (If Uncertain)
- If design is straightforward → proceed
- If multiple approaches → ask user
- If breaking changes → definitely ask

### Phase 2: Implementation

#### 2.1 Create Models First
```python
# apps/memory_api/models/preference.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PreferenceInput(BaseModel):
    """Input model for user preferences."""
    theme: str = Field(..., description="UI theme (light/dark)")
    language: str = Field(default="en", description="Language code")
    notifications_enabled: bool = Field(default=True)

class PreferenceOutput(BaseModel):
    """Output model for user preferences."""
    id: str
    user_id: str
    tenant_id: str
    theme: str
    language: str
    notifications_enabled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

#### 2.2 Create Repository (Copy from Template!)
```bash
# Open template:
cat .ai-templates/repository_template.py

# Copy structure, replace "Entity" with "Preference"
# Keep all patterns: RLS, logging, error handling
```

Key points from template:
- ✅ Include `tenant_id` in ALL queries
- ✅ Use `asyncpg.Pool` for connections
- ✅ Add structured logging
- ✅ Return `Dict` or `None` (not Pydantic models)

#### 2.3 Create Service (Copy from Template!)
```bash
cat .ai-templates/service_template.py

# Copy structure, implement business logic
```

Key points:
- ✅ Dependency Injection in `__init__`
- ✅ Use Pydantic models for input/output
- ✅ Validate business rules before calling repo
- ✅ Add error handling

#### 2.4 Create API Routes (Copy from Template!)
```bash
cat .ai-templates/route_template.py

# Copy endpoint structure
```

Key points:
- ✅ Use `Depends(get_and_verify_tenant_id)`
- ✅ Proper HTTP status codes
- ✅ OpenAPI documentation in docstrings
- ✅ Delegate to service layer

#### 2.5 Create Tests (Copy from Template!)
```bash
cat .ai-templates/test_template.py

# Use AAA pattern (Arrange-Act-Assert)
```

### Phase 3: Testing & Quality

#### 3.1 Run Focused Tests (Development)
```bash
# ✅ CORRECT - Use --no-cov during development
make test-focus FILE=apps/memory_api/tests/services/test_preference_service.py

# OR
pytest --no-cov apps/memory_api/tests/services/test_preference_service.py -v
```

**⚠️ NEVER**: Run single test without `--no-cov` - it will fail due to global coverage threshold!

#### 3.2 Format & Lint
```bash
make format  # Auto-fix formatting
make lint    # Check for issues
```

#### 3.3 Run Full Test Suite (Before Commit)
```bash
make test-unit  # All unit tests with coverage
```

### Phase 4: Git Workflow

#### 4.1 Create Feature Branch
```bash
git checkout develop
git pull origin develop
git checkout -b feature/user-preferences
```

#### 4.2 Commit with Conventional Commits
```bash
git add .
git commit -m "feat: add user preferences management

Implements 3-layer architecture for user preferences:
- PreferenceRepository for data access
- PreferenceService for business logic
- API endpoints at /api/v1/users/preferences

Includes:
- CRUD operations with tenant isolation
- Input validation
- Comprehensive tests (80%+ coverage)
- OpenAPI documentation"
```

#### 4.3 Merge to Develop
```bash
git checkout develop
git merge feature/user-preferences --no-ff
```

#### 4.4 Run Full Test Suite on Develop
```bash
make test-unit  # Must pass!
make lint       # Must pass!
make security   # Check warnings
```

#### 4.5 Merge to Main & Push Both
```bash
git checkout main
git merge develop --no-ff
git push origin main develop
```

#### 4.6 Verify GitHub Actions
```bash
gh run list --branch main --limit 1
gh run watch  # Wait for green CI
```

**If CI fails**: Fix immediately and push again. NEVER leave main with red CI!

## 🛡️ Critical Rules (NEVER VIOLATE!)

### 1. Design-First Protocol
- ❌ DON'T: Start coding without design
- ✅ DO: Write design document first
- ✅ DO: Use templates for implementation

### 2. Layer Separation
- ❌ DON'T: Put SQL in API routes
- ❌ DON'T: Put business logic in repositories
- ✅ DO: Follow API → Service → Repository

### 3. Security (Multi-Tenancy)
- ❌ DON'T: Write queries without `tenant_id`
- ✅ DO: Always include `tenant_id` in WHERE clause
- ✅ DO: Use `Depends(get_and_verify_tenant_id)` in routes

### 4. Testing
- ❌ DON'T: Run single tests without `--no-cov`
- ❌ DON'T: Change tests to make them pass if behavior is correct
- ✅ DO: Use `make test-focus FILE=...` during development
- ✅ DO: Treat tests as contracts, not snapshots

### 5. Git Workflow
- ❌ DON'T: Push to main with failing tests
- ❌ DON'T: Skip full test suite on develop
- ✅ DO: Test feature only on feature branch
- ✅ DO: Test everything on develop before main
- ✅ DO: Keep main == develop (always synchronized)

### 6. Autonomous Work
- ❌ DON'T: Ask for permission to create files
- ❌ DON'T: Stop work and wait unnecessarily
- ✅ DO: Work autonomously following patterns
- ✅ DO: Make decisions based on existing patterns
- ✅ DO: Only ask when genuinely ambiguous

### 7. Forbidden Commands
- ❌ NEVER: `nano`, `vim`, `vi`, `emacs` (interactive editors)
- ❌ NEVER: `less`, `more` (interactive pagers)
- ❌ NEVER: `git add -i`, `git rebase -i` (interactive git)
- ✅ DO: Use `cat`, `head`, `tail` for viewing
- ✅ DO: Use Edit/Write tools for file changes
- ✅ DO: Use non-interactive git commands

## 🔧 Essential Commands

### Development Loop
```bash
# 1. Format code
make format

# 2. Run focused test (during development)
make test-focus FILE=path/to/test_file.py

# 3. Run linter
make lint

# 4. Run full test suite (before commit)
make test-unit

# 5. Run security scan
make security
```

### Git Operations
```bash
# Create feature branch
git checkout develop && git checkout -b feature/name

# Commit
git add .
git commit -m "feat: description"

# Merge to develop
git checkout develop && git merge feature/name --no-ff

# Run tests on develop
make test-unit && make lint

# Merge to main and push both
git checkout main && git merge develop --no-ff
git push origin main develop

# Check CI status
gh run list --branch main --limit 1
```

### Testing
```bash
# Quick test during development (NO COVERAGE!)
pytest --no-cov path/to/test.py -v

# Or use make target
make test-focus FILE=path/to/test.py

# Full unit test suite with coverage
make test-unit

# Integration tests (requires services)
make test-integration

# All tests with coverage report
make test-cov
```

## 📋 Pre-Commit Checklist

Before every commit, verify:

- [ ] Code follows PROJECT_STRUCTURE.md (correct locations)
- [ ] Code follows CONVENTIONS.md (Repository/Service/API patterns)
- [ ] Used templates from `.ai-templates/`
- [ ] Tests added for all layers
- [ ] Docstrings added (Google style)
- [ ] Structured logging added (structlog)
- [ ] Security: `tenant_id` in all database queries
- [ ] No interactive commands used
- [ ] `make format` executed
- [ ] `make lint` passes
- [ ] `make test-unit` passes (full suite)
- [ ] No secrets/API keys in code

## 🎨 Code Quality Standards

### Imports
```python
# ✅ CORRECT - Absolute imports
from apps.memory_api.models import Memory
from apps.memory_api.repositories.memory_repository import MemoryRepository
from apps.memory_api.services.hybrid_search import HybridSearchService

# ❌ WRONG - Relative imports
from ..models import Memory
from .memory_repository import MemoryRepository
```

### Logging
```python
# ✅ CORRECT - Structured logging
import structlog
logger = structlog.get_logger(__name__)

logger.info("operation_started", tenant_id=tenant_id, operation="search")
logger.error("operation_failed", error=str(e), tenant_id=tenant_id)

# ❌ WRONG - String formatting
logger.info(f"Operation started for {tenant_id}")
```

### Error Handling
```python
# ✅ CORRECT - Proper exception handling
try:
    result = await service.do_work()
    return result
except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    logger.exception("unexpected_error", error=str(e))
    raise HTTPException(status_code=500, detail="Internal server error")

# ❌ WRONG - Bare except
try:
    result = await service.do_work()
except:
    pass  # ❌ Never do this!
```

## 🚨 Common Mistakes & How to Avoid Them

### Mistake 1: Skipping Design-First
**Wrong**: Start coding immediately
**Right**: Write design document, get approval, then code

### Mistake 2: Mixing Layers
**Wrong**: SQL in API routes
**Right**: API → Service → Repository (always)

### Mistake 3: Missing tenant_id
**Wrong**: `SELECT * FROM users WHERE id = $1`
**Right**: `SELECT * FROM users WHERE id = $1 AND tenant_id = $2`

### Mistake 4: Testing Without --no-cov
**Wrong**: `pytest path/to/test.py` (fails due to coverage threshold)
**Right**: `pytest --no-cov path/to/test.py` or `make test-focus FILE=...`

### Mistake 5: Changing Tests Instead of Code
**Wrong**: Test fails → change test to pass
**Right**: Test fails → understand WHY → fix CODE (tests = contracts!)

### Mistake 6: Using Interactive Commands
**Wrong**: `nano file.py`, `vim file.py`, `git add -i`
**Right**: Use Edit/Write tools, `cat`/`head`/`tail`, non-interactive git

## 🎯 Success Indicators

You're doing it right when:
- ✅ Code fits naturally into existing structure
- ✅ Tests pass on first try
- ✅ No refactoring needed after 2-3 days
- ✅ Code review has minimal comments
- ✅ CI passes without fixes
- ✅ Other agents can understand your code immediately

## 📞 Getting Help

### Quick References
- **File locations**: `PROJECT_STRUCTURE.md`
- **Coding patterns**: `CONVENTIONS.md`
- **Complete rules**: `.cursorrules`
- **Templates**: `.ai-templates/README.md`
- **Testing**: `docs/AGENTS_TEST_POLICY.md`
- **Git workflow**: `docs/BRANCHING.md`

### Finding Examples
```bash
# Find similar code
grep -r "class.*Repository" apps/memory_api/repositories/

# Find API endpoints
grep -r "@router\." apps/memory_api/api/

# Find test patterns
ls apps/memory_api/tests/
```

### Command Reference
```bash
make help          # Show all available commands
make test-focus    # Test single file (dev mode)
make test-unit     # Full test suite
make lint          # Check code quality
make format        # Auto-format code
```

## 🎓 Learning Path

### Week 1: Familiarization
1. Read all essential docs (PROJECT_STRUCTURE, CONVENTIONS, .cursorrules)
2. Study templates in `.ai-templates/`
3. Explore existing code in `apps/memory_api/`
4. Run tests to understand coverage

### Week 2: First Contributions
1. Add a simple service using templates
2. Add API endpoint with tests
3. Follow full git workflow
4. Get comfortable with make commands

### Week 3: Advanced Patterns
1. Implement complex business logic
2. Add integration tests
3. Contribute to documentation
4. Optimize existing code

### Week 4: Mastery
1. Design new features independently
2. Review other agents' code
3. Improve templates and docs
4. Help onboard new agents

## 🚀 Ready to Start!

You now have everything you need to contribute high-quality code to RAE!

**Next Steps:**
1. ✅ Read PROJECT_STRUCTURE.md (10 min)
2. ✅ Read CONVENTIONS.md (20 min)
3. ✅ Explore `.ai-templates/` (10 min)
4. ✅ Try your first task following this guide
5. ✅ Ask questions if stuck

**Remember:**
- 📚 Design first, code second
- 🏗️ Use templates always
- 🧪 Test continuously (--no-cov in dev)
- 🔒 Security always (tenant_id everywhere)
- 🤖 Work autonomously, ask only when genuinely unclear

**Welcome to the team! 🎉**

---

**Last Updated**: 2025-12-04
**Maintained by**: AI Agent Code Quality System
