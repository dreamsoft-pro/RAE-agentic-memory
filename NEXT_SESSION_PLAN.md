# Next Session Plan: Oracle Resilience (System 12.2)

## 🎯 Goal: Restore "Silicon Oracle" Peak (MRR 1.0000)
Current System 12.1 achieved **MRR 0.7854** on Industrial Large (1k). We are ~22% below the historical peak reported on GitHub.

## 🔍 Findings from Session 2026-02-08
1. **Fusion Bug Fixed:** `LogicGateway` was dropping vector results in `LEXICAL_FIRST` mode when FullText recall was 0.
2. **Clipping Sensitivity:** Disabling clipping crashed MRR to 0.61. Aggressive clipping (0.7+) was also harmful. Lenient clipping (0.3-0.5) is the current sweet spot.
3. **Synergy Boost:** Increasing Oracle Synergy to 3.0x and reducing `rrf_k` to 20 improved ranking sharpness.
4. **Instability:** Bandit detects "Drift" frequently on the Industrial 1k set, leading to memory resets and lost convergence.

## 🛠️ Tasks for Next Session
1. **[Precision Scalpel]** Implement a fixed `ORACLE` profile in `math_controller.yaml` that bypasses the Bandit for Industrial sets to verify if 1.0 is achievable with static weights (txt=100, vec=1).
2. **[Bridge Alignment]** Compare bridge induction logic in `run_benchmark.py` (ALIAS induction) with `RAECoreService` reflection induction to ensure benchmark results are replicable in production.
3. **[Multi-Vector Calibration]** Investigate if `MultiVectorSearchStrategy` RRF is diluting signal before it reaches the `LogicGateway`.
4. **[Szubar Energy]** Test lowering `szubar_induction_energy` to 0.4 during the benchmark to trigger more aggressive graph recovery.

## 📉 Target Metrics
- **Industrial Small (100):** 1.0000 MRR
- **Industrial Large (1k):** > 0.9500 MRR
- **Bandit Stability:** 0 resets per 100 queries.
