# 🤖 AUTONOMOUS OPERATIONS - Pełna Autonomia Agenta

> **🎯 Cel**: Agent realizuje plan od początku do końca BEZ interakcji z użytkownikiem dla standardowych operacji
>
> **🔴 Status**: MANDATORY - To nie jest sugestia, to WYMAGANIE

---

## 📜 ZASADA GŁÓWNA

**Agent ZAWSZE działa AUTONOMICZNIE dla wszystkich standardowych operacji.**

```
┌────────────────────────────────────────────────────────────┐
│  "Yes to all" - Użytkownik NIE chce klikać "Yes" 100 razy │
│                                                            │
│  Jeśli operacja jest na liście "AUTONOMICZNE" poniżej,    │
│  wykonujesz ją NATYCHMIAST bez pytania.                   │
│                                                            │
│  Pytasz TYLKO o rzeczy NAPRAWDĘ niejednoznaczne.         │
└────────────────────────────────────────────────────────────┘
```

---

## ✅ OPERACJE AUTONOMICZNE (NIE PYTAJ!)

### 1. Operacje na Systemie Plików

#### 1.1 Tworzenie

| Operacja | Autonomiczna? | Przykład | Kiedy NIE pytać |
|----------|---------------|----------|-----------------|
| `mkdir` | ✅ TAK | `mkdir -p apps/memory_api/services/cache/` | ZAWSZE - struktura katalogów jest standardowa |
| `mkdir -p` (nested) | ✅ TAK | `mkdir -p tests/unit/services/graph/` | ZAWSZE - deep directories są OK |
| `touch` | ✅ TAK | `touch apps/memory_api/services/cache_service.py` | ZAWSZE - tworzenie plików jest standardowe |
| Tworzenie z template | ✅ TAK | `cp .ai-templates/service.py services/new.py` | ZAWSZE - templates istnieją po to |

**Przykład - Prawidłowy (Autonomiczny):**
```bash
# User: "Dodaj cache service"
# Agent: [BEZ PYTANIA]
mkdir -p apps/memory_api/services/cache
mkdir -p apps/memory_api/tests/services/cache
cp .ai-templates/service_template.py apps/memory_api/services/cache/cache_service.py
cp .ai-templates/test_template.py apps/memory_api/tests/services/cache/test_cache_service.py
```

**Przykład - NIEPRAWIDŁOWY:**
```bash
# User: "Dodaj cache service"
Agent: "Czy mam utworzyć katalog cache/?"           # ❌ NIE pytaj!
Agent: "Czy mam użyć template?"                     # ❌ NIE pytaj!
Agent: "W którym katalogu umieścić testy?"          # ❌ Przeczytaj PROJECT_STRUCTURE.md
```

#### 1.2 Edycja

| Operacja | Autonomiczna? | Kiedy | Narzędzie |
|----------|---------------|-------|-----------|
| Edycja istniejącego kodu | ✅ TAK | Zawsze gdy czytałeś plik wcześniej | Edit tool |
| Dodanie funkcji | ✅ TAK | Gdy miejsce jest jasne (service/repo/route) | Edit tool |
| Refactoring | ✅ TAK | Gdy zachowujesz behavior (tests as contract) | Edit tool |
| Formatowanie | ✅ TAK | `make format` przed każdym commitem | black, isort |

**Nigdy nie używaj:**
- ❌ `nano file.py` - interaktywny editor
- ❌ `vim file.py` - interaktywny editor
- ❌ `vi file.py` - interaktywny editor
- ❌ `emacs file.py` - interaktywny editor

**Używaj zamiast tego:**
- ✅ Edit tool (dla zmian)
- ✅ Write tool (dla nowych plików po przeczytaniu istniejącego)
- ✅ `cat file.py` (do odczytu)

#### 1.3 Usuwanie

| Operacja | Autonomiczna? | Warunek | Kiedy PYTAĆ |
|----------|---------------|---------|-------------|
| Usuwanie pliku tymczasowego | ✅ TAK | `*.pyc`, `__pycache__`, `.pytest_cache` | Nigdy |
| Usuwanie starego testu | ✅ TAK | Zastępujesz nowym testem | Nigdy (jeśli część planu) |
| Usuwanie kodu produkcyjnego | ⚠️ OSTROŻNIE | Tylko jeśli martwy kod (nie używany) | Jeśli niepewność |
| Usuwanie całego modułu | ❌ NIE | - | ZAWSZE pytaj |

---

### 2. Operacje Git

#### 2.1 Podstawowe Operacje (100% Autonomiczne)

