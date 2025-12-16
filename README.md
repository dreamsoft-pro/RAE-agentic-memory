# RAE – Reflective Agentic Memory Architecture
*(czyt. „Rej”)*

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-892%20passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-69%25-green.svg)]())
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

RAE is an open-source reference architecture for **long-term memory and reasoning continuity** in complex systems. It addresses the fundamental problem of **Reasoning Drift**—the gradual loss of alignment between past decisions, their original rationales, and present system behavior.

---

## What Problem Does RAE Solve?

Most systems can store information. Few can preserve **why decisions were made**.

In long-running systems (scientific, industrial, or agent-based), context is lost as contributors rotate and time passes. This leads to an inability to audit reasoning paths, an accumulation of contradictory knowledge, and a degradation of decision quality.

RAE solves this by introducing a structured memory architecture that preserves decision rationale as a first-class object.

---

## The Core Idea: Structured Memory

Long-term reasoning continuity cannot be achieved with undifferentiated memory (e.g., logs, embeddings). It requires an explicit architectural separation of memory into functionally distinct layers.

RAE models memory as **four functionally distinct layers**:

1.  **Episodic Memory** – What happened
2.  **Semantic Memory** – What is known
3.  **Working Memory** – What is currently relevant
4.  **Reflective Memory** – Why decisions were made and whether they remain valid

This separation prevents reasoning drift.
It is governed by a 3-layer Mathematical Verification Engine (Logic, Set Theory, Graph) that ensures retrieved context is not just semantically similar, but logically consistent

---

## 3x First Philosophy

RAE is built on three core principles:

-   🔐 **Privacy-first**: Designed for full control over data. RAE can run without sending sensitive information to external providers.
-   🏠 **Local-first**: Supports fully on-premise or air-gapped deployments. The cloud is an option, not a requirement.
-   👐 **Open-Source-first**: The core of RAE is and will remain available under the Apache-2.0 license as an open standard.

---

## What RAE Is (and Is Not)

**RAE is:**
- An architectural model for cognitive memory.
- A framework for preserving decision rationale.
- A reference implementation for research and engineering.

**RAE is not:**
- A chatbot framework.
- A simple LLM wrapper.
- A vector database replacement.

---

## Choose Your Path

- 👨‍💻 **For Developers** – See [Quick Start & API Integration](docs/paths/developer.md)
- 🔬 **For Scientists/Researchers** – See [Mathematical Layers, Benchmarks & Telemetry](docs/paths/scientist.md)
- 🏭 **For Industry** – See [Industrial Use Cases & ROI](docs/paths/industry.md)
- 🏥 **For Healthcare** – See [Data Security & On-Premise Deployments](docs/paths/healthcare.md)
- 🏛️ **For Public Administration** – See [Transparency, Audit & Policies](docs/paths/public-sector.md)
- 🤝 **For Philanthropists or VCs** – See [Research Partnerships & Pilots](docs/paths/partners.md)

*
---

## Quick Start

The easiest way to run RAE locally is with Docker.

```bash
git clone https://github.com/dreamsoft-pro/RAE-agentic-memory.git
cd RAE-agentic-memory
docker-compose -f docker-compose.lite.yml up -d
```
For more detailed instructions, see the [Getting Started Guide](docs/LOCAL_SETUP.md).

---

## Project Status

RAE is an active research and engineering project. The architecture is stable, and the implementation is "Enterprise Ready" for many use cases.

-   **Core Functionality**: 4-layer memory, hybrid search, JWT authentication, and multi-tenancy are stable.
-   **Maturity**: Test coverage is actively being increased. Production deployment guides are in development.
-   **See [STATUS.md](docs/.auto-generated/status/STATUS.md)** for a detailed feature breakdown.

---

## Open Source and Collaboration

RAE is and will remain a fully open-source project under the Apache-2.0 license. We aim to create an open, auditable standard for agent memory.

Commercial services and extensions (e.g., enterprise support, specialized integrations) may be developed around the open-source core. This does not change the fact that the RAE engine itself is available to everyone under the same permissive license.

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
