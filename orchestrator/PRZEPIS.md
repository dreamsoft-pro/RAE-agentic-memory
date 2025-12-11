# 📋 PRZEPIS - Jak Uruchomić Orkiestrator Samodzielnie

> **Cel:** Uruchomić orkiestrator BEZ pomocy Claude Code, żeby NIE marnować tokenów.

---

## ⚡ SZYBKI START (2 minuty)

### Krok 1: Otwórz Terminal
```bash
# Przejdź do katalogu projektu
cd /home/grzegorz/cloud/Dockerized/RAE-agentic-memory
```

### Krok 2: Aktywuj Środowisko
```bash
# Aktywuj Python virtual environment
source .venv/bin/activate
```

### Krok 3: Uruchom Zadanie
```bash
# Uruchom DEMO-001 (najprostsze zadanie)
python -m orchestrator.main --task-id DEMO-001
```

**GOTOWE!** 🎉

---

## 📖 PRZEPIS SZCZEGÓŁOWY

### Przygotowanie (raz, na początku)

#### 1. Sprawdź czy Gemini działa
```bash
cd /home/grzegorz/cloud/Dockerized/RAE-agentic-memory
source .venv/bin/activate
cd orchestrator
python test_simple.py
```

**Oczekiwany wynik:**
```
✅ PASS - Registry
✅ PASS - Gemini Provider
✅ PASS - Generation
✅ PASS - Claude Provider

🎉 All tests passed! Orchestrator is ready to use.
```

Jeśli widzisz to - możesz kontynuować!

---

### Sposób 1: Uruchom Istniejące Zadanie

#### Krok 1: Zobacz dostępne zadania
```bash
cd /home/grzegorz/cloud/Dockerized/RAE-agentic-memory
cat .orchestrator/tasks.yaml
```

**Zobaczysz:**
- `DEMO-001` - Funkcja timestamp (prosty, DARMOWY)
- `TEST-001` - Dodaj docstrings (prosty, DARMOWY)
- `TEST-002` - Dodaj testy (średni, DARMOWY)
- `RAE-PHASE2-001` - Core implementation (trudny, płatny ~$0.15)

#### Krok 2: Wybierz ID zadania
```bash
# Na przykład DEMO-001
TASK_ID="DEMO-001"
```

#### Krok 3: Uruchom
```bash
# Z głównego katalogu projektu
cd /home/grzegorz/cloud/Dockerized/RAE-agentic-memory
source .venv/bin/activate
python -m orchestrator.main --task-id $TASK_ID
```

#### Krok 4: Zobacz wyniki
```bash
# Główny log
cat ORCHESTRATOR_RUN_LOG.md | tail -100

# Stan zadania
cat orchestrator/state/${TASK_ID}.json | jq .

# Podsumowanie
cd orchestrator
python cli.py summary
```

---

### Sposób 2: Dodaj Własne Zadanie

#### Krok 1: Edytuj plik z zadaniami
```bash
nano .orchestrator/tasks.yaml
# lub
vim .orchestrator/tasks.yaml
# lub
code .orchestrator/tasks.yaml  # VS Code
```

#### Krok 2: Dodaj swoje zadanie
```yaml
  # Na końcu pliku dodaj:
  - id: MOJE-001
    goal: "Twój opis zadania tutaj"
    risk: low          # low=darmowy, medium=darmowy, high=płatny
    area: test         # test, docs, api, core
    repo: RAE-agentic-memory
    constraints:
      - ZERO-WARNINGS
      - Add docstring
      - Add tests
```

#### Krok 3: Zapisz i uruchom
```bash
# Zapisz plik (Ctrl+O w nano, :wq w vim)
# Potem uruchom:
python -m orchestrator.main --task-id MOJE-001
```

---

## 🎛️ KONFIGURACJA - Wybór Modelu

### Opcja A: Tylko DARMOWY Gemini (zalecane na start)

