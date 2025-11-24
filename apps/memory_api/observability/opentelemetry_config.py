"""
OpenTelemetry Configuration - Enterprise Distributed Tracing

This module configures OpenTelemetry for comprehensive distributed tracing across:
- FastAPI HTTP requests
- Database queries (PostgreSQL via asyncpg/psycopg2)
- Redis operations
- External HTTP requests
- LLM API calls

Traces are exported to OTLP-compatible backends:
- Jaeger (local development)
- Tempo (Grafana Cloud)
- Elastic APM
- AWS X-Ray
- Google Cloud Trace

Environment Variables:
- OTEL_EXPORTER_OTLP_ENDPOINT: OTLP endpoint (default: http://localhost:4317)
- OTEL_SERVICE_NAME: Service name (default: rae-memory-api)
- OTEL_TRACES_ENABLED: Enable tracing (default: true)
- OTEL_EXPORTER_TYPE: otlp, jaeger, console (default: otlp)
"""

import os

import structlog
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_VERSION, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)

logger = structlog.get_logger(__name__)


# ============================================================================
# Configuration
# ============================================================================

OTEL_ENABLED = os.getenv("OTEL_TRACES_ENABLED", "true").lower() == "true"
OTEL_SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "rae-memory-api")
OTEL_SERVICE_VERSION = os.getenv("OTEL_SERVICE_VERSION", "2.0.0-enterprise")
OTEL_EXPORTER_ENDPOINT = os.getenv(
    "OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317"
)
OTEL_EXPORTER_TYPE = os.getenv("OTEL_EXPORTER_TYPE", "otlp")  # otlp, console, none


# ============================================================================
# Tracer Provider Setup
# ============================================================================


def setup_opentelemetry():
    """
    Initialize OpenTelemetry tracing with configured exporter.

    This function should be called once during application startup,
    before any instrumented code runs.
    """
    if not OTEL_ENABLED:
        logger.info("opentelemetry_disabled", reason="OTEL_TRACES_ENABLED=false")
        return None

    try:
        # Create resource with service metadata
        resource = Resource.create(
            {
                SERVICE_NAME: OTEL_SERVICE_NAME,
                SERVICE_VERSION: OTEL_SERVICE_VERSION,
                "deployment.environment": os.getenv("ENVIRONMENT", "development"),
                "service.namespace": "rae",
                "service.instance.id": os.getenv("HOSTNAME", "localhost"),
            }
        )

        # Create tracer provider
        tracer_provider = TracerProvider(resource=resource)

        # Configure exporter based on type
        if OTEL_EXPORTER_TYPE == "console":
            # Console exporter for debugging
            span_exporter = ConsoleSpanExporter()
            logger.info("opentelemetry_console_exporter", service=OTEL_SERVICE_NAME)
        elif OTEL_EXPORTER_TYPE == "otlp":
            # OTLP exporter (default) for Jaeger, Tempo, etc.
            span_exporter = OTLPSpanExporter(
                endpoint=OTEL_EXPORTER_ENDPOINT, insecure=True  # Use TLS in production
            )
            logger.info(
                "opentelemetry_otlp_exporter",
                service=OTEL_SERVICE_NAME,
                endpoint=OTEL_EXPORTER_ENDPOINT,
            )
        else:
            logger.warning("opentelemetry_no_exporter", type=OTEL_EXPORTER_TYPE)
            return None

        # Add batch span processor (buffers spans for efficiency)
        tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))

        # Set global tracer provider
        trace.set_tracer_provider(tracer_provider)

        logger.info(
            "opentelemetry_initialized",
            service=OTEL_SERVICE_NAME,
            version=OTEL_SERVICE_VERSION,
            exporter=OTEL_EXPORTER_TYPE,
        )

        return tracer_provider

    except Exception as e:
        logger.error("opentelemetry_setup_failed", error=str(e))
        return None


# ============================================================================
# Auto-Instrumentation
# ============================================================================


def instrument_fastapi(app):
    """
    Instrument FastAPI application with OpenTelemetry.

    This adds automatic tracing for all HTTP requests, including:
    - Request/response timing
    - HTTP method, path, status code
    - Request headers (filtered)
    - Exceptions and errors

    Args:
        app: FastAPI application instance
    """
    if not OTEL_ENABLED:
        return

    try:
        FastAPIInstrumentor.instrument_app(app)
        logger.info("opentelemetry_fastapi_instrumented")
    except Exception as e:
        logger.error("opentelemetry_fastapi_failed", error=str(e))


def instrument_libraries():
    """
    Instrument common libraries for automatic tracing.

    This adds tracing for:
    - HTTP requests (requests library)
    - PostgreSQL queries (psycopg2)
    - Redis operations (redis-py)
    - Python logging (adds trace context to logs)
    """
    if not OTEL_ENABLED:
        return

    try:
        # Instrument requests library (for external HTTP calls)
        RequestsInstrumentor().instrument()
        logger.info("opentelemetry_requests_instrumented")

        # Instrument PostgreSQL (psycopg2)
        # Note: For asyncpg, you'll need custom instrumentation
        Psycopg2Instrumentor().instrument()
        logger.info("opentelemetry_psycopg2_instrumented")

        # Instrument Redis
        RedisInstrumentor().instrument()
        logger.info("opentelemetry_redis_instrumented")

        # Instrument logging (adds trace_id to logs)
        LoggingInstrumentor().instrument(set_logging_format=False)
        logger.info("opentelemetry_logging_instrumented")

    except Exception as e:
        logger.error("opentelemetry_library_instrumentation_failed", error=str(e))


