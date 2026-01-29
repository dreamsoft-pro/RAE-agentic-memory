# RAE for Scientists & Researchers

*Current Version: 3.2.0 (Silicon Oracle)*
*Historical Version (Nov 2025): [scientist_november_2025.md](../history/scientist_november_2025.md)*

This document provides a technical deep-dive into RAE (Reflective Agentic Memory Engine) architecture, mathematical foundations, and recent empirical results. RAE is a deterministic, hardware-agnostic memory core designed for high-performance agentic systems.

---

## 🔬 Core Architecture: The Silicon Oracle

RAE operates on a unified principle of **Deterministic Cognitive Simulation**. Every retrieval and reflection operation is governed by mathematical laws rather than stochastic LLM calls, ensuring reproducibility and reliability.

### 1. 4-Layer Memory Model
Inspired by human cognitive systems, RAE partitions information into four distinct processing stages:

1.  **Episodic (Log-Based):** Raw, chronological interactions. Immutable ground truth stored in PostgreSQL.
2.  **Working (Context-Gated):** Active context for the current reasoning step. Governed by the **Information Bottleneck (IB) Theory**.
3.  **Semantic (Graph-Augmented):** Factual knowledge extracted as triples. Uses **GraphRAG** for multi-hop reasoning.
4.  **Reflective (Meta-Knowledge):** Higher-order insights, strategies, and failure patterns (Szubar Mode).

### 2. 3 Match Layers (Math-1/2/3)
Retrieval is not a simple "top-k" vector search. RAE uses a hierarchical scoring stack:

-   **L1 (Heuristics):** Signal-to-Noise Ratio (SNR) analysis, Term Frequency (TF), and structural filters. Execution time: <1ms.
-   **L2 (Probabilistic):** **Bayesian Tool Router** calculates the probability of retrieval success based on query entropy.
-   **L3 (Optimization):** **Multi-Armed Bandit (MAB)** with Thompson Sampling. Dynamically adjusts weights between Vector Search and Full-Text Search (FTS) based on real-time success signals.

---

## ⚡ Key Technical Innovations

### ONNX: Local & Agnostic Intelligence
RAE uses **Native ONNX Embedding Providers**. By running models like `nomic-embed-text-v1.5` or `all-MiniLM-L6-v2` locally via ONNX Runtime:
-   **Hardware Agnosticism:** Seamless execution on CPU, NVIDIA GPU (CUDA), or AMD (ROCm).
-   **No API Latency:** 100% independent of external providers (OpenAI/Anthropic).
-   **High Throughput:** Optimized for bulk memory ingestion (up to 100k memories in one session).

### Semantic Resonance (Resonance Induction)
When a core memory is retrieved, RAE triggers **Semantic Resonance**. It traverses the Knowledge Graph to find 1st and 2nd-degree neighbors. If their "energy" (centrality * relevance) exceeds a threshold, they are induced into the Working Memory even if they weren't explicitly matched by the query.

### SZUBAR Mode: Evolutionary Pressure
Named after the principle of "Emergent Learning from Failure", **Szubar Mode** induces known system failures into the context. By forcing the agent to see past mistakes ("What NOT to do"), RAE creates an evolutionary pressure that prevents the repetition of reasoning loops.

---

## 📊 Empirical Analysis & Benchmark Results

### Convergence & "Cold Start" Dynamics
In recent tests on **Node 1 (Lumina)**, we observed a critical convergence phenomenon:

-   **The 2k Memory Paradox:** At 2,000 memories with **50 queries**, the system achieved an MRR of only **0.49**.
-   **The 200 Query Breakthrough:** Upon extending the benchmark to **200 queries**, the MRR reached **1.00 (Perfect Calibration)**.
-   **Explanation:** The Math-3 Layer (Bandit Auto-Tuner) requires a "warm-up" period to explore the reward space. At 50 queries, the Bandit was still in the *Exploration* phase. By 200 queries, it converged on the optimal Vector/FTS weight distribution for that specific dataset.

### Scale Benchmarks (Lumina & Local Laptop)
Testing the "Silicon Oracle" architecture at scale. Note that the **10k and 100k results were achieved on a resource-constrained laptop (N550JK)**, proving that Native ONNX and Auto-Tuned Szubar Mode eliminate the need for heavy server hardware.

| Dataset Size | MRR (Hybrid) | Szubar Reflections | Strategy |
| :--- | :--- | :--- | :--- |
| **1k (Small)** | 1.00 | 0 | Math-First |
| **10k (Extreme)** | **1.00** | 0 | **Native ONNX + Szubar** |
| **100k (Ultra)** | **0.85** | 42 | Full Resonance |

*Note: The 100k Ultra benchmark results prove that RAE's hierarchical Match Layers effectively filter noise even on local hardware. The breakthrough in 10k performance (from 0.50 to 1.00) was directly attributed to switching to local ONNX embeddings, which unblocked the high-pressure Szubar Mode reasoning.*

---

## 🧬 Mathematical Foundations

### Information Bottleneck (IB) Objective
RAE minimizes the IB Lagrangian to select the optimal context $Z$:
$$
L = I(Z; Y) - \beta \cdot I(Z; X)
$$
Where $I(Z; Y)$ is relevance and $I(Z; X)$ is compression cost.

### Auto-Tuner Thompson Sampling
The weight $\alpha$ for Vector search is sampled from:
$$P(\alpha | \mathcal{D}) \propto P(\text{success} | \alpha) \cdot P(\alpha)$$
where success is defined by the **Semantic Coherence** of the retrieved results.

---

## 🔗 Related Resources
- **[Benchmark Documentation](../../benchmarking/README.md)** - Reproduce these results.
- **[Math Metrics Guide](../../benchmarking/math_metrics/README.md)** - Deep dive into L1/L2/L3 logic.
- **[Silicon Oracle Spec](../../docs/specs/RAE-Silicon-Oracle.md)** - Full system specification.
