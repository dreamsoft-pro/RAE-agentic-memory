# RAE System 2.0 Implementation Plan

**Goal:** Transform RAE from a "Resilient Search Engine" into an "Ultra-Effective Intelligent Memory Core" by integrating native physics (ONNX), adaptive control (Math Layer), and failure learning (Szubar).

## 1. Native Vector Foundation (The "Engine")
- **Action:** Replace external API calls (Ollama/LiteLLM) with `NativeEmbeddingProvider` via `onnxruntime`.
- **Benefit:** 
    - Consistent vectors across Windows/Mobile/Server.
    - Full control over prefixing (`search_query:`/`search_document:`) and normalization.
    - Support for 4 vector lengths (Matryoshka slicing) from a single model.
- **Target:** Lumina Node 1.

## 2. Adaptive Intelligence (The "Transmission")
- **Action:** Integrate `MathLayerController` into the search loop.
- **Logic:** Move away from hardcoded weights. The Controller analyzes the query context:
    - *Factual Query* (Entities, Dates) → Boost FullText (Weight 10.0).
    - *Abstract Query* (Concepts, Intent) → Boost Vector (Weight 5.0).
- **Benefit:** Dynamic adaptation to query type, maximizing MRR for both "Academic" and "Industrial" patterns automatically.

## 3. Failure Learning (The "Driver" - Szubar)
- **Action:** Capture `MISS` events (queries with 0 relevant results).
- **Reaction:** 
    - Log failure context.
    - (Future) Generate synthetic "Reflection" memories to bridge the semantic gap.
    - (Future) Adjust `importance` of missed documents.

## Execution Strategy (Lumina)
1. Use `.venv312` with `onnxruntime` and `tokenizers`.
2. Deploy updated `run_benchmark.py` acting as the "System 2.0 Prototype" runner.
3. Verify `Industrial Large` performance with this integrated architecture.
