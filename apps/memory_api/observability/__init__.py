"""Observability package - OpenTelemetry configuration and memory tracing"""

from .memory_tracing import (
    MemoryTracer,
    get_memory_tracer,
    trace_episodic_operation,
    trace_graph_operation,
    trace_memory,
    trace_reflective_operation,
    trace_semantic_operation,
)
from .opentelemetry_config import (
    OTEL_ENABLED,
    LLMTracer,
    add_span_attributes,
    get_tracer,
    instrument_fastapi,
    instrument_libraries,
    record_exception,
    setup_opentelemetry,
)
from .traced_qdrant import TracedQdrantClient, create_traced_client

__all__ = [
    # OpenTelemetry Core
    "setup_opentelemetry",
    "instrument_fastapi",
    "instrument_libraries",
    "get_tracer",
    "add_span_attributes",
    "record_exception",
    "LLMTracer",
    "OTEL_ENABLED",
    # Memory Tracing
    "MemoryTracer",
    "get_memory_tracer",
    "trace_memory",
    "trace_episodic_operation",
    "trace_semantic_operation",
    "trace_graph_operation",
    "trace_reflective_operation",
    # Traced Clients
    "TracedQdrantClient",
    "create_traced_client",
]
