# Strategic Proposal: Evolution of the RAE Ingest Segmenter

**Author:** Gemini Agent (in research mode)
**Date:** 2026-02-18
**Branch:** `research/segmenter-overhaul`
**Status:** DRAFT

## 1. Executive Summary

This document proposes a strategic evolution of the RAE `IngestSegmenter` to enhance its capabilities in creating logically coherent and context-aware text chunks. The recommendation is based on a thorough analysis of the current implementation, external research into state-of-the-art techniques, and the prototyping of a `HierarchicalRecursiveSegmenter`.

The proposed strategy is to **evolve the existing `IngestSegmenter` by incorporating a configurable, hierarchical, and domain-aware segmentation model.** This approach builds on the current solid foundation while elevating its capabilities to a world-class level, in full alignment with RAE's core principles of determinism, auditability, LLM-agnosticism, and future-readiness for the Rust ecosystem.

## 2. Analysis of the Current `IngestSegmenter`

The current segmenter is a strong, policy-driven system that already surpasses naive chunking methods.

*   **Strengths:**
    *   **Content-Aware:** Uses different policies for logs, documents, etc.
    *   **Rule-Based:** Avoids "magic numbers" by pulling patterns from a configuration file.
    *   **Atomic Aggregation:** Intelligently groups smaller "atoms" (like log lines or paragraphs) without splitting them.
*   **Opportunities for Enhancement:**
    *   **Limited Hierarchy:** Relies on a single boundary pattern per policy, which can be insufficient for complex, nested documents (e.g., Markdown with multiple header levels).
    *   **No Semantic Awareness:** The grouping of "atoms" is based on size, not semantic relevance. Two adjacent but unrelated paragraphs might be merged.

## 3. Research & Prototyping: The `HierarchicalRecursiveSegmenter`

To explore potential improvements, a prototype named `HierarchicalRecursiveSegmenter` was developed.

*   **Concept:** This segmenter takes a **prioritized list of separators** (from coarse to fine, e.g., `["
## ", "
### ", "

", ". "]`) and recursively splits text. This ensures that the most significant logical boundaries are respected first.
*   **Implementation:** The v3 prototype successfully demonstrated this concept on complex Markdown, Python code, and unstructured prose. It proved to be highly effective at preserving the logical structure of documents.
*   **Alignment with RAE Principles:**
    *   **Deterministic & Auditable:** The process is 100% repeatable and can be logged at each step.
    *   **Configurable:** The list of separators for each document type is externalized, avoiding hardcoding.
    *   **LLM-Agnostic:** The logic is purely algorithmic and does not rely on any specific model.
    *   **Rust-Ready:** The concept is simple and clear, making it straightforward to implement in Rust without complex dependencies.

## 4. Strategic Recommendation: A Hybrid, Multi-Level Approach

Instead of replacing the current segmenter, I recommend **enhancing it** by integrating the hierarchical model. The `UniversalIngestPipeline` is the perfect architecture for this.

**Proposed Architecture:**

The `IngestSegmenter`'s `segment` method should be refactored. Instead of a simple `if/elif/else` on the policy, it should dispatch to a dedicated, configurable "Segmentation Module" for that policy.

```
// Pseudocode for the enhanced segmenter
class IngestSegmenter:
    def segment(text, policy, signature):
        # 1. Select the right segmentation module based on policy/signature
        if policy in ["POLICY_MARKDOWN", "POLICY_DOCS"]:
            module = MarkdownSegmenterModule(config)
        elif policy == "POLICY_CODE_PYTHON":
            module = CodeSegmenterModule(config)
        else:
            module = DefaultSegmenterModule(config)
        
        # 2. Let the module handle the segmentation
        return module.segment(text)

// Each module uses the hierarchical strategy
class MarkdownSegmenterModule:
    def __init__(self, config):
        self.separators = config.get_markdown_separators() # e.g., ["
# ", "
## ", ...]
        self.chunk_size = config.get_chunk_size()
        self.segmenter = HierarchicalRecursiveSegmenter(self.separators, self.chunk_size)

    def segment(self, text):
        return self.segmenter.segment(text)
```

**Key Advantages of this Approach:**

1.  **Domain Specialization:** Directly implements the vision of separating knowledge domains (legal, medical, code). We can create highly specialized separator lists and logic for each domain in its own module.
2.  **Preserves Logical Structure:** The hierarchical splitting ensures that documents are chunked in a way that aligns with human understanding, creating a better foundation for all subsequent memory layers, especially the **Reflective Layer**.
3.  **Future-Proof & Extensible:** Adding support for a new data type (e.g., LaTeX documents) is as simple as creating a new `LatexSegmenterModule` and its configuration, with no changes to the core pipeline.
4.  **Enables Semantic Enhancement (Optional/Future):** This architecture provides the perfect entry point to introduce an optional "semantic splitting" step in the future. After a module creates structurally coherent chunks, a separate process could (if enabled) run to check for semantic shifts *within* those chunks, providing the best of both worlds.

## 5. Next Steps

1.  **Refactor `IngestSegmenter`:** Implement the proposed modular architecture.
2.  **Externalize Separator Configurations:** Move the hierarchical separator lists for different domains into the `math_controller.yaml` configuration file.
3.  **Integrate Prototype Logic:** Adapt the refined logic from the `HierarchicalRecursiveSegmenter` prototype into the new modules.
4.  **Test Rigorously:** Expand the test suite to cover more edge cases and domains.

This evolutionary path enhances RAE’s core capabilities in a way that is robust, scalable, and perfectly aligned with its foundational principles. It is a crucial step towards achieving a world-class, truly intelligent memory system.
