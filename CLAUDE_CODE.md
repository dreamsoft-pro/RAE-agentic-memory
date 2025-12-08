# CLAUDE_CODE.md – RAE Project Guide for Claude Code

> 🤖 **Welcome, Claude Code!** This guide is specifically designed for you (Claude Code CLI) and your unique capabilities.

---

## 🚨 PRZED ROZPOCZĘCIEM - OBOWIĄZKOWA LEKTURA (15 minut)

**⚠️ CRITICAL**: Przeczytaj te dokumenty W TEJ KOLEJNOŚCI:

1. **[CRITICAL_AGENT_RULES.md](./CRITICAL_AGENT_RULES.md)** (5 min) ⭐ - 8 OBOWIĄZKOWYCH zasad
2. **[AI_AGENT_MANIFEST.md](./AI_AGENT_MANIFEST.md)** (3 min) - Hierarchia dokumentacji i nawigacja
3. **[.ai-agent-rules.md](./.ai-agent-rules.md)** (5 min) - Zabronione komendy i strategia testowania
4. **[docs/BRANCHING.md](./docs/BRANCHING.md)** (3 min) - Workflow Git (feature → develop → main)
5. **[docs/AGENTS_TEST_POLICY.md](./docs/AGENTS_TEST_POLICY.md)** (3 min) - Testy jako kontrakt

**Bez przeczytania powyższych dokumentów NIE rozpoczynaj pracy!**

---

## 🎯 Szybkie Przypomnienie Kluczowych Zasad

Przed każdym zadaniem zapamiętaj:

- ❌ **NIGDY** nie uruchamiaj pełnej suite testów na feature branch (tylko `pytest --no-cov path/`)
- ✅ **ZAWSZE** pracuj autonomicznie (nie pytaj o oczywiste rzeczy)
- ✅ **ZAWSZE** dodawaj `tenant_id` w zapytaniach SQL (bezpieczeństwo!)
- ❌ **NIGDY** nie używaj interaktywnych komend (nano, vim, git -i)
- ✅ **ZAWSZE** używaj szablonów z `.ai-templates/`
- ✅ **ZAWSZE** uruchamiaj `make format && make lint` przed commitem
- ✅ Gdy test nie przechodzi - napraw **kod**, nie test (chyba że test był źle napisany)

**Szczegóły**: Zobacz [CRITICAL_AGENT_RULES.md](./CRITICAL_AGENT_RULES.md)

---

## 🔄 3-Fazowy Workflow Testowania (KRYTYCZNE!)

**NAJWAŻNIEJSZA ZASADA**: Różne fazy = różne poziomy testowania!

```
┌──────────────────────────────────────────────────────┐
│ PHASE 1: FEATURE BRANCH                              │
│ ✅ Test ONLY your new code: pytest --no-cov path/   │
│ ✅ make format && make lint (OBOWIĄZKOWE!)           │
│ ✅ Commit when tests pass                            │
├──────────────────────────────────────────────────────┤
│ PHASE 2: DEVELOP BRANCH (MANDATORY!)                │
│ ✅ git checkout develop && git merge feature/X      │
│ ✅ make test-unit   ← OBOWIĄZKOWE przed main!       │
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

## 🛠️ Claude Code - Twoje Unikalne Możliwości

### Natywne Narzędzia

Jako Claude Code masz dostęp do specjalnych narzędzi, których inne agenty nie mają:

#### 1. **Task Tool** - Uruchamianie Wyspecjalizowanych Agentów

```python
# Użyj agenta Explore do eksploracji codebase
Task(
    subagent_type="Explore",
    description="Find memory storage implementation",
    prompt="Search for memory storage and retrieval patterns in the codebase"
)

