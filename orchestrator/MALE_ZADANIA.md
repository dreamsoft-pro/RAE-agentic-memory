# 📋 Małe Zadania dla Orkiestratora (Fixed!)

> **Problem:** Gemini CLI miał błędy parsowania i "thinking mode not supported"
> **Rozwiązanie:** Przełączenie na Claude + małe zadania!

---

## ✅ Co Naprawiliśmy:

1. **Provider:** Gemini CLI → **Claude Sonnet 4.5** (niezawodny, działa!)
   - Gemini CLI error: "thinking is not supported by this model"
   - Claude API jest stabilny i bez problemów

2. **Reguły projektowe:** 73KB → 5KB (tylko pierwsze 50 linii CRITICAL_AGENT_RULES.md)

3. **Duże zadania rozbite:**
   - ~~RAE-DOC-001 (1 ogromne)~~ → **3 małe zadania** (RAE-DOC-001, 002, 003)
   - ~~RAE-PHASE2-FULL (2 tygodnie!)~~ → **3 adaptery** (RAE-PHASE2-001, 002, 003)

**Koszt:** Trochę drożej (~$0.15-0.30 zamiast $0), ale **DZIAŁA stabilnie!**

---

## 📝 Dostępne Małe Zadania

### Grupa 1: Dokumentacja (małe koszty, bezpieczne)

#### RAE-DOC-001
**Cel:** Sprawdź czy ContextBuilder jest zaimplementowany
**Risk:** Low
**Czas:** 3-5 minut
**Koszt:** ~$0.01-0.02 (Claude Sonnet 4.5)
```bash
python -m orchestrator.main --task-id RAE-DOC-001
```

#### RAE-DOC-002
**Cel:** Sprawdź status SQLite adapterów
**Risk:** Low
**Czas:** 3-5 minut
**Koszt:** ~$0.01-0.02 (Claude Sonnet 4.5)
```bash
python -m orchestrator.main --task-id RAE-DOC-002
```

#### RAE-DOC-003
**Cel:** Sprawdź status In-Memory adapterów
**Risk:** Low
**Czas:** 3-5 minut
**Koszt:** ~$0.01-0.02 (Claude Sonnet 4.5)
```bash
python -m orchestrator.main --task-id RAE-DOC-003
```

---

### Grupa 2: Phase 2 Adaptery (średnie koszty)

#### RAE-PHASE2-001
**Cel:** Implementuj PostgresMemoryStorage adapter
**Risk:** Medium
**Czas:** 10-15 minut
**Koszt:** ~$0.05-0.10 (Claude Sonnet 4.5)
```bash
python -m orchestrator.main --task-id RAE-PHASE2-001
```

#### RAE-PHASE2-002
**Cel:** Implementuj QdrantVectorStore adapter
**Risk:** Medium
**Czas:** 10-15 minut
**Koszt:** ~$0.05-0.10 (Claude Sonnet 4.5)
```bash
python -m orchestrator.main --task-id RAE-PHASE2-002
```

#### RAE-PHASE2-003
**Cel:** Implementuj RedisCacheProvider adapter
**Risk:** Low
**Czas:** 10-15 minut
**Koszt:** ~$0.02-0.05 (Claude Sonnet 4.5)
```bash
python -m orchestrator.main --task-id RAE-PHASE2-003
```

---

## 🚀 Szybki Start

### Krok 1: Przygotowanie
```bash
cd /home/grzegorz/cloud/Dockerized/RAE-agentic-memory
source .venv/bin/activate
```

### Krok 2: Test podstawowy
```bash
# Sprawdź czy orkiestrator działa
cd orchestrator
python test_simple.py
cd ..
```

### Krok 3: Uruchom MAŁE zadanie
```bash
# Najpierw darmowe (dokumentacja)
python -m orchestrator.main --task-id RAE-DOC-001
```

---

## 💡 Rekomendowana Kolejność

### Dzień 1: Dokumentacja (tanie!)
```bash
# 3 szybkie zadania - małe koszty
python -m orchestrator.main --task-id RAE-DOC-001
python -m orchestrator.main --task-id RAE-DOC-002
python -m orchestrator.main --task-id RAE-DOC-003
```

