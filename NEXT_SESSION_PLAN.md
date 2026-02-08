# Next Session Plan: System 23.0 - Neural Scalpel & Adaptive Intelligence

## Overview
Unify "Neural Scalpel" precision (System 22.1) with "Adaptive Intelligence" (CRAG/Routing) to achieve MRR 1.0 on Industrial Benchmarks. The goal is to close the semantic gap (e.g., iPhone != mobile) via metadata injection while handling failure cases gracefully via Corrective RAG.

## 1. Priority: Neural Scalpel + Metadata Injection (The "MRR 1.0" Fix)
- **Problem:** TinyBERT reranker lacks domain knowledge (semantic gap).
- **Goal:** Achieve MRR > 0.95 on Industrial sets by injecting context before reranking.
- **Tasks:**
    - **Metadata Injection:** Implement `MetadataInjector` to enrich query/doc context with synonyms and parent entities (e.g., "iPhone" -> "iPhone mobile phone smartphone") *before* embedding/reranking.
    - **Tuning:** Calibrate the current 10,000x reranker weight against the new injected metadata.
    - **Verify:** Run `industrial_small` benchmark to confirm the "iPhone/Mobile" fix.

## 2. Adaptive RAG (Policy & Routing)
- **Goal:** Stop wasting compute on simple queries; use Deep Logic only when needed.
- **Tasks:**
    - Implement `PolicyRouter` in Math Layer.
    - **Fast Path:** Math-Only (FullText) or simple Vector for high-confidence matches.
    - **Deep Path:** Triggered when Fast Path score < Threshold. Activates Neural Scalpel (Reranker) + Graph Resonance.
    - **Logging:** Audit all routing decisions in the **Working** layer.

## 3. Corrective RAG (CRAG) - The Safety Net
- **Goal:** Handle "Zero Result" or "Low Confidence" scenarios without hallucination.
- **Tasks:**
    - Implement `VerificationLoop`: If retrieved documents contradict or lack answer, trigger Web Search (if allowed) or "Szubar" Reflection.
    - **Query Correction:** Automatically rewrite queries if initial retrieval fails (e.g., strip specific IDs, relax constraints).

## 4. Housekeeping & Stabilization
- **Tasks:**
    - **Merge:** Push confirmed System 22.1 fixes to `develop` (Node 1 is synced).
    - **Tests:** Review and fix the 7 skipped tests in `make test-core`.
    - **Zero Drift:** Ensure all new logic is covered by tests before commit.

## Success Metrics
- **MRR:** > 0.95 on Industrial Small (fixing the semantic gap).
- **Efficiency:** Fast Path used for >60% of trivial queries.
- **Resilience:** 0 Hallucinations on missing data (Corrective fallback).
