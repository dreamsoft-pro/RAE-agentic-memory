# Eval Suite

This directory contains tools for evaluating the performance of the Agentic Memory API.

## Usage

To run the evaluation script, execute the following command from the root of the repository:

```bash
python -m eval.run_eval
```

The script will send queries from `goldenset.yaml` to the API and calculate the following metrics:

- `hit_rate@5`: The percentage of queries for which at least one of the top 5 results is correct.
- `mrr`: The Mean Reciprocal Rank of the correct results.
- `p95_ms`: The 95th percentile of the query latency in milliseconds.
