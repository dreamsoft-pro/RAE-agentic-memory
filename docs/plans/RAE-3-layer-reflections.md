RAE_REFLECTIVE_ARCHITECTURE_V3_SPEC.md
Status

Implementation Specification
Target: Laptop + Mobile compatible
Mode: Hard Frames compatible
Scope: 3-Layer Reflective Architecture (QFT-Inspired, Engineering Simplified)

1. Cel dokumentu

Celem jest implementacja trójwarstwowej architektury refleksyjnej w RAE przy zachowaniu:

minimalnego, czystego Core

pełnej deterministyczności

zgodności z Hard Frames

działania na urządzeniach o ograniczonych zasobach

modularności (możliwość wyłączenia warstw)

Architektura ma umożliwiać:

blokowanie konfabulacji

ocenę jakości strategii

wykrywanie anomalii strukturalnych

detekcję powstawania nowych idei (Idea Field)

analizę spójności między skalami danych

2. Zasady nadrzędne

Core nie może zostać obciążony.

Refleksja jest osobnym modułem.

Hard Frames może wymusić blokadę odpowiedzi.

Każda warstwa generuje ustandaryzowany JSON wynikowy.

Wszystko działa lokalnie.

Brak automodyfikacji zasad systemu.

Brak generowania narracji w warstwie L3 — tylko raporty strukturalne.

3. Architektura logiczna
Core
  ├── Memory
  ├── Retrieval
  ├── Contracts
  └── Provenance

Reflection Module
  ├── L1 Operational Reflection
  ├── L2 Structural Reflection
  └── L3 Meta-Field Reflection

Każda warstwa ma 3 wyspecjalizowanych agentów.

Łącznie: 9 agentów refleksyjnych.

4. L1 – Operational Reflection
Cel

Ocena poprawności odpowiedzi względem źródeł i kontraktów.

Agenci
L1-A EvidenceVerifier

Oblicza coverage_ratio

Sprawdza czy twierdzenia mają źródła

Weryfikuje istnienie danych

L1-B ContractEnforcer

Egzekwuje Hard Frames

Sprawdza domenę danych

Sprawdza zgodność z politykami

L1-C UncertaintyEstimator

Określa poziom niepewności

Wskazuje brakujące dane

Output L1
{
  "block": false,
  "coverage_ratio": 0.82,
  "contract_status": "ok",
  "uncertainty_level": 0.15,
  "missing_sources": [],
  "trace_id": "uuid"
}

Jeśli:

coverage_ratio < threshold

contract_status != ok

uncertainty_level > max_allowed

→ block = true

5. L2 – Structural Reflection
Cel

Ocena jakości strategii wyszukiwania i struktury rozwiązania.

Agenci
L2-A RetrievalAnalyzer

Ocena poprawności doboru źródeł

Wykrywanie pominiętych źródeł

L2-B PatternDetector

Wykrywanie powtarzalnych wzorców

Budowa insight_candidates (bez narracji)

L2-C CostOptimizer

Pomiar kosztów (tokeny, zapytania, czas)

Sugestie optymalizacyjne

Output L2
{
  "retrieval_quality": 0.74,
  "missed_sources": ["machine_log_18_02"],
  "insight_candidates": [
    {"pattern": "repeated_speed_drop_monday", "confidence": 0.67}
  ],
  "optimization_suggestion": "increase_top_k"
}

L2 nie blokuje odpowiedzi, ale może generować ostrzeżenia.

6. L3 – Meta-Field Reflection (QFT-Inspired Engineering)
Cel

Ocena stabilności strukturalnej systemu.

Fundament: IdeaField

Dynamiczny graf:

Node = pojęcie
Edge = współwystępowanie
Weight = intensywność relacji
Time dimension = znacznik czasowy
Domain = kontekst

Graf przechowywany jako struktura sparse.

L3-A FieldDensityMonitor
Funkcja

Wykrywa:

wzrost zagęszczenia grafu

powstawanie nowych klastrów

nowe mosty między domenami

Metryki

density_delta

cluster_growth_rate

cross_domain_edge_growth

L3-B RenormalizationEngine
Funkcja

Sprawdza spójność między skalami danych.

Przykład skal

11s

5min

1h

zmiana

dzień

Testy

weighted aggregation consistency

scale invariance tolerance

sampling anomaly detection

L3-C SymmetryAndAnomalyDetector
Symetrie = twarde zasady

brak twierdzeń bez evidence

brak mieszania domen bez mapowania

brak konfliktu definicji KPI

brak narracji bez źródeł

Wykrywa

policy_violation

domain_leakage

structural_contradiction

intent_drift

Output L3
{
  "field_stability_index": 0.81,
  "emerging_clusters": ["local_first + grant_strategy"],
  "scale_inconsistencies": [],
  "anomalies": [
    {"type": "domain_leakage", "severity": 0.42}
  ]
}
7. Field Stability Index

Prosty wzór początkowy:

FSI = 1
      - anomaly_severity_weighted
      - scale_inconsistency_penalty
      + density_coherence_bonus

Zakres: 0 – 1

8. Hard Frames Integracja

Jeśli Hard Frames aktywny:

Odpowiedź blokowana gdy:

L1.block = true

L3.anomalies.severity > critical_threshold

scale_inconsistency > tolerance

9. Tryby działania
Minimal (Mobile)

L1 aktywne

L2 ograniczone

L3 wyłączone

Standard (Laptop)

L1 pełne

L2 pełne

L3 batch co X godzin

Advanced

L3 aktywne przy zapytaniach strategicznych

10. API Kontrakt między warstwami

Każda warstwa otrzymuje:

{
  "query_id": "...",
  "retrieved_sources": [],
  "answer_draft": "...",
  "metadata": {}
}

Każda warstwa zwraca JSON zgodny ze swoją specyfikacją.

Koordynator refleksji agreguje wyniki.

11. Bezpieczeństwo

Wszystko lokalne

Brak eksportu grafu

Brak uczenia modelu na danych

Pełny audit trail

Feature flag dla każdej warstwy

12. Roadmapa implementacji
Etap 1

L1 pełne

L2 podstawowe

Prosty IdeaField

Etap 2

RenormalizationEngine

SymmetryAndAnomalyDetector

Etap 3

Stabilny Field Stability Index

Insight Radar

13. Filozofia końcowa

Core:

mały

czysty

deterministyczny

Refleksja:

3 warstwy

9 agentów

QFT-inspired tylko strukturalnie

brak metafizyki

pełna audytowalność