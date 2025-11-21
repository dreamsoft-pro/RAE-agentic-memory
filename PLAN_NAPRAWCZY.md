# Plan Naprawczy RAE (Reflective Agentic-mode Engine)

Data sporządzenia: 2025-11-21
Status: Draft

## Cel
Celem tego planu jest podniesienie jakości kodu, stabilności, bezpieczeństwa oraz pokrycia testami projektu RAE do poziomu "Enterprise Grade", przygotowując go do szerszego wdrożenia produkcyjnego.

## 1. Jakość Kodu i Testy (Priorytet: Wysoki)

- [ ] **Zwiększenie Code Coverage:**
    - Cel: Minimum 80% pokrycia dla kluczowych modułów (`services/*`).
    - Akcja: Napisać brakujące testy jednostkowe dla `graph_algorithms.py` (obecnie 0%), `temporal_graph.py` (0%), `analytics.py` (0%).
    - Akcja: Naprawić testy w `test_api_e2e.py` i `test_background_tasks.py`, aby były niezależne od zewnętrznych usług (pełne mockowanie).
- [ ] **Refaktoryzacja Testów:**
    - Akcja: Wydzielić wspólne fixtury (np. dla bazy danych, Redis) do `conftest.py` w sposób modularny.
    - Akcja: Usunąć/naprawić "flaky tests" (testy dające losowe wyniki), jeśli takie istnieją (analiza logów CI).

## 2. Bezpieczeństwo i Konfiguracja (Priorytet: Wysoki)

- [ ] **Zarządzanie Sekretami:**
    - Akcja: Audyt kodu pod kątem hardcodowanych sekretów (np. w testach lub domyślnych wartościach `config.py`).
    - Akcja: Wdrożenie obsługi Docker Secrets w `docker-compose.prod.yml` dla środowisk produkcyjnych.
- [ ] **Walidacja Konfiguracji:**
    - Akcja: Dodać walidatory w `apps/memory_api/config.py` dla kluczowych zmiennych (URL-e baz danych, klucze API). Aplikacja powinna "fail fast" przy starcie, jeśli konfiguracja jest błędna.
- [ ] **Bezpieczeństwo API:**
    - Akcja: Zweryfikować i zaostrzyć politykę CORS w `main.py` (obecnie przykłady mogą być zbyt permisywne).
    - Akcja: Upewnić się, że rate limiting (`security/rate_limit.py`) działa poprawnie i jest skonfigurowany dla wszystkich endpointów publicznych.

## 3. Wydajność i Optymalizacja (Priorytet: Średni)

- [ ] **Optymalizacja GraphRAG:**
    - Akcja: Zaimplementować mechanizm "Entity Resolution" w `GraphExtractionService` w celu redukcji duplikatów węzłów w grafie wiedzy.
    - Akcja: Dodać indeksy w bazie danych dla zapytań grafowych (sprawdzić `alembic` migrations czy są optymalne).
- [ ] **Zarządzanie Zasobami:**
    - Akcja: Przejrzeć konfigurację puli połączeń (`asyncpg`, `redis`) pod kątem wycieków i optymalnych rozmiarów dla środowiska produkcyjnego.

## 4. Dokumentacja i DX (Priorytet: Średni)

- [ ] **Aktualizacja README i Guide'ów:**
    - Akcja: Zaktualizować instrukcje "Quick Start", aby były idiotoodporne (np. sprawdzenie wersji Dockera, Pythona).
    - Akcja: Dodać sekcję "Troubleshooting" z rozwiązaniami typowych problemów.
- [ ] **Przykłady Użycia:**
    - Akcja: Zaktualizować przykłady w `examples/` tak, aby korzystały z najnowszej wersji SDK i były zgodne z obecnym API.

## 5. Architektura (Priorytet: Niski/Długoterminowy)

- [ ] **Modularność:**
    - Akcja: Rozważyć wydzielenie `graph_service` jako osobnego modułu/mikroserwisu, aby odciążyć główne API pamięci.
- [ ] **Observability:**
    - Akcja: Dodać `Tracing` (np. OpenTelemetry) do śledzenia zapytań przechodzących przez różne serwisy (API -> Redis -> Postgres -> LLM).

## Harmonogram Wdrożenia

1. **Tydzień 1:** Testy jednostkowe i Code Coverage (Sekcja 1).
2. **Tydzień 2:** Bezpieczeństwo i Konfiguracja (Sekcja 2).
3. **Tydzień 3:** Optymalizacja GraphRAG i Refaktoryzacja (Sekcja 3 & 5).
4. **Tydzień 4:** Dokumentacja i finalne testy E2E (Sekcja 4).
