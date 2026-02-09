# RAE Agnostic Core: Full Architectural Specification
*Version 3.4.0 (Silicon Oracle)*

This document is the single source of truth for RAE's internal mechanics, memory models, and mathematical foundations.

---

## 1. Memory Hierarchy (The 4-Layer Model)

RAE organizes data into cognitive layers to prevent **Reasoning Drift** and ensure high-precision retrieval.

### Episodic Layer (`em` / `episodic`)
- **Purpose**: Chronological event logging.
- **Storage**: Optimized for time-series queries in PostgreSQL.
- **Data**: Log lines, tool outputs, sensory data.

### Working Layer (`wm` / `working`)
- **Purpose**: Immediate task context.
- **Privacy**: The only layer where `RESTRICTED` data is processed.
- **Mechanism**: Dynamic context windowing using Information Bottleneck theory.

### Semantic Layer (`sm` / `semantic`)
- **Purpose**: Long-term factual knowledge.
- **Structure**: Knowledge Graph (Entities & Relations).
- **Tooling**: GraphRAG for multi-hop reasoning.

### Reflective Layer (`rm` / `reflective`)
- **Purpose**: Meta-cognition and self-improvement.
- **Content**: Optimization weights, success/failure traces, and **Szubar Mode** induction patterns.

---

## 2. Retrieval Engines (The 3 Math Planes)

Retrieval is not just vector similarity. It's a hierarchical decision process.

### L1: Heuristic Filter
- Filters by `agent_id`, `project`, `layer`, and `tags`.
- Performs Signal-to-Noise (SNR) calculation.

### L2: Bayesian Fusion
- Uses **Reciprocal Rank Fusion (RRF)** to merge results from Vector, Full-Text, and Graph engines.
- **Formula**: $score = \sum \frac{1}{k + rank}$.

### L3: Multi-Armed Bandit (MAB)
- Dynamically adjusts the importance of Text vs. Vector search based on real-time feedback.
- Uses **Thompson Sampling** to explore optimal weight configurations.

---

## 3. Advanced Features

### SZUBAR Mode (Autonomous Recovery)
Triggered when search confidence is low. It induces "Failure Context" to prevent the agent from repeating past mistakes.

### Semantic Resonance (Wave Induction)
Spreads retrieval "energy" through the Knowledge Graph, bringing in related context that wasn't explicitly mentioned in the query.

### Native ONNX Embeddings
100% local embedding generation using `nomic-embed-text-v1.5` (768d) and `all-MiniLM-L6-v2` (384d). Independent of external APIs.
