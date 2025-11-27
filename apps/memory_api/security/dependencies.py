"""
FastAPI dependencies for RBAC and tenant access control.

These dependencies can be used with Depends() in route definitions.
"""

from typing import Callable

from fastapi import Depends, HTTPException, Request, status

from apps.memory_api.security import auth


async def verify_tenant_access(
    request: Request,
    tenant_id: str,
) -> bool:
    """
    Dependency to verify user has access to tenant (for path parameters).

    Usage:
        @router.get("/tenant/{tenant_id}/stats")
        async def get_stats(
            tenant_id: str,
            _: bool = Depends(verify_tenant_access),
        ):
            ...
    """
    return await auth.check_tenant_access(request, tenant_id)


async def get_and_verify_tenant_id(request: Request) -> str:
    """
    Dependency to extract tenant_id from X-Tenant-Id header and verify access.

    Usage:
        @router.post("/memories")
        async def create_memory(
            tenant_id: str = Depends(get_and_verify_tenant_id),
        ):
            ...
    """
    tenant_id = request.headers.get("X-Tenant-Id")
    if not tenant_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Tenant-Id header is required",
        )

    # Verify user has access to this tenant
    await auth.check_tenant_access(request, tenant_id)

    return tenant_id


def require_action(action: str) -> Callable:
    """
    Create a dependency that requires specific permission.

    Args:
        action: Action to require (e.g., "memories:write", "users:delete")

    Returns:
        Dependency function

    Usage:
        @router.post("/tenant/{tenant_id}/memories")
        async def create_memory(
            tenant_id: str,
            _: bool = Depends(require_action("memories:write")),
        ):
            ...
    """

    async def _check_permission(
        request: Request,
        tenant_id: str,
    ) -> bool:
        return await auth.require_permission(request, tenant_id, action)

    return _check_permission


async def require_admin(request: Request) -> bool:
    """
    Dependency to require admin role for system-wide operations.

    This checks if the user is authenticated and should have admin privileges.
    For tenant-specific admin, use require_action("admin:*") instead.

    Usage:
        @router.get("/admin/overview")
        async def admin_overview(
            _: bool = Depends(require_admin),
        ):
            ...
    """
    # For now, just verify authentication
    # In production, this should check a system-wide admin role
    user_id = await auth.get_user_id_from_token(request)
    if not user_id:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required for admin access",
        )

    # TODO: Implement system-wide admin check
    # For now, allow authenticated users (this is temporary)
    return True


def require_tenant_role(min_role: str) -> Callable:
    """
    Create a dependency that requires minimum role level for tenant.

    Args:
        min_role: Minimum role required (owner, admin, developer, analyst, viewer)

    Returns:
        Dependency function

    Usage:
        @router.delete("/tenant/{tenant_id}/user/{user_id}")
        async def remove_user(
            tenant_id: str,
            user_id: str,
            _: bool = Depends(require_tenant_role("admin")),
        ):
            ...
    """
    from uuid import UUID

    from apps.memory_api.models.rbac import Role
    from apps.memory_api.services.rbac_service import RBACService

    async def _check_role(
        request: Request,
        tenant_id: str,
    ) -> bool:
        from fastapi import HTTPException, status

        # Get user ID
        user_id = await auth.get_user_id_from_token(request)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
            )

        # Get database pool
        if not hasattr(request.app.state, "pool"):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database not initialized",
            )

        # Convert tenant_id to UUID
        try:
            tenant_uuid = UUID(tenant_id)
        except (ValueError, AttributeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid tenant ID format: {tenant_id}",
            )

        # Check role
        rbac_service = RBACService(request.app.state.pool)
        user_role = await rbac_service.get_user_role(user_id, tenant_uuid)

        if not user_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You don't have access to this tenant",
            )

        # Check if role level is sufficient
        required_role = Role(min_role)
        if user_role.role.level < required_role.level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: {required_role.value} role or higher required",
            )

        return True

    return _check_role
