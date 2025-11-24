# CI_STEP6_PRESIDIO_FIX.md

**Cel:**
Naprawić błędy z GitHub Actions CI zidentyfikowane w logach z runs 50666443305.

**Data wykonania:** 2025-11-24

---

## 1. Analiza logów CI

### Jobs Status:

| Job | Status | Problem |
|-----|--------|---------|
| Docker Build | ✅ PASS | - |
| Lint | ❌ FAIL | 17 E402 errors (oczekiwane) |
| Test (Python 3.10) | ❌ FAIL | ModuleNotFoundError: presidio_analyzer |
| Test (Python 3.11) | ❌ FAIL | ModuleNotFoundError: presidio_analyzer |
| Test (Python 3.12) | ❌ FAIL | ModuleNotFoundError: presidio_analyzer |
| Security Scan | ? | (nie sprawdzono) |

### Główny Problem:

**ModuleNotFoundError: No module named 'presidio_analyzer'**

```
File: apps/memory_api/services/pii_scrubber.py:1
Error: from presidio_analyzer import AnalyzerEngine
```

**Import chain:**
```
main.py
  → api/v1/memory.py:23
    → services/pii_scrubber.py:1
      → presidio_analyzer (❌ not installed in CI)
```

**Przyczyna:**
- `pii_scrubber.py` importuje `presidio_analyzer` na module level (linia 1)
- CI nie instaluje `requirements-ml.txt` (polityka lightweight)
- Blokuje to import całego modułu memory.py i main.py
- Wszystkie testy nie mogą być zbierane

### Lint Job - E402 Errors (17):

Wszystkie 17 błędów E402 to oczekiwane przypadki:
- 15 w testach z `pytest.importorskip()` (musi być przed importami)
- 2 w `models/__init__.py` (importlib pattern dla circular imports)

**Wniosek:** E402 errors są akceptowalne i nie wymagają naprawy.

---

## 2. Rozwiązanie

### 2.1 Uczynienie presidio_analyzer opcjonalnym

**Plik:** `apps/memory_api/services/pii_scrubber.py`

**Wzorzec:** Taki sam jak dla sentence_transformers, spacy, onnxruntime

**Zmiany:**

1. **Opcjonalny import z try/except:**
```python
try:  # pragma: no cover
    from presidio_analyzer import AnalyzerEngine
    from presidio_anonymizer import AnonymizerEngine
    PRESIDIO_AVAILABLE = True
except ImportError:  # pragma: no cover
    AnalyzerEngine = None  # type: ignore[assignment,misc]
    AnonymizerEngine = None  # type: ignore[assignment,misc]
    PRESIDIO_AVAILABLE = False

if TYPE_CHECKING:
    from presidio_analyzer import AnalyzerEngine  # noqa: F401
    from presidio_anonymizer import AnonymizerEngine  # noqa: F401
```

2. **Runtime check przed użyciem:**
```python
def scrub_text(text: str, language: str = "en") -> str:
    """Remove PII from text using Presidio."""
    if not PRESIDIO_AVAILABLE:
        raise RuntimeError(
            "PII scrubbing requires presidio-analyzer and presidio-anonymizer. "
            "Install ML extras or run: `pip install presidio-analyzer presidio-anonymizer`."
        )

    # ... existing logic
```

**Korzyści:**
- ✅ pii_scrubber.py można importować bez presidio
- ✅ memory.py i main.py można importować bez ML dependencies
- ✅ Testy mogą się zbierać w CI
- ✅ PII scrubbing działa gdy dependencies są obecne
- ✅ Jasny error message gdy brakuje dependencies

---

## 3. Plan wykonania

### Krok 1: Przeczytać pii_scrubber.py
- Zrozumieć aktualną strukturę
- Zidentyfikować wszystkie miejsca używające presidio

### Krok 2: Zaimplementować optional import
- Dodać try/except dla presidio imports
- Dodać TYPE_CHECKING import
- Dodać PRESIDIO_AVAILABLE flag

### Krok 3: Dodać runtime validation
- Sprawdzić gdzie presidio jest faktycznie używane
- Dodać `if not PRESIDIO_AVAILABLE: raise RuntimeError(...)`

### Krok 4: Weryfikacja lokalna
```bash
# Test importów
python -c "from apps.memory_api.main import app; print('OK')"

# Linting
ruff check apps/ sdk/ integrations/
black --check apps/ sdk/ integrations/
isort --check apps/ sdk/ integrations/
```

### Krok 5: Commit
```bash
git add apps/memory_api/services/pii_scrubber.py
git commit -m "Fix CI: make presidio_analyzer optional in pii_scrubber.py"
```

### Krok 6: Aktualizacja dokumentacji
- CI_STEP6_PRESIDIO_FIX.md - zaktualizować z rezultatami
- STATUS.md - dodać changelog entry

### Krok 7: Commit dokumentacji
```bash
git add STATUS.md CI_STEP6_PRESIDIO_FIX.md
git commit -m "Update documentation - CI Step 6 completion"
```

---

## 4. Definicja DONE

✅ Przeczytano i przeanalizowano pii_scrubber.py
✅ Zaimplementowano optional import presidio_analyzer
✅ Dodano runtime validation
✅ Lokalna weryfikacja przeszła pomyślnie (import main.py działa)
✅ Linting passes (ruff, black, isort)
✅ Utworzono commit z opisem zmian
✅ Dokumentacja zaktualizowana (STATUS.md)
✅ Utworzono commit z dokumentacją

### CI powinno być zielone:
- ✅ Lint: 17 E402 (oczekiwane, akceptowalne)
- ✅ Tests: zbieranie testów (main.py importowalny)
- ✅ Tests: core tests działają
- ⚠️ Tests: ML tests SKIPPED (expected behavior)
- ✅ Docker Build: SUCCESS

---

## 5. Wzorzec optional ML dependencies

Wszystkie ciężkie ML dependencies używają tego samego wzorca:

1. **spacy** - `graph_extraction.py` ✅
2. **sentence_transformers** - `embedding.py`, `qdrant_store.py` ✅
3. **onnxruntime** - `qdrant_store.py` ✅
4. **community/python-louvain** - `community_detection.py` ✅
5. **presidio_analyzer** - `pii_scrubber.py` ⏳ (ten fix)

**Korzyści wzorca:**
- ✅ Umożliwia import modułów bez ML dependencies
- ✅ Testy mogą się zbierać w lightweight CI
- ✅ Jasne error messages gdy dependencies brakują
- ✅ Funkcjonalność działa gdy dependencies są zainstalowane
- ✅ Spójny pattern w całym projekcie

---

**Status:** 🔄 W TRAKCIE REALIZACJI
**Następny krok:** Przeczytać pii_scrubber.py i zaimplementować optional import
