# RAE_ENTERPRISE_REFINEMENT_PLAN.md  
**Cel:** Doprowadzenie projektu **RAE – Reflective Agentic Memory Engine** do wzorcowego poziomu enterprise (v2.0), z naciskiem na:  
- deterministyczną kontrolę kosztów i tokenów,  
- realne governance & audyt,  
- silnik eventów i automatyzacji,  
- dashboard produkcyjny,  
- stabilne SDK dla agentów,  
- wydajny GraphRAG/Hybrid Search,  
- przygotowanie pod pluginy i integracje.

Plan uzupełnia istniejące dokumenty: `COST_CONTROLLER_REFINEMENT_PLAN.md` oraz `IMPLEMENTATION_REFINEMENT_PLAN.md`. :contentReference[oaicite:0]{index=0}  

---

## 0. Założenia i Konwencje

- **Wersja docelowa:** `v2.0.0` (pierwsza w pełni enterprise’owa).  
- **Branch główny do prac:** `develop` (main to wyłącznie wersje stabilne).  
- **Styl:** “Infrastructure as Code + Tests as Specification”:  
  - Każdy duży krok → osobny PR + opis w `CHANGELOG.md`.  
  - Każda funkcja krytyczna → komplet testów (unit + integration).  
- **Priorytet:** kolejność implementacji jest twarda (Faza 1 → Faza 8).  
- **Własny “Definition of Done”:** każdy etap kończy się:
  - testami (min. 80% coverage w krytycznych modułach),  
  - metrykami,  
  - dokumentacją,  
  - przykładem (SDK / curl / agent).

---

## Faza 1 – Cost Controller v1.0 (Runtime z prawdziwymi kosztami)

**Cel:** Każde wywołanie LLM (i embeddingów) ma policzony koszt, zapis do logów, aktualizację budżetu oraz metryki. Zero 0.0 USD z powodu braków implementacyjnych.

### 1.1. Model danych i migracje

**Zadania:**
1. Dodać tabelę `cost_logs`:
   - `id: UUID`  
   - `tenant_id: UUID / TEXT`  
   - `project_id: TEXT`  
   - `model: TEXT`  
   - `operation: TEXT` (np. `query`, `embedding`, `reflection`)  
   - `input_tokens: INT`  
   - `output_tokens: INT`  
   - `total_cost_usd: NUMERIC(18,8)`  
   - `cache_hit: BOOL` (dla context cache)  
   - `created_at: TIMESTAMPTZ`  

2. Rozszerzyć tabelę budżetów (`budgets` lub analogiczną):
   - `daily_tokens_limit`, `monthly_tokens_limit`  
   - `daily_tokens_used`, `monthly_tokens_used`  
   - `last_token_update_at`  

3. Uzupełnić migracje Alembic:
   - nowa migracja z wersją `v2_cost_controller_init`  
   - indeksy po `tenant_id`, `project_id`, `created_at`.

**Akceptacja:**
- `alembic upgrade head` przechodzi bez błędów na pustej i istniejącej bazie.
- `SELECT COUNT(*) FROM cost_logs;` → działa, struktura poprawna.

---

### 1.2. Warstwa pricing & tokenów

**Zadania:**
1. Dodać moduł `apps/memory_api/services/pricing.py`:
   - `get_model_pricing(model: str, provider: str) -> ModelPricing`  
     - pola: `input_per_million`, `output_per_million`, `currency` (`USD`)  
   - `calculate_cost(model, provider, input_tokens, output_tokens) -> float`  

2. Dodać konfigurację modeli w kodzie + fallback w `.env`:
   - np. `RAE_PRICING_GPT4O`, `RAE_PRICING_GEMINI_PRO`, itp.  
   - sensowny default, żeby system nie był bezużyteczny bez kluczy.

3. Ujednolicić pobieranie tokenów:
   - dla OpenAI / Anthropic / Gemini → czytać z pól w odpowiedzi (usage).  
   - dla lokalnych modeli → heurystyka (np. `tiktoken` / prosty licznik słów * współczynnik).

**Akceptacja:**
- Testy jednostkowe `test_pricing.py`:
  - różne modele → poprawne przeliczenia.  
  - wyzerowane usage → fallback heurystyczny działa.

---

### 1.3. Integracja LLM Client → Cost Info

