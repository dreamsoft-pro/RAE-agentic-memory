# apps/memory-api/metrics.py
from prometheus_client import Counter, Gauge, Histogram

# --- Custom Metrics ---
LABELS = ["tenant_id", "project"]
memory_store_counter = Counter(
    "memory_store_total", "Total number of memory store operations", ["tenant_id"]
)
memory_query_counter = Counter(
    "memory_query_total", "Total number of memory query operations", ["tenant_id"]
)
memory_delete_counter = Counter(
    "memory_delete_total", "Total number of memory delete operations", ["tenant_id"]
)
llm_cost_counter = Counter(
    "llm_cost_usd_total", "Cumulative cost of LLM calls in USD", LABELS
)

# --- Cost Controller Metrics (Enterprise Cost Tracking) ---
# These metrics provide comprehensive cost and token observability for LLM usage

# Total LLM costs by tenant/project (cumulative counter)
rae_cost_llm_total_usd = Counter(
    "rae_cost_llm_total_usd",
    "Total cumulative LLM costs in USD",
    ["tenant_id", "project", "model", "provider"],
)

# Daily and Monthly cost gauges (reset at boundaries)
rae_cost_llm_daily_usd = Gauge(
    "rae_cost_llm_daily_usd",
    "Current daily LLM costs in USD (resets at midnight UTC)",
    ["tenant_id", "project"],
)

rae_cost_llm_monthly_usd = Gauge(
    "rae_cost_llm_monthly_usd",
    "Current monthly LLM costs in USD (resets on 1st of month)",
    ["tenant_id", "project"],
)

# Token usage tracking
rae_cost_llm_tokens_used = Counter(
    "rae_cost_llm_tokens_used",
    "Total cumulative tokens used (input + output)",
    ["tenant_id", "project", "model", "provider"],
)

# Cache savings tracking
rae_cost_cache_saved_usd = Counter(
    "rae_cost_cache_saved_usd",
    "Estimated cost savings from cache hits in USD",
    ["tenant_id", "project"],
)

# Budget enforcement tracking
rae_cost_budget_rejections_total = Counter(
    "rae_cost_budget_rejections_total",
    "Total number of requests rejected due to budget limits",
    [
        "tenant_id",
        "project",
        "limit_type",
    ],  # limit_type: daily_usd, monthly_usd, daily_tokens, monthly_tokens
)

# LLM call counting
rae_cost_llm_calls_total = Counter(
    "rae_cost_llm_calls_total",
    "Total number of LLM API calls",
    ["tenant_id", "project", "model", "provider", "operation"],
)

# Token distribution analysis
rae_cost_tokens_per_call_histogram = Histogram(
    "rae_cost_tokens_per_call",
    "Distribution of tokens used per LLM call",
    ["model", "provider"],
    buckets=[100, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000],
)
deduplication_hit_counter = Counter(
    "memory_deduplication_hit_total",
    "Total number of deduplication hits",
    ["tenant_id"],
)
reflection_event_counter = Counter(
    "memory_reflection_event_total", "Total number of reflection events", LABELS
)
embedding_time_histogram = Histogram(
    "embedding_time_seconds", "Time taken for embedding generation"
)
vector_query_time_histogram = Histogram(
    "vector_query_time_seconds", "Time taken for vector store queries"
)

# --- Cache Metrics ---
cache_hit_counter = Counter(
    "cache_hit_total",
    "Total number of cache hits",
    ["tenant_id", "project", "cache_type"],
)
cache_miss_counter = Counter(
    "cache_miss_total",
    "Total number of cache misses",
    ["tenant_id", "project", "cache_type"],
)
cache_rebuild_time_gauge = Gauge(
    "cache_rebuild_time_seconds", "Time taken for the last cache rebuild"
)
cache_size_gauge = Gauge(
    "cache_size_mb", "Size of the cache in MB", ["cache_type", "project"]
)
