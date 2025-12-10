# Orchestrator - Quick Start Guide

## ✅ Wymagania

### 1. Klucz API Claude (opcjonalny, ale zalecany)
```bash
# W pliku .env (już skonfigurowany):
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### 2. Gemini CLI (darmowy, już zainstalowany)
```bash
# Sprawdź wersję:
gemini --version  # ✅ 0.20.0

# Jeśli nie zalogowany, zaloguj się:
gemini auth login  # Otworzy przeglądarkę do autentykacji
```

## 🚀 Weryfikacja - Czy Orkiestrator Działa?

```bash
cd orchestrator
python test_simple.py
```

**Oczekiwany output:**
```
🎉 All tests passed! Orchestrator is ready to use.
Passed: 4/4
```

## 📋 Jak Używać Orkiestratora?

### Opcja 1: Przykładowe Zadanie z YAML

Utwórz plik zadania w `.orchestrator/tasks.yaml`:

```yaml
tasks:
  - id: TEST-001
    goal: "Write a simple Python function to calculate factorial"
    description: |
      Create a recursive factorial function with:
      - Input validation (only non-negative integers)
      - Docstring with examples
      - Type hints
      - Unit tests
    risk: low
    area: test
    complexity: small
```

Uruchom:
```bash
cd orchestrator
python main.py --task-id TEST-001
```

### Opcja 2: Bezpośrednio z CLI

```bash
cd orchestrator
python cli.py execute \
  --goal "Add logging to the factorial function" \
  --risk low \
  --area test
```

### Opcja 3: Programowo (Python API)

```python
import asyncio
from orchestrator.main import Orchestrator
from orchestrator.core.state_machine import TaskDefinition, TaskRisk

async def main():
    # Utwórz orkiestrator
    orchestrator = Orchestrator()

    # Zdefiniuj zadanie
    task = TaskDefinition(
        task_id="TEST-001",
        goal="Write a function to check if a number is prime",
        description="Simple prime checker with tests",
        risk=TaskRisk.LOW,
        area="test",
    )

    # Wykonaj
    result = await orchestrator.execute_task(task)

    print(f"Status: {result.status}")
    print(f"Cost: ${result.total_cost_usd:.4f}")

asyncio.run(main())
```

## 🔧 Konfiguracja Modeli

### Plik: `.orchestrator/providers.yaml`

```yaml
providers:
  # Claude - Płatny, ale najlepszy dla critical tasks
  claude:
    enabled: true
    default_model: claude-sonnet-4-5-20250929
    settings:
      api_key: ${ANTHROPIC_API_KEY}

  # Gemini - DARMOWY przez CLI!
  gemini:
    enabled: true
    default_model: gemini-2.5-flash
    settings:
      cli_path: gemini
      rate_limit_delay: true  # Ważne dla wersji bez API key
      min_delay: 1.0
      max_delay: 10.0

routing:
  # Preferuj tańsze modele gdy jakość wystarczająca
  prefer_local: false
  max_cost_per_task: 1.0
  fallback_provider: claude
```

## 💰 Strategie Kosztów

### 1. **Maksymalna oszczędność** (90% zadań na Gemini)
```yaml
# Gemini dla wszystkiego poza critical tasks
gemini:
  enabled: true
  default_model: gemini-2.5-flash  # Najszybszy, darmowy

# Claude tylko dla high-risk
routing:
  max_cost_per_task: 0.10  # Maksymalnie $0.10 na task
```

### 2. **Balanced** (70% Gemini, 30% Claude)
```yaml
# Domyślna konfiguracja
# Gemini: low/medium risk
# Claude: high risk, critical areas
```

### 3. **Maximum Quality** (Claude dla wszystkiego)
```yaml
claude:
  enabled: true
  default_model: claude-opus-4-20250514  # Najlepszy

gemini:
  enabled: false  # Wyłącz Gemini
```

## 📊 Smart Routing - Jak To Działa?

Orkiestrator automatycznie wybiera model na podstawie:

### 1. **Task Risk** (3 poziomy)
```python
TaskRisk.LOW     → Gemini 2.5 Flash Lite  (FREE)
TaskRisk.MEDIUM  → Gemini 2.5 Pro         (FREE)
TaskRisk.HIGH    → Claude Sonnet 4.5      ($0.003/1K)
```

### 2. **Task Area** (gdzie w kodzie)
```python
area = "core"        → Claude (critical code)
area = "api"         → Gemini Pro
area = "tests"       → Gemini Flash
area = "docs"        → Gemini Flash Lite
```

### 3. **Historical Performance** (uczenie się)
Po ~200 zadaniach orkiestrator wie:
- Które modele są najlepsze dla danego typu zadania
- Gdzie można zaoszczędzić bez utraty jakości
- Które zadania wymagają review

## 🎯 Przykłady Użycia

### Przykład 1: Prosty Test (Darmowy - Gemini)
```bash
cd orchestrator
python cli.py execute \
  --goal "Write tests for user authentication" \
  --risk low \
  --area tests

