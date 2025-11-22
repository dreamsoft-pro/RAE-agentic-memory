"""
Cost Guard Middleware v3.0 - Enterprise Budget Enforcement & Audit Trail

This middleware provides comprehensive cost and token tracking for all LLM API calls:
- Pre-flight budget checks (USD and tokens)
- Post-execution budget increments
- Complete audit logging via cost_logs table
- Automatic cost calculation if LLM returns 0
- Dry-run mode for testing
- Prometheus metrics integration

Key Improvements over v2.0:
- Uses unified calculate_cost() for all providers (fixes $0.00 bug)
- Tracks tokens in addition to USD costs
- Logs every LLM call to cost_logs table
- Extracts model/provider/operation metadata
- Validates and corrects LLM-reported costs
"""

from functools import wraps
from typing import Optional
from fastapi import HTTPException, Request
import json
import structlog

from apps.memory_api.services import budget_service
from apps.memory_api.services.cost_controller import calculate_cost, estimate_cost, validate_cost_calculation
from apps.memory_api.repositories import cost_logs_repository
from apps.memory_api.repositories.cost_logs_repository import LogLLMCallParams
from apps.memory_api.services.budget_service import BudgetUsageIncrement
from apps.memory_api.metrics import (
    llm_cost_counter,
    rae_cost_llm_total_usd,
    rae_cost_llm_daily_usd,
    rae_cost_llm_monthly_usd,
    rae_cost_llm_tokens_used,
    rae_cost_cache_saved_usd,
    rae_cost_budget_rejections_total,
    rae_cost_llm_calls_total,
    rae_cost_tokens_per_call_histogram
)
from apps.memory_api.models import AgentExecuteResponse, AgentExecuteRequest

logger = structlog.get_logger(__name__)


# ============================================================================
# Helper Functions
# ============================================================================

