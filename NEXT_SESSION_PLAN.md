# Next Session Plan - RAE System 3.1 (Reflection-Aware)

## 1. Benchmark Evolution (The "Meta-Metric")
- [ ] **Refactor Benchmark Logic:**
    - Current Flaw: Finding a "Reflection" memory counts as a MISS because its ID differs from the source document ID.
    - New Logic: If the retrieved memory is a Reflection (`layer='reflective'`) and its content references the target document ID/Content, count it as an **Indirect HIT**.
    - Goal: Prove that "Learning in the Loop" actually works (MRR should rise during the session as reflections are created).

## 2. In-Session Learning Verification
- [ ] **Run "Repeat Benchmark"**:
    - Query Set A (Baseline) -> Failures generate Reflections.
    - Query Set A (Repeat) -> Should hit Reflections -> 100% Success.
    - This proves the "Self-Healing Memory" concept definitively.

## 3. Productionize Native ONNX
- [ ] Move `NativeEmbeddingProvider` from prototype to default production configuration for Windows/Mobile builds.
- [ ] Ensure `rae-core` uses ONNX by default when available, falling back to API only if configured.

## 4. Final Polish
- [ ] Integrate `Bandit` persistence into the main `RAEEngine` (not just the benchmark script) so the production app learns user preferences over time.