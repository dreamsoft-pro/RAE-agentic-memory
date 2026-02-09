# RAE: Reflective Agentic Memory Core
*(read: „Ray”)*

RAE is an open-source cognitive memory system for AI agents. It addresses the fundamental problem of **Reasoning Drift**—the gradual loss of alignment between past decisions and present behavior.

[![DOI](https://zenodo.org/badge/1088095844.svg)](https://zenodo.org/badge/latestdoi/1088095844)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

> **💡 New to RAE? Start Here:** [**What is RAE? Architecture & Philosophy**](docs/CONCEPT.md)  
> *Learn why RAE is not just a Vector DB, how the "Hive Mind" works, and the "RAE-First" workflow.*

---

## 🔬 The Silicon Oracle (Current Performance)

| Suite | Scale | MRR / Score | Status | Device |
| :--- | :--- | :--- | :--- | :--- |
| **Industrial Small** | 100 mems | **1.0000** | ✅ PASS | Laptop CPU |
| **Industrial Large** | 1k mems | **1.0000** | ✅ PASS | Laptop CPU |
| **Industrial Extreme**| 10k mems | **1.0000** | ✅ PASS | Laptop CPU |
| **Industrial Ultra** | 100k mems| **1.0000** | ✅ PASS | Cluster (Lumina) |

*> RAE achieves SOTA performance on standard hardware via Native ONNX and Auto-Tuned Szubar Mode.*

---

## What Problem Does RAE Solve?

Most systems can store information. Few can preserve **why decisions were made**.

In long-running systems (scientific, industrial, or agent-based), context is lost as contributors rotate and time passes. This leads to an inability to audit reasoning paths, an accumulation of contradictory knowledge, and a degradation of decision quality.

RAE solves this by introducing a structured memory architecture that preserves decision rationale as a first-class object.

---

## 🧠 Core Architecture: 4 Layers / 3 Math Planes

RAE models memory as **four functionally distinct layers**:

1.  **Episodic Memory** – What happened (Stream of events).
2.  **Semantic Memory** – What is known (Facts and knowledge graph).
3.  **Working Memory** – What is currently relevant (Agent's active context).
4.  **Reflective Memory** – Why decisions were made (Self-correction and mapping).

It is governed by a 3-layer Mathematical Verification Engine (Logic, Set Theory, Graph) that ensures retrieved context is not just semantically similar, but logically consistent.

---

## 🛡️ Security: Hard Frames & Isolation

RAE physically isolates agents in **Hard Frames**:
- **Network Isolation**: Zero internet access for agent containers.
- **Protocol Exclusivity**: Communication ONLY via the RAE Kernel.
- **Implicit Capture**: Every thought and action is automatically logged into the Working Memory.
- **Privacy-First Mesh**: Asynchronous memory synchronization between instances with explicit User Consent (Trust Handshake).

---

## 3x First Philosophy

- 🔐 **Privacy-first**: Designed for full control over data. RAE can run without sending sensitive information to external providers.
- 🏠 **Local-first**: Supports fully on-premise or air-gapped deployments. The cloud is an option, not a requirement.
- 👐 **Open-Source-first**: Available under the Apache-2.0 license as an open standard.

---

## 🚀 Key Use Cases

- **Cross-Platform Knowledge Bridge**: Connect a Windows-based AI agent (like Cursor or Claude) to a high-performance RAE instance running on a Linux server.
- **Persistent Project Context**: Ensure your agent remembers architectural decisions across sessions and model switches.
- **Autonomous Quality Maintenance**: Periodic "Dreaming" cycles that compress and optimize memory for better retrieval.

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