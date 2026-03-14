# 🧪 TESTING OPTIMIZATION - Smart Test Classification

> **Cel**: Oszczędzaj czas nie marnując go na zbędne testy
>
> **Zasada**: Test proporcjonalnie do ryzyka i rozmiaru zmiany

---

## 🎯 Filozofia

```
┌──────────────────────────────────────────────────────────────┐
│  Nie wszystkie zmiany wymagają pełnego test suite!          │
│                                                              │
│  Dokumentacja: 0 testów, tylko lint (~10 sekund)            │
│  Mała zmiana: Quick tests (~1-2 minuty)                     │
│  Średnia zmiana: Full tests 1 Python (~3-5 minut)           │
│  Duża zmiana: Full tests + integration (~10-15 minut)       │
└──────────────────────────────────────────────────────────────┘
```

**Oszczędność**: ~50-70% czasu dla drobnych zmian!

---

## 📊 SYSTEM KLASYFIKACJI ZMIAN

### TRIVIAL - Pomijalne

**Definicja**: Zmiany które nie wpływają na kod wykonywany.

**Kryteria**:
- ✅ Tylko pliki `*.md`, `*.rst`, `*.txt`
- ✅ Tylko komentarze w kodzie
- ✅ Whitespace/formatowanie (black, isort auto-fix)
- ✅ `.gitignore`, `.editorconfig`, `.env.example`
- ✅ Typos w stringach (bez logiki)

**Przykłady**:
```
✅ TRIVIAL:
- Update README.md
- Fix typo in docstring
- Add comment explaining algorithm
- Reformat with black (no logic change)
- Update .gitignore

❌ NIE TRIVIAL:
- Update docstring + change function signature
- Fix typo in variable name (zmienia kod!)
```

**Testowanie**:
```bash
# SKIP testy całkowicie
make lint  # Tylko lint check (~10 sekund)
```

**CI Behavior**:
- Quick skip jeśli tylko `*.md` changed
- Git commit message może zawierać `[skip tests]`

---

### SMALL - Drobna Zmiana

**Definicja**: Lokalna zmiana w małym zakresie.

**Kryteria**:
- ✅ Zmiany w < 3 plikach Python
- ✅ Zmiany w < 50 liniach kodu
- ✅ Lokalne zmiany (1 service/1 repository/1 route)
- ✅ Bug fix w 1 funkcji
- ✅ Dodanie 1-2 testów

**Przykłady**:
```
✅ SMALL:
- Fix null pointer in specific function
- Add single helper method
- Update 1 API endpoint logic
- Add validation for 1 field
- Fix 1 test that was broken

❌ NIE SMALL:
- Fix null pointer + refactor entire service (>3 files)
- Add helper + update 5 callers (>50 lines)
```

**Testowanie**:

```bash
# Na feature branch - QUICK tests
pytest --testmon --no-cov  # Tylko affected tests
# LUB
pytest --no-cov path/to/changed_test.py

# Na develop - FULL tests (1 Python version)
make test-unit  # Wszystkie, ale tylko Python 3.11
```

**Czas**:
- Feature: ~1-2 minuty (quick tests)
- Develop: ~3-5 minut (full suite, 1 Python)

---

### MEDIUM - Średnia Zmiana

**Definicja**: Zmiana wpływająca na więcej niż 1 komponent.

**Kryteria**:
- ✅ Zmiany w 3-10 plikach Python
- ✅ Zmiany w 50-200 liniach kodu
- ✅ Nowy service/repository (1 layer)
- ✅ Refactoring istniejącego kodu
- ✅ Zmiany w API (bez breaking changes)
- ✅ Dodanie integracji z zewnętrznym serwisem

**Przykłady**:
```
✅ MEDIUM:
- Add new CacheService (service + tests + API route)
- Refactor GraphRepository (extract queries)
- Add new API endpoint family (/users CRUD)
- Update authentication flow (5 files)

❌ NIE MEDIUM:
- Add cache service + refactor all services to use it (>10 files)
- Breaking API change (wymaga LARGE)
```