# Koszt: $0.00 (Gemini FREE)
# Czas: ~2-3 min
```

### Przykład 2: Krytyczna Funkcja (Płatny - Claude)
```bash
python cli.py execute \
  --goal "Implement memory pruning algorithm" \
  --risk high \
  --area core \
  --complexity medium

# Koszt: ~$0.05-0.15 (Claude Sonnet)
# Czas: ~5-10 min
# Quality: Maximum
```

### Przykład 3: Batch Processing (Mix)
```yaml
# tasks.yaml
tasks:
  - id: BATCH-001
    goal: "Add logging to all services"
    risk: low

  - id: BATCH-002
    goal: "Update API documentation"
    risk: low

  - id: BATCH-003
    goal: "Fix memory leak in graph service"
    risk: high

# Uruchom wszystkie:
python main.py --batch
```

**Koszt:**
- BATCH-001 + BATCH-002: $0.00 (Gemini)
- BATCH-003: $0.10 (Claude)
- **Total: $0.10**

## 🔍 Monitoring

### 1. Run Logs
Każdy run zapisywany w `ORCHESTRATOR_RUN_LOG.md`:
```markdown
## Run #42 - 2025-12-10 18:00:00
Task: Add caching to API
Status: SUCCESS
Cost: $0.05
Duration: 8m 23s
```

### 2. Performance Dashboard
```bash
cd orchestrator/intelligence
python dashboard.py summary
```

Output:
```
📊 Overall Statistics
Total executions: 156
Success rate: 94.2%
Average cost: $0.03
Total cost saved: $12.45 (vs all-Claude)

🏆 Top Performers
1. gemini-2.5-flash: 92% success, $0.00 avg
2. claude-sonnet-4-5: 98% success, $0.05 avg
```

### 3. RAE Memory Integration (przyszłość)
```python
# Orkiestrator zapisze swoje doświadczenie w RAE
# Potem może się uczyć z poprzednich runów
```

## ⚠️ Ważne Uwagi

### Rate Limiting (Gemini Free)
Gemini CLI bez API key ma limity:
- **Per-second**: ~2-3 requests/s
- **Per-day**: ~1500 requests/day

Orkiestrator automatycznie dodaje losowe opóźnienia (1-10s) między requestami.

### Jeśli Potrzebujesz Więcej
```bash
# Opcja 1: Gemini API Key (płatny)
export GOOGLE_API_KEY=...
# W providers.yaml:
gemini:
  settings:
    api_key: ${GOOGLE_API_KEY}
    rate_limit_delay: false  # Wyłącz delays

# Opcja 2: Użyj tylko Claude
gemini:
  enabled: false
```

## 🐛 Troubleshooting

### Problem: "Gemini CLI not available"
```bash
# Zaloguj się:
gemini auth login

# Sprawdź:
gemini --version
```

### Problem: "ANTHROPIC_API_KEY not found"
```bash
# Sprawdź .env:
grep ANTHROPIC_API_KEY .env

# Lub export:
export ANTHROPIC_API_KEY=sk-ant-...
```

### Problem: Rate limit errors (429)
```yaml
# Zwiększ delays w providers.yaml:
gemini:
  settings:
    min_delay: 5.0   # Było 1.0
    max_delay: 20.0  # Było 10.0
```

## 📖 Dalsze Czytanie

- `README.md` - Pełna dokumentacja
- `docs/ORCHESTRATOR_PHASE2.5_COMPLETE.md` - Provider system
- `docs/ORCHESTRATOR_PHASE3_COMPLETE.md` - Intelligence & learning
- `docs/ORCHESTRATOR_MODELS_UPDATE.md` - Modele i rate limiting

---

**Pierwszych kroków:**
1. ✅ Uruchom `test_simple.py` - sprawdź czy działa
2. 🎯 Utwórz proste zadanie w `tasks.yaml`
3. 🚀 Uruchom `python main.py --task-id YOUR-TASK`
4. 📊 Zobacz wyniki w `ORCHESTRATOR_RUN_LOG.md`
5. 💰 Sprawdź koszt (większość zadań = $0.00!)
