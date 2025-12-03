"""
Memory Tracing Utilities for RAE

This module provides specialized tracing for RAE's memory operations:
- Episodic memory (event storage and retrieval)
- Semantic memory (knowledge extraction and search)
- Graph memory (entity relationships and traversal)
- Reflective memory (reasoning and polishing pipeline)

Traces include:
- Memory layer and operation type
- Vector/node/edge counts
- Reasoning depth and iterations
- Token usage and costs
- Query parameters and performance metrics
"""

import functools
import time
from contextlib import contextmanager
from typing import Any, Callable, Dict, Optional

import structlog

from .opentelemetry_config import (
    OPENTELEMETRY_AVAILABLE,
    get_tracer,
    record_exception,
)

logger = structlog.get_logger(__name__)


# ============================================================================
# Memory Layer Tracer
# ============================================================================


class MemoryTracer:
    """
    Specialized tracer for RAE memory operations.

    Provides context-aware tracing for different memory layers with
    automatic attribute collection and performance tracking.
    """

    # Memory layer constants
    LAYER_EPISODIC = "episodic"
    LAYER_SEMANTIC = "semantic"
    LAYER_GRAPH = "graph"
    LAYER_REFLECTIVE = "reflective"

    # Operation types
    OP_CREATE = "create"
    OP_READ = "read"
    OP_UPDATE = "update"
    OP_DELETE = "delete"
    OP_SEARCH = "search"
    OP_EXTRACT = "extract"
    OP_REASON = "reason"
    OP_POLISH = "polish"
    OP_EVALUATE = "evaluate"

    def __init__(self):
        """Initialize memory tracer."""
        self.tracer = get_tracer("rae.memory") if OPENTELEMETRY_AVAILABLE else None

    @contextmanager
    def trace_operation(
        self,
        layer: str,
        operation: str,
        **attributes,
    ):
        """
        Create a span for a memory operation.

        Args:
            layer: Memory layer (episodic, semantic, graph, reflective)
            operation: Operation type (create, read, search, etc.)
            **attributes: Additional span attributes

        Example:
            with tracer.trace_operation("semantic", "search", query="test"):
                results = search_semantic_memory(query)
        """
        if not self.tracer:
            yield None
            return

        span_name = f"memory.{layer}.{operation}"
        start_time = time.time()

        with self.tracer.start_as_current_span(span_name) as span:
            # Set base attributes
            span.set_attribute("memory.layer", layer)
            span.set_attribute("memory.operation", operation)

            # Set additional attributes
            for key, value in attributes.items():
                if value is not None:
                    span.set_attribute(f"memory.{key}", value)

            try:
                yield span
            except Exception as e:
                span.set_attribute("error", True)
                span.set_attribute("error.type", type(e).__name__)
                span.set_attribute("error.message", str(e))
                record_exception(e)
                raise
            finally:
                # Record latency
                latency_ms = (time.time() - start_time) * 1000
                span.set_attribute("memory.latency_ms", round(latency_ms, 2))

    def record_vector_operation(
        self,
        span,
        vector_count: int,
        dimension: Optional[int] = None,
        similarity_threshold: Optional[float] = None,
    ):
        """
        Record vector operation metrics.

        Args:
            span: Current span
            vector_count: Number of vectors processed
            dimension: Vector dimension
            similarity_threshold: Similarity threshold used
        """
        if not span:
            return

        span.set_attribute("memory.vector_count", vector_count)
        if dimension:
            span.set_attribute("memory.vector_dimension", dimension)
        if similarity_threshold:
            span.set_attribute("memory.similarity_threshold", similarity_threshold)

    def record_graph_operation(
        self,
        span,
        node_count: int = 0,
        edge_count: int = 0,
        traversal_depth: Optional[int] = None,
    ):
        """
        Record graph operation metrics.

        Args:
            span: Current span
            node_count: Number of nodes processed
            edge_count: Number of edges processed
            traversal_depth: Graph traversal depth
        """
        if not span:
            return

        if node_count > 0:
            span.set_attribute("memory.graph_nodes", node_count)
        if edge_count > 0:
            span.set_attribute("memory.graph_edges", edge_count)
        if traversal_depth:
            span.set_attribute("memory.graph_traversal_depth", traversal_depth)

    def record_reasoning_operation(
        self,
        span,
        iteration: int,
        depth: int,
        confidence_score: Optional[float] = None,
    ):
        """
        Record reasoning operation metrics.

        Args:
            span: Current span
            iteration: Current reasoning iteration
            depth: Reasoning depth
            confidence_score: Confidence score of reasoning result
        """
        if not span:
            return

        span.set_attribute("memory.reasoning_iteration", iteration)
        span.set_attribute("memory.reasoning_depth", depth)
        if confidence_score is not None:
            span.set_attribute("memory.reasoning_confidence", confidence_score)

    def record_tokens(
        self,
        span,
        input_tokens: int,
        output_tokens: int,
        cost_usd: Optional[float] = None,
    ):
        """
        Record token usage and cost.

        Args:
            span: Current span
            input_tokens: Input token count
            output_tokens: Output token count
            cost_usd: Cost in USD
        """
        if not span:
            return

        span.set_attribute("memory.tokens_input", input_tokens)
        span.set_attribute("memory.tokens_output", output_tokens)
        span.set_attribute("memory.tokens_total", input_tokens + output_tokens)
        if cost_usd is not None:
            span.set_attribute("memory.cost_usd", cost_usd)