# ============================================================================
# Custom Span Helpers
# ============================================================================


def get_tracer(name: str = OTEL_SERVICE_NAME):
    """
    Get a tracer instance for creating custom spans.

    Usage:
        tracer = get_tracer("my-component")
        with tracer.start_as_current_span("my-operation") as span:
            span.set_attribute("custom.key", "value")
            # ... do work ...
    """
    return trace.get_tracer(name, OTEL_SERVICE_VERSION)


def add_span_attributes(**attributes):
    """
    Add attributes to the current active span.

    Usage:
        add_span_attributes(
            user_id="user123",
            tenant_id="tenant456",
            operation="memory_create"
        )
    """
    span = trace.get_current_span()
    if span.is_recording():
        for key, value in attributes.items():
            span.set_attribute(key, value)


def record_exception(exception: Exception):
    """
    Record an exception in the current span.

    Usage:
        try:
            # ... code that might fail ...
        except Exception as e:
            record_exception(e)
            raise
    """
    span = trace.get_current_span()
    if span.is_recording():
        span.record_exception(exception)
        span.set_status(trace.Status(trace.StatusCode.ERROR))


# ============================================================================
# Custom Instrumentation for LLM Calls
# ============================================================================


class LLMTracer:
    """
    Custom tracer for LLM API calls.

    Adds detailed tracing for expensive LLM operations, including:
    - Model name and provider
    - Token counts (input/output)
    - Cost information
    - Cache hits
    - Latency

    Usage:
        async with LLMTracer.trace(model="gpt-4o-mini", operation="embedding"):
            result = await llm_client.generate(...)
            LLMTracer.record_tokens(input=1000, output=500)
            LLMTracer.record_cost(0.0025)
    """

    @staticmethod
    def trace(model: str, operation: str, provider: str = "unknown"):
        """
        Create a span for an LLM operation.
        """
        tracer = get_tracer("rae.llm")
        span = tracer.start_span(f"llm.{operation}")
        span.set_attribute("llm.model", model)
        span.set_attribute("llm.provider", provider)
        span.set_attribute("llm.operation", operation)
        return span

    @staticmethod
    def record_tokens(input_tokens: int, output_tokens: int):
        """Record token usage in current span."""
        add_span_attributes(
            llm_input_tokens=input_tokens,
            llm_output_tokens=output_tokens,
            llm_total_tokens=input_tokens + output_tokens,
        )

    @staticmethod
    def record_cost(cost_usd: float):
        """Record cost in current span."""
        add_span_attributes(llm_cost_usd=cost_usd)

    @staticmethod
    def record_cache_hit(is_hit: bool):
        """Record cache hit/miss."""
        add_span_attributes(llm_cache_hit=is_hit)


# ============================================================================
# Deployment Examples
# ============================================================================

"""
=== Local Development with Jaeger ===

1. Start Jaeger (all-in-one):
   docker run -d --name jaeger \
     -p 4317:4317 \
     -p 16686:16686 \
     jaegertracing/all-in-one:latest

2. Configure environment:
   export OTEL_TRACES_ENABLED=true
   export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
   export OTEL_SERVICE_NAME=rae-memory-api

3. View traces:
   http://localhost:16686


=== Grafana Cloud Tempo ===

1. Get OTLP endpoint and API key from Grafana Cloud

2. Configure environment:
   export OTEL_TRACES_ENABLED=true
   export OTEL_EXPORTER_OTLP_ENDPOINT=https://tempo-prod-xx-xxx.grafana.net:443
   export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Basic <base64-api-key>"


=== Elastic APM ===

1. Get APM Server URL and secret token

2. Configure environment:
   export OTEL_TRACES_ENABLED=true
   export OTEL_EXPORTER_OTLP_ENDPOINT=https://apm-server:8200
   export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer <secret-token>"


=== AWS X-Ray (via ADOT Collector) ===

1. Deploy AWS Distro for OpenTelemetry Collector

2. Configure environment:
   export OTEL_TRACES_ENABLED=true
   export OTEL_EXPORTER_OTLP_ENDPOINT=http://adot-collector:4317


=== Kubernetes with Tempo ===

apiVersion: v1
kind: ConfigMap
metadata:
  name: rae-otel-config
data:
  OTEL_TRACES_ENABLED: "true"
  OTEL_EXPORTER_OTLP_ENDPOINT: "http://tempo:4317"
  OTEL_SERVICE_NAME: "rae-memory-api"

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rae-api
spec:
  template:
    spec:
      containers:
      - name: api
        envFrom:
        - configMapRef:
            name: rae-otel-config
"""


# ============================================================================
# Trace Context Propagation
# ============================================================================

"""
For distributed tracing across services, trace context is automatically
propagated via W3C TraceContext headers:

- traceparent: 00-<trace-id>-<span-id>-<flags>
- tracestate: <vendor-specific-state>

When calling external services or Celery tasks, ensure these headers
are forwarded to maintain the trace chain.

Example with httpx:
    from opentelemetry.propagate import inject

    headers = {}
    inject(headers)  # Adds traceparent/tracestate
    response = await httpx.get(url, headers=headers)

Example with Celery:
    from opentelemetry.propagate import inject

    headers = {}
    inject(headers)
    task.apply_async(args=(...), headers=headers)
"""
