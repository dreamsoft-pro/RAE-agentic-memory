"""
Enterprise Budget Service - Enhanced with Token Tracking

This service provides comprehensive budget management including:
- USD cost tracking (daily/monthly)
- Token usage tracking (daily/monthly)
- Automatic counter resets
- Budget enforcement with detailed error messages
- Integration with cost_logs for audit trail
"""

from datetime import datetime
from typing import Optional

import asyncpg
import structlog
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field

logger = structlog.get_logger(__name__)


class Budget(BaseModel):
    """Enhanced Budget model with token tracking"""

    id: str
    tenant_id: str
    project_id: str

    # USD Limits
    monthly_limit_usd: Optional[float] = Field(
        None, description="Monthly USD limit (NULL = unlimited)"
    )
    daily_limit_usd: Optional[float] = Field(
        None, description="Daily USD limit (NULL = unlimited)"
    )

    # USD Usage
    monthly_usage_usd: float = Field(0.0, ge=0, description="Current monthly USD usage")
    daily_usage_usd: float = Field(0.0, ge=0, description="Current daily USD usage")

    # Token Limits (NEW)
    monthly_tokens_limit: Optional[int] = Field(
        None, description="Monthly token limit (NULL = unlimited)"
    )
    daily_tokens_limit: Optional[int] = Field(
        None, description="Daily token limit (NULL = unlimited)"
    )

    # Token Usage (NEW)
    monthly_tokens_used: int = Field(0, ge=0, description="Current monthly tokens used")
    daily_tokens_used: int = Field(0, ge=0, description="Current daily tokens used")

    # Timestamps
    created_at: datetime
    last_usage_at: datetime
    last_token_update_at: datetime
    last_daily_reset: datetime
    last_monthly_reset: datetime

    model_config = ConfigDict(from_attributes=True)


class BudgetUsageIncrement(BaseModel):
    """Data model for incrementing budget usage"""

    cost_usd: float = Field(..., ge=0, description="Cost in USD to increment")
    input_tokens: int = Field(..., ge=0, description="Number of input tokens")
    output_tokens: int = Field(..., ge=0, description="Number of output tokens")

    @property
    def total_tokens(self) -> int:
        """Total tokens = input + output"""
        return self.input_tokens + self.output_tokens


class BudgetService:
    """Service class for budget management (wrapper around standalone functions)."""

    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool

    async def get_or_create_budget(
        self, tenant_id: str, project_id: str = "default"
    ) -> Budget:
        return await get_or_create_budget(self.pool, tenant_id, project_id)

    async def check_budget_exceeded(
        self, tenant_id: str, project_id: str = "default"
    ) -> tuple[bool, float, float]:
        """
        Check if budget is exceeded for a tenant.
        Returns: (is_exceeded, remaining_budget, total_limit)
        """
        budget = await self.get_or_create_budget(tenant_id, project_id)

        # Check monthly limit
        if budget.monthly_limit_usd is not None:
            remaining = budget.monthly_limit_usd - budget.monthly_usage_usd
            if remaining <= 0:
                return True, 0.0, budget.monthly_limit_usd

        # Check daily limit
        if budget.daily_limit_usd is not None:
            remaining = budget.daily_limit_usd - budget.daily_usage_usd
            if remaining <= 0:
                return True, 0.0, budget.daily_limit_usd

        return False, 999999.0, 999999.0  # Not exceeded or unlimited


async def get_or_create_budget(
    pool: asyncpg.Pool, tenant_id: str, project_id: str
) -> Budget:
    """
    Retrieves the budget for a tenant/project, creating a new one with default limits if it doesn't exist.

    Args:
        pool: Database connection pool
        tenant_id: Tenant identifier
        project_id: Project identifier

    Returns:
        Budget object with current usage and limits

    Note:
        The trigger `trigger_reset_budget_counters` automatically resets daily/monthly counters
        at day/month boundaries when the budget is fetched.
    """
    logger.info("get_or_create_budget", tenant_id=tenant_id, project_id=project_id)

    # Try to fetch existing budget
    record = await pool.fetchrow(
        """
        SELECT * FROM budgets
        WHERE tenant_id = $1 AND project_id = $2
        """,
        tenant_id,
        project_id,
    )

    if not record:
        # Create new budget with default limits (can be customized via ENV or admin API)
        logger.info("creating_new_budget", tenant_id=tenant_id, project_id=project_id)
        record = await pool.fetchrow(
            """
            INSERT INTO budgets (
                tenant_id,
                project_id,
                daily_limit_usd,
                monthly_limit_usd,
                daily_tokens_limit,
                monthly_tokens_limit
            ) VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING *
            """,
            tenant_id,
            project_id,
            None,  # No daily USD limit by default
            None,  # No monthly USD limit by default
            None,  # No daily token limit by default
            None,  # No monthly token limit by default
        )
        logger.info(
            "budget_created",
            tenant_id=tenant_id,
            project_id=project_id,
            budget_id=record["id"],
        )

    return Budget(**dict(record))


