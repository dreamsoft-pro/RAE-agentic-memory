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
deduplication_hit_counter = Counter(
    "memory_deduplication_hit_total", "Total number of deduplication hits", ["tenant_id"]
)
reflection_event_counter = Counter(
    "memory_reflection_event_total", "Total number of reflection events", LABELS
)
embedding_time_histogram = Histogram(
    'embedding_time_seconds', 'Time taken for embedding generation'
)
vector_query_time_histogram = Histogram(
    'vector_query_time_seconds', 'Time taken for vector store queries'
)

# --- Cache Metrics ---
cache_hit_counter = Counter(
    "cache_hit_total", "Total number of cache hits", ["tenant_id", "project", "cache_type"]
)
cache_miss_counter = Counter(
    "cache_miss_total", "Total number of cache misses", ["tenant_id", "project", "cache_type"]
)
cache_rebuild_time_gauge = Gauge(
    "cache_rebuild_time_seconds", "Time taken for the last cache rebuild"
)
cache_size_gauge = Gauge(
    "cache_size_mb", "Size of the cache in MB", ["cache_type", "project"]
)