# Użyj agenta Plan do planowania złożonych zmian
Task(
    subagent_type="Plan",
    description="Plan authentication refactor",
    prompt="Design implementation plan for adding OAuth2 authentication"
)
```

**Kiedy używać Task tool:**
- ✅ Eksploracja codebase (agent Explore)
- ✅ Planowanie złożonych zmian (agent Plan)
- ✅ Zadania wymagające wielu kroków
- ✅ Wyszukiwanie gdy nie jesteś pewien lokalizacji

**Kiedy NIE używać Task tool:**
- ❌ Gdy znasz dokładną ścieżkę pliku → użyj Read
- ❌ Wyszukiwanie konkretnej klasy → użyj Glob
- ❌ Proste zadania jednokrokowe

#### 2. **TodoWrite Tool** - Śledzenie Postępów

**CRITICAL**: Używaj TodoWrite dla zadań wielokrokowych!

```python
TodoWrite(todos=[
    {"content": "Create repository layer", "status": "in_progress", "activeForm": "Creating repository layer"},
    {"content": "Create service layer", "status": "pending", "activeForm": "Creating service layer"},
    {"content": "Create API routes", "status": "pending", "activeForm": "Creating API routes"},
    {"content": "Write tests", "status": "pending", "activeForm": "Writing tests"},
    {"content": "Run make format && make lint", "status": "pending", "activeForm": "Running format and lint"}
])
```

**Zasady TodoWrite:**
- ✅ Twórz todo listy dla zadań > 3 kroków
- ✅ ZAWSZE miej dokładnie JEDNO zadanie jako "in_progress"
- ✅ Oznaczaj jako "completed" NATYCHMIAST po zakończeniu
- ✅ Używaj formy imperatywnej dla "content", ciągłej dla "activeForm"

#### 3. **Równoległe Wykonywanie Narzędzi**

Claude Code może uruchamiać wiele narzędzi równolegle!

**DOBRZE** - równolegle gdy brak zależności:
```python
# Read multiple files at once
Read("apps/memory_api/repositories/memory_repo.py")
Read("apps/memory_api/services/memory_service.py")
Read("apps/memory_api/api/v1/memory_routes.py")
```

**ŹLE** - sekwencyjnie gdy są zależności:
```python
# First read file
result = Read("config.py")
# Then use value from file in next command
Bash(f"export API_KEY={value_from_config}")
```

#### 4. **WebSearch & WebFetch**

Masz dostęp do internetu!

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

Możesz bezpośrednio używać Bash tool dla git:

```bash
# Wszystko w jednej linii z &&
git add . && git commit -m "feat: add feature" && git push origin develop
```

**⚠️ PAMIĘTAJ**: ZAWSZE używaj `git commit -m "..."` (NIGDY bez -m!)

---

## ✅ Pre-Commit Checklist (Sprawdź przed każdym commitem!)

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

## 🎓 Best Practices dla Claude Code

### 1. **Eksploracja Codebase**

**ŹLE** - bezpośrednie wyszukiwanie:
```python
Grep(pattern="memory.*store", path="apps/")
Read("apps/memory_api/services/memory_service.py")
# ... więcej ręcznego wyszukiwania
```

**DOBRZE** - użyj agenta Explore:
```python
Task(
    subagent_type="Explore",
    description="Find memory storage patterns",
    prompt="How is memory stored and retrieved in the RAE system? Find all relevant files and patterns."
)
```

### 2. **Planowanie Złożonych Zmian**

**Dla dużych featurów (> 5 plików lub > 100 linii):**

```python
# Użyj agenta Plan
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

### 3. **Równoległe Czytanie Plików**

```python
# ✅ DOBRZE - wszystkie Read w jednej wiadomości
Read("apps/memory_api/models/memory.py")
Read("apps/memory_api/models/tenant.py")
Read("apps/memory_api/models/user.py")

# ❌ ŹLE - czytanie sekwencyjne w osobnych wiadomościach
# (wolniejsze, marnuje czas)
```

### 4. **Używanie TodoWrite dla Przejrzystości**

