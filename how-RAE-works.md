# 🧠 RAE: Silicon Oracle Architecture Manifest

RAE (Reflective Agentic-memory Engine) Agnostic Core is a multi-layered cognitive memory operating system for AI agents. It integrates mathematical determinism with evolutionary adaptation to provide what is known as the **"Silicon Oracle"** performance standard.

---

## 1. The Four Memory Layers (The 4 Pillars)

RAE categorizes every piece of information (Memory) according to its functional role within the cognitive cycle:

1.  **Episodic Memory (EM / em):**
    *   **Role:** Raw stream of events, technical logs, and time-series data.
    *   **Characteristics:** High temporal precision ($t$), low abstraction. Answers: *"What exactly happened?"*.
2.  **Working Memory (WM / wm):**
    *   **Role:** Current task context and short-term reasoning.
    *   **Security Contract:** The only layer permitted to handle `RESTRICTED` data. WM data never leaks to the Reflective layer without semantic scrubbing/anonymization.
3.  **Semantic Memory (SM / sm):**
    *   **Role:** The Knowledge Graph. Entities and relations extracted from episodes.
    *   **Mechanism:** GraphRAG. Builds the structure: `(Entity) -[Relation]-> (Entity)`.
4.  **Reflective Memory (RM / rm):**
    *   **Role:** Meta-memory. Stores search success/failure logs, Bandit weights, and **Szubar Mode** mappings. Answers: *"How should I think about what I know?"*.

---

## 2. The Three Math Layers (The Math Core)

RAE processes queries through a cascade of optimization filters:

### L1: Heuristics & "Oracle Seed"
*   **Action:** Static weight biasing based on query characteristics.
*   **Theory:** Bayesian Prior. If a query has high token density (technical terms), L1 favors Full-Text Search (FTS). If abstract, it favors Vectors.

### L2: Fusion Strategy (RRF & Confidence)
*   **Action:** Merging results from multiple engines (Vector, FTS, Graph).
*   **Formula (Reciprocal Rank Fusion):**
    $$RRFScore(d) = \sum_{r \in R} \frac{1}{k + r(d)}$$
    Where $r(d)$ is the rank of document $d$ in strategy $R$, and $k$ is a smoothing constant (default 60).

### L3: Multi-Armed Bandit (MAB) - Evolutionary Controller
*   **Action:** RAE treats search configurations as "Arms" in a gambling machine.
*   **Mechanism:** **Thompson Sampling**. The system selects the strategy with the highest statistical "Reward" (relevance).
*   **Theory:** Dirichlet-Multinomial distribution.
    $$P(\theta | D) \propto P(D | \theta) P(\theta)$$
    User/Agent feedback reinforces successful arms and penalizes "MISS" events.

---

## 3. Szubar Mode: Autonomous Induction

**Szubar Mode** is an emergency "consciousness recovery" state triggered when standard retrieval fails (MRR < threshold).

*   **Mechanism:** **High-Energy Induction**. The system pulls the nearest neighbors from the Knowledge Graph for low-confidence vector results.
*   **Semantic Resonance Theory (Wave Theory):**
    A query generates a "wave" in the graph. The wave's energy ($E$) decays with distance ($d$) from the starting node:
    $$E = E_0 \cdot e^{-\lambda d}$$
    Szubar Mode "amplifies" this amplitude, finding hidden connections (e.g., finding a bug fix described in a different module a year ago).

---

## 4. Native ONNX: Agnostic Vector Layer

RAE eliminates dependency on external APIs (OpenAI/Ollama) for embedding generation to ensure 100% determinism.

*   **Engine:** Internal `onnxruntime` + `tokenizers`.
*   **Models:** 
    *   **Nomic-Embed-v1.5 (768d):** Deep semantics. Requires `search_query:` and `search_document:` prefixes.
    *   **MiniLM-L6-v2 (384d):** Lightweight for Edge/Mobile deployments.
*   **Math:** Multidimensional Cosine Similarity:
    $$\cos(\theta) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$

---

## 5. Specialized Algorithms

### Emerald Reranker
Semantic cross-validation. Instead of trusting a single model, RAE compares the grammatical structure of the query with top candidates, eliminating "vector hallucinations" (results that are mathematically close but logically contradictory).

### Semantic Firewall (Phase 3)
A data governance mechanism that blocks `RESTRICTED` data. It calculates the "Information Entropy" ($H$) of a query. If $H$ exceeds the privacy threshold, the query is degraded to an Anonymized Proxy.

---

## 6. Developer Glossary

*   **Arm:** A specific weight configuration (e.g., FTS: 10.0, Vector: 1.0).
*   **Drift:** A sudden change in data nature (e.g., switching a project from Python to Rust) that triggers a Bandit memory reset.
*   **Oracle Seed:** The "genetic" starting weights that allow the system to perform effectively from the first second of installation (Cold Start Protection).

---

**RAE does not just remember facts; it learns the most effective way to find them based on your project's unique context.** It is the difference between a library (static data) and a librarian (active intelligence).
