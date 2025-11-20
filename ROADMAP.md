# RAE Agentic Memory - Public Roadmap

This document outlines the high-level roadmap for the RAE project. Our goal is to be transparent about our priorities and where we are heading. This is a living document and may change based on community feedback and evolving needs.

## Near-Term (Next 1-3 Months)

### 🚀 SDK & Ecosystem
-   **Publish Python SDK to PyPI**: Package and publish the `rae-memory-sdk` to the official Python Package Index (PyPI) to make it easily installable (`pip install rae-memory-sdk`).
-   **Initial Golang SDK**: Release a functional, well-documented SDK for Go developers based on the existing design document (`sdk_go_design.md`).
-   **Initial Node.js/TypeScript SDK**: Release a functional, well-documented SDK for the Node.js ecosystem based on the existing design document (`sdk_nodejs_design.md`).

### 📖 Examples & Tutorials ("Cookbook")
-   **Build a Chatbot with Long-Term Memory**: A step-by-step tutorial on creating a conversational agent that remembers past interactions using RAE.
-   **RAE for Code Analysis & Refactoring**: An example demonstrating how to use RAE to store information about a codebase to assist a coding agent.
-   **RAE with Local LLMs**: A guide focused on setting up and using RAE effectively with local models via Ollama.

## Mid-Term (Next 3-6 Months)

### 🧠 Core Engine Enhancements
-   **Advanced Memory Summarization**: Implement an intelligent background task that summarizes related episodic memories into a new, more concise reflective memory, helping to manage memory bloat and improve retrieval.
-   **Hybrid Search**: Combine vector search with full-text search (e.g., using Postgres's `tsvector`) for improved retrieval accuracy, especially for queries containing keywords or specific terms.
-   **Knowledge Graph Enhancements**: Improve the knowledge graph capabilities, potentially adding support for more complex relationships and graph-based query methods.

### 🌐 Broader Integrations
-   **Official Docker Hub Image**: Publish official, versioned Docker images for the `memory-api` and other services to simplify deployment.
-   **Helm Charts**: Provide Helm charts for easier deployment to Kubernetes clusters.
-   **Deeper LangChain/LlamaIndex Integration**: Move beyond basic memory object support to more advanced integrations, such as supporting LCEL (LangChain Expression Language) and LlamaIndex's advanced retrieval strategies.

## Long-Term (6+ Months)

### 🏢 Enterprise-Grade Features
-   **Granular Access Control**: Implement more fine-grained permissions and roles within a tenant (e.g., read-only vs. read-write access).
-   **SOC2/GDPR Compliance Features**: Add features to help organizations meet compliance requirements, such as data export/deletion APIs and improved audit trails.
-   **High-Availability (HA) Setup**: Provide documentation and configurations for running RAE in a high-availability setup.

### ✨ Community & Vision
-   **Plugin Architecture**: Develop a plugin system to allow the community to easily add new memory types, storage backends, or even LLM providers.
-   **Visual Memory Management UI**: A simple web interface for browsing, searching, and managing an agent's memories.

---

We welcome community feedback on this roadmap. If you have ideas or want to get involved, please [open an issue](https://github.com/dreamsoft-pro/RAE-agentic-memory/issues) to start a discussion!
