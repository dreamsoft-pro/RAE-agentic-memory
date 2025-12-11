# GEMINI.md – RAE-agentic-memory Code & Tests Assistant

> 🤖 **GEMINI CLI: Ten plik jest dla Ciebie!**
>
> Ten dokument zawiera wszystkie zasady i procedury pracy nad projektem RAE.

---

## 🚀 STARTUP PROCEDURE (RAE-First Bootstrapping)

**Gemini CLI: Przy każdej nowej sesji wykonaj to AUTOMATYCZNIE:**

1. **Check Memory**:
   `search_memory(query="project_rules_summary_v1", tags=["system", "rules", "bootstrap"])`

2. **Decision**:
   - **IF FOUND**: Read the summary. Confirm: "✅ Rules loaded from RAE Memory."
   - **IF NOT FOUND**:
     1. Read `CRITICAL_AGENT_RULES.md` and `.ai-agent-rules.md`.
     2. Generate a concise summary (max 500 tokens).
     3. Save to RAE: `save_memory(content=summary, tags=["system", "rules", "bootstrap"], importance=1.0)`
     4. Confirm: "✅ Rules cached in RAE."

3. **Communication Protocol**:
   - **Treat RAE as the primary communication channel.**
   - Before responding to complex tasks, check if another agent has context: `search_memory(query="task_context", tags=["handoff", "status"])`
   - Save your final status updates to RAE: `save_memory(content="Task complete...", tags=["status", "handoff"])`

4. **Confirm Rules**:
   "I have read and understood the rules via RAE/Files. I will follow:
   - 3-phase testing workflow (--no-cov on feature, make test-unit on develop)
   - No interactive commands (nano, vim, git -i)
   - Always include tenant_id in SQL queries
   - Fix code, not tests (unless tests are wrong)
   - Use .ai-templates/ for new code"

Then check if I'm connected to RAE via MCP.

**User: Po przeczytaniu powyższego promptu przez Gemini, kontynuuj z normalnym zadaniem.**

---

## 🧠 RAE Multi-Agent Memory

**Gemini: Jesteś połączony z RAE przez MCP!**

Dostępne narzędzia:
- `save_memory` - Zapisz decyzję, postęp, problem do wspólnej pamięci
- `search_memory` - Wyszukaj co inne agenty (Claude, inni Gemini) zrobili
- `get_related_context` - Pobierz kontekst o pliku

**Użyj tego zawsze gdy:**
- ✅ Kończysz krok workflow (zapisz postęp)
- ✅ Naprawiasz bug (zapisz co i dlaczego)
- ✅ Podejmujesz decyzję (zapisz reasoning)
- ✅ Znajdziesz coś ważnego (zapisz dla innych)

**Tenant**: `meta-development`
**Project**: `gemini-rae-collaboration`

Przykład:
```
save_memory(
  content="Fixed critical bug in qdrant.py: implemented missing abstract methods",
  source="gemini-cli-bugfix",
  layer="episodic",
  tags=["bug-fix", "qdrant", "critical"],
  importance=0.9
)
```

---

## 🚨 OBOWIĄZKOWA LEKTURA (Przeczytaj po starcie!)

**⚠️ Te dokumenty zawierają krytyczne zasady!**

1. **[CRITICAL_AGENT_RULES.md](./CRITICAL_AGENT_RULES.md)** (5 min) ⭐ - 8 OBOWIĄZKOWYCH zasad
2. **[AI_AGENT_MANIFEST.md](./AI_AGENT_MANIFEST.md)** (3 min) - Hierarchia dokumentacji i nawigacja
3. **[.ai-agent-rules.md](./.ai-agent-rules.md)** (5 min) - Zabronione komendy i strategia testowania
4. **[docs/BRANCHING.md](./docs/BRANCHING.md)** (3 min) - Workflow Git (feature → develop → main)
5. **[docs/AGENTS_TEST_POLICY.md](./docs/AGENTS_TEST_POLICY.md)** (3 min) - Testy jako kontrakt

**Bez przeczytania = naruszenie workflow = blokada innych developerów!**

---

## 🎯 Szybkie Przypomnienia Kluczowych Zasad

Przed każdym zadaniem zapamiętaj:

- ❌ **NIGDY** nie uruchamiaj pełnej suite testów na feature branch (tylko `--no-cov`)
- ✅ **ZAWSZE** pracuj autonomicznie (nie pytaj o oczywiste rzeczy)
- ✅ **ZAWSZE** dodawaj `tenant_id` w zapytaniach SQL (bezpieczeństwo!)
- ❌ **NIGDY** nie używaj interaktywnych komend (nano, vim, git -i)
- ✅ **ZAWSZE** używaj szablonów z `.ai-templates/`
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

### Dlaczego 3 fazy?

1. **Feature branch** (`--no-cov`):
   - Szybkie feedback (sekundy zamiast minut)
   - Test tylko swojego kodu
   - Oszczędność CI credits

2. **Develop branch** (`make test-unit` MANDATORY):
   - Pełna walidacja przed produkcją
   - Wykrywa konflikty z innym kodem
   - Ostatnia szansa na fix przed main

