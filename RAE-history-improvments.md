# RAE History of Memory Control & Benchmark Evolution

This document tracks the actual technical methods implemented in RAE (Reflective Agentic Memory) to control memory retrieval and quality, correlated with real benchmark results from the git history.

## 🕰️ Chronology of Improvements

### 1. Era 0: Baseline Retrieval (v1.0)
- **Date:** 2025-12-07
- **Method:** Initial dual-engine implementation (Naive Vector + Lexical retrieval).
- **Core Logic:** Simple top-k merging without advanced weighting.
- **Benchmark (Academic Lite):**
    - **MRR:** 1.0000
    - **Query Latency:** 9.86ms
- **Commit:** Baseline implementation of `benchmarking/scripts/run_benchmark.py`.

### 2. Era 1: Fusion & Contracts (v2.0)
- **Date:** 2025-12-17 to 2025-12-31
- **Methods:**
    - **Reciprocal Rank Fusion (RRF):** Implemented to stabilize results when LLM-based reranking is disabled.
    - **Memory Contract Validation:** Strict schema enforcement at ingestion to prevent "data drift".
- **Commit:** `c0753799` (feat(math): implement Reciprocal Rank Fusion (RRF)).
- **Benchmark (Industrial Small):**
    - **MRR:** ~0.52 (Initial baseline for messy industrial logs).

### 3. Era 2: Bayesian Self-Improvement (System 2.x)
- **Date:** 2026-01-18
- **Method:** **Bayesian Policy Tuner & Thompson Sampling**.
- **Core Logic:** Dynamic scoring weight optimization based on explicit feedback loops. Dirichlet-Multinomial priors used to shift engine weights.
- **Commit:** `411303db` (feat(math): implement Phase 4 Bayesian Self-improvement loop).
- **Results:** Achieved **80% confidence shift** in weighting preferences during live trials on Node 1.

### 4. Era 3: Autonomous Math & Szubar (System 3.0 - 3.4)
- **Date:** 2026-01-26 to 2026-01-30
- **Methods:**
    - **Math-First Strategy:** Prioritizing lexical precision for structured queries.
    - **Szubar Mode:** Autonomous reflection injection where failed queries (MISS) trigger graph-neighbor induction.
    - **Adaptive Determinism:** Sliding window Bandit for weight modulation to handle non-stationary data.
- **Commits:**
    - `f6c29eec` (System 3.0: Math-First and Szubar Learning).
    - `a4f8e1f2` (System 3.4: Adaptive Determinism and Multi-Vector).
- **Benchmark (Industrial Large):**
    - **MRR:** **0.8172** (Target > 0.80 achieved).
- **Benchmark (Academic Lite):** **1.0000**.

### 5. Era 4: Deterministic Logic & Resonance (System 4.0 - 6.5)
- **Date:** 2026-02-07
- **Methods:**
    - **LogicGateway:** Replaced continuous weights with deterministic profiles (`LEXICAL_FIRST`, `CONSENSUS`).
    - **Semantic Resonance:** Query Entropy calculation to detect "ID-like" vs "Semantic" queries.
    - **Safe Early Exit:** If specificity is high (< 5 results in primary engine), terminate search early to save compute.
- **Commits:**
    - `9ec9671f` (System 4.0: Logic-based Math Core).
    - `7e50fd73` (System 6.5: Hybrid Resilience & Semantic Resonance).
- **Benchmark (Industrial Small):**
    - **MRR:** **0.7583** (System 6.3) -> **0.7417** (System 6.5).
- **Benchmark (Industrial Large 1k):**
    - **MRR:** **0.6987**.

### 6. Era 5: Density Adaptation (System 11.2 - 12.1)
- **Date:** 2026-02-07 to 2026-02-08
- **Method:** **Oracle Resilience & Adaptive Waterfall (System 12.1)**.
- **Core Logic:** 
    - **System 12.0:** Merged System 3.4 (Oracle) with 11.2 (Density). Introduced V-Clip.
    - **System 12.1:** Lenient Clipping (0.3 threshold) + Oracle Synergy Boost (3.0x). Fixed a major bug in Lexical-First fusion where vector results were dropped if FullText recall was zero.
- **Benchmark (Industrial Large 1k):**
    - **MRR:** **0.7854** (Baseline was ~0.69).
- **Benchmark (Industrial Small):**
    - **MRR:** **0.7317**.

---

## 📈 Summary of Key Metrics Evolution

| Metric | v1.0 (Dec 7) | Sys 3.4 (Jan 29) | Sys 6.5 (Feb 7) | Current (Sys 12.1) |
| :--- | :---: | :---: | :---: | :---: |
| Academic Lite MRR | 1.00 | 1.00 | 1.00 | 1.00 |
| Industrial Small MRR| - | 0.53 | 0.74 | 0.73 |
| Industrial Large MRR| - | 0.81 | 0.69 | 0.78 |
| Industrial 10k MRR | - | - | 0.33 | 0.33 |
| Query Latency (avg) | 9.8ms | ~12ms | ~15ms | ~11ms |

## 🛠️ Technological Stack Changes
- **Embeddings:** `all-MiniLM-L6-v2` (Initial) -> `nomic-embed-text-v1.5` (Multi-Vector) -> **Native ONNX (System 2.0)**.
- **Search:** Postgres/Qdrant (Separate) -> **HybridSearchEngine (LogicGateway Unified)**.
- **Tuning:** Static YAML -> **Bandit/Thompson Sampling (Autonomous)**.
