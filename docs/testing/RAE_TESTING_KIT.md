# RAE TESTING KIT
Pakiet przygotowujący do uruchomienia testów i benchmarków dla RAE (Reflective Agentic-memory Engine)

Ten dokument opisuje:

1. Minimalne wymagania sprzętowe i programowe
2. Uruchomienie środowiska testowego (RAE Lite / Standard)
3. Instalację zależności Python
4. Uruchamianie testów jednostkowych, integracyjnych i wydajnościowych
5. Korzystanie z Evaluation Suite (`eval/`)
6. Jak przygotować się do benchmarków naukowych
7. Jak raportować wyniki

Dokument przeznaczony jest dla:
- zespołów badawczych (uczelnia, laboratoria AI)
- działów R&D firm
- inżynierów, DevOps i programistów
- niezależnych testerów

---

# 1. Wymagania

## 1.1 Sprzęt
**Konfiguracja minimalna (RAE Lite):**
- CPU: 4 wątki
- RAM: 8 GB
- Dysk: 5–10 GB

**Konfiguracja rekomendowana (RAE Standard / benchmarki):**
- CPU: 8–16 wątków
- RAM: 16–32 GB
- Dysk: 20–50 GB

## 1.2 Oprogramowanie
- Python 3.11+
- Docker + Docker Compose
- Git
- Make (zalecane)

---

# 2. Przygotowanie repozytorium

```bash
git clone https://github.com/dreamsoft-pro/RAE-agentic-memory
cd RAE-agentic-memory
git checkout main
```

Zaleca się wykonanie:

```bash
git pull origin main
```

aby upewnić się, że testy będą zgodne z najnowszą wersją kodu.

---

# 3. Uruchomienie środowiska (tryb Lite)

RAE Lite jest lekką konfiguracją dla małych maszyn, laptopów i środowisk testowych.

```bash
docker compose -f docker compose.lite.yml up -d
```

Po uruchomieniu sprawdź zdrowie API:

```bash
curl http://localhost:8000/health
```

Powinieneś otrzymać JSON typu:

```json
{ "status": "ok" }
```

---

# 4. Przygotowanie środowiska Python

## 4.1 Instalacja minimalna (testy lokalne)
```bash
make install
```

Instaluje:
- środowisko `.venv`
- dependencies z `requirements-dev.txt`
- SDK RAE (Tryb editable)

## 4.2 Instalacja pełna (dla uczelni / R&D)
```bash
make install-all
```

Instaluje dodatkowo:
- ML Service
- Reranker
- Evaluation Suite
- integracje (LangChain, LlamaIndex, MCP, Ollama wrapper itd.)

---

# 5. Uruchamianie testów

## 5.1 Testy jednostkowe (szybkie)
```bash
make test-unit
```

Zawiera testy:
- warstwy pamięci
- operacji bazodanowych
- zarządzania kontekstem
- API bez integracji LLM

Typowy czas wykonania: 15–45 sekund.

## 5.2 Pełne testy (cięższe)
```bash
make test
```

Obejmuje:
- integracje z ML Service
- testy wydajności
- testy kontraktów API
- testy komponentów ISO 42001

---

# 6. Evaluation Suite (eval/)

Evaluation Suite służy do wstępnej oceny:
- jakości retrievalu
- jakości pamięci semantycznej
- zgodności źródeł
- latencji zapytań
- odporności na szum

## 6.1 Uruchomienie

1. Upewnij się, że RAE Lite działa.
2. Zainstaluj zależności do eval:

```bash
pip install -r eval/requirements.txt
```

lub:

```bash
make install-all
```

3. Uruchom test:

```bash
.venv/bin/python eval/run_eval.py
```

## 6.2 Wyniki

Evaluation Suite zwraca:
- Hit Rate@5
- MRR (Mean Reciprocal Rank)
- Średnią latencję
- P95 latency
- Ścieżki źródeł pamięci

---

# 7. Przygotowanie do benchmarków naukowych

Aby testerzy mogli przygotować regulaminowy eksperyment:

1. Stwórz osobny katalog: `benchmarking/`
2. Użyj przykładowych zestawów z [BENCHMARK_STARTER.md](BENCHMARK_STARTER.md)
3. Zdefiniuj konfigurację A/B (np. różne ustawienia pamięci / LLM)
4. Zapisz wyniki zgodnie z szablonem raportu
5. Dodaj wyniki do tabel benchmarków w RAE (opcjonalnie)

---

# 8. Raportowanie wyników

Każdy tester powinien użyć szablonu:

[BENCHMARK_REPORT_TEMPLATE.md](BENCHMARK_REPORT_TEMPLATE.md)

Zawiera on pola:
- konfiguracja testowa
- hardware
- wersja RAE
- przebieg testów
- metryki
- obserwacje

---

# 9. Checklista gotowości do testów

- [ ] RAE Lite uruchamia się i `/health` = ok
- [ ] `make install` lub `make install-all` bez błędów
- [ ] `make test-unit` przechodzi
- [ ] `eval/run_eval.py` zwraca wyniki
- [ ] katalog `benchmarking/` zawiera zestawy testowe
- [ ] tester ma dostęp do [BENCHMARK_REPORT_TEMPLATE.md](BENCHMARK_REPORT_TEMPLATE.md)

**RAE jest teraz gotowe do testów akademickich / R&D.**
