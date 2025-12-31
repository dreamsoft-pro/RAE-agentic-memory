from prometheus_client import Counter, Gauge, Histogram
import time

# Custom Metrics for RAE Memory API
# Based on TELEMETRY_IMPLEMENTATION_PLAN.md - Layer 1: Operational Metrics

# Uptime metric (set to current time on import, delta calculated by scraper or client)
# Ideally, this Gauge should be set to the start time, or use a callback.
# For simplicity, we'll store the start timestamp and let Prometheus calculate uptime (time() - start_time)
# OR we can just have a Gauge that we update periodically.
# A better pattern for "uptime" in Prometheus is often `process_start_time_seconds` which is standard.
# However, the plan asks for `rae_uptime_seconds`. We can define it as a Gauge.
_START_TIME = time.time()
uptime_seconds = Gauge(
    "rae_uptime_seconds",
    "Time in seconds since RAE started",
)
uptime_seconds.set_function(lambda: time.time() - _START_TIME)


# Counter for total memories stored
memories_stored_total = Counter(
    "rae_memory_count_total",  # Renamed to match plan: rae_memory_count_total
    "Total number of memories stored",
    ["tenant_id", "memory_type"],
)
# Alias for backward compatibility if needed, or just use the new name.
# Keeping the variable name `memories_stored_total` but metric name is updated.

# Gauge for last successful sync
sync_last_success_timestamp = Gauge(
    "rae_sync_last_success_timestamp",
    "Timestamp of last successful sync with a peer",
    ["peer_id", "direction"] # direction: incoming/outgoing
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
# Plan asks for `rae_errors_total`. We can use this one.
api_errors_total = Counter(
    "rae_errors_total", # Renamed to match plan
    "Total number of API errors by error type and endpoint",
    ["tenant_id", "endpoint", "error_type", "http_status"],
)

# Counter for API requests (explicit rae_ metric, though http_requests_total exists)
api_requests_total = Counter(
    "rae_api_requests_total",
    "Total number of API requests handled by RAE",
    ["tenant_id", "method", "endpoint", "status"]
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
