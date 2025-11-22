IMPLEMENTATION_REFINEMENT_PLAN.md
# RAE — Implementation Refinement Plan  
### (for Reflection Engine, Semantic Memory, Hybrid Search, Graph Repository, Evaluation Suite, Event Automations, Dashboard, API Client)

W projekcie RAE istnieje kilka modułów, które są **bardzo dobrze zaprojektowane koncepcyjnie**, ale **nieukończone lub niepełne w implementacji**.  
Ten dokument przedstawia **szczegółowy, techniczny plan doprowadzenia ich do stanu produkcyjnego**.

Zakres dokumentu obejmuje punkty:

3. Reflection Engine  
4. Semantic Memory  
5. Graph Repository  
6. Hybrid Search  
7. Evaluation Suite  
8. Event Triggers & Automations  
9. Memory Dashboard  
10. API Client Enhancements  

---

# 3. Reflection Engine — Full Implementation Plan

## 3.1. Braki w obecnej implementacji
- brak refleksji hierarchicznej (insight → meta-insight)
- brak scoringu wartości refleksji  
- brak klasyfikacji „rodzaju refleksji”  
- brak priorytetów refleksji  
- brak powiązań między refleksjami  
- ograniczona logika triggerów  
- brak caching / reuse of reflections  
- brak telemetry per reflection

---

## 3.2. Plan implementacyjny

### 3.2.1. Wprowadzić model ReflectionUnit
```json
{
  "id": "...",
  "type": ["insight", "analysis", "pattern", "meta"],
  "priority": 1–5,
  "score": float,
  "source_memories": [...],
  "timestamp": "...",
  "content": "...",
  "parent_reflection_id": null | uuid
}

3.2.2. Pipeline generowania refleksji

Pobierz powiązane memories

Oblicz embeddings

Zastosuj clustering heuristic (k-means / HDBSCAN)

Dla każdego klastra:

generuj insight

generuj meta-insight

Oblicz reflection.score:

novelty

importance

utility

model confidence

3.2.3. Wprowadzić ReflectionGraph

refleksje powiązane krawędziami:

supports

contradicts

refines

generalizes

3.2.4. Nowe endpointy:

/v1/reflections/generate

/v1/reflections/related

/v1/reflections/graph

3.2.5. Testy

testy per cluster

test scoringu

test consistency refleksji

test meta-insights

4. Semantic Memory — Full Implementation Plan
4.1. Braki

brak semantycznej klasyfikacji memories

brak dedykowanej struktury „knowledge nodes”

brak analizy ontologicznej

brak własnego semantic indexu

brak query-routing

brak TTL / LTM model

4.2. Plan implementacyjny
4.2.1. Nowy model SemanticNode
{
  "id": "...",
  "topic": "...",
  "canonical_form": "...",
  "definitions": [],
  "relations": {},
  "embedding": "vector",
  "created_at": "...",
  "updated_at": "..."
}

4.2.2. Semantic Extractor

LLM pipeline:

Extract topics

Extract canonical terms

Extract definitions and categories

Extract relations (X → related_to → Y)

Update graph + semantic index

4.2.3. Semantic Search

Trzy etapy:

topic → vector search

term normalization → canonicalization

semantic re-ranking

4.2.4. Semantic TTL

semantic_decay_time = 60 days

update policy:

jeśli node nie był używany X dni → „degrade priority”

jeśli node jest stale wzmacniany → „upgrade priority”

5. Graph Repository — Full Implementation Plan
5.1. Braki

brak cyklodetekcji

brak edge roles (cause → effect)

brak weighted graph

brak temporal graph traversal

brak graph snapshots

brak walidacji węzłów

5.2. Plan implementacyjny
5.2.1. Rozszerzenie modelu krawędzi
(source, target, role, weight, timestamp)

5.2.2. Cyklodetekcja

dodać funkcję:

detect_cycles(node_id)

DFS z markerami visited / recursion stack

5.2.3. Temporal Traversal

nowe parametry:

since, until

max_depth

time_decay

5.2.4. Graph Snapshots

Tabela:

graph_snapshots
  id
  created_at
  graph_jsonb

5.2.5. Testy:

BFS/DFS z wagami

cyklodetekcja

temporal traversal

6. Hybrid Search — Full Implementation Plan
6.1. Braki

brak ML re-ranking

brak dynamicznych wag

brak query decomposition

brak caching warstwy hybrydowej

brak explicable scoring breakdown

6.2. Plan implementacyjny
6.2.1. Wprowadzić Query Analyzer

Zwraca:

semantic intent

symbolic entities

keywords

query class: fact, instruction, concept, temporal

6.2.2. Dynamic Hybrid Weights

Funkcja:

α = semantic_confidence
β = symbolic_relevance
score = α * vector_score + β * graph_score

6.2.3. LLM Re-Ranker

bierz top 10 wyników z hybrydy

generuj ranking na podstawie:

informativeness

precision

contextual fit

6.2.4. Hybrid Cache

Klucz:

hash(query + tenant + timestamp_window)

6.2.5. Testy:

scoring stability

re-ranking reproducibility

7. Evaluation Suite — Full Implementation Plan
7.1. Braki

tylko golden set

brak testów długoterminowych

brak MRR per embedding model

brak drift detection

brak eval hybrydy

brak eval refleksji

7.2. Plan implementacyjny
7.2.1. Dodać: Large Evaluation Dataset

1000 memories

100 queries

multi-label answers

7.2.2. Nowe metryki:

MRR

NDCG

Recall@K

Precision@K

Reflection Precision

Semantic Coherence Score

Graph Traversal Accuracy

7.2.3. Drift Detection

porównanie embeddingów w czasie

alert gdy delta > threshold

8. Event Triggers & Automations
8.1. Braki

brak schedulerów

brak rules engine

brak event-driven processing

8.2. Plan implementacyjny
8.2.1. Wprowadzić moduł automations/

Zawiera:

rules/

triggers/

scheduler/

actions/

8.2.2. Typy triggerów

event trigger:

„new_memory”

„new_reflection”

„threshold_exceeded”

time trigger:

cron: hourly/daily/weekly

8.2.3. Actions

generate reflection

rebuild graph

re-evaluate semantic memory

compact embeddings

summarize timeline

9. Memory Dashboard — Full Implementation Plan
9.1. Braki

brak live updates

brak multi-tenant switching

brak grafu relacji

brak timeline refleksji

brak alertów budżetowych

9.2. Plan implementacyjny
9.2.1. Live Updates (WebSockets)

kanały:

memory_changes

reflection_updates

graph_updates

9.2.2. Nowe widoki dashboardu:

Semantic Map

Reflection Tree

Budget Heatmap

Graph Explorer (interactive)

Hybrid Search Breakdown (explainable AI)

9.2.3. Alerty:

płynne powiadomienia o przekroczeniu budżetu

wyjątkowo duże odpytanie hybrydowe

wykrycie memory drift

10. API Client — Full Implementation Plan
10.1. Braki

brak retry logic

brak circuit-breakera

brak integracji z MCP

brak unified error schema

10.2. Plan implementacyjny
10.2.1. Retry + Exponential Backoff
retry_count = 3
initial_delay = 0.25

10.2.2. Circuit Breaker

otwiera się po 5 błędach / 60 sek.

automatycznie resetuje po cooldownie

10.2.3. MCP Integration

from rae_mcp import MCPClient

adapter:

send_tool_request()

parse_mcp_response()

bridge_to_rae_api()

10.2.4. Unified Error Schema
{
  "code": "RAE_CLIENT_ERROR",
  "message": "",
  "details": {}
}