Edytuj: `.orchestrator/providers.yaml`
```yaml
providers:
  claude:
    enabled: false      # ❌ Wyłącz Claude (płatny)

  gemini:
    enabled: true       # ✅ Tylko Gemini (darmowy)
    default_model: gemini-2.5-flash
    settings:
      cli_path: gemini
      rate_limit_delay: true
      min_delay: 1.0
      max_delay: 10.0
```

**Koszt:** $0.00 dla WSZYSTKICH zadań!

---

### Opcja B: Mix (Smart - Gemini + Claude)

```yaml
providers:
  claude:
    enabled: true       # ✅ Dla high-risk tylko
    default_model: claude-sonnet-4-5-20250929

  gemini:
    enabled: true       # ✅ Dla low/medium risk
    default_model: gemini-2.5-flash
```

Orkiestrator automatycznie wybierze:
- **low/medium risk** → Gemini (FREE)
- **high risk** → Claude (~$0.05-0.15)

---

### Opcja C: Tylko Claude (najlepsza jakość)

```yaml
providers:
  claude:
    enabled: true
    default_model: claude-sonnet-4-5-20250929

  gemini:
    enabled: false      # ❌ Wyłącz Gemini
```

**Koszt:** ~$0.05-0.15 per zadanie (wysokiej jakości)

---

## 📝 KOMPLETNY PRZYKŁAD - Krok po Kroku

### Scenariusz: Dodaj docstrings do pliku

```bash
# 1. Otwórz terminal
cd /home/grzegorz/cloud/Dockerized/RAE-agentic-memory

# 2. Aktywuj venv
source .venv/bin/activate

# 3. Sprawdź czy działa (opcjonalnie)
cd orchestrator
python test_simple.py
cd ..

# 4. Zobacz dostępne zadania
cat .orchestrator/tasks.yaml | grep "id:"

# 5. Wybierz zadanie TEST-001 (dodaj docstrings)
# To zadanie jest DARMOWE (używa Gemini)

# 6. Uruchom
python -m orchestrator.main --task-id TEST-001

# Orkiestrator:
# - Załaduje zadanie
# - Wybierze Gemini (FREE)
# - Utworzy plan
# - Zaimplementuje
# - Sprawdzi jakość
# - Zapisze wyniki

# 7. Zobacz wyniki
cat ORCHESTRATOR_RUN_LOG.md | tail -100

# 8. Sprawdź status
cd orchestrator
python cli.py summary
```

---

## 🐛 TROUBLESHOOTING

### Problem 1: "ModuleNotFoundError: No module named 'orchestrator'"

**Rozwiązanie:**
```bash
# Upewnij się że jesteś w głównym katalogu
cd /home/grzegorz/cloud/Dockerized/RAE-agentic-memory

# I używasz python -m orchestrator.main (nie python orchestrator/main.py)
python -m orchestrator.main --task-id DEMO-001
```

---

### Problem 2: "Gemini CLI not available"

**Rozwiązanie:**
```bash
# Zaloguj się do Gemini CLI
gemini auth login

# Sprawdź czy działa
gemini --version
```

---

### Problem 3: "ANTHROPIC_API_KEY not found" (gdy używasz Claude)

**Rozwiązanie:**
```bash
# Sprawdź czy klucz jest w .env
grep ANTHROPIC_API_KEY .env

# Jeśli nie ma - dodaj:
echo "ANTHROPIC_API_KEY=sk-ant-api03-..." >> .env

# Lub eksportuj:
export ANTHROPIC_API_KEY=sk-ant-api03-...
```

---

### Problem 4: Gemini zwraca błąd parsowania

**Rozwiązanie 1: Użyj prostszego zadania**
```bash
# Zamiast skomplikowanego, uruchom DEMO-001
python -m orchestrator.main --task-id DEMO-001
```

**Rozwiązanie 2: Przełącz na Claude**
```bash
# Edytuj .orchestrator/providers.yaml
# Ustaw gemini: enabled: false
# Ustaw claude: enabled: true
```

