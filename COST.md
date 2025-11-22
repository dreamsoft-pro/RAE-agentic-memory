COST_CONTROLLER_REFINEMENT_PLAN.md
Wersja: 1.0 — Specyfikacja wzorcowej implementacji kontroli kosztów i zużycia tokenów w RAE
1. Wprowadzenie

Celem tego dokumentu jest dopracowanie warstwy Cost Controller w RAE tak, aby była:

kompletna – nalicza koszt i tokeny w każdym wywołaniu,

deterministyczna – nie ma możliwości uzyskania 0.0 USD,

przewidywalna – budżety działają identycznie dla OpenAI, Anthropic, Gemini i modeli lokalnych,

osadzona w runtime – realne liczenie, realne limity, realne raporty,

obserwowalna – Prometheus, event logs, audyt, API do statystyk,

rozszerzalna – nowe modele, niestandardowe koszty, kontekst cache, dynamiczne ceny, multi-tenant.

Po wdrożeniu tego planu warstwa kosztów w RAE będzie mogła być przedstawiona jako wzorcowe rozwiązanie OSS.

2. Problemy, które trzeba rozwiązać

Aktualna implementacja ma dobrą architekturę, ale kluczowe elementy są niepełne:

❌ total_estimate zawsze 0

LLM nie wylicza kosztu, a Cost Guard ufa temu polu.

❌ BudgetService nie otrzymuje realnych kosztów

increment_usage(cost_usd=0) → budżety się „nigdy nie kończą”.

❌ Brakuje agregacji tokenów

GovernanceService zwraca zawsze 0 tokenów i 0 USD.

❌ Cost avoidance (cache savings) istnieje tylko w dokumentacji
❌ Brak realnego cost_logs → stats generują dane zerowe.
❌ Brak twardych limitów tokenowych

(W budgetach są pola USD, ale logicznie potrzebny jest także limit tokenów.)

3. Architektura docelowa (wzorowa)

Poniżej idealny przepływ kosztów:

 [Client API]
      │  
      ▼
 [CostGuardMiddleware] ───► check_budget(budget_id)
      │
      ▼
 [LLM Client]
      │  generates:
      │     - input_tokens
      │     - output_tokens
      │     - provider_model
      ▼
 [calculate_cost()]  ◄────— cennik providerów
      │
      ▼
 [CostGuardMiddleware]
      │ update:
      │    - daily_usage_usd
      │    - monthly_usage_usd
      │    - daily_tokens
      │    - monthly_tokens
      ▼
 [BudgetService.increment_usage()]
      │
      ▼
 [cost_logs table]
      │
      ▼
 [GovernanceService.get_tenant_stats()]


Dodatkowa gałąź:

 [Context Cache]
      │ hit/miss
      ▼
 [cache_cost_saved_usd = hits × avg_cost ]

4. Rekomendowane modyfikacje kodu (konkrety do implementacji)
4.1. LLM Client → musi wyliczać tokeny + koszt
Do zrobienia:

W każdym wywołaniu LLM (OpenAI/Gemini/Anthropic/lokalny):

pobrać liczbę tokenów z odpowiedzi providera,

jeżeli provider ich nie zwraca — policzyć heurystyką (tiktoken, sentencepiece),

wywołać:

total_estimate = calculate_cost(
    model=model_name,
    input_tokens=input_tokens,
    output_tokens=output_tokens
)

Wynik musi trafić do:

CostInfo

AgentResponse.cost.total_estimate

4.2. CostGuardMiddleware → obowiązkowe liczenie (nawet jeśli LLM poda 0)

Pseudokod nowej logiki:

if response.cost.total_estimate == 0:
    response.cost.total_estimate = calculate_cost(
        model=response.model,
        input_tokens=response.cost.input_tokens,
        output_tokens=response.cost.output_tokens,
    )

4.3. BudgetService → uzupełnienie pól
Nowe pola budżetu:

daily_tokens_limit

monthly_tokens_limit

daily_tokens_used

monthly_tokens_used

last_token_update_at

Aktualizacja usage:
budget.daily_usage_usd += cost
budget.monthly_usage_usd += cost