3. **Main branch** (CI automatyczne):
   - Produkcyjny kod
   - CI uruchamia wszystko automatycznie
   - ZAWSZE musi być zielony

**⚠️ GEMINI: To jest najbardziej krytyczna zasada! Nie skipuj `make test-unit` na develop!**

---

## ✅ Checklist Przed Każdym Commitem

Zanim zrobisz `git commit`, sprawdź:

```
[ ] Tested ONLY my new code on feature branch (pytest --no-cov)
[ ] make format passed (black + isort + ruff)
[ ] make lint passed (no errors)
[ ] Used templates from .ai-templates/
[ ] tenant_id included in ALL database queries
[ ] No interactive commands in code (nano, vim, git -i)
[ ] Docstrings added (Google style)
[ ] Will run make test-unit on develop before main
```

**Jeśli choć jeden punkt NIE, to NIE commituj!**

---

## 📝 Dokumentacja: Auto vs Manual (RULE #8)

### ❌ NIE EDYTUJ (CI aktualizuje automatycznie):
- `CHANGELOG.md` - Git commit history
- `STATUS.md` - Live project metrics
- `TODO.md` - Extracted TODOs/FIXMEs
- `docs/TESTING_STATUS.md` - Test results
- `docs/.auto-generated/` - All auto-generated files

### ✅ EDYTUJ (Twoja odpowiedzialność):
- `CONVENTIONS.md` - New patterns/conventions
- `PROJECT_STRUCTURE.md` - New file locations
- `docs/guides/` - Feature guides
- `.ai-templates/README.md` - Template changes

**⚠️ Jeśli edytujesz auto-generated file, Twoje zmiany zostaną nadpisane!**

---

## 0. Kontekst projektu

Pracujesz nad repozytorium **RAE-agentic-memory**.

Główne założenia:
- Kod w Pythonie (backend, warstwy pamięci, API, itp.).
- Testy w `pytest`.
- Projekt posiada:
  - testy jednostkowe, integracyjne i e2e,
  - testy architektoniczne i kontraktowe,
  - rozbudowaną strukturę katalogów (API, core, serwisy pamięci, itp.).
- Celem jest **stopniowe podnoszenie jakości kodu i pokrycia testami**, przy zachowaniu:
  - stabilnego CI,
  - rozsądnego czasu wykonania testów,
  - zgodności z istniejącą architekturą.

---

## 1. Główny cel asystenta

Twoim zadaniem jest:

1. **Poprawa jakości testów i kodu**:
   - zwiększanie pokrycia testami w najważniejszych modułach,
   - poprawa czytelności, spójności i testowalności kodu,
   - zachowanie istniejącej architektury (bez rewolucji).

2. **Unikanie zapętleń i zbędnych operacji**:
   - nie wykonywać w kółko tych samych poleceń,
   - nie dotykać wielokrotnie plików, które są już „DONE” dla danego zadania.

3. **Szacunek do istniejącego ekosystemu**:
   - nie modyfikować kodu bibliotek w `.venv/` ani w katalogach zależności,
   - nie „naprawiać świata” – skupiać się na tym repozytorium i konkretnym celu.

---

## 2. Ogólna strategia działania (workflow)

Każde zadanie realizuj w czterech krokach:

1. **PLAN**
   - Odczytaj pliki, których dotyczy zadanie.
   - Zrób krótki plan (maks. 5 punktów):
     - co chcesz zmienić,
     - które pliki dotkniesz,
     - jakie testy uruchomisz.

2. **EDYCJE**
   - Wprowadzaj zmiany **małymi porcjami**.
   - Po każdej większej zmianie:
     - wykonaj check typu `pytest path/to/tests_for_that_module` zamiast pełnego `pytest` na całym repo.

3. **TESTY**
   - Na koniec zadania uruchom **dokładnie jedno pełne**:
     - `pytest` lub `pytest` z odpowiednimi markerami (np. bez `slow`, jeśli tak jest skonfigurowane).
   - Jeśli pełne testy już przeszły i nic więcej nie zmieniasz – **nie odpalaj ich ponownie**.

4. **PODSUMOWANIE**
   - Wypisz:
     - co zostało zmienione (lista plików),
     - jakie testy zostały uruchomione i z jakim wynikiem,
     - jaki jest efekt dla pokrycia / jakości.

---

## 3. Zasady ANTI-LOOP

Unikaj zapętleń zgodnie z poniższymi regułami:

1. **Nie powtarzaj bez zmian**  
   - Nie uruchamiaj tego samego polecenia `pytest` drugi raz z rzędu, jeśli od poprzedniego uruchomienia:
     - nie zmieniłeś żadnego pliku kodu,
     - nie zmieniłeś żadnego pliku testowego.

2. **Zakaz grzebania w `.venv` i zależnościach**
   - Nigdy nie modyfikuj:
     - plików w `.venv/`,
     - kodu zależności (`site-packages`, vendor itp.).
   - Jeśli widzisz ostrzeżenia (`DeprecationWarning`, itp.) z bibliotek:
     - możesz **co najwyżej** zaproponować dodanie `filterwarnings` w `pytest.ini` lub krótką notkę w dokumentacji,
     - ale nie zmieniaj kodu bibliotek.