**Testowanie**:

```bash
# Na feature branch - QUICK tests
pytest --testmon --no-cov

# Na develop - FULL tests (3 Python versions)
make test-unit  # Full suite
pytest -m integration  # Integration tests
make security-scan
```

**Czas**:
- Feature: ~2-3 minuty (quick tests)
- Develop: ~5-8 minut (full suite, 3 Python + integration)

---

### LARGE - Duża Zmiana

**Definicja**: Znacząca zmiana wpływająca na wiele komponentów lub architekturę.

**Kryteria**:
- ✅ Zmiany w > 10 plikach Python
- ✅ Zmiany w > 200 liniach kodu
- ✅ Nowy feature (wszystkie 3 layers: API + Service + Repository)
- ✅ Breaking API changes
- ✅ Zmiany w dependencies (`pyproject.toml`, `requirements*.txt`)
- ✅ Zmiany w konfiguracji/infrastrukturze
- ✅ Refactoring wpływający na wiele modułów

**Przykłady**:
```
✅ LARGE:
- Implement RAE-core 4-layer memory architecture (20+ files)
- Add multi-tenancy support across all services
- Breaking API v2 (change response format)
- Upgrade from Pydantic v1 to v2
- Add new ML model with dependencies (3GB)

❌ NIE LARGE (mogą być MEDIUM):
- Add single large service (10 files ale 1 layer)
```

**Testowanie**:

```bash
# Na feature branch - FULL tests (lokalnie!)
pytest -m unit --cov  # Full unit tests z coverage
make lint
make security-scan

# Na develop - COMPREHENSIVE
make test-unit  # Full suite, 3 Python versions
pytest -m integration  # Integration tests
make benchmark-smoke  # Performance check
pytest -m contract  # Contract tests jeśli API changes
make security-scan
```

**Czas**:
- Feature: ~5-10 minut (full unit tests lokalnie)
- Develop: ~10-15 minut (everything)
- Release: ~15-20 minut (full validation)

---

## 🤖 AUTOMATYCZNA KLASYFIKACJA (CI)

### Algorytm Klasyfikacji

```python
def classify_change(changed_files, total_lines_changed):
    """
    Automatycznie klasyfikuj zmianę na podstawie plików i linii.
    """
    # Filtruj tylko pliki Python
    py_files = [f for f in changed_files if f.endswith('.py')]

    # Sprawdź czy tylko dokumentacja
    if not py_files and all(f.endswith(('.md', '.rst', '.txt')) for f in changed_files):
        return 'TRIVIAL'

    # Policz pliki i linie Python
    py_count = len(py_files)

    # Klasyfikacja
    if py_count == 0:
        return 'TRIVIAL'
    elif py_count < 3 and total_lines_changed < 50:
        return 'SMALL'
    elif py_count < 10 and total_lines_changed < 200:
        return 'MEDIUM'
    else:
        return 'LARGE'
```

### Git Commit Hints (Opcjonalne)

Możesz ręcznie oznaczyć klasyfikację w commit message:

```bash
# Oznacz jako trivial (CI skipnie testy)
git commit -m "docs: update README [trivial]"

# Wymusz full tests nawet dla small change
git commit -m "fix: small bug [full-test]"

# Oznacz jako large (wymusza comprehensive testing)
git commit -m "feat: add multi-tenancy [large]"
```

---

## 📋 TESTING MATRIX

### Feature Branch Testing

| Change Type | Command | Duration | What Runs |
|-------------|---------|----------|-----------|
| TRIVIAL | `make lint` | ~10s | Lint only |
| SMALL | `pytest --testmon --no-cov` | ~1-2 min | Affected tests |
| MEDIUM | `pytest --testmon --no-cov` | ~2-3 min | Affected tests |
| LARGE | `pytest -m unit --cov` | ~5-10 min | All unit tests |

