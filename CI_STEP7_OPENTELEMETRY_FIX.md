# CI_STEP7_OPENTELEMETRY_FIX.md

**Cel:**
Naprawić błędy z GitHub Actions CI zidentyfikowane w logach z runs 50668315125.

**Data wykonania:** 2025-11-24

---

## 1. Analiza logów CI

### Jobs Status:

| Job | Status | Problem |
|-----|--------|---------|
| Docker Build | ✅ PASS | - |
| Lint | ❌ FAIL | 17 E402 errors (oczekiwane) |
| Test (Python 3.10) | ❌ FAIL | ModuleNotFoundError: opentelemetry.exporter |
| Test (Python 3.11) | ❌ FAIL | ModuleNotFoundError: opentelemetry.exporter |
| Test (Python 3.12) | ❌ FAIL | ModuleNotFoundError: opentelemetry.exporter |
| Security Scan | ? | (nie sprawdzono) |

### Główny Problem:

**ModuleNotFoundError: No module named 'opentelemetry.exporter'**

```
File: apps/memory_api/observability/opentelemetry_config.py:29
Error: from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
```

**Import chain:**
```
test_openapi.py:3
  → main.py:18
    → observability/__init__.py:3
      → opentelemetry_config.py:29
        → opentelemetry.exporter (❌ not installed in CI)
```

**Przyczyna:**
- `opentelemetry_config.py` importuje wiele modułów opentelemetry na module level (linie 28-37)
- CI nie instaluje opentelemetry packages (nie są w requirements-base.txt ani requirements-test.txt)
- Blokuje to import całego modułu main.py
- Wszystkie testy nie mogą być zbierane

**Importy opentelemetry w opentelemetry_config.py:**
- `from opentelemetry import trace`
- `from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter`
- `from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor`
- `from opentelemetry.instrumentation.logging import LoggingInstrumentor`
- `from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor`
- `from opentelemetry.instrumentation.redis import RedisInstrumentor`
- `from opentelemetry.instrumentation.requests import RequestsInstrumentor`
- `from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_VERSION, Resource`
- `from opentelemetry.sdk.trace import TracerProvider`
- `from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter`

### Lint Job - E402 Errors (17):

Wszystkie 17 błędów E402 to oczekiwane przypadki (bez zmian od poprzedniego runa):
- 15 w testach z `pytest.importorskip()`
- 2 w `models/__init__.py` (importlib pattern)

**Wniosek:** E402 errors są akceptowalne i nie wymagają naprawy.

---

## 2. Rozwiązanie

### 2.1 Uczynienie opentelemetry opcjonalnym

**Plik:** `apps/memory_api/observability/opentelemetry_config.py`

**Wzorzec:** Taki sam jak dla presidio, spacy, sentence_transformers

**Strategia:**

Moduł opentelemetry jest używany do distributed tracing - funkcjonalność opcjonalna, nie krytyczna dla działania API.

**Zmiany:**

1. **Opcjonalny import z try/except:**
```python
try:  # pragma: no cover
    from opentelemetry import trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.logging import LoggingInstrumentor
    from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
    from opentelemetry.instrumentation.redis import RedisInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_VERSION, Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    OPENTELEMETRY_AVAILABLE = True
except ImportError:  # pragma: no cover
    # All imports set to None
    OPENTELEMETRY_AVAILABLE = False

if TYPE_CHECKING:
    from opentelemetry import trace  # noqa: F401
    # ... other imports for type checking
```

2. **Early return w setup_opentelemetry():**
```python
def setup_opentelemetry():
    """Setup OpenTelemetry tracing."""
    if not OPENTELEMETRY_AVAILABLE:
        logger.info(
            "opentelemetry_disabled",
            reason="OpenTelemetry packages not installed. "
            "Install with: pip install opentelemetry-api opentelemetry-sdk "
            "opentelemetry-exporter-otlp-proto-grpc opentelemetry-instrumentation-*"
        )
        return

    if not OTEL_ENABLED:
        logger.info("opentelemetry_disabled", reason="OTEL_TRACES_ENABLED=false")
        return

    # ... existing setup logic
```

**Korzyści:**
- ✅ opentelemetry_config.py można importować bez opentelemetry
- ✅ main.py można importować bez opentelemetry
- ✅ Testy mogą się zbierać w CI
- ✅ Tracing działa gdy dependencies są obecne
- ✅ Graceful degradation - API działa bez tracingu
- ✅ Jasny log message gdy tracing jest wyłączony