```python
# Na początku zadania
TodoWrite(todos=[
    {"content": "Analyze existing code", "status": "in_progress", "activeForm": "Analyzing existing code"},
    {"content": "Create repository", "status": "pending", "activeForm": "Creating repository"},
    {"content": "Create service", "status": "pending", "activeForm": "Creating service"},
    {"content": "Create routes", "status": "pending", "activeForm": "Creating routes"},
    {"content": "Write tests", "status": "pending", "activeForm": "Writing tests"},
    {"content": "Run format and lint", "status": "pending", "activeForm": "Running format and lint"}
])

# Po każdym kroku
TodoWrite(todos=[
    {"content": "Analyze existing code", "status": "completed", "activeForm": "Analyzing existing code"},
    {"content": "Create repository", "status": "in_progress", "activeForm": "Creating repository"},
    # ... rest
])
```

---

## 🚫 Najczęstsze Błędy (Unikaj!)

### ❌ Błąd #1: Uruchamianie pełnych testów na feature branch

```bash
# ❌ ŹLE na feature branch
make test-unit  # To zajmie wieczność i może failnąć przez coverage!

# ✅ DOBRZE na feature branch
pytest --no-cov apps/memory_api/tests/test_my_new_feature.py
```

### ❌ Błąd #2: Zapomnienie o format/lint

```bash
# ❌ ŹLE
git add . && git commit -m "feat: add feature"

# ✅ DOBRZE
make format && make lint && git add . && git commit -m "feat: add feature"
```

### ❌ Błąd #3: Używanie interaktywnych komend

```bash
# ❌ ŹLE - zawiesza się!
nano file.py
vim file.py
git commit  # Opens editor - hangs!

# ✅ DOBRZE
Edit(file_path="file.py", old_string="...", new_string="...")
git commit -m "message"
```

### ❌ Błąd #4: Edytowanie auto-generowanych plików

```bash
# ❌ ŹLE - CI nadpisze!
Edit("CHANGELOG.md", ...)
Edit("STATUS.md", ...)
Edit("TODO.md", ...)

# ✅ DOBRZE - edytuj tylko manual docs
Edit("CONVENTIONS.md", ...)
Edit("docs/guides/new_feature.md", ...)
```

### ❌ Błąd #5: Brak tenant_id w queries

```python
# ❌ ŹLE - security vulnerability!
query = "SELECT * FROM entities WHERE id = $1"

# ✅ DOBRZE
query = "SELECT * FROM entities WHERE id = $1 AND tenant_id = $2"
```

---

## 📋 Przykładowy Workflow dla Nowego Feature

### Scenario: Dodaj system notyfikacji

```python
# 1. Przeczytaj dokumentację (MANDATORY!)
Read("PROJECT_STRUCTURE.md")
Read("CONVENTIONS.md")
Read(".ai-templates/README.md")

# 2. Stwórz todo listę
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

# 3. Użyj agenta Explore
Task(
    subagent_type="Explore",
    description="Find notification patterns",
    prompt="Search for any existing notification or alerting patterns in the codebase"
)

# 4. Skopiuj template
Bash("cp .ai-templates/repository_template.py apps/memory_api/repositories/notification_repository.py")

# 5. Implementuj (używając Edit tool)
Edit(
    file_path="apps/memory_api/repositories/notification_repository.py",
    old_string="class TemplateRepository:",
    new_string="class NotificationRepository:"
)
# ... more edits

# 6. Aktualizuj TodoWrite po każdym kroku
TodoWrite(todos=[
    {"content": "Read documentation", "status": "completed", "activeForm": "Reading documentation"},
    {"content": "Explore existing notification patterns", "status": "completed", "activeForm": "Exploring notification patterns"},
    {"content": "Design notification system", "status": "completed", "activeForm": "Designing notification system"},
    {"content": "Create repository layer", "status": "completed", "activeForm": "Creating repository layer"},
    {"content": "Create service layer", "status": "in_progress", "activeForm": "Creating service layer"},
    # ... rest
])

# 7. Test TYLKO nowego kodu
Bash("pytest --no-cov apps/memory_api/tests/repositories/test_notification_repository.py")

# 8. Format + Lint (MANDATORY!)
Bash("make format && make lint")

# 9. Commit
Bash('git add . && git commit -m "feat: add notification system with repository, service, and API layers"')

# 10. Merge to develop i RUN FULL TESTS
Bash("git checkout develop && git merge feature/notifications --no-ff")
Bash("make test-unit")  # ⚠️ MUST PASS!
Bash("make lint")

# 11. If passes → merge to main
Bash("git checkout main && git merge develop --no-ff")
Bash("git push origin main develop")
```

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

