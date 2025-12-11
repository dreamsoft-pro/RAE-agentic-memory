# Tutorial - Pierwsze Kroki z Orkiestratorem

## 🎯 Cel
Nauka używania orkiestratora w 5 minut.

---

## Krok 1: Sprawdź czy działa (30 sekund)

```bash
cd orchestrator
python test_simple.py
```

**Oczekiwany wynik:**
```
🎉 All tests passed! Orchestrator is ready to use.
Passed: 4/4
```

✅ Jeśli widzisz to - możesz kontynuować!
❌ Jeśli błąd - sprawdź QUICK_START.md sekcję "Troubleshooting"

---

## Krok 2: Zobacz dostępne zadania (10 sekund)

```bash
cd ..  # Wróć do głównego katalogu projektu
cat .orchestrator/tasks.yaml
```

**Dostępne przykłady:**
- `TEST-001` - Dodaj docstrings (prosty, **DARMOWY** - Gemini)
- `TEST-002` - Dodaj testy (średni, **DARMOWY** - Gemini Pro)
- `RAE-PHASE2-001` - Core implementation (trudny, **$0.10-0.20** - Claude)
- `RAE-API-001` - REST endpoint (średni, **DARMOWY** - Gemini Pro)

---

## Krok 3A: Uruchom PROSTE zadanie (ZALECANE dla pierwszego razu)

### Dodaj NOWE proste zadanie do `.orchestrator/tasks.yaml`:

```yaml
  # Twoje pierwsze zadanie - bardzo proste!
  - id: MY-FIRST-001
    goal: "Write a simple hello_world() function in Python"
    risk: low
    area: test
    repo: RAE-agentic-memory
    constraints:
      - Add docstring
      - Add type hints
      - Return greeting string
```

### Uruchom:

```bash
cd orchestrator
python main.py --task-id MY-FIRST-001
```

**Co się stanie:**
1. Orkiestrator załaduje zadanie z YAML
2. Smart routing wybierze **Gemini 2.5 Flash** (DARMOWY!)
3. Planner utworzy plan implementacji
4. Implementer napisze kod
5. Reviewer sprawdzi jakość
6. Wyniki zapisane w `ORCHESTRATOR_RUN_LOG.md`

**Czas:** ~2-3 minuty
**Koszt:** $0.00 (Gemini FREE)

---

## Krok 3B: Uruchom ISTNIEJĄCE zadanie

```bash
cd orchestrator
python main.py --task-id TEST-001
```

To doda docstrings do `ContextBuilder` - prosty, darmowy task.

---

## Krok 4: Zobacz wyniki

### Logi główne:
```bash
cat ../ORCHESTRATOR_RUN_LOG.md | tail -100
```

### Stan zadania:
```bash
cat state/MY-FIRST-001.json | jq .
# lub bez jq:
cat state/MY-FIRST-001.json
```

### Podsumowanie:
```bash
python cli.py summary
```

Output:
```
📊 Orchestrator Summary

Total Tasks: 1
Active Tasks: 0
Needs Human Review: 0
Total Cost: $0.00
```

---

## Krok 5: Dodaj własne zadanie

### Edytuj `.orchestrator/tasks.yaml`:

```yaml
  - id: MY-TASK-001
    goal: "Twój opis zadania..."
    risk: low       # low, medium, high
    area: test      # test, docs, api, core
    repo: RAE-agentic-memory
    context_files:  # Opcjonalne - pliki do przeczytania
      - path/to/file.py
    constraints:    # Wymagania
      - ZERO-WARNINGS
      - Add tests
```

### Uruchom:
```bash
cd orchestrator
python main.py --task-id MY-TASK-001
```

---

## 💡 Wskazówki

### 1. **Wybór Risk Level:**
```yaml
risk: low     # Gemini Flash Lite → FREE
risk: medium  # Gemini Pro → FREE
risk: high    # Claude Sonnet → ~$0.05-0.15 (płatny)
```

### 2. **Wybór Area:**
```yaml
area: docs    # Dokumentacja → Gemini Flash Lite (najszybszy, FREE)
area: tests   # Testy → Gemini Flash (FREE)
area: api     # API → Gemini Pro (FREE)
area: core    # Core logic → Claude Sonnet (płatny, ale najlepszy)
```

### 3. **Batch Processing (wiele zadań naraz):**
```bash
# Uruchom wszystkie zadania z pliku
cd orchestrator
python main.py
```

To wykona **wszystkie** zadania z `tasks.yaml` po kolei.

### 4. **Monitorowanie:**
```bash
# Zobacz aktywne zadania
cd orchestrator
python cli.py summary

# Zobacz zadania wymagające review
python cli.py review
```

---

## 🎓 Przykład: Praktyczny Workflow

### Scenariusz: Dodaj feature do RAE

**1. Zaplanuj zadania w YAML:**
```yaml
tasks:
  # Krok 1: Dokumentacja (darmowy)
  - id: FEATURE-001-DOCS
    goal: "Document new caching strategy in API_DOCS.md"
    risk: low
    area: docs

  # Krok 2: Implementacja (darmowy)
  - id: FEATURE-002-IMPL
    goal: "Implement Redis caching layer"
    risk: medium
    area: api

  # Krok 3: Testy (darmowy)
  - id: FEATURE-003-TESTS
    goal: "Add integration tests for caching"
    risk: medium
    area: tests
```

**2. Uruchom wszystkie:**
```bash
cd orchestrator
python main.py
```

**3. Zobacz wyniki:**
```bash
python cli.py summary
cat ../ORCHESTRATOR_RUN_LOG.md | tail -200
```

**Koszt całości:** $0.00 (wszystkie na Gemini!)
**Czas:** ~10-15 minut total

---

## ❓ FAQ

**Q: Czy muszę mieć klucz API Claude?**
A: NIE - większość zadań (70-80%) działa na Gemini (FREE). Claude potrzebny tylko dla high-risk tasks.

**Q: Jak zmniejszyć koszty?**
A: Ustaw `risk: low` lub `risk: medium` - użyje darmowego Gemini.

**Q: Co jeśli zadanie się nie uda?**
A: Sprawdź logi w `ORCHESTRATOR_RUN_LOG.md`. Orkiestrator ma retry logic (3 próby).

**Q: Czy mogę uruchomić zadanie bez YAML?**
A: Nie bezpośrednio, ale możesz użyć Python API (przykład w QUICK_START.md).

**Q: Jak wyłączyć Claude i używać tylko Gemini?**
A: W `.orchestrator/providers.yaml` ustaw `claude: enabled: false`

---

## 🚀 Następne Kroki

1. ✅ Uruchom `MY-FIRST-001` - proste zadanie testowe
2. ✅ Zobacz wyniki w logach
3. ✅ Dodaj własne zadanie do YAML
4. ✅ Eksperymentuj z różnymi `risk` i `area`
5. 📖 Przeczytaj `QUICK_START.md` dla zaawansowanych opcji

---

**Potrzebujesz pomocy?**
- `orchestrator/QUICK_START.md` - Kompletny przewodnik
- `orchestrator/README.md` - Pełna dokumentacja
- `docs/ORCHESTRATOR_PHASE2.5_COMPLETE.md` - Provider system
- `docs/ORCHESTRATOR_PHASE3_COMPLETE.md` - Intelligence & learning

**Ready to automate?** 🤖
