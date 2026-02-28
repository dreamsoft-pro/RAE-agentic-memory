# RAE Benchmark Session Report - 2026-02-07
**Topic:** Industrial Retrieval Optimization & Resonance Cascade (System 6.x)

## 📊 Benchmark Results

| System Version | Architecture | Academic Lite | Academic Ext. | Ind. Small | Ind. Large (1k) | Ind. 10k |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **System 6.3** | Dual-Engine, RRF-60, Tie-Breakers | **1.0000** | **1.0000** | **0.7583** | **0.6987** | 0.3333 |
| **System 6.4** | Resonance Routing, Aggressive Early Exit | 1.0000 | 0.9750 | - | 0.5852 (Reg.) | - |
| **System 6.5** | Hybrid Resilience, Safe Early Exit (<5), RRF-10 | 1.0000 | 0.9750 | 0.7417 | 0.6772 | - |

> *Note: Industrial 10k score of 0.33 in Sys 6.3 is attributed to generic dataset queries (Top-k cut-off for 200+ valid hits), not engine failure.*

## 🧠 Architectural Evolution

### System 6.3 "Parallel Consensus"
- **Logic:** Run Vector and Lexical in parallel. Fuse with Reciprocal Rank Fusion (k=60).
- **Key Win:** Tie-Breaking in Postgres (`ORDER BY importance DESC`) solved the "random sort" issue for logs.
- **Verdict:** Most stable baseline.

### System 6.4 "Resonance Cascade"
- **Logic:** Use Query Entropy (Semantic Resonance) to choose `LEXICAL` or `VECTOR` priority. Stop immediately if priority engine finds results.
- **Failure Mode:** Industrial logs matched generic keywords (e.g., "error") in Postgres (200 hits). Aggressive "Early Exit" prevented Vectors from re-ranking the noise.
- **Lesson:** "Presence of results" != "Confidence" in full-text search.

### System 6.5 "Hybrid Resilience"
- **Logic:** "Safe Early Exit" - only stop if Lexical finds **< 5 results** (high specificity). Otherwise, force fusion.
- **Regression:** Changed RRF constant to `k=10`. This proved too aggressive for the "long tail" of vector signals, causing slight drop vs 6.3.

## 🚀 Strategic Roadmap (System 6.6)
1. **Revert RRF Constant:** Switch `k` back to `60` (from System 6.3) to restore 0.69+ score.
2. **Keep Safe Early Exit:** The `< 5 results` rule from System 6.5 is the correct "Guard Rail" for performance.
3. **Fix Dataset:** `industrial_100k.yaml` needs re-uploading (file corruption).
4. **Resonance Tuning:** `SemanticResonance` class is working correctly to distinguish IDs from questions.

## 📂 Artifacts
- `rae-core/rae_core/math/semantic_resonance.py`: New Entropy Calculator.
- `rae-core/rae_core/math/logic_gateway.py`: Updated with Thresholds and Early Exit.
