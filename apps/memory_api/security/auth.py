"""
Authentication and Authorization Module

Provides API key authentication and optional JWT token verification.
"""

from typing import Optional

import structlog
from fastapi import HTTPException, Request, Security, status
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer

from apps.memory_api.config import settings

logger = structlog.get_logger(__name__)

# Security schemes
security = HTTPBearer(auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(
    api_key: Optional[str] = Security(api_key_header),
) -> Optional[str]:
    """
    Verify API key from X-API-Key header.

    Args:
        api_key: API key from header

    Returns:
        API key if valid, None if API key authentication is disabled

    Raises:
        HTTPException: If API key is invalid or missing when required
    """
    # If API key authentication is disabled, skip verification
    if not settings.ENABLE_API_KEY_AUTH:
        return None

    # If API key is missing
    if not api_key:
        logger.warning("missing_api_key")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key is required. Please provide X-API-Key header.",
        )

    # Verify API key
    if api_key != settings.API_KEY:
        logger.warning("invalid_api_key", provided_key=api_key[:10] + "...")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key"
        )

    return api_key


async def verify_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
    api_key: Optional[str] = Security(api_key_header),
) -> dict:
    """
    Verify authentication token (Bearer token or API key).

    Supports two authentication methods:
    1. Bearer token (JWT) in Authorization header
    2. API key in X-API-Key header

    Args:
        credentials: Bearer token credentials
        api_key: API key from header

    Returns:
        User information dictionary

    Raises:
        HTTPException: If authentication fails
    """
    # Try API key first
    if api_key:
        try:
            await verify_api_key(api_key)
            return {"authenticated": True, "method": "api_key"}
        except HTTPException:
            pass

    # Try Bearer token
    if credentials:
        token = credentials.credentials

        # For now, we accept any token if JWT verification is disabled
        if not settings.ENABLE_JWT_AUTH:
            return {"authenticated": True, "method": "bearer", "token": token}

        # JWT verification implementation
        from jose import JWTError, jwt

        try:
            # Decode and validate the token using the secret key
            # This verifies the signature and expiration automatically
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            # Ensure subject (user_id) is present
            if "sub" not in decoded:
                raise JWTError("Token missing subject claim")

            return {
                "authenticated": True,
                "method": "bearer",
                "user_id": decoded["sub"],
                "email": decoded.get("email"),
                "token": token,
                "claims": decoded,
            }

        except JWTError as e:
            logger.warning("invalid_jwt_token", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid authentication credentials: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            logger.error("jwt_verification_error", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed",
                headers={"WWW-Authenticate": "Bearer"},
            )

    # If both API key and token authentication are disabled, allow access
    if not settings.ENABLE_API_KEY_AUTH and not settings.ENABLE_JWT_AUTH:
        return {"authenticated": False, "method": "none"}

    # No valid authentication provided
    logger.warning("authentication_failed")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required. Provide either Bearer token or X-API-Key header.",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(request: Request) -> dict:
    """
    Get current authenticated user from request state.

    Args:
        request: FastAPI request object

    Returns:
        User information dictionary
    """
    if hasattr(request.state, "user"):
        return request.state.user

    return {"authenticated": False}


async def get_user_id_from_token(request: Request) -> Optional[str]:
    """
    Extract user ID from authentication token.

    Args:
        request: FastAPI request object

    Returns:
        User ID if authenticated, None otherwise
    """
    # Try to get from request state first
    if hasattr(request.state, "user"):
        user = request.state.user
        if user.get("user_id"):
            return user["user_id"]

    # Try to extract from token
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]

        # If JWT is enabled, decode it to get the real user_id
        if settings.ENABLE_JWT_AUTH:
            from jose import JWTError, jwt

            try:
                decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                return decoded.get("sub")
            except JWTError:
                return None

        # Fallback for testing/non-JWT mode: use token hash
        import hashlib

        return hashlib.sha256(token.encode()).hexdigest()[:32]

    # Try API key as user identifier
    api_key = request.headers.get("X-API-Key")
    if api_key:
        return f"apikey_{api_key[:20]}"

    return None


