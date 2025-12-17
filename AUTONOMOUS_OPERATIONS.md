# 🤖 AUTONOMOUS OPERATIONS - Full Agent Autonomy

> **🎯 Goal**: The agent executes the plan from start to finish WITHOUT user interaction for standard operations
>
> **🔴 Status**: MANDATORY - This is not a suggestion, it's a REQUIREMENT

---

## 📜 MAIN PRINCIPLE

**The Agent ALWAYS acts AUTONOMOUSLY for all standard operations.**

```
┌────────────────────────────────────────────────────────────┐
│  "Yes to all" - User does NOT want to click "Yes" 100 times │
│                                                            │
│  If an operation is on the "AUTONOMOUS" list below,      │
│  you perform it IMMEDIATELY without asking.               │
│                                                            │
│  You ask ONLY about TRULY ambiguous things.               │
└────────────────────────────────────────────────────────────┘
```

---

## ✅ AUTONOMOUS OPERATIONS (DO NOT ASK!)

### 1. File System Operations

#### 1.1 Creation

| Operation | Autonomous? | Example | When NOT to ask |
|-----------|-------------|---------|-----------------|
| `mkdir` | ✅ YES | `mkdir -p apps/memory_api/services/cache/` | ALWAYS - directory structure is standard |
| `mkdir -p` (nested) | ✅ YES | `mkdir -p tests/unit/services/graph/` | ALWAYS - deep directories are OK |
| `touch` | ✅ YES | `touch apps/memory_api/services/cache_service.py` | ALWAYS - file creation is standard |
| Creation from template | ✅ YES | `cp .ai-templates/service.py services/new.py` | ALWAYS - templates are for this purpose |

**Example - Correct (Autonomous):**
```bash
# User: "Add cache service"
# Agent: [WITHOUT ASKING]
mkdir -p apps/memory_api/services/cache
mkdir -p apps/memory_api/tests/services/cache
cp .ai-templates/service_template.py apps/memory_api/services/cache/cache_service.py
cp .ai-templates/test_template.py apps/memory_api/tests/services/cache/test_cache_service.py
```

**Example - INCORRECT:**
```bash
# User: "Add cache service"
Agent: "Should I create a cache/ directory?"           # ❌ DO NOT ask!
Agent: "Should I use a template?"                     # ❌ DO NOT ask!
Agent: "In which directory should I put tests?"          # ❌ Read PROJECT_STRUCTURE.md
```

#### 1.2 Editing

| Operation | Autonomous? | When | Tool |
|-----------|-------------|------|------|
| Editing existing code | ✅ YES | Always when you have read the file before | Edit tool |
| Adding a function | ✅ YES | When the location is clear (service/repo/route) | Edit tool |
| Refactoring | ✅ YES | When behavior is preserved (tests as contract) | Edit tool |
| Formatting | ✅ YES | `make format` before every commit | black, isort |

**Never use:**
- ❌ `nano file.py` - interactive editor
- ❌ `vim file.py` - interactive editor
- ❌ `vi file.py` - interactive editor
- ❌ `emacs file.py` - interactive editor

**Use instead:**
- ✅ Edit tool (for changes)
- ✅ Write tool (for new files after reading an existing one)
- ✅ `cat file.py` (for reading)

#### 1.3 Deletion

| Operation | Autonomous? | Condition | When to ASK |
|-----------|-------------|-----------|-------------|
| Deleting a temporary file | ✅ YES | `*.pyc`, `__pycache__`, `.pytest_cache` | Never |
| Deleting an old test | ✅ YES | Replacing with a new test | Never (if part of the plan) |
| Deleting production code | ⚠️ CAUTION | Only if dead code (not used) | If unsure |
| Deleting an entire module | ❌ NO | - | ALWAYS ask |

---

### 2. Git Operations

#### 2.1 Basic Operations (100% Autonomous)

