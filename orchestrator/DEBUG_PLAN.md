# 🔧 Plan Debugowania Orkiestratora

## Co Zrobiłem (Podczas Twojego Spaceru):

### 1. Wyłączyłem Reguły Projektowe
**Plik:** `orchestrator/agents/base.py`
```python
def _load_project_rules(self, working_dir: str) -> str:
    # DISABLED: Project rules cause issues with LLM prompts
    return ""
```

**Dlaczego:** Reguły dodawały ~5-50KB do każdego promptu, mogły powodować problemy.

---

### 2. Dodałem Ekstensywne Logowanie
**Plik:** `orchestrator/adapters/claude_adapter.py`

Teraz w każdym API calli zobaczysz:
```
INFO: Claude API call: model=claude-sonnet-4-5-20250929, prompt_len=1234
DEBUG: Prompt preview: Task: Check if file exists...
INFO: Claude API success: input=456, output=123
```

Przy błędzie:
```
ERROR: Claude API error: ConnectionError: Connection refused
```

---

### 3. Stworzyłem Ultra-Proste Zadanie Testowe
**Plik:** `.orchestrator/tasks.yaml`

```yaml
- id: TEST-SIMPLE
  goal: "Check if file exists: rae-core/rae_core/context/builder.py"
  risk: low
  area: docs
  repo: RAE-agentic-memory
  constraints:
    - Read file rae-core/rae_core/context/builder.py
    - Report if file exists or not
    - Output: YES or NO
```

To najprostsze możliwe zadanie - tylko sprawdzenie czy plik istnieje.

---

### 4. Dodałem Test Claude API (bez orkiestratora)
**Plik:** `orchestrator/test_claude_direct.py`

Możesz sprawdzić czy Claude działa sam w sobie:
```bash
cd orchestrator
source ../.venv/bin/activate
python test_claude_direct.py
```

---

## 🚀 Jak Przetestować:

### Test 1: Sprawdź czy Claude API działa
```bash
cd /home/grzegorz/cloud/Dockerized/RAE-agentic-memory/orchestrator
source ../.venv/bin/activate
python test_claude_direct.py
```

**Oczekiwany wynik:**
```
✅ API key found: sk-ant-api03-...
📤 Prompt: What is 2+2? Answer in one word.
⏳ Calling Claude API...
✅ Success!
📥 Response: Four
```

**Jeśli to NIE działa:**
- Problem jest z Claude API / kluczem / siecią
- NIE z orkiestratorem

---

### Test 2: Uruchom najprostsze zadanie orkiestratora
```bash
cd /home/grzegorz/cloud/Dockerized/RAE-agentic-memory
source .venv/bin/activate
python -m orchestrator.main --task-id TEST-SIMPLE 2>&1 | tee orchestrator_test_simple.log
```

**To:**
- Uruchomi orkiestrator
- Z najprostszym możliwym zadaniem
- Z ekstensywnym logowaniem
- Zapisze wszystko do `orchestrator_test_simple.log`

---

### Test 3: Analiza Logów

Po uruchomieniu orkiestratora zobaczysz w logach **dokładnie gdzie failuje**:

**Scenariusz A: Claude API działa**
```
INFO: Claude API call: model=claude-sonnet-4-5-20250929, prompt_len=456
INFO: Claude API success: input=123, output=45
```
→ Problem jest w parsowaniu odpowiedzi lub innej logice

**Scenariusz B: Claude API nie działa**
```
ERROR: Claude API error: ConnectionError: ...
```
→ Problem z API / kluczem / siecią

**Scenariusz C: Coś innego**
```
ERROR: Task TEST-SIMPLE failed with exception
Traceback ...
```
→ Problem gdzieś w orkiestratorze przed Claude API call

---

## 📝 Co Zapisać:

Po uruchomieniu, skopiuj **WSZYSTKIE** logi do:
```
docs/bledy-orkiestrator_04.md
```

Potrzebne informacje:
1. Pełny output z `python -m orchestrator.main --task-id TEST-SIMPLE`
2. Ostatnie linie z `orchestrator_test_simple.log`
3. Czy `test_claude_direct.py` działało

---

## 🔍 Co Sprawdzić:

### Klucz API Claude
```bash
grep ANTHROPIC_API_KEY .env
```
Powinno być: `ANTHROPIC_API_KEY=sk-ant-api03-...`

### Czy anthropic package zainstalowany
```bash
source .venv/bin/activate
pip show anthropic
```
Powinno być: `Version: 0.74.1` lub wyżej

### Internet connectivity
```bash
curl -I https://api.anthropic.com
```
Powinno zwrócić: `HTTP/2 200` (lub 403, ale NIE connection refused)

---

## 💡 Możliwe Przyczyny Błędów:

### 1. Claude API Key Invalid
**Symptom:** `AuthenticationError` w logach
**Fix:** Sprawdź czy klucz w `.env` jest poprawny

### 2. Brak Internetu / Firewall
**Symptom:** `ConnectionError` w logach
**Fix:** Sprawdź połączenie z `curl https://api.anthropic.com`

### 3. anthropic Package Problem
**Symptom:** `ImportError` lub weird errors
**Fix:** `pip install --upgrade anthropic`

### 4. Problem w Orkiestratorze
**Symptom:** Błąd PRZED "Claude API call" w logach
**Fix:** To trzeba będzie debugować dalej

### 5. Problem z Parsowaniem Odpowiedzi
**Symptom:** "Claude API success" w logach, ale potem błąd
**Fix:** Problem w agent logic, nie w Claude

---

## 🎯 Następne Kroki:

1. **Uruchom Test 1** (test_claude_direct.py)
   - Jeśli ❌ → Problem z Claude API
   - Jeśli ✅ → Idź do Test 2

2. **Uruchom Test 2** (TEST-SIMPLE przez orkiestrator)
   - Zapisz WSZYSTKIE logi do docs/bledy-orkiestrator_04.md
   - Wrócę i przeanalizuję co poszło nie tak

3. **Jeśli Test 2 ✅ działa:**
   - Spróbuj RAE-DOC-001: `python -m orchestrator.main --task-id RAE-DOC-001`
   - Jeśli to też działa → PROBLEM ROZWIĄZANY! 🎉

---

## 📊 Status Zmian:

```
✅ Reguły projektowe wyłączone (base.py)
✅ Ekstensywne logowanie dodane (claude_adapter.py)
✅ Ultra-proste zadanie TEST-SIMPLE (.orchestrator/tasks.yaml)
✅ Direct Claude test (test_claude_direct.py)
✅ Wszystko zacommitowane (commit 5e8aaceb4)
```

---

**Jesteś gotowy do testowania!** 🚀

Uruchom testy i zapisz logi. Przeanalizuję je jak wrócisz ze spaceru.