async def check_budget(
    pool: asyncpg.Pool, tenant_id: str, project_id: str, cost_usd: float, tokens: int
) -> None:
    """
    Checks if a new cost and token usage is within the budget.

    Raises HTTPException(402 Payment Required) if either USD or token budget is exceeded.

    Args:
        pool: Database connection pool
        tenant_id: Tenant identifier
        project_id: Project identifier
        cost_usd: Estimated cost in USD
        tokens: Estimated total tokens (input + output)

    Raises:
        HTTPException: 402 if budget exceeded (includes detailed message)

    Note:
        This performs a pre-flight check. The actual increment happens in increment_usage().
    """
    logger.info(
        "check_budget",
        tenant_id=tenant_id,
        project_id=project_id,
        cost_usd=cost_usd,
        tokens=tokens,
    )

    budget = await get_or_create_budget(pool, tenant_id, project_id)
    now = datetime.now()

    # Automatic reset handled by database trigger, but we double-check here for safety
    if budget.last_daily_reset.date() < now.date():
        logger.info(
            "resetting_daily_counters", tenant_id=tenant_id, project_id=project_id
        )
        budget.daily_usage_usd = 0.0
        budget.daily_tokens_used = 0

    if (budget.last_monthly_reset.year < now.year) or (
        budget.last_monthly_reset.year == now.year
        and budget.last_monthly_reset.month < now.month
    ):
        logger.info(
            "resetting_monthly_counters", tenant_id=tenant_id, project_id=project_id
        )
        budget.monthly_usage_usd = 0.0
        budget.monthly_tokens_used = 0

    # Check USD limits
    if budget.daily_limit_usd is not None:
        projected_daily_usd = budget.daily_usage_usd + cost_usd
        if projected_daily_usd > budget.daily_limit_usd:
            logger.warning(
                "daily_usd_budget_exceeded",
                tenant_id=tenant_id,
                project_id=project_id,
                current_usage=budget.daily_usage_usd,
                limit=budget.daily_limit_usd,
                requested_cost=cost_usd,
                projected=projected_daily_usd,
            )
            raise HTTPException(
                status_code=402,  # Payment Required
                detail={
                    "error": "daily_usd_budget_exceeded",
                    "message": f"Daily USD budget exceeded for project '{project_id}'",
                    "current_usage_usd": float(budget.daily_usage_usd),
                    "daily_limit_usd": float(budget.daily_limit_usd),
                    "requested_cost_usd": float(cost_usd),
                    "projected_usage_usd": float(projected_daily_usd),
                    "available_usd": float(
                        budget.daily_limit_usd - budget.daily_usage_usd
                    ),
                },
            )

    if budget.monthly_limit_usd is not None:
        projected_monthly_usd = budget.monthly_usage_usd + cost_usd
        if projected_monthly_usd > budget.monthly_limit_usd:
            logger.warning(
                "monthly_usd_budget_exceeded",
                tenant_id=tenant_id,
                project_id=project_id,
                current_usage=budget.monthly_usage_usd,
                limit=budget.monthly_limit_usd,
                requested_cost=cost_usd,
                projected=projected_monthly_usd,
            )
            raise HTTPException(
                status_code=402,
                detail={
                    "error": "monthly_usd_budget_exceeded",
                    "message": f"Monthly USD budget exceeded for project '{project_id}'",
                    "current_usage_usd": float(budget.monthly_usage_usd),
                    "monthly_limit_usd": float(budget.monthly_limit_usd),
                    "requested_cost_usd": float(cost_usd),
                    "projected_usage_usd": float(projected_monthly_usd),
                    "available_usd": float(
                        budget.monthly_limit_usd - budget.monthly_usage_usd
                    ),
                },
            )

    # Check Token limits (NEW)
    if budget.daily_tokens_limit is not None:
        projected_daily_tokens = budget.daily_tokens_used + tokens
        if projected_daily_tokens > budget.daily_tokens_limit:
            logger.warning(
                "daily_token_budget_exceeded",
                tenant_id=tenant_id,
                project_id=project_id,
                current_usage=budget.daily_tokens_used,
                limit=budget.daily_tokens_limit,
                requested_tokens=tokens,
                projected=projected_daily_tokens,
            )
            raise HTTPException(
                status_code=402,
                detail={
                    "error": "daily_token_budget_exceeded",
                    "message": f"Daily token budget exceeded for project '{project_id}'",
                    "current_tokens_used": budget.daily_tokens_used,
                    "daily_tokens_limit": budget.daily_tokens_limit,
                    "requested_tokens": tokens,
                    "projected_tokens_used": projected_daily_tokens,
                    "available_tokens": budget.daily_tokens_limit
                    - budget.daily_tokens_used,
                },
            )

    if budget.monthly_tokens_limit is not None:
        projected_monthly_tokens = budget.monthly_tokens_used + tokens
        if projected_monthly_tokens > budget.monthly_tokens_limit:
            logger.warning(
                "monthly_token_budget_exceeded",
                tenant_id=tenant_id,
                project_id=project_id,
                current_usage=budget.monthly_tokens_used,
                limit=budget.monthly_tokens_limit,
                requested_tokens=tokens,
                projected=projected_monthly_tokens,
            )
            raise HTTPException(
                status_code=402,
                detail={
                    "error": "monthly_token_budget_exceeded",
                    "message": f"Monthly token budget exceeded for project '{project_id}'",
                    "current_tokens_used": budget.monthly_tokens_used,
                    "monthly_tokens_limit": budget.monthly_tokens_limit,
                    "requested_tokens": tokens,
                    "projected_tokens_used": projected_monthly_tokens,
                    "available_tokens": budget.monthly_tokens_limit
                    - budget.monthly_tokens_used,
                },
            )

    logger.info(
        "budget_check_passed",
        tenant_id=tenant_id,
        project_id=project_id,
        cost_usd=cost_usd,
        tokens=tokens,
    )


