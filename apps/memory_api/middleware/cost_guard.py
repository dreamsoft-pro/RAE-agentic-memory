from functools import wraps
from fastapi import HTTPException, Request
from apps.memory_api.services import budget_service
from apps.memory_api.services.cost_controller import calculate_gemini_cost
from apps.memory_api.metrics import llm_cost_counter
from apps.memory_api.models import AgentExecuteResponse, AgentExecuteRequest
import json

def cost_guard():
    """
    Cost-Guard 2.0: A decorator that checks budgets, tracks costs,
    and supports a dry-run mode.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # The request object is the second positional argument
            request: Request = args[1]
            
            # We need to get the raw body here before it's parsed by FastAPI
            body_bytes = await request.body()
            # Because request.body() can only be read once, we need to put it back
            # so that FastAPI can read it again for model binding.
            request._body = body_bytes
            
            try:
                req_body_dict = json.loads(body_bytes)
                req_body = AgentExecuteRequest(**req_body_dict)
            except (json.JSONDecodeError, TypeError):
                 raise HTTPException(status_code=400, detail="Invalid request body.")
            
            is_dry_run = request.headers.get("X-Dry-Run", "false").lower() == "true"
            pool = request.app.state.pool
            tenant_id = req_body.tenant_id
            project_id = req_body.project

            # For pre-execution check, we need an estimated cost.
            # This is a simplification. A real implementation might need a more complex cost estimation.
            estimated_cost = 0.001 

            if not is_dry_run:
                # Pre-execution: Check budget. This will raise HTTPException if over budget.
                await budget_service.check_budget(pool, tenant_id, project_id, estimated_cost)

            # If check passes or it's a dry run, execute the function
            response: AgentExecuteResponse = await func(*args, **kwargs)
            
            # Post-execution: Calculate actual cost and update budget if not a dry run
            if response.cost:
                actual_cost_usd = response.cost.total_estimate
                if not is_dry_run:
                    # We might need to adjust the increment amount here if the pre-execution estimate
                    # was already "reserved" in some way. For this implementation, we increment by the full actual cost.
                    await budget_service.increment_usage(pool, tenant_id, project_id, actual_cost_usd)
                    llm_cost_counter.labels(tenant_id=tenant_id, project=project_id).inc(actual_cost_usd)
                    print(f"CostGuard: Logged ${actual_cost_usd:.6f} for project {project_id}")
                else:
                    print(f"CostGuard (Dry Run): Estimated cost is ${actual_cost_usd:.6f}")

            return response
        return wrapper
    return decorator