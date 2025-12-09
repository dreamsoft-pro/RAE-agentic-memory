from prometheus_client import Counter, Gauge, Histogram

# Custom Metrics for RAE Memory API
# These are examples; tailor them to your specific business logic and performance needs.

# Counter for total memories stored
memories_stored_total = Counter(
    "rae_memories_stored_total",
    "Total number of memories stored",
    ["tenant_id", "memory_type"],
)

# Gauge for current active sessions
active_sessions = Gauge(
    "rae_active_sessions", "Number of active user sessions", ["tenant_id"]
)

# Histogram for reflection processing time
reflection_processing_seconds = Histogram(
    "rae_reflection_processing_seconds",
    "Histogram of reflection processing duration in seconds",
    ["tenant_id", "reflection_type"],
    buckets=(0.1, 0.5, 1.0, 2.5, 5.0, 10.0, float("inf")),
)

# Counter for API errors by type
api_errors_total = Counter(
    "rae_api_errors_total",
    "Total number of API errors by error type and endpoint",
    ["tenant_id", "endpoint", "error_type", "http_status"],
)

# Example usage:
# from apps.memory_api.observability.metrics import memories_stored_total, active_sessions, reflection_processing_seconds, api_errors_total
#
# # In a service when a memory is stored:
# memories_stored_total.labels(tenant_id="some_tenant", memory_type="episodic").inc()
#
# # In a middleware for active sessions:
# active_sessions.labels(tenant_id="some_tenant").set(current_session_count)
#
# # In a reflection service to measure time:
# with reflection_processing_seconds.labels(tenant_id="some_tenant", reflection_type="hierarchical").time():
#     # ... reflection logic ...
#
# # In an exception handler for API errors:
# api_errors_total.labels(tenant_id="some_tenant", endpoint="/v1/memory", error_type="ValidationError", http_status="422").inc()