# Global memory tracer instance
_memory_tracer = MemoryTracer()


# ============================================================================
# Decorator for Memory Operations
# ============================================================================


def trace_memory(
    layer: str,
    operation: Optional[str] = None,
    extract_params: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
):
    """
    Decorator to trace memory operations.

    Args:
        layer: Memory layer (episodic, semantic, graph, reflective)
        operation: Operation type (auto-detected from function name if not provided)
        extract_params: Optional function to extract span attributes from function args

    Example:
        @trace_memory(layer="semantic", operation="search")
        async def search_semantic_memory(query: str, limit: int = 10):
            # ... implementation ...
            return results

        @trace_memory(
            layer="graph",
            extract_params=lambda kwargs: {"entity_type": kwargs.get("entity_type")}
        )
        async def extract_entities(text: str, entity_type: str):
            # ... implementation ...
            return entities
    """

    def decorator(func: Callable) -> Callable:
        # Auto-detect operation from function name if not provided
        op = operation or _infer_operation(func.__name__)

        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Extract additional attributes from function parameters
            attrs = extract_params(kwargs) if extract_params else {}

            with _memory_tracer.trace_operation(layer, op, **attrs) as span:
                result = await func(*args, **kwargs)

                # Try to extract metrics from result if it's a dict
                if isinstance(result, dict) and span:
                    _extract_result_metrics(span, result, layer)

                return result

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Extract additional attributes from function parameters
            attrs = extract_params(kwargs) if extract_params else {}

            with _memory_tracer.trace_operation(layer, op, **attrs) as span:
                result = func(*args, **kwargs)

                # Try to extract metrics from result if it's a dict
                if isinstance(result, dict) and span:
                    _extract_result_metrics(span, result, layer)

                return result

        # Return appropriate wrapper based on function type
        if functools.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def _infer_operation(func_name: str) -> str:
    """Infer operation type from function name."""
    func_lower = func_name.lower()

    if any(x in func_lower for x in ["create", "store", "add", "insert", "upsert"]):
        return MemoryTracer.OP_CREATE
    elif any(x in func_lower for x in ["get", "retrieve", "fetch", "read", "load"]):
        return MemoryTracer.OP_READ
    elif any(x in func_lower for x in ["update", "modify", "edit"]):
        return MemoryTracer.OP_UPDATE
    elif any(x in func_lower for x in ["delete", "remove", "drop"]):
        return MemoryTracer.OP_DELETE
    elif any(x in func_lower for x in ["search", "query", "find"]):
        return MemoryTracer.OP_SEARCH
    elif any(x in func_lower for x in ["extract", "parse"]):
        return MemoryTracer.OP_EXTRACT
    elif any(x in func_lower for x in ["reason", "think", "infer"]):
        return MemoryTracer.OP_REASON
    elif any(x in func_lower for x in ["polish", "refine", "improve"]):
        return MemoryTracer.OP_POLISH
    elif any(x in func_lower for x in ["evaluate", "assess", "score"]):
        return MemoryTracer.OP_EVALUATE
    else:
        return "unknown"