**Zadania:**
1. W klientach LLM (`ml_service_client` / `llm_client` / analogiczne):
   - dodać generowanie obiektu `CostInfo`:
     - `input_tokens`, `output_tokens`, `total_estimate`, `provider`, `model`.  

2. Jeśli provider nie zwraca usage:
   - policzyć heurystycznie przed zwrotem odpowiedzi.

3. Zaktualizować `AgentResponse` / `LLMResponse`:
   - pole `cost: CostInfo` musi zawsze być wypełnione.

**Akceptacja:**
- Test: `test_llm_client_cost_populated`:
  - po jednym wywołaniu mamy niezerowe `input_tokens` i `total_estimate > 0`.

---

### 1.4. CostGuardMiddleware – twarde egzekwowanie kosztów

**Zadania:**
1. W middleware:
   - jeśli `response.cost.total_estimate == 0`:
     - wywołać `calculate_cost()` z tokenami i nadpisać wartość.  

2. Po sprawdzeniu budżetu wejściowego (`check_budget_before`):
   - po odpowiedzi z LLM:
     - wywołać `BudgetService.increment_usage(...)` z:
       - `cost_usd`, `input_tokens`, `output_tokens`, `operation_type`.  

3. Dodać obsługę:
   - limitów USD dziennych / miesięcznych,  
   - limitów tokenów dziennych / miesięcznych,  
   - wyjątek / HTTP 429 z czytelnym komunikatem.

**Akceptacja:**
- Scenariusz integracyjny:
  - budżet dzienny: 0.01 USD.  
  - 2 wywołania LLM po 0.006 USD.  
  - pierwsze przechodzi, drugie blokowane.  

---

### 1.5. Rejestracja w `cost_logs` + metryki Prometheus

**Zadania:**
1. Logging:
   - w `BudgetService.increment_usage()`:
     - tworzyć wpis w `cost_logs` (każde wywołanie LLM).  

2. Prometheus:
   - dodać metryki:
     - `rae_cost_llm_total_usd{tenant,model}`  
     - `rae_cost_llm_calls_total{tenant,model}`  
     - `rae_cost_tokens_total{tenant}`  
     - `rae_cost_budget_rejections_total{tenant}`  
     - histogram `rae_cost_tokens_per_call`.  

3. Logi audytowe:
   - `[COST] tenant=... model=... in=... out=... cost=... usage(usd)=... usage(tokens)=...`  
   - `[COST-BLOCK] tenant=... reason=exceeded_daily_usd_limit ...`.

**Akceptacja:**
- `curl /metrics` zawiera nowe metryki.  
- W logach pojawiają się wpisy `[COST]` i `[COST-BLOCK]`.

---

## Faza 2 – Governance & Statystyki na realnych danych

**Cel:** Governance nie jest już “papierowe”, tylko oparte o realne `cost_logs` i usage budżetów.

### 2.1. Implementacja w GovernanceService

**Zadania:**
1. Zaimplementować:
   - `_count_tokens_used(tenant_id, period_days)`:
     - `SELECT SUM(input_tokens + output_tokens) FROM cost_logs WHERE ...`.  

   - `_estimate_llm_cost(tenant_id, period_days)`:
     - `SELECT SUM(total_cost_usd) FROM cost_logs WHERE ...`.  

2. Dodać metody:
   - `get_tenant_stats(tenant_id)`  
     - zwraca:
       - dzienne / miesięczne użycie USD,  
       - dzienne / miesięczne tokeny,  
       - procent wykorzystania limitów,  
       - licznik odrzuconych żądań.  

3. API endpoint:
   - `GET /v1/governance/tenant/{tenant_id}/stats`  
   - `GET /v1/governance/overview` (lista tenantów z agregatami).

**Akceptacja:**
- Testy integracyjne z wypełnioną tabelą `cost_logs`:
  - Governance zwraca prawidłowe agregaty.  

---

### 2.2. Dokumentacja Governance & Cost

**Zadania:**
1. `docs/cost-controller.md`:
   - przepływ requestów,  
   - cenniki modeli,  
   - przykładowe wyliczenia,  
   - jak ustawić limity tenantów,  
   - jak czytać metryki Prometheus i logi.