### Develop Branch Testing

| Change Type | Command | Duration | What Runs |
|-------------|---------|----------|-----------|
| TRIVIAL | `make lint` | ~30s | Lint (CI) |
| SMALL | `make test-unit` (1 Python) | ~3-5 min | Full suite, Python 3.11 |
| MEDIUM | `make test-unit` (3 Python) | ~5-8 min | Full + integration |
| LARGE | Full validation | ~10-15 min | Everything |

### Release Branch Testing

| Change Type | Command | Duration | What Runs |
|-------------|---------|----------|-----------|
| ALL | Full validation | ~10-15 min | Full + integration + benchmark |

**Uwaga**: Na release ZAWSZE full validation bez względu na change type!

---

## 🚀 SMART TEST SELECTION

### Testmon - Inteligentne Testy

```bash
# Instalacja
pip install pytest-testmon

# Użycie (automatyczne w CI)
pytest --testmon --no-cov

# Co robi:
# 1. Śledzi które testy pokrywają który kod
# 2. Uruchamia TYLKO testy affected przez zmiany
# 3. Oszczędza 70-90% czasu dla małych zmian
```

**Przykład**:
```
Zmieniony plik: apps/memory_api/services/cache_service.py

Tradycyjnie:
pytest apps/memory_api/tests/
# 461 tests, 5 minut

Z testmon:
pytest --testmon apps/memory_api/tests/
# 12 tests (tylko cache_service related), 30 sekund
```

### Affected Test Mapping

```bash
# Automatyczne mapowanie (CI script)
python scripts/map_affected_tests.py

# Przykład mapowania:
services/cache_service.py → tests/services/test_cache_service.py
services/cache_service.py → tests/api/v2/test_cache.py (jeśli używa)
repositories/cache_repository.py → tests/repositories/test_cache_repository.py
```

---

## ⚡ OPTIMIZATION TIPS

### 1. Parallel Testing

```bash
# Instalacja
pip install pytest-xdist

# Użycie (4 workers)
pytest -n 4 apps/memory_api/tests/

# Oszczędność: ~50% czasu
# 10 minut → 5 minut
```

### 2. Skip Slow Tests Locally

```bash
# Na feature branch skipuj integration tests
pytest -m "not integration and not llm"

# Oszczędność: ~30% czasu
# 10 minut → 7 minut
```

### 3. Test Fokus

```bash
# Testuj TYLKO changed module
pytest apps/memory_api/tests/services/test_cache_service.py -v

# Oszczędność: ~95% czasu
# 10 minut → 30 sekund
```

---

## 🎯 DECISION TREE

```
                   Commitujesz zmiany
                            │
                            ▼
                   ┌─────────────────┐
                   │ Jakie pliki?    │
                   └────┬──────┬─────┘
                       .md?   .py?
                        │      │
                        ▼      ▼
                    ┌──────┐ ┌───────────┐
                    │TRIVIAL│ │Ile plików?│
                    │lint  │ └─┬────┬────┘
                    │10s   │  <3  3-10  >10
                    └──────┘   │   │    │
                               ▼   ▼    ▼
                           ┌───────────────┐
                           │Ile linii?     │
                           └─┬──────┬──────┘
                            <50  50-200  >200
                             │     │      │
                             ▼     ▼      ▼
                          SMALL MEDIUM LARGE
                          Quick  Full  Comprehensive
                          1-2min 5-8min 10-15min
```

---

## 📊 PRZYKŁADY

### Przykład 1: Dokumentacja (TRIVIAL)

```bash
# Zmiana
git diff
# diff --git a/README.md b/README.md
# +## New section

# Klasyfikacja
Change type: TRIVIAL

# Testowanie
make lint
# ✅ 10 seconds

# CI
[skip tests] in commit message
# ✅ ~30 seconds (lint only)
```