**Koszt:** ~$0.03-0.06
**Czas:** 15-20 minut
**Efekt:** Zaktualizowana dokumentacja Phase 1

---

### Dzień 2: Pierwszy Adapter (PostgreSQL)
```bash
# Test płatnego zadania
python -m orchestrator.main --task-id RAE-PHASE2-001
```

**Koszt:** ~$0.05
**Czas:** 10-15 minut
**Efekt:** PostgresMemoryStorage adapter gotowy

---

### Dzień 3-4: Pozostałe Adaptery
```bash
python -m orchestrator.main --task-id RAE-PHASE2-002
python -m orchestrator.main --task-id RAE-PHASE2-003
```

**Koszt:** ~$0.05 każdy
**Czas:** 10-15 minut każdy
**Efekt:** Wszystkie 3 adaptery gotowe

---

## 📊 Monitorowanie

### Zobacz postęp na żywo
```bash
# W innym terminalu
tail -f ORCHESTRATOR_RUN_LOG.md
```

### Po zakończeniu
```bash
# Zobacz wyniki
cat ORCHESTRATOR_RUN_LOG.md | tail -100

# Stan zadania
cat orchestrator/state/RAE-DOC-001.json | jq .

# Podsumowanie kosztów
cd orchestrator && python cli.py summary
```

---

## 🔧 Troubleshooting

### Problem: "Gemini CLI error"
**Rozwiązanie:** Małe zadania powinny działać! Jeśli dalej błąd:
```bash
# Sprawdź czy CLI działa
gemini --version
gemini "test prompt"

# Zaloguj się ponownie
gemini auth login
```

### Problem: Zadanie za długie
**Odpowiedź:** To niemożliwe! Teraz każde zadanie to maksymalnie 5 minut pracy.

---

## 💰 Szacunkowe Koszty

| Zadanie | Model | Koszt | Czas |
|---------|-------|-------|------|
| RAE-DOC-001 | Claude Sonnet 4.5 | ~$0.01-0.02 | 3-5 min |
| RAE-DOC-002 | Claude Sonnet 4.5 | ~$0.01-0.02 | 3-5 min |
| RAE-DOC-003 | Claude Sonnet 4.5 | ~$0.01-0.02 | 3-5 min |
| RAE-PHASE2-001 | Claude Sonnet 4.5 | ~$0.05-0.10 | 10-15 min |
| RAE-PHASE2-002 | Claude Sonnet 4.5 | ~$0.05-0.10 | 10-15 min |
| RAE-PHASE2-003 | Claude Sonnet 4.5 | ~$0.02-0.05 | 10-15 min |

**RAZEM:** ~$0.15-0.30 dla wszystkich 6 zadań

**UWAGA:** Gemini CLI wyłączony z powodu błędów "thinking mode not supported"

---

## ✅ Podsumowanie Zmian

### Przed:
- ❌ RAE-DOC-001: 1 duże zadanie (wszystkie sprawdzenia naraz)
- ❌ RAE-PHASE2-FULL: 2 TYGODNIE pracy w jednym zadaniu!
- ❌ Prompty 73KB (reguły + kontekst)
- ❌ Gemini CLI crashed

### Po:
- ✅ RAE-DOC-001/002/003: 3 małe zadania (po 1 sprawdzenie)
- ✅ RAE-PHASE2-001/002/003: 3 adaptery (po 1 plik)
- ✅ Prompty ~5KB (tylko krytyczne reguły)
- ✅ Gemini CLI działa!

---

## 🎯 Następne Kroki

Po wykonaniu tych 6 zadań możesz:

1. **Dodać więcej małych zadań** - np. kolejne adaptery (Ollama, Embedding)
2. **Week 6 Integration** - rozbić na małe zadania refaktoryzacji
3. **Testy** - każdy adapter = osobne zadanie na testy

**Klucz to:** 1 zadanie = 1 konkretna rzecz = krótki prompt = działa z Gemini CLI!

---

**Gotowy? Uruchom pierwsze małe zadanie:**

```bash
cd /home/grzegorz/cloud/Dockerized/RAE-agentic-memory
source .venv/bin/activate
python -m orchestrator.main --task-id RAE-DOC-001
```

**To zajmie tylko 3-5 minut i jest DARMOWE!** 🎉