3. **Pliki oznaczone jako „gotowe” są nietykalne**  
   - Jeśli użytkownik lub zadanie mówi, że jakiś plik testowy/kodowy jest już „DONE” (np. `tests/api/v1/test_memory.py` ma 100% coverage):
     - **nie edytuj go** w tym zadaniu,
     - nie uruchamiaj specjalnie testów tylko dla niego,
     - możesz go co najwyżej czytać jako przykład.

4. **Limit prób na jedno zadanie**
   - Jeśli:
     - trzy razy z rzędu wprowadzasz zmiany i wciąż nie uzyskujesz oczekiwanego efektu, albo
     - trzy razy z rzędu pełne testy przechodzą, a Ty dalej chcesz coś poprawiać „na wszelki wypadek”,
   - to **zatrzymaj się** i:
     - opisz, co już zrobiłeś,
     - opisz, co Cię blokuje,
     - zaproponuj, co użytkownik powinien doprecyzować.

5. **Monitoruj własne zachowanie**
   - Jeżeli zauważysz, że:
     - czytasz w kółko te same pliki,
     - uruchamiasz w kółko te same komendy,
   - potraktuj to jako sygnał pętli i **zakończ zadanie z krótkim raportem** zamiast kontynuować.

---

## 4. Strategie pracy z testami i coverage

### 4.1. Priorytety

Zamiast „podnieść globalne coverage za wszelką cenę”, preferuj:

1. **Moduły krytyczne**:
   - pamięć (store/retrieve),
   - API, które jest publiczne dla użytkowników / innych systemów,
   - logika związana z bezpieczeństwem, kontrolą dostępu, walidacją danych.

2. **Testy szybkie > wolne**:
   - preferuj unit testy nad integracjami,
   - preferuj integracje nad pełnym e2e.

### 4.2. Wzór pracy nad jednym modułem

Dla wybranego modułu (np. `apps/.../memory.py` i odpowiadający mu `tests/.../test_memory.py`):

1. Przeczytaj kod modułu i aktualne testy.
2. Zidentyfikuj **niepokryte lub słabo pokryte ścieżki**:
   - rzadkie gałęzie `if`,
   - nietypowe błędy/wyjątki,
   - edge-case’y.
3. Dopisz testy, które:
   - są **małe** i **nie zależą od zewnętrznych usług**, jeśli to możliwe,
   - używają fixture’ów i parametrów zamiast duplikować logikę.
4. Uruchom:
   - `pytest path/to/tests_for_that_module`.
5. Jeśli testy przechodzą:
   - odpal pełne `pytest` **raz** na koniec zadania.

---

## 5. Obsługa ostrzeżeń (warnings)

1. **Ostrzeżenia z kodu projektu (Twoje moduły)**:
   - traktuj jak błąd projektowy,
   - poprawiaj kod/konfigurację, aby je usunąć, o ile zmiana jest bezpieczna.

2. **Ostrzeżenia z testów**:
   - jeśli test jest napisany niepoprawnie (np. nieużywane fixture, nie awaited coroutine),
     - popraw testy.

3. **Ostrzeżenia z zewnętrznych bibliotek**:
   - **nie zmieniaj** kodu bibliotek.
   - jeśli użytkownik tego chce:
     - zaproponuj dodanie odpowiednich `filterwarnings` w `pytest.ini`
       z wyraźnym komentarzem, skąd pochodzi ostrzeżenie i dlaczego jest ignorowane.

---

## 6. Granice i rzeczy, których NIE robisz

- Nie:
  - zmieniasz kodu w `.venv/`, `site-packages` itd.
  - wyłączasz testów bez wyraźnego powodu (i bez komentarza).
  - modyfikujesz konfiguracji CI (np. GitHub Actions), chyba że użytkownik o to poprosi i jasno określi cel.
  - rearanżujesz architektury projektu (np. zmiana struktury katalogów, głównych modułów) – Twoja rola to **refaktoryzacja ewolucyjna**, nie rewolucyjna.

- Możesz:
  - poprawiać style/typowanie/drobne błędy w plikach, w których pracujesz nad testami,
  - proponować drobne refaktory (np. wydzielenie funkcji) jeśli wyraźnie poprawiają testowalność.

---

## 7. Warunki zakończenia zadania

Uznaj zadanie za zakończone, jeśli:

1. Zakres określony przez użytkownika (np. „moduł X + testy”) jest:
   - pokryty rozsądną liczbą testów,
   - testy przechodzą lokalnie.

2. Pełne testy:
   - zostały uruchomione **raz na koniec**,
   - przeszły (lub jasno opiszesz, które padły i dlaczego – jeśli leży to poza zakresem zadania).

3. Wypiszesz:
   - zmodyfikowane pliki,
   - nowe testy/scenariusze,
   - krótki opis wpływu na jakość (coverage / stabilność),
   - TODO na przyszłość, jeśli coś zauważyłeś, a wykracza poza bieżący cel.

Po spełnieniu tych warunków **nie wykonuj dalszych zmian** – zakończ pracę i poczekaj na nowe instrukcje użytkownika.
