# RAE Architecture Deep Dive

This document provides a comprehensive overview of the RAE (Retrieval-Augmented Engine) architecture, focusing on its core principles and multi-layered design.

## 1. Core Philosophy

RAE is built on a set of foundational principles that guide its development. These are not just technical choices but a philosophical stance on how AI systems should be built.

### 1.1. Local-First and Privacy-First
All core operations must be able to run entirely offline. The system should never depend on a cloud service for its primary functions. This ensures user data remains private and under user control. Cloud integration is an option, not a necessity.

### 1.2. LLM-Agnostic
RAE is not a wrapper for a single LLM. It is a reasoning and memory engine that can *use* any LLM as a pluggable tool. This is achieved through a generic `IEmbeddingProvider` interface and support for multiple vector dimensions from different models. Techniques like Matryoshka embeddings or averaging are explicitly avoided to prevent information loss.

### 1.3. Determinism and Auditability
Every process in RAE must be deterministic, repeatable, and auditable. This is a core requirement for enterprise and scientific applications, aligned with ISO 27001 (Information Security) and ISO 42001 (AI Management).

```python
# Example of an auditable log entry
logger.info(
    "universal_ingest_complete", 
    chunk_count=len(compressed_chunks),
    mode=signature.struct.get("mode"),
    policy=policy
)
```

## 2. Ingestion Pipeline (The 5-Layer Input)

RAE's Universal Ingest Pipeline is a 5-stage process designed for content-aware chunking.

1.  **Normalize:** Cleans and standardizes raw text.
2.  **Detect:** Identifies the content's "signature" (e.g., code, prose, log).
3.  **Policy:** Selects an appropriate processing policy based on the signature.
4.  **Segment:** Splits the text into logical, atomic chunks using the selected policy. This is where hierarchical splitting occurs.
5.  **Compress:** Performs semantic folding or other compression on the chunks.

This multi-stage approach avoids rigid, fixed-size chunking and preserves the logical integrity of the source data.

## 3. Memory Architecture (The 4-Layer System)

RAE's memory is not monolithic. It's divided into four distinct layers to manage knowledge effectively.

*   **Short-Term Memory:** Volatile, for immediate context.
*   **Medium-Term Memory:** For conversational context over a session.
*   **Long-Term Memory:** The main repository of facts, procedures, and core knowledge.
*   **Reflective Memory:** The most advanced layer. It's designed to synthesize non-obvious ideas, concepts, and connections from the other memory layers. It doesn't just store data; it creates new insights.

---

This architecture, while complex, provides the foundation for a scalable, robust, and truly intelligent system capable of supporting mixed teams of humans and AI agents.
