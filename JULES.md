Plan naprawczy dla projektu RAE (Reflective Agentic-mode Engine)
Po szczegółowej analizie dostarczonych plików projektu RAE, zidentyfikowałem szereg obszarów wymagających poprawy, optymalizacji lub dalszego rozwoju. Poniższy plan naprawczy został podzielony na sekcje tematyczne, z wyszczególnieniem konkretnych działań (Action Items) oraz uzasadnieniem ich konieczności.

1. Poprawa Testów i Code Coverage
Analiza raportu pokrycia kodu (coverage.xml) ujawniła, że obecne pokrycie wynosi około 49%, co jest wynikiem poniżej standardów produkcyjnych (zwykle >80%). Wiele kluczowych modułów ma zerowe lub bardzo niskie pokrycie.

Problem: Niskie pokrycie testami (apps/memory_api/services/graph_algorithms.py - 0%, apps/memory_api/services/temporal_graph.py - 0%, apps/memory_api/services/analytics.py - 0%). Brak testów integracyjnych dla kluczowych ścieżek (e2e).

Rozwiązanie:

Napisanie testów jednostkowych: Priorytetowo dla modułów graph_algorithms.py, temporal_graph.py, analytics.py oraz importance_scoring.py. Należy dążyć do minimum 80% pokrycia w każdym module.

Testy integracyjne: Rozbudowa tests/test_api_e2e.py o scenariusze obejmujące pełen cykl życia pamięci: dodanie -> refleksja -> zapytanie -> graf -> usunięcie.

Mockowanie serwisów zewnętrznych: Upewnienie się, że wszystkie testy jednostkowe używają mocków dla baz danych (Postgres, Redis, Qdrant) oraz API LLM, aby były szybkie i deterministyczne.

2. Optymalizacja Zarządzania Konfiguracją i Sekretami
W plikach konfiguracyjnych i dokumentacji widoczne są pewne nieścisłości oraz potencjalne ryzyka bezpieczeństwa.

Problem: Przykłady w dokumentacji (np. examples/simple-refactor-agent/README.md) sugerują używanie curl z kluczami API wprost w komendzie, co może prowadzić do ich wycieku w historii shella. Konfiguracja pydantic w config.py jest poprawna, ale brakuje walidacji niektórych kluczowych zmiennych.

Rozwiązanie:

Walidacja konfiguracji: W apps/memory_api/config.py dodać walidatory pydantic sprawdzające poprawność formatu kluczowych zmiennych (np. czy URL-e są poprawne, czy klucze API nie są puste, jeśli backend ich wymaga).

Bezpieczne przykłady: Zaktualizować dokumentację, aby w przykładach curl używać zmiennych środowiskowych (np. $RAE_API_KEY) zamiast hardcodowanych wartości lub placeholderów, które mogą zostać przypadkowo skopiowane.

Secrets Management: W docker-compose.prod.yml rozważyć użycie Docker Secrets zamiast zmiennych środowiskowych dla haseł i kluczy API w środowisku produkcyjnym.

3. Ulepszenie Obsługi Błędów i Logowania
Obecna obsługa błędów w niektórych miejscach jest zbyt ogólna, a logowanie nie zawsze dostarcza wystarczającego kontekstu.

Problem: W apps/memory_api/api/v1/agent.py i innych endpointach zdarzają się bloki except Exception as e, które logują błąd i zwracają generyczny kod 500 lub 502. Brakuje ustrukturyzowanych logów w formacie JSON dla łatwiejszego parsowania przez systemy logowania (np. ELK, Loki), mimo użycia structlog.

Rozwiązanie:

Szczegółowe kody błędów: Zdefiniować niestandardowe wyjątki biznesowe i mapować je na odpowiednie kody HTTP (np. MemoryNotFoundException -> 404, QuotaExceededException -> 429).

