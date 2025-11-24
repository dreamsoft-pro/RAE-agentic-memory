"""Observability package - OpenTelemetry configuration"""

from .opentelemetry_config import (OTEL_ENABLED, LLMTracer,
                                   add_span_attributes, get_tracer,
                                   instrument_fastapi, instrument_libraries,
                                   record_exception, setup_opentelemetry)

__all__ = [
    "setup_opentelemetry",
    "instrument_fastapi",
    "instrument_libraries",
    "get_tracer",
    "add_span_attributes",
    "record_exception",
    "LLMTracer",
    "OTEL_ENABLED",
]