### Przykład 2: Bug Fix (SMALL)

```bash
# Zmiana
git diff
# apps/memory_api/services/reflection_engine.py | 5 ++---
# 1 file changed, 2 insertions(+), 3 deletions(-)

# Klasyfikacja
Change type: SMALL (1 file, 5 lines)

# Testowanie (feature branch)
pytest --testmon --no-cov tests/services/test_reflection_engine.py
# ✅ 18 tests, 45 seconds

# Testowanie (develop)
make test-unit
# ✅ 461 tests, 4 minutes (1 Python version)
```

### Przykład 3: Nowy Service (MEDIUM)

```bash
# Zmiana
git diff --stat
# apps/memory_api/services/cache/cache_service.py | 150 +++++
# apps/memory_api/tests/services/cache/test_cache_service.py | 120 +++++
# apps/memory_api/api/v2/cache.py | 80 +++++
# apps/memory_api/repositories/cache_repository.py | 100 +++++
# 4 files changed, 450 insertions(+)

# Klasyfikacja
Change type: MEDIUM (4 files, 450 lines)

# Testowanie (feature branch)
pytest --testmon --no-cov tests/services/cache/ tests/api/v2/test_cache.py
# ✅ 30 tests, 2 minutes

# Testowanie (develop)
make test-unit  # 3 Python versions
pytest -m integration
make security-scan
# ✅ 6 minutes total
```

### Przykład 4: Breaking API Change (LARGE)

```bash
# Zmiana
git diff --stat
# 25 files changed, 1200 insertions(+), 800 deletions(-)

# Klasyfikacja
Change type: LARGE (25 files, 2000 lines)

# Testowanie (feature branch)
pytest -m unit --cov
# ✅ Full unit tests, 8 minutes

# Testowanie (develop)
make test-unit  # 3 Python versions
pytest -m integration
pytest -m contract  # API contract tests
make benchmark-smoke
make security-scan
# ✅ 15 minutes total

# Testowanie (release)
[Full validation przez CI]
# ✅ 20 minutes (wszystko + manual QA)
```

---

## ✅ CHECKLIST - Wybór Strategii Testowania

Przed testem, odpowiedz:

- [ ] Ile plików Python zmieniłem? (<3, 3-10, >10)
- [ ] Ile linii kodu zmieniłem? (<50, 50-200, >200)
- [ ] Czy to tylko dokumentacja? (TRIVIAL)
- [ ] Czy to breaking change? (LARGE)
- [ ] Czy dodałem nowe dependency? (LARGE)
- [ ] Na jakim branchu jestem? (feature/develop/release)

**Decision**:
- **TRIVIAL**: `make lint` (~10s)
- **SMALL**: `pytest --testmon --no-cov` (~1-2 min)
- **MEDIUM**: Full tests 1-3 Python (~3-8 min)
- **LARGE**: Everything (~10-20 min)

---

## 🎓 TRAINING EXAMPLES

### Quiz: Jakie Testy Uruchomić?

**Scenario 1**: Poprawiłem typo w docstringu (1 file, 1 line)
- **Odpowiedź**: TRIVIAL - `make lint` (10s)

**Scenario 2**: Dodałem null check w funkcji (1 file, 3 lines)
- **Odpowiedź**: SMALL - `pytest --testmon --no-cov` (1-2 min)

**Scenario 3**: Dodałem nowy CacheService (4 files, 450 lines)
- **Odpowiedź**: MEDIUM - Full tests (5-8 min)

**Scenario 4**: Upgrade Pydantic v1 → v2 (30 files, 2000 lines)
- **Odpowiedź**: LARGE - Everything (10-20 min)

---

**Wersja**: 1.0.0
**Data**: 2025-12-10
**Status**: 🟢 RECOMMENDED - Zalecane dla wszystkich
**Oszczędność**: ~50-70% czasu testowania