budget.daily_tokens_used += input_tokens + output_tokens
budget.monthly_tokens_used += input_tokens + output_tokens

4.4. cost_logs – pełna implementacja

Log powinien zawierać:

pole	opis
id	UUID
tenant_id	właściciel
model	np. gpt-4o-mini
input_tokens	int
output_tokens	int
total_cost_usd	float
operation	"query" / "reflection" / "embedding"
timestamp	datetime
4.5. GovernanceService – obsługa prawdziwych danych
Implementacja _count_tokens_used:
SELECT SUM(input_tokens + output_tokens)
FROM cost_logs
WHERE tenant_id = :id AND timestamp > NOW() - interval ':period_days days';

Implementacja _estimate_llm_cost:
SELECT SUM(total_cost_usd)
FROM cost_logs
WHERE tenant_id = :id AND timestamp > NOW() - interval ':period_days days';

4.6. Context Cache – realne wyliczenie „oszczędności”
Metryka:
cache_cost_saved_usd = cache_hits * avg_cost_per_request

avg_cost_per_request:

jeśli jest cost_logs: avg(total_cost_usd)

jeśli nie ma: fallback: default_estimated_cost z ENV

5. Testy – pełne pokrycie
5.1. Testy jednostkowe
Test	Cel
test_calculate_cost_openai()	poprawne ceny gor/1M
test_calculate_cost_anthropic()	jw
test_costguard_forces_cost_value()	nawet gdy provider zwróci 0
test_budget_exceeded_usd()	odrzucenie nadmiaru
test_budget_exceeded_tokens()	limit tokenów
test_increment_usage_logs_cost()	wpisy cost_logs
5.2. Testy integracyjne (testcontainers)
Test	Cel
LLM → CostGuard → DB	aktualizacja cost_logs + budgets
GovernanceService	poprawna agregacja tokenów i USD
Cache hit → cache_cost_saved_usd	poprawny wzrost metryki
6. Obserwowalność (Prometheus + logs)
6.1. Prometheus metrics
rae_cost_llm_total_usd
rae_cost_llm_daily_usd
rae_cost_llm_monthly_usd
rae_cost_llm_tokens_used
rae_cost_cache_saved_usd
rae_cost_budget_rejections_total
rae_cost_llm_calls_total
rae_cost_tokens_per_call_histogram

6.2. Logi audytowe

Każde wywołanie LLM:

[COST] tenant=abc model=gpt-4o-mini in=431 out=102 cost=0.0042 USD usage(usd)=0.012 usage(tokens)=533


Każde przekroczenie budżetu:

[COST-BLOCK] tenant=abc exceeded daily_usd_limit (12.00 / 10.00)

7. Dokumentacja – ujednolicenie

Nowy dokument:

docs/cost-controller.md (rozszerzona wersja)

Zawiera:

architekturę

przepływ requestów

jak liczone są tokeny

jak liczone są koszty

przykłady cenników providerów

jak działają limity

jak działa context cache

jak działają statystyki i governance

jak debugować błędy

8. Checklist finalna (przed oznaczeniem jako wzorcowe)
⚙ Runtime

 total_estimate liczone zawsze

 tokeny liczone zawsze

 budżety uaktualniane prawidłowo

 limit USD i limit tokenów w pełni działa

🗃 Storage

 kompletne cost_logs

 agregacja w governance

📊 Observability

 metryki Prometheus

 logi audytowe

 dashboard grafana (opcjonalnie)

📘 Dokumentacja

 odświeżone cost-controller.md

 sekcja w README

 przykłady API

🧪 Testy

 unittesty pricing

 unittesty BudgetService

 integracyjne: LLM → CostGuard → DB

 governance stats

9. Podsumowanie

Po wprowadzeniu wszystkich punktów:

✔ Budżety w USD i tokenach będą działać deterministycznie
✔ Koszty będą realnie liczone, niezależnie od providera
✔ Każde wywołanie LLM będzie zapisane w cost_logs
✔ Governance będzie zwracać prawdziwe statystyki
✔ System będzie w pełni obserwowalny (metrics + logs)
✔ Będziesz mieć wzorcową implementację kontroli kosztów, którą można stosować w firmie, OSS, projektach akademickich i u klientów.