---

### Problem 5: "Rate limit exceeded" (Gemini)

**Rozwiązanie:**
```bash
# Zwiększ delays w .orchestrator/providers.yaml:
gemini:
  settings:
    min_delay: 5.0    # Było 1.0
    max_delay: 20.0   # Było 10.0
```

---

## 💰 KONTROLA KOSZTÓW

### Zobacz ile wydałeś:
```bash
cd orchestrator
python cli.py summary
```

Output:
```
Total Cost: $0.00    # Jeśli używasz Gemini
# lub
Total Cost: $2.45    # Jeśli używasz Claude
```

### Zobacz szczegóły zadania:
```bash
cat orchestrator/state/DEMO-001.json | jq '.total_cost_usd'
```

---

## 🚀 ZAAWANSOWANE UŻYCIE

### Batch Processing (wiele zadań naraz)
```bash
# Uruchom wszystkie zadania z tasks.yaml
python -m orchestrator.main

# Orkiestrator wykona wszystkie zadania po kolei
```

### Tylko określone zadania:
```bash
# Uruchom TEST-001 i TEST-002
python -m orchestrator.main --task-id TEST-001
python -m orchestrator.main --task-id TEST-002
```

### Z custom working directory:
```bash
python -m orchestrator.main \
  --task-id TEST-001 \
  --working-dir /path/to/your/project
```

---

## 📊 MONITORING

### Dashboard (zobacz statystyki):
```bash
cd orchestrator/intelligence
python dashboard.py summary
```

### Zobacz top performers:
```bash
python dashboard.py rankings
```

### Optymalizacje kosztów:
```bash
python dashboard.py optimize
```

---

## ✅ CHECKLIST - Pierwsze Uruchomienie

- [ ] Jestem w katalogu projektu
- [ ] Aktywowałem `.venv` (`source .venv/bin/activate`)
- [ ] Test działa (`python test_simple.py` - 4/4 passed)
- [ ] Gemini jest zalogowany (`gemini --version`)
- [ ] Wybrałem zadanie z `tasks.yaml`
- [ ] Uruchamiam: `python -m orchestrator.main --task-id XXX`
- [ ] Czekam na wyniki (2-5 minut)
- [ ] Sprawdzam logi: `cat ORCHESTRATOR_RUN_LOG.md`

---

## 🎯 PODSUMOWANIE

### Co ROBIĆ:
✅ Uruchamiaj orkiestrator SAM (bez Claude Code)
✅ Używaj Gemini dla prostych zadań (FREE)
✅ Używaj Claude dla krytycznych zadań (płatny)
✅ Sprawdzaj koszty: `python cli.py summary`

### Czego NIE robić:
❌ Nie uruchamiaj przez Claude Code (marnowanie tokenów)
❌ Nie używaj Claude dla wszystkiego (drogo)
❌ Nie uruchamiaj bez rate limiting (Gemini)

---

## 📞 SZYBKA POMOC

**Coś nie działa?**

1. **Test podstawowy:**
   ```bash
   cd orchestrator && python test_simple.py
   ```
   Jeśli 4/4 passed = wszystko OK!

2. **Prosty test generowania:**
   ```bash
   cd orchestrator && python test_direct_generation.py
   ```
   Jeśli zwraca kod Python = Gemini działa!

3. **Sprawdź konfigurację:**
   ```bash
   cat .orchestrator/providers.yaml
   ```

4. **Zobacz logi:**
   ```bash
   cat ORCHESTRATOR_RUN_LOG.md | tail -200
   ```

---

**GOTOWY DO AUTOMATYZACJI? 🤖**

Skopiuj i wklej do terminala:
```bash
cd /home/grzegorz/cloud/Dockerized/RAE-agentic-memory
source .venv/bin/activate
python -m orchestrator.main --task-id DEMO-001
```

**Koszt: $0.00 | Czas: 2-3 min | Jakość: ✅**
