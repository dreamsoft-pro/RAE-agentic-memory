# RAE_IMPROVEMENT_PLAN_v2_ENTERPRISE.md  
**Cel:** Doprowadzić RAE – Reflective Agentic Memory Engine – do w pełni „Enterprise-Grade” jakości, łącząc:  
- aktualny stan projektu (GraphRAG, DI, CI/CD, logging, docs),  
- wcześniejsze rekomendacje dot. testów, spójności wersji, cost/governance, event engine, dashboard, OSS onboarding,  
- **nowe wymagania enterprise**:  
  - **OpenTelemetry (Distributed Tracing)**  
  - **Helm Chart (Kubernetes-ready deployment)**  
  - **Rate Limiting (FastAPI middleware)**  

Źródło analizy: pełny zrzut repozytorium projektu. :contentReference[oaicite:0]{index=0}  

---

# 0. STAN OBECNY – SYNTETYCZNA DIAGNOZA

### ✔ Co już jest na bardzo wysokim poziomie
- **Architektura:** DI, modularyzacja, GraphRAG, Hybrid Search, Reflection Engine, Events, Evaluation, Dashboard API.  
- **CI/CD:** matrix tests 3×Python, integration with Postgres/Redis/Qdrant, security scans, docker build+push.  
- **Logging:** pełna konfiguracja structlog + JSON + różne poziomy logowania dla aplikacji i bibliotek.  
- **Dokumentacja:** obszerne API v2.0, security checklist, cost controller plan, implementation plan.  

### ❗ Kluczowe problemy nadal do naprawy
- **Testy:** realnie ~58% coverage, niespójności w raportach, testy legacy vs nowe API.  
- **Dokumentacja:** niespójność wersjonowania (1.x vs 2.x), stare endpointy MCP w planach/examples.  
- **Runtime:** cost controller i governance nie są w pełni wdrożone (istnieje doskonały plan, nie finalna implementacja).  
- **Event Engine:** brak pełnej implementacji retry, cooldown, prioritetów, itd.  
- **Dashboard:** API jest, UI w fazie początkowej.  

Dodajemy teraz **OpenTelemetry**, **Helm Chart** i **Rate Limiting** jako obowiązkowy element wersji enterprise.

---

# 1. PRIORYTET 1 – TESTY + SPÓJNOŚĆ DOKUMENTACJI

## 1.1. TESTING_STATUS.md – jedyne źródło prawdy
**Zadania:**
- Utworzyć `docs/TESTING_STATUS.md` zawierający:  
  - liczbę testów unit/integration/e2e,  
  - coverage globalne i per moduł,  
  - status: prod-ready / beta / lab,  
  - ostatnia aktualizacja: data + commit SHA.

**Definition of Done:**  
Wszystkie dokumenty odsyłają do tego jednego miejsca.

---

## 1.2. Naprawa testów: FAIL/ERROR/legacy
**Zadania:**
1. Zeskanować wszystkie testy → oznaczyć:
   - (a) realny bug,  
   - (b) test przestarzały po refaktorze API,  
   - (c) flaky.  
2. Dla (b) przepisać test pod aktualne API (`/v1/memories`, `/v1/search/hybrid`, `/v1/graph`).  
3. Dla (c) wyeliminować timing dependency, dołożyć testcontainers.

**Definition of Done:**  
`pytest` na CI: 0× FAIL, 0× ERROR.

---

## 1.3. Podniesienie coverage z ~58% → 80%+ w modułach kluczowych
Moduły do objęcia testami obowiązkowo:

- memory_service  
- reflection_engine  
- semantic_service  
- graph_extraction  
- hybrid_search  
- cost_guard  
- budget_service  
- evaluation_service (jeśli używany)

**Definition of Done:**  
Coverage w tych modułach ≥ 80%, globalnie ≥ 75%.

---

# 2. PRIORYTET 2 – WERSJONOWANIE + CZYSTA DOKUMENTACJA

## 2.1. Jedna wersja: 1.2.0-enterprise **lub** 2.0.0
**Zadania:**
- Zdecydować: stable release = `1.2.0-enterprise` lub `2.0.0`.  
- Uporządkować wszystkie pliki zawierające numery wersji.  
- Dodać `docs/VERSION_MATRIX.md`.

---

## 2.2. Usunięcie przestarzałych endpointów MCP z docs/README/examples
**Zadania:**
- Wyszukać `/memory/add`, `/memory/store`, stare payloady, stare schematy MCP.  
- Przenieść do `docs/legacy/mcp.md` albo usunąć.  
- Zaktualizować przykłady SDK.

---

# 3. PRIORYTET 3 – COST CONTROLLER + GOVERNANCE (RUNTIME)

## 3.1. Cost Controller – implementacja planu
**Zadania:**
- Dodać migracje dla `cost_logs`.  
- Wprowadzić pricing map dla providerów i modeli.  
- Uzupełnić klientów LLM o token usage i total_estimate.  
- Dokończyć CostGuardMiddleware → blokady limitów tokenów i USD.  
- Dodać Prometheus metrics.

---

## 3.2. Governance – oparte o realne cost_logs
**Zadania:**
- Implementacje metod `_count_tokens_used`, `_estimate_llm_cost`.  
- Endpointy: `/v1/governance/tenant/...` i `/overview`.  
- Testy integracyjne: symulacja kosztów → poprawne agregacje.

---

