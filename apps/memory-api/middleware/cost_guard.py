from functools import wraps
from fastapi import HTTPException

def cost_guard(budget_field: str = "budget_tokens"):

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            req = kwargs.get("req") or (args[1] if len(args) > 1 else None)
            budget = getattr(req, budget_field, None) if req else None
            # Tu: estymacja tokenów i porównanie z budżetem
            if budget is not None and budget <= 0:
                raise HTTPException(status_code=402, detail="Budget exceeded or zero.")
            return await func(*args, **kwargs)
        return wrapper
    return decorator