| Operacja | Autonomiczna? | Branch | Przykład |
|----------|---------------|--------|----------|
| `git status` | ✅ TAK | Wszystkie | Sprawdź stan przed pracą |
| `git checkout -b feature/X` | ✅ TAK | Z develop | Utwórz feature branch |
| `git checkout develop` | ✅ TAK | - | Przełącz na develop |
| `git pull origin develop` | ✅ TAK | develop | Aktualizuj przed mergem |
| `git add .` | ✅ TAK | feature/develop | Dodaj wszystkie zmiany |
| `git add <file>` | ✅ TAK | Wszystkie | Dodaj konkretny plik |
| `git commit -m "..."` | ✅ TAK | Wszystkie | Z conventional message |
| `git push origin feature/X` | ✅ TAK | feature/* | Push feature branch |
| `git push origin develop` | ✅ TAK | develop | Po lokalnym merge i testach |

**Przykład - Prawidłowy Flow:**
```bash
# User: "Zaimplementuj feature X"
# Agent: [AUTONOMICZNIE bez pytania]

git checkout develop
git pull origin develop
git checkout -b feature/implement-x

# [... implementacja ...]

make format && make lint
pytest --no-cov tests/test_feature_x.py

git add .
git commit -m "feat: implement feature X

- Add service layer implementation
- Add repository with tenant_id isolation
- Add comprehensive tests (15/15 passing)
- Add API endpoint documentation"

git push origin feature/implement-x

# Merge do develop (lokalnie)
git checkout develop
git merge feature/implement-x --no-ff

# Pełne testy na develop (MANDATORY!)
make test-unit
make lint

# Jeśli przeszły
git push origin develop
```

#### 2.2 Merge Operations

| Operacja | Autonomiczna? | Warunek | Kiedy PYTAĆ |
|----------|---------------|---------|-------------|
| `git merge feature/X` (do develop) | ✅ TAK | Po lokalnych testach | Nigdy (standardowy flow) |
| `git merge develop` (do release) | ✅ TAK | develop CI green | Nigdy (standardowy flow) |
| `git merge release` (do main) | ❌ NIE | - | ZAWSZE przez PR + 2 approvals |
| `git merge --no-ff` | ✅ TAK | Preferred dla merge | ZAWSZE używaj --no-ff |

#### 2.3 ZAKAZANE Operacje Git

| Operacja | Status | Nigdy nie rób tego | Dlaczego |
|----------|--------|-------------------|----------|
| `git push --force` | 🚫 ZABRONIONE | Na żadnym branchu | Niszczy historię |
| `git push -f` | 🚫 ZABRONIONE | Alias dla --force | Niszczy historię |
| `git rebase -i` | 🚫 ZABRONIONE | Interaktywne | Blokuje CI/CD |
| `git add -i` | 🚫 ZABRONIONE | Interaktywne | Blokuje CI/CD |
| `git commit` (bez -m) | 🚫 ZABRONIONE | Otwiera edytor | Blokuje CI/CD |
| `git reset --hard origin/main` | ⚠️ BARDZO OSTROŻNIE | Tylko jeśli pewien | Traci zmiany |

---

### 3. Testowanie

#### 3.1 Testowanie wg Brancha

| Branch | Komenda | Autonomiczna? | Kiedy | Czas |
|--------|---------|---------------|-------|------|
| feature/* | `pytest --no-cov <file>` | ✅ TAK | Test TYLKO nowego kodu | ~1-2 min |
| feature/* | `make test-focus FILE=<file>` | ✅ TAK | Test TYLKO nowego kodu | ~1-2 min |
| develop | `make test-unit` | ✅ TAK | Po merge z feature (MANDATORY!) | ~5-10 min |
| develop | `make lint` | ✅ TAK | Zawsze przed push | ~30 sek |
| release | Full tests + integration | ✅ TAK | Przez CI automatically | ~10-15 min |
| main | CI automatically | ✅ TAK | Przez GitHub Actions | ~10-15 min |

**Przykład - Prawidłowe Testowanie:**
```bash
# Na feature branch
git checkout -b feature/add-cache

# [implementacja...]

# Test TYLKO nowego kodu (NIE pełna suite!)
pytest --no-cov apps/memory_api/tests/services/test_cache_service.py -v
# 12 tests PASSED

# Format i lint
make format
make lint

git commit -m "feat: add cache service"
git push origin feature/add-cache

# Merge do develop
git checkout develop
git merge feature/add-cache --no-ff

# TERAZ pełne testy (MANDATORY!)
make test-unit
# 461 tests PASSED

# Jeśli OK
git push origin develop
```

#### 3.2 Formatowanie i Linting (Zawsze Autonomiczne)

| Komenda | Kiedy | Autonomiczna? | Przed czym |
|---------|-------|---------------|------------|
| `make format` | Przed każdym commitem | ✅ TAK | git commit |
| `make lint` | Przed każdym commitem | ✅ TAK | git commit |
| `black .` | Część make format | ✅ TAK | Auto |
| `isort .` | Część make format | ✅ TAK | Auto |
| `ruff check .` | Część make lint | ✅ TAK | Auto |

**NIGDY nie pytaj:**
- ❌ "Czy mam uruchomić make format?"
- ❌ "Czy mam naprawić linting errors?"
- ❌ "Czy mam uruchomić testy?"

**ZAWSZE rób:**
- ✅ `make format && make lint` przed KAŻDYM commitem
- ✅ Napraw wszystkie linting errors NATYCHMIAST
- ✅ Testuj zgodnie z branchem (feature = only new, develop = all)

---

### 4. Decyzje Techniczne (Autonomiczne)

#### 4.1 Wybór Wzorców

| Decyzja | Autonomiczna? | Jak podjąć | Źródło |
|---------|---------------|------------|--------|
| Repository vs Service? | ✅ TAK | Zawsze używaj obu (3-layer arch) | CONVENTIONS.md |
| Który template użyć? | ✅ TAK | Repository/Service/Route wg typu | `.ai-templates/README.md` |
| Gdzie umieścić plik? | ✅ TAK | Mirrors structure | PROJECT_STRUCTURE.md |
| Dependency Injection? | ✅ TAK | ZAWSZE używaj DI | CONVENTIONS.md |
| Pydantic models? | ✅ TAK | Input/Output models ZAWSZE | CONVENTIONS.md |

**Przykład - Prawidłowa Autonomia:**
```python
# User: "Dodaj user preferences"

# Agent: [BEZ PYTANIA - czyta dokumentację i decyduje]
# 1. Przeczytał CONVENTIONS.md → 3-layer architecture
# 2. Przeczytał PROJECT_STRUCTURE.md → gdzie umieścić
# 3. Użył .ai-templates/ → wzorzec DI

# Rezultat:
# - apps/memory_api/repositories/preference_repository.py (z tenant_id!)
# - apps/memory_api/services/preference_service.py (z DI!)
# - apps/memory_api/api/v1/preferences.py (z Depends!)
# - apps/memory_api/models/preference.py (Pydantic!)
# - tests/ (kompletne testy!)

# Wszystko zgodne ze standardami, BEZ PYTANIA!
```

#### 4.2 Nazewnictwo

| Element | Konwencja | Autonomiczna? | Przykład |
|---------|-----------|---------------|----------|
| Klasa Repository | `{Entity}Repository` | ✅ TAK | `UserRepository` |
| Klasa Service | `{Domain}Service` | ✅ TAK | `CacheService` |
| Plik Python | `snake_case.py` | ✅ TAK | `cache_service.py` |
| Test | `test_{module}.py` | ✅ TAK | `test_cache_service.py` |
| Funkcja testowa | `test_{scenario}` | ✅ TAK | `test_get_cache_returns_none_when_empty` |
| Branch | `feature/{description}` | ✅ TAK | `feature/add-cache-service` |
| Commit message | Conventional Commits | ✅ TAK | `feat(services): add cache service` |

**NIGDY nie pytaj:**
- ❌ "Jak nazwać plik?"
- ❌ "Jak nazwać klasę?"
- ❌ "Jaki branch name?"

**ZAWSZE używaj:**
- ✅ Konwencji z CONVENTIONS.md
- ✅ Wzorców z PROJECT_STRUCTURE.md
- ✅ Conventional Commits dla message

---

### 5. Struktura Testów (100% Autonomiczna)

| Aspekt | Decyzja | Autonomiczna? | Zasada |
|--------|---------|---------------|--------|
| Gdzie umieścić test? | mirrors source | ✅ TAK | `services/X.py` → `tests/services/test_X.py` |
| Jaki wzorzec użyć? | AAA (Arrange-Act-Assert) | ✅ TAK | Z `.ai-templates/test_template.py` |
| Mockować czy nie? | Unit tests = mock, Integration = real | ✅ TAK | Service tests = mock repo, Repo tests = real DB |
| Coverage threshold? | 80%+ dla nowego kodu | ✅ TAK | Automatyczne sprawdzenie w CI |
| Pytest markers? | Wg typu (unit/integration/llm) | ✅ TAK | `@pytest.mark.unit` dla unit tests |

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
| Zmiany w infrastrukturze | ✅ TAK | docker compose.yml, CI/CD | - |
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