# 4. PRIORYTET 4 – EVENT ENGINE + DASHBOARD

## 4.1. Event Engine – stabilny subset
**Zakres mandatory:**
- automatyczna reflection przy X nowych memories,  
- alert przy niskiej jakości eval,  
- trigger przy przekroczeniu budżetu.

**Zadania:**  
- Implementacja retry, cooldown, idempotencji.  
- Audyt + metryki Prometheus.

---

## 4.2. Dashboard – MVP
**Zadania:**
- Panel Overview (memories/reflections/koszty 24h).  
- Panel GraphRAG (nodes/edges counts).  
- Panel Event Engine (ostatnie trigery + błędy).  
- UI Next.js w `tools/memory-dashboard`.

---

# 5. PRIORYTET 5 – UX KONTRYBUTORÓW (OSS)

## 5.1. CONTRIBUTING.md – onboarding
**Zadania:**
- Sekcja: good first issues,  
- Linki do TESTING_STATUS.md, VERSION_MATRIX.md, cost-controller docs.  
- „How to run integration tests locally” – z testcontainers.

---

# 6. PRIORYTET 6 – RELEASE ENGINEERING

## 6.1. Gałęzie i CI
- `main`: tylko releasy,  
- `develop`: bieżąca praca,  
- feature branches: `feat/...`.

## 6.2. Release Notes
- Sekcje: production-ready, beta, deprecated, breaking changes.

---

# 7. NOWE PUNKTY ENTERPRISE

# 7.1. OpenTelemetry (Distributed Tracing)

## 7.1.1. Wprowadzenie OTel do API
**Zadania:**
- Zainstalować:
opentelemetry-sdk
opentelemetry-exporter-otlp
opentelemetry-instrumentation-fastapi
opentelemetry-instrumentation-logging
opentelemetry-instrumentation-requests

markdown
Skopiuj kod
- Dodać `opentelemetry_config.py`:  
- exporter OTLP → Jaeger/Tempo/Elastic APM,  
- propagacja W3C TraceContext.  
- Owinąć FastAPI w tracing middleware:
```python
FastAPIInstrumentor().instrument_app(app)
7.1.2. Tracing Celery
Zadania:

opentelemetry-instrumentation-celery

dodanie traceparent/trace-id do zadań Celery, aby łańcuch:
API → Event Trigger → Celery Task → ML Service → DB
był widoczny jako jedna transakcja.

7.1.3. Tracing ML Service i Postgresa
Zadania:

opentelemetry-instrumentation-psycopg2

opentelemetry-instrumentation-asyncpg

opentelemetry-instrumentation-httpx

Widoczność: koszt tokenów i nazwa modelu jako custom attributes.

Definition of Done:
W Jaegerze/Tempo pojawia się pełny trace requestu od HTTP aż po odpowiedź modelu i zapis w cost_logs.

7.2. Helm Chart (deploy K8s)
7.2.1. Struktura charts/rae/
Zadania:

Dodać katalog: charts/rae/

W środku:

Chart.yaml

values.yaml

templates/deployment.yaml

templates/service.yaml

templates/configmap.yaml

templates/ingress.yaml

templates/secrets.yaml

templates/hpa.yaml

7.2.2. Funkcje
Deployment dla:

API,

Celery worker,

Celery beat,

ML Service.

Auto-scaling CPU/memory.

Gotowość i żywotność (readinessProbe/livenessProbe).

Sekrety: API keys, DB, Redis, Qdrant – w sealed-secrets lub external-secrets.

Definition of Done:
helm install rae charts/rae/ uruchamia RAE na Minikube lub dowolnym K8s.

7.3. Rate Limiting (SlowAPI / Starlette-Limiter)
7.3.1. Instalacja
nginx
Skopiuj kod
pip install slowapi
lub:

nginx
Skopiuj kod
pip install fastapi-limiter
7.3.2. Konfiguracja
Zadania:

W dependencies.py dodać Redis jako store dla limitów.

W main.py dodać middleware:

python
Skopiuj kod
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_handler)
Dodać limity:

/v1/memories/create: 30/min per tenant,

/v1/search/hybrid: 60/min per tenant,

/v1/ml/generate: 20/min per tenant.

7.3.3. Rate limiting a tenant_id
Zadania:

key_func = tenant_id if dostępny, fallback = IP

custom header: X-RateLimit-Remaining, X-RateLimit-Reset.

Definition of Done:
Przy przeciążeniu endpointów system zwraca 429 Too Many Requests z jasną informacją o limicie.

8. KOLEJNOŚĆ REALIZACJI
Testy + spójność docs

Cost Controller + Governance

Event Engine subset

Dashboard MVP

OpenTelemetry

Rate Limiting

Helm Chart

Release 1.2.0-enterprise (lub 2.0.0)

9. PODSUMOWANIE
Po wdrożeniu wszystkich punktów projekt będzie posiadał:

Distributed Tracing (OpenTelemetry) → pełna obserwowalność API → Celery → ML → Postgres.

Helm Chart → możliwość automatycznego wdrożenia w K8s jednym poleceniem.

Rate Limiting → odporność przy publicznym wystawieniu API.

Pełne testy, spójne dokumenty, jednoznaczne wersjonowanie.

Produkcyjny Cost Controller i Governance.

Stabilny mini-Event Engine i działający Dashboard.

Profesjonalny onboarding dla kontrybutorów OSS.