# Welcome to RAE Agentic Memory

RAE (Reflective Agentic Memory) is an open-source **Memory Engine** designed to provide intelligent agents with a robust, structured, and reflective long-term memory. Unlike traditional RAG (Retrieval Augmented Generation) systems, RAE focuses on building a true meta-memory, enabling agents to learn, adapt, and make more informed decisions over time.

## Why RAE?

Intelligent agents often struggle with:

*   **Context Window Limitations**: LLMs have limited context windows, making it hard to retain long-term information.
*   **Lack of Persistence**: Agents often "forget" past interactions, decisions, and learnings between sessions.
*   **Static Knowledge**: RAG systems provide static knowledge retrieval, but lack the ability to synthesize new insights or adapt to changing environments.
*   **Cost Management**: Blindly calling LLMs can be expensive.

RAE addresses these challenges by providing:

*   **Standardized Memory Protocol**: A simple, technology-agnostic API for storing, querying, and managing memories.
*   **Scoring & Heuristics**: Advanced algorithms to determine the relevance, recency, importance, and usage frequency of memories.
*   **Reflection & Meta-Memory**: Mechanisms for agents to reflect on their experiences, consolidate similar information, filter noise, and build higher-level insights.
*   **Cost-Aware LLM Selection**: Dynamic model selection to optimize for cost and performance.
*   **Observability**: Built-in metrics and a visual dashboard to understand memory flow and agent behavior.

## Key Features

*   **Standard API**: `/memory/store`, `/memory/query`, `/memory/delete`, `/memory/reflect`, etc.
*   **Structured Memory Records**: Flexible JSON Schema for diverse memory types.
*   **Advanced Retrieval**: Hybrid search (dense + sparse vectors) with intelligent re-scoring.
*   **Cost Controller**: Manages LLM usage, prioritizes local models, and tracks expenses.
*   **PII Scrubber**: Integrates with Presidio for sensitive data handling.
*   **Reflection Hook**: Enables agents to create new semantic memories from interactions.
*   **Ecosystem Integrations**: Ollama wrapper, MCP (Memory Context Provider) for file watching.
*   **SDKs**: Python SDK (with Node.js and Go planned).
*   **Visual Dashboard**: Prometheus/Grafana integration for real-time monitoring.
*   **Reference Agents**: Examples demonstrating practical applications.

## Getting Started

To get started with RAE, check out our [Getting Started](getting_started.md) guide.

## Architecture

Dive deeper into the system's design in the [Architecture](architecture.md) section.

## Contributing

RAE is an open-source project, and we welcome contributions from the community. Please see our [Contributing](contributing.md) guide for more details.