def extract_model_info(request_body: AgentExecuteRequest) -> dict:
    """
    Extracts model name, provider, and operation from request.

    Returns:
        Dictionary with model, provider, operation, estimated_input_tokens
    """
    # Default values
    model_name = "gpt-4o-mini"  # Default model
    provider = "openai"
    operation = "query"
    estimated_input_tokens = 2000  # Conservative estimate
    estimated_output_tokens = 1000  # Conservative estimate

    # Extract from request if available
    if hasattr(request_body, 'model') and request_body.model:
        model_name = request_body.model

    # Determine provider from model name
    if "gpt" in model_name.lower() or "o1" in model_name.lower():
        provider = "openai"
    elif "claude" in model_name.lower():
        provider = "anthropic"
    elif "gemini" in model_name.lower():
        provider = "google"
    elif "ollama" in model_name.lower() or "phi" in model_name.lower():
        provider = "ollama"

    # Determine operation type
    if hasattr(request_body, 'operation_type') and request_body.operation_type:
        operation = request_body.operation_type
    elif hasattr(request_body, 'query') and request_body.query:
        operation = "query"

    # Estimate input tokens from query length (rough: 1 token ≈ 4 chars)
    if hasattr(request_body, 'query') and request_body.query:
        estimated_input_tokens = max(len(request_body.query) // 4, 100)
    elif hasattr(request_body, 'prompt') and request_body.prompt:
        estimated_input_tokens = max(len(request_body.prompt) // 4, 100)

    return {
        "model": model_name,
        "provider": provider,
        "operation": operation,
        "estimated_input_tokens": estimated_input_tokens,
        "estimated_output_tokens": estimated_output_tokens
    }


def extract_actual_tokens(response: AgentExecuteResponse) -> dict:
    """
    Extracts actual token usage from LLM response.

    Returns:
        Dictionary with input_tokens, output_tokens
    """
    input_tokens = 0
    output_tokens = 0

    # Try to extract from response.cost if available
    if hasattr(response, 'cost') and response.cost:
        if hasattr(response.cost, 'input_tokens'):
            input_tokens = response.cost.input_tokens or 0
        if hasattr(response.cost, 'output_tokens'):
            output_tokens = response.cost.output_tokens or 0

    # Fallback: estimate from response length if tokens not provided
    if input_tokens == 0 and output_tokens == 0:
        if hasattr(response, 'content') and response.content:
            output_tokens = max(len(str(response.content)) // 4, 50)
        if hasattr(response, 'result') and response.result:
            output_tokens = max(len(str(response.result)) // 4, 50)

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens
    }


# ============================================================================
# Cost Guard Decorator
# ============================================================================

def cost_guard():
    """
    Cost Guard v3.0: Enterprise-grade budget enforcement and audit trail.

    Features:
    - Pre-flight budget checks for both USD and tokens
    - Post-execution cost and token tracking
    - Complete audit logging to cost_logs table
    - Automatic cost calculation if LLM returns 0 (fixes $0.00 bug)
    - Dry-run mode for testing without budget enforcement
    - Comprehensive error handling and logging

    Usage:
        @cost_guard()
        async def agent_execute(self, request: AgentExecuteRequest):
            # Your LLM call here
            return response

    HTTP Headers:
        X-Dry-Run: "true" - Skip budget enforcement (for testing)

    Raises:
        HTTPException(402) - If budget exceeded (USD or tokens)
        HTTPException(400) - If request body invalid
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request object (second positional argument)
            request: Request = args[1]

            # Read request body (FastAPI requires this workaround)
            body_bytes = await request.body()
            request._body = body_bytes

            try:
                req_body_dict = json.loads(body_bytes)
                req_body = AgentExecuteRequest(**req_body_dict)
            except (json.JSONDecodeError, TypeError, ValueError) as e:
                logger.error("cost_guard_invalid_request", error=str(e))
                raise HTTPException(status_code=400, detail="Invalid request body.")

            # Extract metadata
            is_dry_run = request.headers.get("X-Dry-Run", "false").lower() == "true"
            pool = request.app.state.pool
            tenant_id = req_body.tenant_id
            project_id = req_body.project
            request_id = request.headers.get("X-Request-ID", "unknown")

            # Extract model information from request
            model_info = extract_model_info(req_body)
            model_name = model_info["model"]
            provider = model_info["provider"]
            operation = model_info["operation"]

            logger.info(
                "cost_guard_pre_execution",
                tenant_id=tenant_id,
                project_id=project_id,
                model=model_name,
                provider=provider,
                operation=operation,
                dry_run=is_dry_run
            )

            # ================================================================
            # PRE-EXECUTION: Budget Check
            # ================================================================

            # Estimate cost and tokens for budget check
            estimated_cost = estimate_cost(
                model_name,
                model_info["estimated_input_tokens"],
                model_info["estimated_output_tokens"]
            )
            estimated_tokens = (
                model_info["estimated_input_tokens"] +
                model_info["estimated_output_tokens"]
            )

            logger.info(
                "cost_guard_estimate",
                estimated_cost_usd=estimated_cost,
                estimated_tokens=estimated_tokens,
                model=model_name
            )

            if not is_dry_run:
                # Check budget (raises HTTPException(402) if exceeded)
                try:
                    await budget_service.check_budget(
                        pool,
                        tenant_id,
                        project_id,
                        estimated_cost,
                        estimated_tokens
                    )
                    logger.info("cost_guard_budget_check_passed", tenant_id=tenant_id)
                except HTTPException as e:
                    # Determine which limit was exceeded
                    limit_type = "unknown"
                    if isinstance(e.detail, dict) and "error" in e.detail:
                        error_type = e.detail["error"]
                        if "daily_usd" in error_type:
                            limit_type = "daily_usd"
                        elif "monthly_usd" in error_type:
                            limit_type = "monthly_usd"
                        elif "daily_token" in error_type:
                            limit_type = "daily_tokens"
                        elif "monthly_token" in error_type:
                            limit_type = "monthly_tokens"

                    # Track budget rejection in Prometheus
                    rae_cost_budget_rejections_total.labels(
                        tenant_id=tenant_id,
                        project=project_id,
                        limit_type=limit_type
                    ).inc()

                    logger.warning(
                        "cost_guard_budget_exceeded",
                        tenant_id=tenant_id,
                        project_id=project_id,
                        estimated_cost=estimated_cost,
                        estimated_tokens=estimated_tokens,
                        limit_type=limit_type,
                        error=e.detail
                    )
                    raise

            # ================================================================
            # EXECUTE: Call the actual function
            # ================================================================

            response: AgentExecuteResponse = await func(*args, **kwargs)

            # ================================================================
            # POST-EXECUTION: Cost Tracking & Audit Logging
            # ================================================================

            # Extract actual token usage from response
            actual_tokens = extract_actual_tokens(response)
            input_tokens = actual_tokens["input_tokens"]
            output_tokens = actual_tokens["output_tokens"]

            # Get LLM-reported cost (often returns 0)
            llm_reported_cost = 0.0
            if hasattr(response, 'cost') and response.cost:
                llm_reported_cost = response.cost.total_estimate or 0.0

            # Calculate actual cost using our cost model
            cost_info = calculate_cost(
                model_name,
                input_tokens,
                output_tokens,
                cache_hit=False  # TODO: Detect cache hits from response
            )

            actual_cost_usd = cost_info["total_cost_usd"]
            input_cost_per_million = cost_info["input_cost_per_million"]
            output_cost_per_million = cost_info["output_cost_per_million"]

            # Validate LLM-reported cost against our calculation
            if llm_reported_cost > 0:
                is_valid = validate_cost_calculation(
                    model_name,
                    input_tokens,
                    output_tokens,
                    llm_reported_cost,
                    tolerance=0.0001
                )
                if not is_valid:
                    logger.warning(
                        "cost_guard_cost_mismatch",
                        model=model_name,
                        our_cost=actual_cost_usd,
                        llm_reported=llm_reported_cost,
                        message="Using our cost calculation instead of LLM-reported cost"
                    )
            else:
                # LLM returned 0 (common with litellm) - use our calculation
                logger.info(
                    "cost_guard_forced_calculation",
                    model=model_name,
                    calculated_cost=actual_cost_usd,
                    message="LLM returned $0.00, using our cost model"
                )

            logger.info(
                "cost_guard_post_execution",
                tenant_id=tenant_id,
                model=model_name,
                actual_cost_usd=actual_cost_usd,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=input_tokens + output_tokens
            )

            # ================================================================
            # AUDIT LOG: Write to cost_logs table
            # ================================================================

            try:
                log_id = await cost_logs_repository.log_llm_call(
                    pool,
                    LogLLMCallParams(
                        tenant_id=tenant_id,
                        project_id=project_id,
                        model=model_name,
                        provider=provider,
                        operation=operation,
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                        input_cost_per_million=input_cost_per_million,
                        output_cost_per_million=output_cost_per_million,
                        total_cost_usd=actual_cost_usd,
                        cache_hit=False,  # TODO: Detect cache hits
                        cache_tokens_saved=0,
                        request_id=request_id,
                        error=False,
                        error_message=None
                    )
                )
                logger.info("cost_guard_logged", log_id=log_id)
            except Exception as e:
                logger.error(
                    "cost_guard_log_failed",
                    error=str(e),
                    tenant_id=tenant_id,
                    message="Failed to write to cost_logs, but continuing"
                )
                # Don't fail the request if logging fails

            # ================================================================
            # BUDGET INCREMENT: Update budgets table
            # ================================================================

            if not is_dry_run:
                try:
                    await budget_service.increment_usage(
                        pool,
                        tenant_id,
                        project_id,
                        BudgetUsageIncrement(
                            cost_usd=actual_cost_usd,
                            input_tokens=input_tokens,
                            output_tokens=output_tokens
                        )
                    )
                    logger.info(
                        "cost_guard_budget_incremented",
                        tenant_id=tenant_id,
                        cost_usd=actual_cost_usd,
                        tokens=input_tokens + output_tokens
                    )
                except Exception as e:
                    logger.error(
                        "cost_guard_increment_failed",
                        error=str(e),
                        tenant_id=tenant_id,
                        message="Failed to increment budget"
                    )
                    # Don't fail the request if budget increment fails

                # ================================================================
                # PROMETHEUS METRICS: Update counters
                # ================================================================

                try:
                    # Legacy metric (keep for backwards compatibility)
                    llm_cost_counter.labels(
                        tenant_id=tenant_id,
                        project=project_id
                    ).inc(actual_cost_usd)

                    # 1. Total cumulative LLM costs
                    rae_cost_llm_total_usd.labels(
                        tenant_id=tenant_id,
                        project=project_id,
                        model=model_name,
                        provider=provider
                    ).inc(actual_cost_usd)

                    # 2. Total cumulative tokens used
                    rae_cost_llm_tokens_used.labels(
                        tenant_id=tenant_id,
                        project=project_id,
                        model=model_name,
                        provider=provider
                    ).inc(input_tokens + output_tokens)

                    # 3. LLM call counter
                    rae_cost_llm_calls_total.labels(
                        tenant_id=tenant_id,
                        project=project_id,
                        model=model_name,
                        provider=provider,
                        operation=operation
                    ).inc()

                    # 4. Token distribution histogram
                    rae_cost_tokens_per_call_histogram.labels(
                        model=model_name,
                        provider=provider
                    ).observe(input_tokens + output_tokens)

                    # 5. Daily/Monthly costs (gauges) - fetch from budgets table
                    try:
                        from apps.memory_api.repositories import cost_logs_repository
                        daily_cost = await cost_logs_repository.get_daily_cost(pool, tenant_id, project_id)
                        monthly_cost = await cost_logs_repository.get_monthly_cost(pool, tenant_id, project_id)

                        rae_cost_llm_daily_usd.labels(
                            tenant_id=tenant_id,
                            project=project_id
                        ).set(daily_cost)

                        rae_cost_llm_monthly_usd.labels(
                            tenant_id=tenant_id,
                            project=project_id
                        ).set(monthly_cost)
                    except Exception as gauge_error:
                        logger.warning("cost_guard_gauge_update_failed", error=str(gauge_error))

                    # 6. Cache savings (if cache hit detected)
                    # TODO: Implement cache hit detection and savings calculation

                except Exception as e:
                    logger.error("cost_guard_metrics_failed", error=str(e))

                logger.info(
                    "cost_guard_complete",
                    tenant_id=tenant_id,
                    cost_usd=actual_cost_usd,
                    tokens=input_tokens + output_tokens,
                    message=f"Logged ${actual_cost_usd:.6f} for project {project_id}"
                )
            else:
                logger.info(
                    "cost_guard_dry_run_complete",
                    estimated_cost=actual_cost_usd,
                    message=f"Dry Run: Estimated cost is ${actual_cost_usd:.6f}"
                )

            return response

        return wrapper
    return decorator