2. Sekcja w `API_DOCUMENTATION.md`:
   - opis endpointów governance,  
   - przykładowe wywołania curl / SDK.

**Akceptacja:**
- Nowe dokumenty są powiązane linkami z README.  
- README zawiera sekcję “Cost & Governance”.

---

## Faza 3 – Event Engine & Automations

**Cel:** Zaimplementować **realny** silnik eventów, który automatyzuje operacje (reflections, decay, alerts) i jest bezpieczny oraz przewidywalny.

### 3.1. Model danych i kolejki

**Zadania:**
1. Tabele:
   - `triggers` (reguły),  
   - `trigger_executions` (historia),  
   - `workflows`, `workflow_steps` (jeśli brak).  

2. Dodać kolejkę (Celery / Redis Streams) dla:
   - przetwarzania eventów,  
   - wykonywania akcji (async).  

3. Zdefiniować kontrakt eventu:
   - `tenant_id`, `project_id`, `event_type`, `payload`, `tags`, `timestamp`.

**Akceptacja:**
- Eventy mogą być puszczone przez API → lądują w kolejce.

---

### 3.2. Silnik reguł (rules engine)

**Zadania:**
1. Funkcja `evaluate_condition(condition_group, event)`:
   - obsługa operatorów: `AND`, `OR`, `NOT`.  
   - obsługa operatorów pól: `equals`, `greater_than`, `in`, `matches_regex`, itd.  

2. Funkcja `should_fire_trigger(trigger, event)`:
   - uwzględnia:
     - cooldown,  
     - `max_executions_per_hour`,  
     - priorytety.  

3. Funkcja `execute_actions(trigger, event)`:
   - obsługa akcji:
     - `generate_reflection`, `create_memory`, `send_notification`, itd.  
   - zapisy do `trigger_executions`.

**Akceptacja:**
- Testy jednostkowe pokrywające wszystkie operatory.  
- Test integracyjny:
  - wstaw trigger: *przy 50 nowych memories → reflection*  
  - generuj 50 memories, eventy `memory_created` → reflection jest tworzony, trigger się loguje.

---

### 3.3. Obsługa błędów i idempotencja

**Zadania:**
1. Retry:
   - dla każdej akcji `max_retries`, `retry_on_failure`.  
   - wykorzystywać mechanizm Celery (retry).  

2. Idempotencja:
   - `trigger_executions` z `execution_key`,  
   - unikać powtórek przy ponownych eventach.  

3. Metryki:
   - `rae_triggers_fired_total{trigger_id}`  
   - `rae_triggers_failed_total{trigger_id}`  
   - `rae_triggers_latency_seconds`.

**Akceptacja:**
- Test integracyjny: symulacja błędów → retries działają zgodnie z konfiguracją.

---

### 3.4. API + Dokumentacja

**Zadania:**
1. Uzupełnić/utwardzić:
   - `POST /v1/triggers/create`  
   - `GET /v1/triggers/list`  
   - `POST /v1/triggers/events/emit`  
   - `POST /v1/triggers/workflows/create`  
   - `POST /v1/triggers/executions`.  

2. Dokumentacja:
   - “Event & Automation Guide” w `docs/events_automation.md`:  
     - jak tworzyć reguły,  
     - jak testować,  
     - jak monitorować.

**Akceptacja:**
- Przynajmniej 3 kompletne przykłady workflow w dokumentacji.  

---

## Faza 4 – Dashboard Web UI (Monitoring & Observability)

**Cel:** Dostarczyć **gotowy dashboard** dla operatorów/architektów: zużycie pamięci, koszty, jakość, trigery, zdrowie systemu.

### 4.1. Backend – uzupełnienie API Dashboard

**Zadania:**
1. Upewnić się, że w `/v1/dashboard/*`:
   - istnieją endpointy:
     - `metrics`, `visualizations`, `health`, `activity`.  
   - zwracają dane na podstawie:
     - `cost_logs`, `memories`, `reflections`, `triggers`, `governance`.  

2. Dodać prosty “aggregator”:
   - ostatnie 24h:  
     - liczba memories, reflections,  
     - koszty,  
     - liczba fired triggers,  
     - zdrowie usług.

**Akceptacja:**
- Test: `test_dashboard_api_returns_valid_data`.

---

### 4.2. Frontend – aplikacja dashboardowa