def _extract_result_metrics(span, result: Dict[str, Any], layer: str):
    """Extract metrics from result dictionary."""
    # Common metrics
    if "count" in result:
        span.set_attribute("memory.result_count", result["count"])
    if "total" in result:
        span.set_attribute("memory.result_total", result["total"])

    # Vector metrics
    if layer in [MemoryTracer.LAYER_SEMANTIC, MemoryTracer.LAYER_EPISODIC]:
        if "vectors" in result:
            span.set_attribute("memory.vector_count", len(result["vectors"]))
        if "similarity_scores" in result:
            scores = result["similarity_scores"]
            if scores:
                span.set_attribute("memory.max_similarity", max(scores))
                span.set_attribute("memory.avg_similarity", sum(scores) / len(scores))

    # Graph metrics
    if layer == MemoryTracer.LAYER_GRAPH:
        if "nodes" in result:
            span.set_attribute("memory.graph_nodes", len(result["nodes"]))
        if "edges" in result:
            span.set_attribute("memory.graph_edges", len(result["edges"]))
        if "communities" in result:
            span.set_attribute("memory.graph_communities", len(result["communities"]))

    # Reasoning metrics
    if layer == MemoryTracer.LAYER_REFLECTIVE:
        if "iterations" in result:
            span.set_attribute("memory.reasoning_iterations", result["iterations"])
        if "confidence" in result:
            span.set_attribute("memory.reasoning_confidence", result["confidence"])
        if "tokens_used" in result:
            span.set_attribute("memory.tokens_total", result["tokens_used"])
        if "cost" in result:
            span.set_attribute("memory.cost_usd", result["cost"])


# ============================================================================
# Convenience Functions
# ============================================================================


def get_memory_tracer() -> MemoryTracer:
    """
    Get the global memory tracer instance.

    Returns:
        MemoryTracer instance

    Example:
        tracer = get_memory_tracer()
        with tracer.trace_operation("semantic", "search"):
            results = perform_search()
    """
    return _memory_tracer


def trace_episodic_operation(operation: str, **attributes):
    """
    Context manager for episodic memory operations.

    Args:
        operation: Operation type
        **attributes: Additional span attributes
    """
    return _memory_tracer.trace_operation(
        MemoryTracer.LAYER_EPISODIC, operation, **attributes
    )


def trace_semantic_operation(operation: str, **attributes):
    """
    Context manager for semantic memory operations.

    Args:
        operation: Operation type
        **attributes: Additional span attributes
    """
    return _memory_tracer.trace_operation(
        MemoryTracer.LAYER_SEMANTIC, operation, **attributes
    )


def trace_graph_operation(operation: str, **attributes):
    """
    Context manager for graph memory operations.

    Args:
        operation: Operation type
        **attributes: Additional span attributes
    """
    return _memory_tracer.trace_operation(
        MemoryTracer.LAYER_GRAPH, operation, **attributes
    )


def trace_reflective_operation(operation: str, **attributes):
    """
    Context manager for reflective memory operations.

    Args:
        operation: Operation type
        **attributes: Additional span attributes
    """
    return _memory_tracer.trace_operation(
        MemoryTracer.LAYER_REFLECTIVE, operation, **attributes
    )


# ============================================================================
# Usage Examples
# ============================================================================

"""
# Example 1: Using decorator
@trace_memory(layer="semantic", operation="search")
async def search_memories(query: str, limit: int = 10):
    results = await vector_search(query, limit)
    return results

# Example 2: Using context manager
async def extract_entities(text: str):
    tracer = get_memory_tracer()
    with tracer.trace_operation("graph", "extract") as span:
        entities = await llm_extract(text)
        tracer.record_graph_operation(span, node_count=len(entities))
        tracer.record_tokens(span, input_tokens=100, output_tokens=50, cost_usd=0.001)
        return entities

# Example 3: Tracing reasoning pipeline
async def reflection_pipeline(memory_id: str):
    tracer = get_memory_tracer()

    with tracer.trace_operation("reflective", "reason") as parent_span:
        # Evaluation step
        with tracer.trace_operation("reflective", "evaluate") as eval_span:
            evaluation = await evaluate_memory(memory_id)
            tracer.record_reasoning_operation(eval_span, iteration=1, depth=1)
            tracer.record_tokens(eval_span, input_tokens=200, output_tokens=100)

        # Polish step
        with tracer.trace_operation("reflective", "polish") as polish_span:
            polished = await polish_memory(memory_id, evaluation)
            tracer.record_reasoning_operation(polish_span, iteration=2, depth=1)
            tracer.record_tokens(polish_span, input_tokens=300, output_tokens=150)

        tracer.record_reasoning_operation(parent_span, iteration=2, depth=2)
        return polished

# Example 4: Custom parameter extraction
@trace_memory(
    layer="graph",
    operation="search",
    extract_params=lambda kwargs: {
        "entity_type": kwargs.get("entity_type"),
        "max_depth": kwargs.get("max_depth", 3)
    }
)
async def traverse_graph(start_node: str, entity_type: str, max_depth: int = 3):
    path = await graph_traversal(start_node, entity_type, max_depth)
    return {"nodes": path, "depth": len(path)}
"""