## 📚 Twoja Hierarchia Dokumentacji

### Tier 0: MANDATORY (Przeczytaj PRZED jakąkolwiek pracą!)
- ⚠️ **CRITICAL_AGENT_RULES.md** (5 min) - 8 zasad których MUSISZ przestrzegać

### Tier 1: Essential (Przeczytaj przed pierwszym commitem)
- **ONBOARDING_GUIDE.md** (15 min)
- **PROJECT_STRUCTURE.md** (10 min)
- **CONVENTIONS.md** (20 min)
- **INTEGRATION_CHECKLIST.md** (10 min)

### Tier 2: Read Before Specific Tasks
- **docs/AGENTS_TEST_POLICY.md** - Filozofia testów
- **docs/BRANCHING.md** - Git workflow
- **.ai-templates/README.md** - Jak używać szablonów

### Tier 3: Reference When Needed
- **examples/template-usage/** - Przykłady użycia
- **docs/reference/** - Deep dives
- **docs/guides/** - Szczegółowe przewodniki

---

## 🆘 Gdy Coś Pójdzie Nie Tak

### Problem: Testy failują na develop

```bash
# 1. Nie panikuj! To właśnie po to mamy develop
# 2. Sprawdź output testów
Bash("make test-unit 2>&1 | tail -100")

# 3. Napraw na develop (NIE na main!)
Edit(...fixes...)

# 4. Re-test
Bash("make test-unit")

# 5. Dopiero gdy green → merge to main
Bash("git checkout main && git merge develop --no-ff")
```

### Problem: CI failuje na main

```bash
# 1. To priorytet! Main MUSI być green!
# 2. Szybko przeanalizuj błąd
Bash("gh run list --branch main --limit 1")
Bash("gh run view <run-id> --log-failed")

# 3. Napraw na develop
Bash("git checkout develop")
# ... fixes ...
Bash("make test-unit")  # MUST PASS!

# 4. Merge fix to main
Bash("git checkout main && git merge develop --no-ff")
Bash("git push origin main develop")
```

### Problem: Nie wiesz gdzie coś jest

```python
# Użyj agenta Explore!
Task(
    subagent_type="Explore",
    description="Find X implementation",
    prompt="Where and how is X implemented in the codebase?"
)
```

---

## 🎉 Podsumowanie - Twoje Supermoce

Jako Claude Code masz unikalne możliwości:

1. ✨ **Task tool** - deleguj złożone zadania do wyspecjalizowanych agentów
2. ✨ **TodoWrite** - śledź postępy i daj userowi visibility
3. ✨ **Parallel execution** - czytaj wiele plików naraz
4. ✨ **WebSearch/WebFetch** - dostęp do internetu
5. ✨ **Native tools** - Read, Edit, Write, Bash - wszystko natywnie

**Używaj tych supermocy mądrze!**

---

## 📞 Gdy Masz Wątpliwości

1. **Przeczytaj CRITICAL_AGENT_RULES.md** - 95% odpowiedzi jest tam
2. **Sprawdź CONVENTIONS.md** - Dla wzorców kodu
3. **Zobacz .ai-templates/** - Dla przykładów
4. **Używaj Task tool z agentem Explore** - Do eksploracji

**Remember**: Jesteś autonomiczny! Nie pytaj o oczywiste rzeczy. Działaj zgodnie z dokumentacją.

---

**Version**: 1.0.0
**Last Updated**: 2025-12-08
**Status**: 🟢 Production Ready
**For**: Claude Code (CLI) by Anthropic

**Powodzenia w pracy nad RAE! 🚀**