async def increment_usage(
    pool: asyncpg.Pool, tenant_id: str, project_id: str, usage: BudgetUsageIncrement
) -> None:
    """
    Increments the daily and monthly usage for both USD and tokens.

    This should be called AFTER the LLM call completes successfully.

    Args:
        pool: Database connection pool
        tenant_id: Tenant identifier
        project_id: Project identifier
        usage: Budget usage increment with cost_usd and tokens

    Note:
        The database trigger handles automatic reset of counters at day/month boundaries.
    """
    logger.info(
        "increment_usage",
        tenant_id=tenant_id,
        project_id=project_id,
        cost_usd=usage.cost_usd,
        input_tokens=usage.input_tokens,
        output_tokens=usage.output_tokens,
        total_tokens=usage.total_tokens,
    )

    await pool.execute(
        """
        UPDATE budgets
        SET
            daily_usage_usd = daily_usage_usd + $3,
            monthly_usage_usd = monthly_usage_usd + $3,
            daily_tokens_used = daily_tokens_used + $4,
            monthly_tokens_used = monthly_tokens_used + $4,
            last_usage_at = NOW(),
            last_token_update_at = NOW()
        WHERE tenant_id = $1 AND project_id = $2
        """,
        tenant_id,
        project_id,
        usage.cost_usd,
        usage.total_tokens,
    )

    logger.info(
        "usage_incremented",
        tenant_id=tenant_id,
        project_id=project_id,
        cost_usd=usage.cost_usd,
        tokens=usage.total_tokens,
    )


