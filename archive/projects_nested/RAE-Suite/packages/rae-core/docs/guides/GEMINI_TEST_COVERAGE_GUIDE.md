# Gemini: Iteracyjne Zwiększanie Pokrycia Testami

## 🎯 Cel: Osiągnąć 75%+ pokrycia testami w sposób iteracyjny

**Obecne pokrycie:** 48% → **Docelowe:** 75%+

---

## 📋 Instrukcje dla Gemini

### Workflow:

1. **Analiza**: Znajdź pliki z niskim pokryciem
2. **Priorytetyzacja**: Wybierz najważniejsze moduły
3. **Implementacja**: Dodaj testy dla pojedynczego modułu
4. **Walidacja**: Uruchom testy i sprawdź pokrycie
5. **Commit**: Zatwierdź zmiany
6. **Powtórz**: Przejdź do kolejnego modułu

---

## 🔍 Krok 1: Analiza Pokrycia

### Znajdź pliki z niskim pokryciem:

```bash
# Generuj raport pokrycia
pytest --cov=apps --cov-report=term-missing --cov-report=html

# Otwórz htmlcov/index.html w przeglądarce
# LUB sprawdź raport tekstowy
pytest --cov=apps --cov-report=term-missing | grep -v "100%"
```

### Priorytetyzacja modułów:

**NAJWYŻSZY PRIORYTET (krytyczne dla biznesu):**
1. `apps/memory_api/core/` - Logika biznesowa
2. `apps/memory_api/services/` - Główne serwisy
3. `apps/memory_api/api/` - API endpoints

**ŚREDNI PRIORYTET:**
4. `apps/memory_api/repositories/` - Dostęp do danych
5. `apps/memory_api/workers/` - Background tasks

**NISKI PRIORYTET:**
6. `apps/memory_api/middleware/` - Middleware
7. `apps/memory_api/utils/` - Utilities

---

## 📝 Krok 2: Szablon Zadania dla Gemini

### Zadanie pojedyncze iteracji:

```
Zwiększ pokrycie testami dla modułu: <MODULE_NAME>

Krok po kroku:
1. Przeanalizuj plik: apps/memory_api/<path>/<file>.py
2. Sprawdź istniejące testy: apps/memory_api/tests/<path>/test_<file>.py
3. Zidentyfikuj nieprzetestowane linie (patrz coverage report)
4. Dodaj testy dla:
   - Edge cases (puste listy, None, błędne dane)
   - Error handling (wyjątki, błędy walidacji)
   - Happy paths (główne ścieżki wykonania)
   - Boundary conditions (max/min wartości)

Wymagania:
- Każdy test musi mieć docstring wyjaśniający co testuje
- Używaj pytest fixtures dla setup/teardown
- Mockuj zewnętrzne zależności (DB, API, etc.)
- Testy muszą być fast (<100ms każdy)
- Nazwij testy opisowo: test_<function>_<scenario>_<expected>

Przykład:
```python
def test_calculate_score_with_empty_list_returns_zero():
    """Test that calculate_score returns 0 for empty input"""
    result = calculate_score([])
    assert result == 0.0
```

Po zakończeniu:
- Uruchom: pytest apps/memory_api/tests/<path>/test_<file>.py -v
- Sprawdź pokrycie: pytest --cov=apps/memory_api/<path>/<file>.py
- Zakomituj: git commit -m "test: increase coverage for <module> to XX%"
```

---

## 🚀 Krok 3: Uruchamianie Testów

### Lokalne testowanie:

```bash
# Test pojedynczego pliku
pytest apps/memory_api/tests/core/test_state.py -v

# Test z pokryciem
pytest apps/memory_api/tests/core/test_state.py --cov=apps/memory_api/core/state.py --cov-report=term-missing

# Test całego modułu
pytest apps/memory_api/tests/core/ --cov=apps/memory_api/core/ --cov-report=html

# Szybkie testy (tylko zmienione)
pytest --testmon -x
```

### Interpretacja wyników:

```
apps/memory_api/core/state.py    85%  Missing: 45-47, 89-92
```

Oznacza: Linie 45-47 i 89-92 nie są przetestowane. Dodaj testy pokrywające te linie.

---

## 📊 Krok 4: Monitoring Postępu

### Sprawdzanie globalnego pokrycia:

```bash
# Całe pokrycie projektu
pytest --cov=apps --cov-report=term

# Zapisz raport
pytest --cov=apps --cov-report=html
open htmlcov/index.html
```

### Target per moduł:

- **core/**: 85%+ (krytyczna logika)
- **services/**: 80%+ (serwisy biznesowe)
- **api/**: 75%+ (endpoints)
- **repositories/**: 70%+ (data access)
- **utils/**: 65%+ (utilities)

---

## 🎯 Krok 5: Lista Modułów do Pokrycia

### Iteracja 1-5: Core Modules (Najwyższy priorytet)

```bash
# Iteracja 1
apps/memory_api/core/state.py
apps/memory_api/tests/core/test_state.py

# Iteracja 2
apps/memory_api/core/actions.py
apps/memory_api/tests/core/test_actions.py

# Iteracja 3
apps/memory_api/core/reward.py
apps/memory_api/tests/core/test_reward.py

# Iteracja 4
apps/memory_api/core/information_bottleneck.py
apps/memory_api/tests/core/test_information_bottleneck.py

# Iteracja 5
apps/memory_api/core/graph_operator.py
apps/memory_api/tests/core/test_graph_operator.py
```

### Iteracja 6-10: Services (Wysoki priorytet)

```bash
# Iteracja 6
apps/memory_api/services/memory_scoring_v2.py
apps/memory_api/tests/services/test_memory_scoring_v2.py

# Iteracja 7
apps/memory_api/services/hybrid_search_service.py
apps/memory_api/tests/services/test_hybrid_search_service.py

# Iteracja 8
apps/memory_api/services/reflection_engine_v2.py
apps/memory_api/tests/services/test_reflection_engine_v2.py

# Iteracja 9
apps/memory_api/services/entity_resolution.py
apps/memory_api/tests/services/test_entity_resolution.py

# Iteracja 10
apps/memory_api/services/graph_algorithms.py
apps/memory_api/tests/services/test_graph_algorithms.py
```

### Iteracja 11-15: API Endpoints

```bash
# Iteracja 11
apps/memory_api/api/v2/memory.py
tests/api/v2/test_memory.py

# Iteracja 12
apps/memory_api/api/v2/agent.py
tests/api/v2/test_agent.py

# Iteracja 13
apps/memory_api/api/v2/graph.py
tests/api/v2/test_graph.py

# Iteracja 14
apps/memory_api/api/v2/search_hybrid.py
tests/api/v2/test_search_hybrid.py

# Iteracja 15
apps/memory_api/api/v2/triggers.py
tests/api/v2/test_triggers.py
```

---

## 🧪 Krok 6: Best Practices dla Testów

### 1. Testuj Edge Cases:

```python
def test_function_with_empty_input():
    """Test with empty input"""
    result = my_function([])
    assert result == []

def test_function_with_none_input():
    """Test with None input"""
    with pytest.raises(ValueError):
        my_function(None)

def test_function_with_large_input():
    """Test with large input (1000 items)"""
    result = my_function(list(range(1000)))
    assert len(result) == 1000
```

### 2. Mockuj Zewnętrzne Zależności:

```python
from unittest.mock import Mock, patch

def test_service_calls_database(mocker):
    """Test that service calls database correctly"""
    mock_db = mocker.patch('apps.memory_api.services.database')
    mock_db.query.return_value = [{"id": 1}]

    service = MyService(mock_db)
    result = service.get_data()

    mock_db.query.assert_called_once()
    assert len(result) == 1
```

### 3. Używaj Fixtures:

```python
@pytest.fixture
def sample_data():
    """Fixture providing sample data"""
    return {
        "id": "123",
        "content": "test",
        "importance": 0.8
    }

def test_process_data(sample_data):
    """Test data processing"""
    result = process(sample_data)
    assert result["id"] == "123"
```

### 4. Testuj Async Code:

```python
@pytest.mark.asyncio
async def test_async_function():
    """Test async function"""
    result = await my_async_function()
    assert result is not None
```

---

## 🔄 Krok 7: Workflow Iteracyjny

### Pojedyncza iteracja (30-60 minut):

```bash
# 1. Wybierz moduł
MODULE="apps/memory_api/core/state.py"
TEST_FILE="apps/memory_api/tests/core/test_state.py"

# 2. Sprawdź obecne pokrycie
pytest --cov=$MODULE --cov-report=term-missing $TEST_FILE

# 3. Zidentyfikuj missing lines
# Przykład output: "Missing: 45-47, 89-92"

# 4. Otwórz plik i przeanalizuj kod
# Pytania:
# - Co robią linie 45-47?
# - Jakie edge cases mogą wystąpić?
# - Jak wywołać te linie w teście?

# 5. Dodaj testy
# ... pisze testy ...

# 6. Uruchom testy
pytest $TEST_FILE -v

# 7. Sprawdź nowe pokrycie
pytest --cov=$MODULE --cov-report=term-missing $TEST_FILE

# 8. Powtarzaj kroki 4-7 aż osiągniesz target (85%)

# 9. Commit
git add $TEST_FILE
git commit -m "test: increase coverage for $(basename $MODULE) to 85%"

# 10. Push feature branch
git push origin feature/test-coverage-$(basename $MODULE .py)
```

---

## 📈 Krok 8: Tracking Progress

### Twórz feature branch dla każdego modułu:

```bash
# Nowy branch
git checkout -b feature/test-coverage-state develop

# Dodaj testy
# ...

# Commit
git commit -m "test: increase coverage for state.py to 85%"

# Push
git push origin feature/test-coverage-state

# Merge to develop (jeśli testy przechodzą)
git checkout develop
git merge feature/test-coverage-state
```

### Twórz issue dla tracking:

```markdown
## Test Coverage - Core Modules

- [x] state.py (85%)
- [x] actions.py (80%)
- [ ] reward.py (65% → target 85%)
- [ ] information_bottleneck.py (70% → target 85%)
- [ ] graph_operator.py (75% → target 85%)

Current overall: 52% → Target: 75%
```

---

## ⚡ Krok 9: Szybkie Wskazówki

### DO:
✅ Testuj jedną funkcję/metodę na raz
✅ Zacznij od prostych przypadków (happy path)
✅ Dodaj edge cases po happy path
✅ Mockuj zewnętrzne zależności
✅ Używaj descriptive test names
✅ Dodaj docstrings do testów
✅ Uruchamiaj testy często (po każdym dodaniu)

### DON'T:
❌ Nie pisz testów dla wszystkiego naraz
❌ Nie testuj implementacji (test behavior, not internals)
❌ Nie kopiuj-wklej testów bez zrozumienia
❌ Nie pomijaj edge cases
❌ Nie commituj bez uruchomienia testów

---

## 🎓 Przykładowa Sesja

```bash
# Gemini rozpoczyna pracę:

$ pytest --cov=apps/memory_api/core/state.py --cov-report=term-missing

apps/memory_api/core/state.py    65%    Missing: 45-47, 89-92, 110-115

# Gemini analizuje:
# Linie 45-47: Walidacja state_dict
# Linie 89-92: Error handling dla invalid layer
# Linie 110-115: Edge case: empty memory_layers

# Gemini dodaje testy:
# test_validate_state_dict_with_invalid_keys()
# test_get_layer_with_invalid_name_raises_error()
# test_state_with_empty_memory_layers_returns_default()

$ pytest apps/memory_api/tests/core/test_state.py -v
===== 3 passed in 0.5s =====

$ pytest --cov=apps/memory_api/core/state.py --cov-report=term-missing
apps/memory_api/core/state.py    85%    Missing: 110-112

# Gemini dodaje ostatni test
# test_state_edge_case_for_lines_110_112()

$ pytest --cov=apps/memory_api/core/state.py --cov-report=term-missing
apps/memory_api/core/state.py    87%    ✅

$ git commit -m "test: increase coverage for state.py to 87%"
```

---

## 🏆 Metryki Sukcesu

### Cel końcowy:
- **Overall coverage: 75%+**
- **Core modules: 85%+**
- **Services: 80%+**
- **API endpoints: 75%+**

### Monitorowanie:
- CI automatycznie sprawdza pokrycie
- Coverage threshold: 65% (zwiększony z 48%)
- Coverage trend tracking: nie pozwala na spadek >2%

---

## 🆘 Troubleshooting

### Problem: Nie wiem jak przetestować async kod
```python
# Rozwiązanie:
@pytest.mark.asyncio
async def test_my_async_function():
    result = await my_async_function()
    assert result is not None
```

### Problem: Test wymaga bazy danych
```python
# Rozwiązanie: Mockuj
def test_with_mock_db(mocker):
    mock_db = mocker.patch('module.database')
    mock_db.query.return_value = [{"id": 1}]
    # ... test ...
```

### Problem: Nie wiem które linie są missing
```bash
# Rozwiązanie:
pytest --cov=file.py --cov-report=html
open htmlcov/index.html  # Zobacz highlighted missing lines
```

---

## 📚 Zasoby

- **Pytest Docs**: https://docs.pytest.org/
- **Coverage.py**: https://coverage.readthedocs.io/
- **Mocking Guide**: https://docs.python.org/3/library/unittest.mock.html
- **Best Practices**: https://docs.pytest.org/en/stable/goodpractices.html

---

## ✅ Checklist dla Gemini

Przed rozpoczęciem każdej iteracji:
- [ ] Wybrałem moduł z listy priorytetów
- [ ] Sprawdziłem obecne pokrycie tego modułu
- [ ] Zidentyfikowałem missing lines
- [ ] Przeanalizowałem kod (rozumiem co robi)

Podczas pisania testów:
- [ ] Testuję edge cases
- [ ] Mockuję zewnętrzne zależności
- [ ] Używam descriptive names
- [ ] Dodaję docstrings

Po napisaniu testów:
- [ ] Wszystkie testy przechodzą (pytest -v)
- [ ] Pokrycie wzrosło do target
- [ ] Zacommitowałem zmiany
- [ ] Zaktualizowałem tracking issue

---

**START HERE:** Zacznij od `apps/memory_api/core/state.py` i pracuj zgodnie z listą priorytetów!
