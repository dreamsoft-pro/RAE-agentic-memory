# RAE: Reflective Agentic Memory Core
*(read: „Ray”)*

RAE is an open-source cognitive memory system for AI agents. It addresses the fundamental problem of **Reasoning Drift**—the gradual loss of alignment between past decisions and present behavior.

> **💡 New to RAE? Start Here:** [**What is RAE? Architecture & Philosophy**](docs/CONCEPT.md)  
> *Learn why RAE is not just a Vector DB, how the "Hive Mind" works, and the "RAE-First" workflow.*

---

## 🔬 The Silicon Oracle (Current Performance)

| Suite | Scale | MRR / Score | Status | Device |
| :--- | :--- | :--- | :--- | :--- |
| **Industrial Small** | 100 mems | **1.0000** | ✅ PASS | Laptop CPU |
| **Industrial Large** | 1k mems | **1.0000** | ✅ PASS | Laptop CPU |
| **Industrial Extreme**| 10k mems | **1.0000** | ✅ PASS | Laptop CPU |
| **Industrial Ultra** | 100k mems| **0.8542** | ✅ PASS | Laptop CPU |

*> RAE achieves SOTA performance on standard hardware via Native ONNX and Auto-Tuned Szubar Mode.*

---

## 🧠 Core Architecture: 4 Layers / 3 Math Planes

RAE models memory as four functionally distinct layers governed by a 3-layer mathematical control plane:

1.  **Episodic Memory** – What happened (Immutable Logs)
2.  **Semantic Memory** – What is known (Knowledge Graph)
3.  **Working Memory** – What is currently relevant (Context Gate)
4.  **Reflective Memory** – How to think about what I know (Meta-Knowledge)

**Retrieval is optimized via:**
- **L1 Heuristics**: Static signal-to-noise biasing.
- **L2 Probabilistics**: Bayesian tool routing.
- **L3 Evolutionary**: Multi-Armed Bandit (Thompson Sampling) for real-time weight adaptation.

---

## 🛡️ Security: Hard Frames

RAE physically isolates agents in **Hard Frames**:
- **Network Isolation**: Zero internet access for agent containers.
- **Protocol Exclusivity**: Communication ONLY via the RAE Kernel.
- **Implicit Capture**: Every thought and action is automatically logged into the Working Memory.

---

## 🚀 Quick Start

```bash
git clone https://github.com/dreamsoft-pro/RAE-agentic-memory.git
cd RAE-agentic-memory

# 1. Start Development Environment (Hot-Reload)
docker compose --profile dev up -d

# 2. Start Lite Environment (Minimal)
docker compose --profile lite up -d
```

---

## 🔗 Choose Your Path

- 👨‍💻 **[For Developers](docs/paths/developer.md)** – Quick Start & API Integration.
- 🔬 **[For Scientists](docs/paths/scientist.md)** – Mathematical Foundations & Benchmarks.
- 🏭 **[For Industry](docs/paths/industry.md)** – Use Cases & ROI.
- 🔐 **[Security Guide](docs/guides/SECURE_AGENT_DEPLOYMENT.md)** – Hard Frames & Isolation.

---

RAE is licensed under the Apache-2.0 license. We aim to create an open standard for agent memory.