---

## 3. Plan wykonania

### Krok 1: Przeczytać opentelemetry_config.py
- Zrozumieć wszystkie importy opentelemetry
- Zidentyfikować wszystkie miejsca używające opentelemetry

### Krok 2: Zaimplementować optional import
- Dodać try/except dla wszystkich opentelemetry imports
- Dodać TYPE_CHECKING import
- Dodać OPENTELEMETRY_AVAILABLE flag

### Krok 3: Dodać early return w setup_opentelemetry()
- Sprawdzić OPENTELEMETRY_AVAILABLE
- Logować informację o wyłączonym tracingu
- Return zamiast RuntimeError (graceful degradation)

### Krok 4: Sprawdzić observability/__init__.py
- Upewnić się że nie ma innych direct imports

### Krok 5: Weryfikacja lokalna
```bash
# Test importów
python -c "from apps.memory_api.observability.opentelemetry_config import setup_opentelemetry, OPENTELEMETRY_AVAILABLE; print(f'OK: {OPENTELEMETRY_AVAILABLE}')"

# Linting
ruff check apps/memory_api/observability/
black --check apps/memory_api/observability/
isort --check apps/memory_api/observability/
```

### Krok 6: Commit
```bash
git add apps/memory_api/observability/opentelemetry_config.py
git commit -m "Fix CI: make opentelemetry optional in observability module"
```

### Krok 7: Aktualizacja dokumentacji
- CI_STEP7_OPENTELEMETRY_FIX.md - zaktualizować z rezultatami
- STATUS.md - dodać changelog entry

### Krok 8: Commit dokumentacji
```bash
git add STATUS.md CI_STEP7_OPENTELEMETRY_FIX.md
git commit -m "Update documentation - CI Step 7 completion"
```

---

## 4. Definicja DONE

✅ Przeczytano i przeanalizowano opentelemetry_config.py
✅ Zaimplementowano optional import dla wszystkich opentelemetry modules
✅ Dodano early return w setup_opentelemetry()
✅ Sprawdzono observability/__init__.py
✅ Lokalna weryfikacja przeszła pomyślnie (import działa)
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
- ⚠️ Tracing: Disabled in CI (graceful degradation)

---

## 5. Charakterystyka opentelemetry

**Typ dependency:** Observability / Monitoring (opcjonalna)

**Dlaczego opcjonalna:**
- Tracing nie jest wymagany do działania API
- Przydatny w production dla debugowania i monitoringu
- W testach i lightweight CI nie jest potrzebny
- Graceful degradation - API działa bez tracingu

**Packages wymagane:**
- `opentelemetry-api`
- `opentelemetry-sdk`
- `opentelemetry-exporter-otlp-proto-grpc`
- `opentelemetry-instrumentation-fastapi`
- `opentelemetry-instrumentation-logging`
- `opentelemetry-instrumentation-psycopg2`
- `opentelemetry-instrumentation-redis`
- `opentelemetry-instrumentation-requests`

**Instalacja (opcjonalna):**
```bash
pip install opentelemetry-api opentelemetry-sdk \
    opentelemetry-exporter-otlp-proto-grpc \
    opentelemetry-instrumentation-fastapi \
    opentelemetry-instrumentation-logging \
    opentelemetry-instrumentation-psycopg2 \
    opentelemetry-instrumentation-redis \
    opentelemetry-instrumentation-requests
```

---

## 6. Wzorzec optional dependencies - ROZSZERZONY

Po tym fixie będziemy mieli kompletny wzorzec dla:

### ML Dependencies (heavy, optional):
1. **spacy** - `graph_extraction.py` ✅
2. **sentence_transformers** - `embedding.py`, `qdrant_store.py` ✅
3. **onnxruntime** - `qdrant_store.py` ✅
4. **python-louvain** - `community_detection.py` ✅
5. **presidio_analyzer** - `pii_scrubber.py` ✅

### Observability Dependencies (optional):
6. **opentelemetry** - `opentelemetry_config.py` ⏳ (ten fix)

**Wspólny wzorzec:**
- Try/except dla importów
- Availability flag
- Graceful degradation (log message zamiast RuntimeError dla observability)
- Clear error messages dla ML (RuntimeError gdy brakuje i jest używane)

---

**Status:** 🔄 W TRAKCIE REALIZACJI
**Następny krok:** Przeczytać opentelemetry_config.py i zaimplementować optional import