| Operation | Autonomous? | Branch | Example |
|-----------|-------------|--------|---------|
| `git status` | ✅ YES | All | Check status before work |
| `git checkout -b feature/X` | ✅ YES | From develop | Create feature branch |
| `git checkout develop` | ✅ YES | - | Switch to develop |
| `git pull origin develop` | ✅ YES | develop | Update before merge |
| `git add .` | ✅ YES | feature/develop | Add all changes |
| `git add <file>` | ✅ YES | All | Add specific file |
| `git commit -m "..."` | ✅ YES | All | With conventional message |
| `git push origin feature/X` | ✅ YES | feature/* | Push feature branch |
| `git push origin develop` | ✅ YES | develop | After local merge and tests |

**Example - Correct Flow:**
```bash
# User: "Implement feature X"
# Agent: [AUTONOMOUSLY without asking]

git checkout develop
git pull origin develop
git checkout -b feature/implement-x

# [... implementation ...]

make format && make lint
pytest --no-cov tests/test_feature_x.py

git add .
git commit -m "feat: implement feature X

- Add service layer implementation
- Add repository with tenant_id isolation
- Add comprehensive tests (15/15 passing)
- Add API endpoint documentation"

git push origin feature/implement-x

# Merge to develop (locally)
git checkout develop
git merge feature/implement-x --no-ff

# Full tests on develop (MANDATORY!)
make test-unit
make lint

# If passed
git push origin develop
```

#### 2.2 Merge Operations

| Operation | Autonomous? | Condition | When to ASK |
|-----------|-------------|-----------|-------------|
| `git merge feature/X` (to develop) | ✅ YES | After local tests | Never (standard flow) |
| `git merge develop` (to release) | ✅ YES | develop CI green | Never (standard flow) |
| `git merge release` (to main) | ❌ NO | - | ALWAYS via PR + 2 approvals |
| `git merge --no-ff` | ✅ YES | Preferred for merge | ALWAYS use --no-ff |

#### 2.3 FORBIDDEN Git Operations

| Operation | Status | Never do this | Why |
|-----------|--------|---------------|-----|
| `git push --force` | 🚫 FORBIDDEN | On any branch | Destroys history |
| `git push -f` | 🚫 FORBIDDEN | Alias for --force | Destroys history |
| `git rebase -i` | 🚫 FORBIDDEN | Interactive | Blocks CI/CD |
| `git add -i` | 🚫 FORBIDDEN | Interactive | Blocks CI/CD |
| `git commit` (without -m) | 🚫 FORBIDDEN | Opens editor | Blocks CI/CD |
| `git reset --hard origin/main` | ⚠️ VERY CAREFUL | Only if certain | Loses changes |

---

### 3. Testing

#### 3.1 Testing by Branch

| Branch | Command | Autonomous? | When | Time |
|--------|---------|-------------|------|------|
| feature/* | `pytest --no-cov <file>` | ✅ YES | Test ONLY new code | ~1-2 min |
| feature/* | `make test-focus FILE=<file>` | ✅ YES | Test ONLY new code | ~1-2 min |
| develop | `make test-unit` | ✅ YES | After merge from feature (MANDATORY!) | ~5-10 min |
| develop | `make lint` | ✅ YES | Always before push | ~30 sec |
| release | Full tests + integration | ✅ YES | Via CI automatically | ~10-15 min |
| main | CI automatically | ✅ YES | Via GitHub Actions | ~10-15 min |

**Example - Correct Testing:**
```bash
# On feature branch
git checkout -b feature/add-cache

# [implementation...]

# Test ONLY new code (NOT full suite!)
pytest --no-cov apps/memory_api/tests/services/test_cache_service.py -v
# 12 tests PASSED

# Format and lint
make format
make lint

git commit -m "feat: add cache service"
git push origin feature/add-cache

# Merge to develop
git checkout develop
git merge feature/add-cache --no-ff

# NOW full tests (MANDATORY!)
make test-unit
# 461 tests PASSED

# If OK
git push origin develop
```

#### 3.2 Formatting and Linting (Always Autonomous)

| Command | When | Autonomous? | Before what |
|---------|------|-------------|-------------|
| `make format` | Before every commit | ✅ YES | git commit |
| `make lint` | Before every commit | ✅ YES | git commit |
| `black .` | Part of make format | ✅ YES | Auto |
| `isort .` | Part of make format | ✅ YES | Auto |
| `ruff check .` | Part of make lint | ✅ YES | Auto |

**NEVER ask:**
- ❌ "Should I run make format?"
- ❌ "Should I fix linting errors?"
- ❌ "Should I run tests?"

**ALWAYS do:**
- ✅ `make format && make lint` before EVERY commit
- ✅ Fix all linting errors IMMEDIATELY
- ✅ Test according to branch (feature = only new, develop = all)

---

### 4. Technical Decisions (Autonomous)

#### 4.1 Pattern Selection

| Decision | Autonomous? | How to decide | Source |
|----------|-------------|---------------|--------|
| Repository vs Service? | ✅ YES | Always use both (3-layer arch) | CONVENTIONS.md |
| Which template to use? | ✅ YES | Repository/Service/Route by type | `.ai-templates/README.md` |
| Where to place the file? | ✅ YES | Mirrors structure | PROJECT_STRUCTURE.md |
| Dependency Injection? | ✅ YES | ALWAYS use DI | CONVENTIONS.md |
| Pydantic models? | ✅ YES | Input/Output models ALWAYS | CONVENTIONS.md |

**Example - Correct Autonomy:**
```python
# User: "Add user preferences"

# Agent: [WITHOUT ASKING - reads documentation and decides]
# 1. Read CONVENTIONS.md → 3-layer architecture
# 2. Read PROJECT_STRUCTURE.md → where to place
# 3. Used .ai-templates/ → DI pattern

# Result:
# - apps/memory_api/repositories/preference_repository.py (with tenant_id!)
# - apps/memory_api/services/preference_service.py (with DI!)
# - apps/memory_api/api/v1/preferences.py (with Depends!)
# - apps/memory_api/models/preference.py (Pydantic!)
# - tests/ (complete tests!)

# All compliant with standards, WITHOUT ASKING!
```

#### 4.2 Naming Conventions

| Element | Convention | Autonomous? | Example |
|---------|------------|-------------|---------|
| Repository Class | `{Entity}Repository` | ✅ YES | `UserRepository` |
| Service Class | `{Domain}Service` | ✅ YES | `CacheService` |
| Python File | `snake_case.py` | ✅ YES | `cache_service.py` |
| Test | `test_{module}.py` | ✅ YES | `test_cache_service.py` |
| Test Function | `test_{scenario}` | ✅ YES | `test_get_cache_returns_none_when_empty` |
| Branch | `feature/{description}` | ✅ YES | `feature/add-cache-service` |
| Commit message | Conventional Commits | ✅ YES | `feat(services): add cache service` |

**NEVER ask:**
- ❌ "What to name the file?"
- ❌ "What to name the class?"
- ❌ "What branch name?"

**ALWAYS use:**
- ✅ Conventions from CONVENTIONS.md
- ✅ Patterns from PROJECT_STRUCTURE.md
- ✅ Conventional Commits for messages

---

### 5. Test Structure (100% Autonomous)

| Aspect | Decision | Autonomous? | Rule |
|--------|----------|-------------|------|
| Where to place test? | mirrors source | ✅ YES | `services/X.py` → `tests/services/test_X.py` |
| Which pattern to use? | AAA (Arrange-Act-Assert) | ✅ YES | From `.ai-templates/test_template.py` |
| Mock or not? | Unit tests = mock, Integration = real | ✅ YES | Service tests = mock repo, Repo tests = real DB |
| Coverage threshold? | 80%+ for new code | ✅ YES | Automatic check in CI |
| Pytest markers? | By type (unit/integration/llm) | ✅ YES | `@pytest.mark.unit` for unit tests |

---

## ❓ KIEDY PYTAĆ UŻYTKOWNIKA?

Pytasz TYLKO w tych sytuacjach:

### 1. Architektura (Wiele Równie Dobrych Opcji)

| Sytuacja | Pytaj? | Przykład pytania |
|----------|--------|------------------|
| Wiele równie dobrych podejść | ✅ TAK | "Czy użyć Redis czy Memcached dla cache?" |
| Wybór zewnętrznej biblioteki | ✅ TAK | "Która biblioteka: spaCy czy NLTK?" |
| Breaking API changes | ✅ TAK | "Ta zmiana łamie API. Czy kontynuować?" |
| Nowa zależność | ✅ TAK | "Dodać tensorflow (3GB)? To duża zależność." |

**Przykład:**
```
Agent: "Implementuję cache service. Widzę 2 równie dobre opcje:

        Option 1: Redis (szybki, wymaga dodatkowego serwisu)
        Option 2: In-memory (prostszy, brak persistence)

        Która opcja preferowana?"
```

### 2. Biznes (Niejasne Wymagania)

| Sytuacja | Pytaj? | Przykład pytania |
|----------|--------|------------------|
| Niejasna specyfikacja | ✅ TAK | "Czy 'sort by relevance' oznacza hybrid search czy tylko semantic?" |
| Decyzja produktowa | ✅ TAK | "Czy limit 100 wyników to hard limit czy konfigurowalne?" |
| Dane biznesowe | ✅ TAK | "Jaki domyślny TTL dla cache: 5 min czy 1 godzina?" |

**Przykład:**
```
Agent: "Implementuję cache dla queries. Specyfikacja nie określa TTL.

        Co jest preferowane:
        - Short TTL (5 min): świeższe dane, więcej misses
        - Long TTL (1 hour): szybsze, mniej aktualne"
```

### 3. Ryzyko (Niebezpieczne Operacje)

| Operacja | Pytaj? | Zawsze | Nigdy nie rób bez zgody |
|----------|--------|--------|-------------------------|
| Force push | ✅ TAK | NA WSZYSTKICH BRANCHACH | ❌ Odmów natychmiast |
| Usuwanie danych | ✅ TAK | W produkcji lub develop | - |
| Zmiany w infrastrukturze | ✅ TAK | docker-compose.yml, CI/CD | - |
| Zmiany w security | ✅ TAK | RBAC, authentication, tenant isolation | - |

**Przykład:**
```
Agent: "⚠️ UWAGA: Usunięcie tego kodu spowoduje utratę danych w produkcji.

        Czy na pewno kontynuować?
        [Szczegóły: usuwa migration, będzie data loss]"
```

---

## 🎯 WZORCE AUTONOMICZNEJ PRACY

### Pattern 1: Dodaj Nowy Feature

```
1. Otrzymaj zadanie: "Dodaj cache service"

2. [CISZA - NIE pytaj o oczywiste rzeczy]

3. Czytaj dokumentację:
   ✅ PROJECT_STRUCTURE.md → gdzie umieścić
   ✅ CONVENTIONS.md → jak napisać
   ✅ .ai-templates/ → które template

4. Design (dla non-trivial):
   ✅ Napisz design document
   ✅ NIE pytaj o approval (chyba że multiple approaches)

5. Implementuj AUTONOMICZNIE:
   ✅ mkdir -p services/cache
   ✅ cp template → services/cache/cache_service.py
   ✅ [Implementacja z DI, logging, error handling]
   ✅ cp template → tests/services/cache/test_cache_service.py
   ✅ [15 testów covering all scenarios]

6. Testuj:
   ✅ pytest --no-cov tests/services/cache/test_cache_service.py
   ✅ make format && make lint

7. Commit:
   ✅ git add .
   ✅ git commit -m "feat(services): add Redis cache service"
   ✅ git push origin feature/add-cache

8. Raportuj wynik:
   ✅ "Zaimplementowałem cache service. 15/15 testów PASSED. Gotowe."

9. NIE pytaj "czy mogę kontynuować?"
```

### Pattern 2: Napraw Bug

```
1. Otrzymaj: "Napraw null pointer w reflection_engine.py"

2. [CISZA - NIE pytaj gdzie poszukać]

3. Znajdź problem:
   ✅ Czytaj reflection_engine.py
   ✅ Znajdź null pointer (linia 234)
   ✅ Zidentyfikuj root cause

4. Napraw:
   ✅ Edit reflection_engine.py (dodaj null check)
   ✅ Dodaj test dla edge case
   ✅ pytest --no-cov tests/test_reflection_engine.py

5. Commit:
   ✅ git commit -m "fix(reflection): add null check in generate_insights"

6. Raportuj:
   ✅ "Fixed null pointer w reflection_engine.py:234. Test dodany."
```

### Pattern 3: Refactoring

```
1. Otrzymaj: "Zrefactoruj graph_service.py do Repository pattern"

2. [CISZA - to standardowy refactoring]

3. Zaplanuj:
   ✅ Przeczytaj graph_service.py
   ✅ Zidentyfikuj SQL queries (5 queries)
   ✅ Plan: przenieś do GraphRepository

4. Implementuj:
   ✅ Utwórz repositories/graph_repository.py (z template)
   ✅ Przenieś 5 queries do repository
   ✅ Zmień graph_service.py (inject repository)
   ✅ Dodaj testy repository (mock db)
   ✅ Aktualizuj testy service (mock repository)

5. Testuj:
   ✅ pytest --no-cov tests/repositories/test_graph_repository.py
   ✅ pytest --no-cov tests/services/test_graph_service.py
   ✅ make test-unit (na develop po merge)

6. Commit:
   ✅ git commit -m "refactor(graph): extract queries to GraphRepository"

7. Raportuj:
   ✅ "Refactoring complete. Wszystkie testy PASS."
```

---

## 📊 Scorecard - Czy Pracujesz Autonomicznie?

Sprawdź się po każdej sesji:

| Pytanie | TAK = Źle | NIE = Dobrze |
|---------|-----------|--------------|
| Czy zapytałem "czy mogę utworzyć plik?" | ❌ -1 pkt | ✅ +1 pkt |
| Czy zapytałem "czy dodać testy?" | ❌ -1 pkt | ✅ +1 pkt |
| Czy zapytałem "którego wzorca użyć?" | ❌ -1 pkt | ✅ +1 pkt |
| Czy zapytałem "czy mogę commitować?" | ❌ -1 pkt | ✅ +1 pkt |
| Czy użyłem templates z .ai-templates/? | ✅ +1 pkt | ❌ -1 pkt |
| Czy testowałem zgodnie z branchem? | ✅ +1 pkt | ❌ -1 pkt |
| Czy make format && make lint przed commitem? | ✅ +1 pkt | ❌ -1 pkt |
| Czy scommitowałem z conventional message? | ✅ +1 pkt | ❌ -1 pkt |

**Scoring:**
- **8 pkt**: Perfect! Pełna autonomia ⭐⭐⭐
- **5-7 pkt**: Dobre, ale można lepiej ⭐⭐
- **0-4 pkt**: Za dużo pytań, przeczytaj ten dokument ponownie ⭐
- **< 0 pkt**: Przeczytaj SESSION_START.md i zacznij od nowa

---

## 🚦 Quick Decision Tree

```
                     Otrzymałeś zadanie
                            │
                            ▼
               ┌─────────────────────────┐
               │ Czy jest to STANDARDOWA │
               │ operacja z listy?       │
               └────────┬───────┬────────┘
                       TAK     NIE
                        │       │
                        ▼       ▼
                   ┌─────┐  ┌──────────┐
                   │WYKONAJ│ │Czy widzisz│
                   │BEZ    │ │WIELE     │
                   │PYTANIA│ │równie    │
                   └───────┘ │dobrych   │
                             │opcji?    │
                             └─┬────┬───┘
                              TAK  NIE
                               │    │
                               ▼    ▼
                          ┌──────┐ ┌──────┐
                          │ZAPYTAJ││WYBIERZ│
                          │USER  │ │najlepszą│
                          └──────┘ │i WYKONAJ│
                                   └──────┘
```

---

## ✅ Checklist - Przed Każdą Implementacją

- [ ] Przeczytałem CRITICAL_AGENT_RULES.md (10 zasad)
- [ ] Przeczytałem AI_AGENT_MANIFEST.md (nawigacja)
- [ ] Przeczytałem TEN DOKUMENT (autonomous operations)
- [ ] Rozumiem że NIE pytam o standardowe operacje
- [ ] Znam lokalizacje plików (PROJECT_STRUCTURE.md)
- [ ] Znam wzorce kodu (CONVENTIONS.md)
- [ ] Mam dostęp do templates (.ai-templates/)
- [ ] Wiem jak testować wg brancha
- [ ] Rozumiem git workflow (feature→develop→release→main)
- [ ] Gotowy do PEŁNEJ AUTONOMII

---

**Wersja**: 1.0.0
**Data**: 2025-12-10
**Status**: 🔴 MANDATORY - Wymagane dla wszystkich agentów
**Ostatnia aktualizacja**: 2025-12-10

**Pamiętaj**: Autonomia = Szybkość. Każde pytanie o oczywistą rzecz marnuje 2-5 minut użytkownika. Pomnóż to przez 20 pytań = 40-100 minut straconych!
