# Next Session Plan - 2026-01-27 (Part 2)

## 1. Vector Layer Rescue (Priority 1)
- [ ] Investigate "Double Prefixing" Hypothesis:
    - Check if `LiteLLM` automatically adds prefixes for `nomic-embed-text`.
    - Test `run_benchmark.py` WITHOUT manual prefixes.
- [ ] Verify `embedding_dim` consistency (768 vs 384) in all configs.
- [ ] Aim for Hybrid MRR > Math-Only MRR (currently Hybrid is 0.3 vs Math 0.7 on Academic, but 0.5 vs 0.3 on Industrial Large).

## 2. Industrial Large Benchmark
- [x] Run `Industrial Large` on Lumina (Result: Hybrid 0.51, Math 0.30).
- [ ] Analyze why Hybrid is better here but worse elsewhere. (Hypothesis: FullText returns 0 results for semantic queries in Large dataset).

## 3. Documentation
- [ ] Update `BENCHMARK_RESULTS.md` with the "Math-Only Dominance" discovery and "Vector Safety Net" findings.