**Zadania:**
1. W `tools/memory-dashboard`:
   - Next.js / React (lub FastAPI + Jinja jako MVP).  
   - widoki:
     - **Overview:**  
       - koszty dzienne/miesięczne per tenant,  
       - liczba wywołań LLM,  
       - heatmapa zapytań (może prosta tabela).  
     - **Memories & Reflections:**  
       - wykres czasowy,  
       - top projekty.  
     - **GraphRAG:**  
       - statystyki grafu (liczba węzłów, krawędzi, gęstość).  
     - **Events & Triggers:**  
       - ostatnie trigery, błędy, latency.  
     - **Health:**  
       - status usług (Postgres, Redis, Qdrant, ML Service, RAE API).

2. Autoryzacja:
   - prosty token / API key na początek,  
   - docelowo OIDC (w kolejnych wersjach).

**Akceptacja:**
- Dashboard odpala się lokalnie via `docker-compose up`.  
- Przynajmniej 2 grafy + 2 tabele są interaktywne.

---

## Faza 5 – SDK Python (Stabilne API dla Agentów)

**Cel:** Z SDK można komfortowo korzystać w agentach (Gemini CLI, Claude, własne frameworki), z pełnym wsparciem cost/governance i GraphRAG.

### 5.1. API Surface

**Zadania:**
1. Ustalić finalną publiczną powierzchnię SDK (w `rae_memory_sdk`):
   - `RAEClient` z metodami:
     - `create_memory`, `search_memories`,  
     - `generate_reflection`,  
     - `semantic_search`,  
     - `hybrid_search`,  
     - `graph_extract`, `graph_query`,  
     - `get_governance_stats`,  
     - `emit_event`,  
     - `get_dashboard_metrics`.  

2. Dodać:
   - wsparcie async (aiohttp / httpx),  
   - opcjonalny **retry + backoff** na poziomie SDK,  
   - prosty caching (np. dla statycznych zapytań).

**Akceptacja:**
- SDK ma pełne type hints.
- `pip install -e sdk/python/rae_memory_sdk` działa w CI (już jest w workflow).

---

### 5.2. Przykłady użycia dla agentów

**Zadania:**
1. W `examples/`:
   - `agent_with_rae_openai.py`  
   - `agent_with_rae_gemini.py`  
   - `agent_with_rae_local_llm.py`  

2. Pokazać:
   - tworzenie pamięci,  
   - query z `use_graph=True`,  
   - auto-reflection przez event triggers,  
   - odczyt cost/governance jako część raportu agenta.

**Akceptacja:**
- Przynajmniej jeden przykład jest testowany w CI (np. smoke test).

---

## Faza 6 – GraphRAG & Hybrid Search – Wydajność i Stabilność

**Cel:** GraphRAG działa stabilnie, szybko i przewidywalnie przy rosnącej skali.

### 6.1. Testy wydajności

**Zadania:**
1. Dodać `tests/performance/test_graphrag_perf.py`:
   - generacja syntetycznego grafu:  
     - 10k nodes, 50k edges,  
     - różne profile zapytań.  
   - pomiar:
     - czas BFS/DFS,  
     - czas hybrydowego search,  
     - maks. głębokość 3–5.  

2. Wyznaczyć budżety:
   - SLA:  
     - typowe zapytanie hybrydowe: < 500ms,  
     - traversal: < 100ms na poziom głębokości.

**Akceptacja:**
- Testy perf przechodzą lokalnie w sensownym czasie.
- Wyniki opisane w `docs/performance/GRAPHRAG_PERF.md`.

---

### 6.2. Optymalizacje SQL i indeksów

**Zadania:**
1. Przejrzeć `GraphRepository`:
   - użycie indeksów,  
   - query plan (EXPLAIN ANALYZE).  

2. W razie potrzeby:
   - dodać brakujące indeksy,  
   - zoptymalizować CTE,  
   - ograniczyć nadmiarowe joiny.

**Akceptacja:**
- Różnica czasu zapytań przed/po opisana w dokumencie perf.  

---

## Faza 7 – API Load & Chaos Testing

**Cel:** Udowodnić, że RAE wytrzyma ruch typowy dla produkcji, nie gubi transakcji i nie psuje spójności danych.

### 7.1. Load Testing

