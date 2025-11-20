import asyncpg
from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel

class Budget(BaseModel):
    id: str
    tenant_id: str
    project_id: str
    monthly_limit: float | None
    monthly_usage: float
    daily_limit: float | None
    daily_usage: float
    last_usage_at: datetime

async def get_or_create_budget(pool: asyncpg.Pool, tenant_id: str, project_id: str) -> Budget:
    """
    Retrieves the budget for a tenant/project, creating a new one if it doesn't exist.
    """
    record = await pool.fetchrow(
        "SELECT * FROM budgets WHERE tenant_id = $1 AND project_id = $2",
        tenant_id, project_id
    )
    if not record:
        record = await pool.fetchrow(
            "INSERT INTO budgets (tenant_id, project_id) VALUES ($1, $2) RETURNING *",
            tenant_id, project_id
        )
    return Budget(**dict(record))

async def check_budget(pool: asyncpg.Pool, tenant_id: str, project_id: str, cost: float) -> None:
    """
    Checks if a new cost is within the budget, resetting usage if necessary.
    Raises HTTPException if the budget is exceeded.
    """
    budget = await get_or_create_budget(pool, tenant_id, project_id)
    now = datetime.now()

    # Reset daily/monthly usage if a new day/month has started
    if budget.last_usage_at.month != now.month:
        budget.monthly_usage = 0.0
        budget.daily_usage = 0.0
    elif budget.last_usage_at.day != now.day:
        budget.daily_usage = 0.0

    if budget.daily_limit is not None and (budget.daily_usage + cost) > budget.daily_limit:
        raise HTTPException(
            status_code=402, 
            detail=f"Daily budget exceeded. Usage: {budget.daily_usage}, Limit: {budget.daily_limit}, Cost: {cost}"
        )
    if budget.monthly_limit is not None and (budget.monthly_usage + cost) > budget.monthly_limit:
        raise HTTPException(
            status_code=402,
            detail=f"Monthly budget exceeded. Usage: {budget.monthly_usage}, Limit: {budget.monthly_limit}, Cost: {cost}"
        )

async def increment_usage(pool: asyncpg.Pool, tenant_id: str, project_id: str, cost: float) -> None:
    """
    Increments the daily and monthly usage for a given budget.
    """
    await pool.execute(
        """
        UPDATE budgets
        SET 
            daily_usage = daily_usage + $3,
            monthly_usage = monthly_usage + $3,
            last_usage_at = NOW()
        WHERE tenant_id = $1 AND project_id = $2
        """,
        tenant_id, project_id, cost
    )