async def check_tenant_access(
    request: Request,
    tenant_id: str,
) -> bool:
    """
    Check if user has access to specific tenant using RBAC.

    Args:
        request: FastAPI request object
        tenant_id: Tenant ID to check access for

    Returns:
        True if user has access

    Raises:
        HTTPException: If user doesn't have access
    """
    from uuid import UUID

    from apps.memory_api.services.rbac_service import RBACService

    # Get user ID from authentication
    user_id = await get_user_id_from_token(request)
    if not user_id:
        logger.warning("check_tenant_access_no_user_id", tenant_id=tenant_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to access tenant",
        )

    # Get database pool from app state
    if not hasattr(request.app.state, "pool"):
        logger.error("check_tenant_access_no_pool", tenant_id=tenant_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database not initialized",
        )

    # Convert tenant_id to UUID
    try:
        tenant_uuid = UUID(tenant_id)
    except (ValueError, AttributeError):
        logger.warning("check_tenant_access_invalid_tenant_id", tenant_id=tenant_id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid tenant ID format: {tenant_id}",
        )

    # Check RBAC
    rbac_service = RBACService(request.app.state.pool)
    user_role = await rbac_service.get_user_role(user_id, tenant_uuid)

    if not user_role:
        logger.warning(
            "check_tenant_access_denied",
            user_id=user_id,
            tenant_id=tenant_id,
            reason="no_role",
        )
        # Log access attempt
        await rbac_service.log_access(
            tenant_id=tenant_uuid,
            user_id=user_id,
            action="tenant:access",
            resource="tenant",
            allowed=False,
            denial_reason="User has no role in this tenant",
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You don't have access to this tenant",
        )

    # Check if role is expired
    if user_role.is_expired():
        logger.warning(
            "check_tenant_access_denied",
            user_id=user_id,
            tenant_id=tenant_id,
            reason="role_expired",
        )
        await rbac_service.log_access(
            tenant_id=tenant_uuid,
            user_id=user_id,
            action="tenant:access",
            resource="tenant",
            allowed=False,
            denial_reason="Role assignment has expired",
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Your access to this tenant has expired",
        )

    # Log successful access
    await rbac_service.log_access(
        tenant_id=tenant_uuid,
        user_id=user_id,
        action="tenant:access",
        resource="tenant",
        allowed=True,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    logger.info(
        "check_tenant_access_granted",
        user_id=user_id,
        tenant_id=tenant_id,
        role=user_role.role.value,
    )

    return True


async def require_permission(
    request: Request,
    tenant_id: str,
    action: str,
    project_id: Optional[str] = None,
) -> bool:
    """
    Check if user has specific permission to perform action.

    Args:
        request: FastAPI request object
        tenant_id: Tenant ID
        action: Action to check (e.g., "memories:write", "users:delete")
        project_id: Optional project ID for project-scoped permissions

    Returns:
        True if permission granted

    Raises:
        HTTPException: If permission denied
    """
    from uuid import UUID

    from apps.memory_api.services.rbac_service import RBACService

    # Get user ID from authentication
    user_id = await get_user_id_from_token(request)
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

    # Check permission
    rbac_service = RBACService(request.app.state.pool)
    user_role = await rbac_service.get_user_role(user_id, tenant_uuid)

    if not user_role:
        await rbac_service.log_access(
            tenant_id=tenant_uuid,
            user_id=user_id,
            action=action,
            resource=action.split(":")[0],
            allowed=False,
            denial_reason="User has no role in this tenant",
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You don't have access to this tenant",
        )

    # Check if can perform action
    if not user_role.can_perform(action, project_id):
        denial_reason = f"Role {user_role.role.value} cannot perform {action}"
        if project_id and not user_role.has_access_to_project(project_id):
            denial_reason = f"No access to project {project_id}"

        await rbac_service.log_access(
            tenant_id=tenant_uuid,
            user_id=user_id,
            action=action,
            resource=action.split(":")[0],
            allowed=False,
            denial_reason=denial_reason,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied: {denial_reason}",
        )

    # Log successful access
    await rbac_service.log_access(
        tenant_id=tenant_uuid,
        user_id=user_id,
        action=action,
        resource=action.split(":")[0],
        allowed=True,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent"),
    )

    logger.info(
        "permission_granted",
        user_id=user_id,
        tenant_id=tenant_id,
        action=action,
        role=user_role.role.value,
    )

    return True