**Zadania:**
1. Przygotować `tools/load-tests` (np. Locust / K6):  
   - scenariusze:
     - burst memories + reflections,  
     - intensywny hybrid search,  
     - lawina eventów + trigery,  
     - heavy LLM + cost controller.  

2. Zintegrować z Makefile:
   - `make load-test` odpala lokalny scenariusz.

**Akceptacja:**
- System radzi sobie do zadanego progu (np. 100 RPS), bez błędów 5xx > X%.

---

### 7.2. Chaos Testing (opcjonalnie, ale zalecane)

**Zadania:**
1. Proste scenariusze:
   - zabijanie instancji ML Service,  
   - restart Qdrant,  
   - chwilowa niedostępność Postgresa.  

2. Sprawdzenie:
   - jak zachowuje się CostGuard,  
   - czy eventy nie znikają (retry),  
   - czy dashboard prawidłowo raportuje problemy.

**Akceptacja:**
- Raport w `docs/performance/CHAOS_TESTING.md` z opisem zachowania systemu.

---

## Faza 8 – Plugin Architecture & Integracje (v2.0+)

**Cel:** Przygotować RAE na łatwe rozszerzanie: nowe typy pamięci, nowe backendy, nowe akcje triggerów.

### 8.1. Warstwa pluginów

**Zadania:**
1. Zdefiniować kontrakt pluginu:
   - `MemoryBackend`,  
   - `GraphBackend`,  
   - `TriggerAction`,  
   - `PricingProvider`.  

2. Dodać rejestr pluginów (np. prosty entrypoints / configuracja w `.yaml`).

**Akceptacja:**
- Możliwość dodania nowego backendu (np. Neo4j) bez modyfikacji core.

---

### 8.2. Dokumentacja dla integratorów

**Zadania:**
1. `docs/plugins/PLUGIN_GUIDE.md`:
   - jak dodać nowy backend,  
   - jak dodać nowy typ akcji triggerów,  
   - jak opakować RAE w plugin do zewnętrznych agent frameworks.

**Akceptacja:**
- Przynajmniej jeden przykładowy plugin (np. custom TriggerAction).

---

## Meta – Jak tym zarządzać w praktyce

### A. Proponowana sekwencja PR-ów

1. `feat/cost-controller-runtime` (Faza 1).  
2. `feat/governance-real-stats` (Faza 2).  
3. `feat/events-engine` (Faza 3).  
4. `feat/dashboard-api-ui` (Faza 4).  
5. `feat/sdk-v2-agents` (Faza 5).  
6. `feat/graphrag-perf` (Faza 6).  
7. `feat/api-load-chaos-tests` (Faza 7).  
8. `feat/plugins-architecture` (Faza 8).  

### B. Definition of Done (globalne)

Każdy PR jest “done”, jeśli:

- ✅ Testy (unit + integration) przechodzą w CI.  
- ✅ Pokrycie w kluczowych modułach ≥ 80%.  
- ✅ Dodano metryki Prometheus (jeśli dotyczy).  
- ✅ Dodano krótką sekcję do odpowiedniego `.md` w `docs/`.  
- ✅ Zaktualizowano `CHANGELOG.md`.  
- ✅ Jest przynajmniej jeden przykład (curl/SDK/agent).

---

## Podsumowanie

Po zrealizowaniu wszystkich faz:

- **Cost Controller** będzie deterministyczny i audytowalny (USD + tokeny).  
- **Governance** będzie raportować realne dane, nie zera.  
- **Event Engine** stanie się rzeczywistym mózgiem automatyzacji wokół pamięci.  
- **Dashboard** umożliwi obserwowalność na poziomie SRE / architekta.  
- **SDK** będzie pierwszorzędnym narzędziem dla agentów (Gemini/Claude/OpenAI/Lokalne).  
- **GraphRAG** będzie skalować się na dziesiątki tysięcy węzłów.  
- **API** będzie przetestowane obciążeniowo i odporne na proste awarie.  
- **Plugin Architecture** otworzy drogę do ekosystemu rozszerzeń i integracji.

To jest poziom, na którym RAE może być pokazywany jako **wzorcowy silnik pamięci agentowej klasy enterprise**, zarówno w OSS, jak i w komercyjnych wdrożeniach.
