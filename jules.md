Task Name:

RAE – Agentic Memory: Implement Core Features v0.1 → v0.3

Objective:

Doprowadzić repozytorium RAE-agentic-memory do funkcjonalnego, testowalnego i gotowego do użycia stanu open-source quality.
Jules ma zrealizować zadania w kodzie, zgodnie z istniejącą strukturą repozytorium:

apps/
  memory-api/
  reranker-service/
cli/
docs/
infra/
eval/


Efekt końcowy: działający lokalnie system pamięci agentów z API /memory/* oraz /agent/execute.

📌 High-Level Goals

Ukończyć API pamięci (Memory API v1)

pełne modele (Pydantic)

implementacja /memory/add, /memory/query, /memory/timeline

Qdrant dense+sparse hybrid search

pełna obsługa tenant_id + RLS

testy jednostkowe

Ukończyć Agent Bridge v1 (/agent/execute)

pipeline retrieve → rerank → prompt build → LLM call → reflection hook

raportowanie used_memories

koszt operacji (CostInfo)

Ukończyć Reranker Service v1

API /rerank

minimalna implementacja rerankingu

testy

Uzupełnić infra i Docker Compose

kontenery: memory-api, reranker-service, postgres, qdrant, grafana, prometheus

healthchecks

działające środowisko w 1 komendzie

Rozwinąć eval

rozszerzyć goldenset

wprowadzić metryki jakości

dodać eval do CI

Ukończyć CLI

memory_add, memory_query, agent_ask – w pełni działające

obsługa JSON i STDIN

📌 System Requirements for Jules
Jules MUST:

zachować istniejącą strukturę repozytorium, ścieżki i nazw plików,

wypełniać wszystkie miejsca oznaczone ...,

nie zmieniać schematów baz danych ani istniejących kolekcji Qdrant (chyba że jest to oczywista poprawka),

generować działający kod FastAPI, Pydantic, Qdrant, Postgres,

stosować styl Pythona: black + ruff + mypy-friendly,

nie generować kodu eksperymentalnego lub pół-funkcjonalnego.

Jules MUST test:

działanie /memory/add

działanie /memory/query

filtrowanie tenant_id

agent pipeline

reranker identity behavior

Jules MUST NOT:

usuwać lub ingerować w pliki nieobjęte zadaniem,

zmieniać licencji projektu,

zmieniać nazwy folderów, endpointów ani podstawowych komponentów.

📌 Detailed Tasks for Jules
1. Memory API Completion (mandatory)
Pliki:

apps/memory-api/models.py

apps/memory-api/routers/memory.py

apps/memory-api/services/qdrant_client.py

Zadania:
1.1. Dokończyć modele Pydantic

uzupełnić wszystkie klasy zawierające ...

dodać brakujące pola z docs/OPENAPI.md

zapewnić zgodność typów (Optional[], List[], datetime, itp.)

1.2. /memory/add

pełna implementacja:

PII scrub (stub)

insert into Postgres (memories)

embedding → Qdrant payload:

dense vector

sparse vector (jeśli obsługiwane, dopuszczalny stub)

zwrócenie memory_id

1.3. /memory/query

obsługa:

tenant_id filter

memory_type

tags

implementacja:

hybrid_search() w Qdrant

sortowanie wyników

budowa QueryResponse

1.4. /memory/timeline

timeline z tabeli memories

sortowanie po created_at

filtrowanie po tenant_id

2. Agent Bridge Implementation
Plik:

apps/memory-api/routers/agent.py

Zadania:
2.1. Dokończyć AgentExecuteRequest i AgentExecuteResponse

zgodnie z definicjami Pydantic i OpenAPI

2.2. Pipeline /agent/execute

koszt – użycie @cost_guard

retrieve: wewnętrzne wywołanie query

rerank: zapytanie do reranker-service

build prompt

call LLM (OpenAI/Gemini/Ollama – abstrahowane)

reflection hook (stub)

zwrócenie odpowiedzi + użytych memories

3. Reranker Service v1
Plik:

apps/reranker-service/main.py

Zadania:

dokończyć modele Pydantic

implementacja rerankingu:

v1: sortowanie po score lub identity

przygotować miejsce na model w przyszłości

dodać testy jednostkowe

4. Infra & Docker Compose Completion
Pliki:

infra/docker-compose.yml

infra/grafana/

infra/prometheus/

Zadania:

dokończyć brakujące sekcje (...)

dodać kontenery:

memory-api

reranker-service

healthchecks

zapewnić poprawne linkowanie do Qdrant, Postgres

sprawdzić że docker-compose up tworzy w całości działający system

5. Eval Suite
Pliki:

eval/run_eval.py

eval/goldenset.yaml

Zadania:

uzupełnić eval o dodatkowe scenariusze

dodać scoring:

hit_rate@k

MRR

dodać README jak używać eval

zapewnić zgodność z działającym API

6. CLI Completion
Plik:

cli/gemini-cli/main.py

Zadania:

wypełnić ...

zapewnić obsługę JSON w STDIN:

rae memory-add --file payload.json

rae memory-query "What is the project about?"

rae agent-ask "Refactor this function"

📌 Acceptance Criteria

Projekt ma być ukończony, jeśli:

wszystkie modele Pydantic są kompletne,

wszystkie endpointy działają i są pokryte testami,

działająca komenda:

docker-compose up


pamięć można dodać:

rae memory-add --text "hello world"


pamięć można odczytać:

rae memory-query "hello"


agent działający:

rae agent-ask "podsumuj pamięci"


eval uruchamia się i zwraca wynik

brak miejsc z ... w kodzie projektu

📌 Final Constraints

Jules musi pisać kod:

idiomatyczny Python 3.11+

zgodny z FastAPI + Pydantic v2

zrozumiały, modularny, testowalny

respektujący strukturę repozytorium

nie wprowadzać własnych frameworków

📌 BONUS (optional if time allows)

jeśli Jules skończy szybciej:

Dodać middleware dla request logging.

Dodać prostą stronę /docs z opisem API.

Dodać pierwszy „Reflection Stub” do RM.
