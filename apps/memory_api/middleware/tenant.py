from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from apps.memory_api.config import Settings

settings = Settings()


class TenantContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        raw_tenant = (
            request.headers.get("X-Tenant-Id")
            or request.query_params.get("tenant_id")
            or ""
        ).strip()

        if not raw_tenant:
            tenant_id = settings.DEFAULT_TENANT_UUID
        elif raw_tenant.lower() in settings.TENANT_ALIASES:
            tenant_id = settings.TENANT_ALIASES[raw_tenant.lower()]
        elif raw_tenant in settings.TENANT_ALIASES:
            tenant_id = settings.TENANT_ALIASES[raw_tenant]
        else:
            tenant_id = raw_tenant

        request.state.tenant_id = tenant_id
        response: Response = await call_next(request)
        return response