async def get_budget_status(
    pool: asyncpg.Pool, tenant_id: str, project_id: str
) -> dict:
    """
    Returns current budget status including usage percentages.

    Useful for displaying budget information in dashboards.

    Args:
        pool: Database connection pool
        tenant_id: Tenant identifier
        project_id: Project identifier

    Returns:
        Dictionary with budget status including usage percentages
    """
    budget = await get_or_create_budget(pool, tenant_id, project_id)

    status = {
        "tenant_id": budget.tenant_id,
        "project_id": budget.project_id,
        # USD Status
        "usd": {
            "daily": {
                "usage": float(budget.daily_usage_usd),
                "limit": (
                    float(budget.daily_limit_usd) if budget.daily_limit_usd else None
                ),
                "percentage": (
                    (budget.daily_usage_usd / budget.daily_limit_usd * 100)
                    if budget.daily_limit_usd
                    else 0
                ),
                "available": (
                    float(budget.daily_limit_usd - budget.daily_usage_usd)
                    if budget.daily_limit_usd
                    else None
                ),
            },
            "monthly": {
                "usage": float(budget.monthly_usage_usd),
                "limit": (
                    float(budget.monthly_limit_usd)
                    if budget.monthly_limit_usd
                    else None
                ),
                "percentage": (
                    (budget.monthly_usage_usd / budget.monthly_limit_usd * 100)
                    if budget.monthly_limit_usd
                    else 0
                ),
                "available": (
                    float(budget.monthly_limit_usd - budget.monthly_usage_usd)
                    if budget.monthly_limit_usd
                    else None
                ),
            },
        },
        # Token Status
        "tokens": {
            "daily": {
                "usage": budget.daily_tokens_used,
                "limit": budget.daily_tokens_limit,
                "percentage": (
                    (budget.daily_tokens_used / budget.daily_tokens_limit * 100)
                    if budget.daily_tokens_limit
                    else 0
                ),
                "available": (
                    budget.daily_tokens_limit - budget.daily_tokens_used
                    if budget.daily_tokens_limit
                    else None
                ),
            },
            "monthly": {
                "usage": budget.monthly_tokens_used,
                "limit": budget.monthly_tokens_limit,
                "percentage": (
                    (budget.monthly_tokens_used / budget.monthly_tokens_limit * 100)
                    if budget.monthly_tokens_limit
                    else 0
                ),
                "available": (
                    budget.monthly_tokens_limit - budget.monthly_tokens_used
                    if budget.monthly_tokens_limit
                    else None
                ),
            },
        },
        # Metadata
        "last_usage_at": budget.last_usage_at.isoformat(),
        "last_daily_reset": budget.last_daily_reset.isoformat(),
        "last_monthly_reset": budget.last_monthly_reset.isoformat(),
    }

    logger.info(
        "get_budget_status", tenant_id=tenant_id, project_id=project_id, status=status
    )
    return status


async def set_budget_limits(
    pool: asyncpg.Pool,
    tenant_id: str,
    project_id: str,
    daily_limit_usd: Optional[float] = None,
    monthly_limit_usd: Optional[float] = None,
    daily_tokens_limit: Optional[int] = None,
    monthly_tokens_limit: Optional[int] = None,
) -> Budget:
    """
    Sets or updates budget limits for a tenant/project.

    Use None to remove a limit (unlimited).

    Args:
        pool: Database connection pool
        tenant_id: Tenant identifier
        project_id: Project identifier
        daily_limit_usd: Daily USD limit (None = unlimited)
        monthly_limit_usd: Monthly USD limit (None = unlimited)
        daily_tokens_limit: Daily token limit (None = unlimited)
        monthly_tokens_limit: Monthly token limit (None = unlimited)

    Returns:
        Updated Budget object
    """
    logger.info(
        "set_budget_limits",
        tenant_id=tenant_id,
        project_id=project_id,
        daily_limit_usd=daily_limit_usd,
        monthly_limit_usd=monthly_limit_usd,
        daily_tokens_limit=daily_tokens_limit,
        monthly_tokens_limit=monthly_tokens_limit,
    )

    # Ensure budget exists
    await get_or_create_budget(pool, tenant_id, project_id)

    # Update limits
    record = await pool.fetchrow(
        """
        UPDATE budgets
        SET
            daily_limit_usd = $3,
            monthly_limit_usd = $4,
            daily_tokens_limit = $5,
            monthly_tokens_limit = $6
        WHERE tenant_id = $1 AND project_id = $2
        RETURNING *
        """,
        tenant_id,
        project_id,
        daily_limit_usd,
        monthly_limit_usd,
        daily_tokens_limit,
        monthly_tokens_limit,
    )

    logger.info("budget_limits_updated", tenant_id=tenant_id, project_id=project_id)
    return Budget(**dict(record))
