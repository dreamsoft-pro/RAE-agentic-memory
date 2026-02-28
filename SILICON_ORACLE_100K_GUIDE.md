# Silicon Oracle 100K Stabilization Guide
**Status:** MRR 1.0 reached on Academic sets, Scalability verified to 100K memories.
**Date:** Tuesday, 10 February 2026, 10:20 AM

## 🧠 Core Architecture (System 4.16)
This branch contains the "Silicon Oracle" configuration, designed for high-density industrial logs (2GB+) and massive corporate documentation (400+ pages).

### Key Components:
- **Embedding Trio (ONNX Native):**
  - `nomic-embed-text-v1.5` (768d) - Primary Semantic Engine.
  - `all-MiniLM-L6-v2` (384d) - Dense Fallback / Speed Layer.
  - `cross-encoder/ms-marco-TinyBERT-L-2-v2` (18MB) - The "Scalpel" (Reranker).
- **Symbolic Anchoring:** FTS5 weights set to 10.0 vs Vector 0.5 to ensure deterministic keyword hits.
- **Metadata Injection:** Automatic synonym expansion for industrial terms (Metric, Log, Critical).

## 🚀 Running Benchmarks
Benchmarks should be run on **Lumina (Node 1)** for hardware parity (GPU/RTX 4080).

### Command:
```bash
# Full Test (Cold Start - Cleaning DB)
python3 benchmarking/scripts/run_benchmark.py --set benchmarking/sets/industrial_100k.yaml --rerank

# Iterative Tuning (Hot Mode - Fast)
python3 benchmarking/scripts/run_benchmark.py --set benchmarking/sets/industrial_100k.yaml --rerank --skip-ingestion
```

### ⚡ Optimization: --skip-ingestion
To save time during tuning (skipping the 2-minute ingestion for 100k memories), use `--skip-ingestion`.
- **Requirements:** Data must already be in the database for the specific project name.
- **Benefit:** Reduces iteration time from 3 minutes to **~5 seconds** for 100k records.

## 🧹 Database Cleanup
If you need to force a clean state (e.g., after changing embedding models), do NOT use skip-ingestion. The runner will automatically:
1. Delete records from `memories` table for the project.
2. Clean `knowledge_graph_nodes` and `knowledge_graph_edges`.
3. Re-create the Qdrant collection to reset vector dimensions.

## 📍 File Locations
- **Scripts:** `benchmarking/scripts/run_benchmark.py`
- **Datasets:** `benchmarking/sets/`
- **Models:** `/app/models/` (inside docker) or `models/` (local)

## 🏆 Verified Performance
- **Academic Lite:** MRR 1.0000
- **Academic Extended:** MRR 1.0000
- **Industrial 100K Ingestion:** ~120 seconds (800-1000 items/sec)
- **Search Latency:** 100-400ms (with Reranker)
