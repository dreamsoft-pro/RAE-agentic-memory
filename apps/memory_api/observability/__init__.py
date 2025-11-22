"""Observability package - OpenTelemetry configuration"""

from .opentelemetry_config import (
    setup_opentelemetry,
    instrument_fastapi,
    instrument_libraries,
    get_tracer,
    add_span_attributes,
    record_exception,
    LLMTracer,
    OTEL_ENABLED
)

__all__ = [
    "setup_opentelemetry",
    "instrument_fastapi",
    "instrument_libraries",
    "get_tracer",
    "add_span_attributes",
    "record_exception",
    "LLMTracer",
    "OTEL_ENABLED"
]