Ustrukturyzowane logowanie: Upewnić się, że structlog jest skonfigurowany tak, aby zawsze produkować logi w formacie JSON na produkcji. Dodać context_id (np. request_id) do wszystkich logów w ramach jednego żądania, aby ułatwić śledzenie przepływu.

Sentry/Monitoring: Dodać integrację z Sentry lub innym narzędziem do monitorowania błędów w main.py (opcjonalnie, za flagą feature flag).

4. Rozwój Funkcjonalności GraphRAG i Refleksji
Moduły graph_extraction.py i reflection_engine.py są kluczowe dla RAE, ale wymagają dopracowania pod kątem wydajności i jakości.

Problem: Ekstrakcja grafu wiedzy (GraphExtractionService) opiera się na LLM i może być kosztowna oraz wolna. Brak mechanizmu deduplikacji węzłów na poziomie logicznym (np. "User Authentication" vs "Auth").

Rozwiązanie:

Entity Resolution: Zaimplementować prosty mechanizm Entity Resolution (może być oparty na embeddingach nazw węzłów lub regułach), aby łączyć podobne byty przed zapisaniem ich do bazy grafowej.

Batch Processing: Upewnić się, że ekstrakcja grafu i refleksja działają w trybie wsadowym (batch) i asynchronicznie (już częściowo zrobione przez Celery, ale warto zweryfikować wydajność dla dużych wsadów).

Cache dla LLM: Rozważyć agresywniejsze cache'owanie odpowiedzi LLM dla identycznych fragmentów tekstu w ReflectionEngine, aby obniżyć koszty.

5. Dokumentacja i Developer Experience (DX)
Dokumentacja jest obszerna, ale w kilku miejscach może być nieaktualna lub myląca dla nowych użytkowników.

Problem: CONTRIBUTING.md odwołuje się do make install-all, ale Makefile ma target install-all instalujący zależności, które mogą być niepotrzebne dla każdego deva. Brak jasnej ścieżki "Zero to Hero" dla lokalnego uruchomienia bez Dockera (dla szybkiego debugowania).

Rozwiązanie:

Uproszczenie Makefile: Rozdzielić make install na make install-dev (podstawowe) i make install-full (wszystkie integracje).

Aktualizacja README: Dodać sekcję "Troubleshooting" do głównego README z najczęstszymi problemami (np. problemy z połączeniem do Postgresa w Dockerze).

API Specs: Upewnić się, że docs/OPENAPI.md jest automatycznie generowane lub synchronizowane z kodem FastAPI, aby uniknąć rozbieżności.

6. Architektura i Skalowalność
Projekt wykorzystuje asyncpg i Celery, co jest dobre, ale struktura katalogów i zależności między modułami mogą utrudniać skalowanie.

Problem: apps/memory_api staje się monolitem. Logika biznesowa (serwisy) jest wymieszana z logiką API (routery).

Rozwiązanie:

Czysta Architektura: Wyraźniejsze oddzielenie warstwy serwisów (logika biznesowa) od warstwy API (kontrolery). Rozważenie wydzielenia graph_service jako osobnego mikroserwisu w przyszłości, jeśli obciążenie wzrośnie.

Kolejki: Monitorowanie długości kolejek Celery. Dodać metryki Prometheus dla zadań w kolejce, aby móc skalować workery (HPA w K8s).

Podsumowanie Planu Naprawczego (plik .md)
Poniżej znajduje się gotowa zawartość pliku PLAN_NAPRAWCZY.md, którą możesz zapisać w repozytorium.

Markdown

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
Poniżej znajduje się link do filmu na YouTube, który luźno nawiązuje do tematu zarządzania pamięcią i systemami, co może być inspirujące w kontekście budowy "pamięci" dla AI.
https://www.youtube.com/watch?v=fpnE6UAfbtU
Jak działa pamięć komputera?

Film ten jest relewantny, ponieważ w prosty sposób wyjaśnia mechanizmy pamięci komputerowej, co jest dobrą analogią dla warstwowej architektury pamięci (Episodic, Semantic, Working) zastosowanej w projekcie RAE.