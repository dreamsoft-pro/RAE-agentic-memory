# RAE for Scientists & Researchers

*Current Version: 3.4.0 (Silicon Oracle)*
*Historical Versions: [Nov 2025](../history/scientist_november_2025.md), [Dec 2025](../history/scientist_december_2025.md)*

This document provides a technical deep-dive into RAE (Retrieval-Augmented Episodic) Agnostic Core architecture, mathematical foundations, and empirical results.

---

## 🔬 Core Architecture: The Silicon Oracle

RAE (Retrieval-Augmented Episodic) Agnostic Core is a multi-layered cognitive memory operating system for AI agents. It integrates mathematical determinism with evolutionary adaptation.

### 1. The Four Memory Layers (The 4 Pillars)
RAE categorizes every piece of information (Memory) according to its functional role:

1.  **Episodic Memory (EM / em):** Raw stream of events and technical logs. temporal precision ($t$).
2.  **Working Memory (WM / wm):** Current task context. The only layer for `RESTRICTED` data.
3.  **Semantic Memory (SM / sm):** The Knowledge Graph (GraphRAG). Entities and relations.
4.  **Reflective Memory (RM / rm):** Meta-memory. Stores Bandit weights and **Szubar Mode** failure mappings.

---

## 📐 Mathematical Layers (The Math Core)

RAE processes queries through a cascade of optimization filters:

### L1: Heuristics & "Oracle Seed"
*   **Theory:** Bayesian Prior. Static weight biasing based on query token density. Technical logs favor FTS; abstract queries favor Vectors.

### L2: Fusion Strategy (RRF & Confidence)
*   **Formula (Reciprocal Rank Fusion):**
    $$RRFScore(d) = \sum_{r \in R} \frac{1}{k + r(d)}$$

### L3: Multi-Armed Bandit (MAB) - Evolutionary Controller
*   **Mechanism:** **Thompson Sampling**. RAE treats search configurations as "Arms".
*   **Theory:** Dirichlet-Multinomial distribution. User/Agent feedback reinforces successful arms.

---

## ⚡ Key Technical Innovations

### Szubar Mode: Autonomous Induction
**Szubar Mode** is an emergency state triggered when MRR < threshold. It pulls nearest neighbors from the Knowledge Graph for low-confidence results.
*   **Resonance Wave Theory:** $E = E_0 \cdot e^{-\lambda d}$. Szubar Mode amplifies this amplitude to find hidden logical connections.

### Native ONNX: Agnostic Vector Layer
RAE eliminates external API dependency using internal `onnxruntime`.
*   **Models:** `nomic-embed-text-v1.5` (768d) and `all-MiniLM-L6-v2` (384d).
*   **Math:** Multidimensional Cosine Similarity.

---

## 📊 Empirical Analysis & Benchmark Results (Jan 2026)

Testing the "Silicon Oracle" architecture at scale on a standard developer laptop.

| Dataset Size | MRR (Hybrid) | Szubar Reflections | Strategy |
| :--- | :--- | :--- | :--- |
| **1k (Small)** | 1.0000 | 0 | Math-First |
| **10k (Extreme)** | **1.0000** | 4 | **Native ONNX + Szubar** |
| **100k (Ultra)** | **0.8542** | 42 | **Full Resonance** |

---

## 🔗 Related Resources
- **[Benchmark Documentation](../benchmarking/README.md)** - Reproduce these results.
- **[Math Metrics Guide](../architecture/MATH_LAYERS.md)** - Deep dive into scoring logic.
- **[Security Contract](../contracts/RAE_AGENTIC_CONTRACT.md)** - Privacy and governance rules.
