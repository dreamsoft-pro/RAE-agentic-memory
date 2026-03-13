# RAE-Suite: The Deterministic Agentic Factory
## Manifesto and Architecture Specification v1.2 (The Iron Protocol)

### 1. Vision & Core Paradigm
RAE-Suite is not an AI coding assistant; it is a **Deterministic Operating System for Agentic Engineering**. It transforms the uncertainty of Large Language Models into high-density, auditable, and industrial-grade software artifacts. 

The suite follows the **"Architecture as a Service" (RaaS/CaaS)** model, where software is manufactured through a rigorous, 6-stage behavioral funnel, governed by the **3x3x3 Council of Elders**.

---

### 2. The 3x3x3 Council of Elders (Consensus Governance)
Every critical decision in the factory is governed by a multi-layered hierarchy of agents. Each layer requires a consensus of three specialized models. All models are configurable via environment variables (`.env`).

| Layer | Type | Default Models (A / B / C) | Responsibility |
| :--- | :--- | :--- | :--- |
| **L1: Working** | Production | **Gemini 2.5 Flash / DeepSeek V3 / Qwen 2.5** | High-speed code generation, unit testing, static analysis. |
| **L2: Expert** | Auditing | **Claude 3.5 Sonnet / Gemini 1.5 Pro / GPT-4o** | Structural review, contract generation, semantic logic verification. |
| **L3: Supreme** | Final Verdict | **Claude 4.5 / Gemini 2.0 Pro / GPT-o1** | Behavioral symmetry, ISO compliance, final safety arbitration. |

#### Configurability (.env mapping):
```bash
# L1 - Working Layer
RAE_L1_MODEL_A=gemini-2.5-flash
RAE_L1_MODEL_B=deepseek-v3-14b
RAE_L1_MODEL_C=qwen-2.5-14b

# L2 - Expert Layer
RAE_L2_MODEL_A=claude-3-5-sonnet
RAE_L2_MODEL_B=gemini-1-5-pro
RAE_L2_MODEL_C=gpt-4o

# L3 - Supreme Layer
RAE_L3_MODEL_A=claude-4-5-preview
RAE_L3_MODEL_B=gemini-2-0-pro-exp
RAE_L3_MODEL_C=gpt-o1
```

---

### 3. The 6-Stage Production Funnel (The Standard)

#### Stage 1: Ontological Ingestion (Discovery)
*   **Mechanism:** RAE-Phenix + RAE-Core (Szubar Mode).
*   **Action:** Reconstructs the intent field. L2 Expert Council validates the discovered requirements.

#### Stage 2: Behavior-Driven Contracting (Phenix)
*   **Action:** Generation of `.contract.yml` (The Law).
*   **Action:** L3 Supreme Council approves the contract before any code is written.

#### Stage 3: Swarm Execution (Hive Swarm)
*   **Mechanism:** L1 Worker Swarm (Gemini/DeepSeek/Qwen) implements the code.
*   **Verification:** Writer-Auditor feedback loop until the Technical Gate is passed.

#### Stage 4: Hard Frames & Deterministic Validation
*   **Action:** Physical execution of tests and security scanners. 
*   **Constraint:** Zero-warning policy. Any failure triggers an automatic fallback to the Expert Council.

#### Stage 5: Observability & Telemetry Injection (OTel)
*   **Action:** Automatic injection of OTel instrumentation.
*   **Result:** Real-time tracking of code performance and business metrics in Grafana.

#### Stage 6: ISO 42001 Governance & Meta-Reflection
*   **Action:** L3 Supreme Council issues the Final Verdict and signs the Audit Report.
*   **Action:** RAE-Core updates Multi-Armed Bandit weights based on the session's success metrics.

---

### 4. Open Source & Commercial Strategy
*   **The Engine (Open Source):** The architecture, the 3x3x3 protocol, and core packages are open source.
*   **The Intelligence (Proprietary):** Specialized "Knowledge Packs" (e.g., *Dreamsoft Enterprise Blueprint*) and GPU Cluster access (Lumina) form the commercial offering.

---
*Created on: February 25, 2026*  
*Standard: RAE-Suite-Iron-Protocol-v1.2*
