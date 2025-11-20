"""
Authentication and Authorization Module

Provides API key authentication and optional JWT token verification.
"""

from typing import Optional
from fastapi import Security, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, APIKeyHeader
from apps.memory_api.config import settings
import structlog

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
            detail="API key is required. Please provide X-API-Key header."
        )

    # Verify API key
    if api_key != settings.API_KEY:
        logger.warning("invalid_api_key", provided_key=api_key[:10] + "...")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
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
        # In production, implement proper JWT verification
        if not settings.ENABLE_JWT_AUTH:
            return {"authenticated": True, "method": "bearer", "token": token}

        # TODO: Implement JWT token verification
        # decoded_token = verify_jwt_token(token)
        # return {"authenticated": True, "user_id": decoded_token["sub"], ...}

        return {"authenticated": True, "method": "bearer", "token": token}

    # If both API key and token authentication are disabled, allow access
    if not settings.ENABLE_API_KEY_AUTH and not settings.ENABLE_JWT_AUTH:
        return {"authenticated": False, "method": "none"}

    # No valid authentication provided
    logger.warning("authentication_failed")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required. Provide either Bearer token or X-API-Key header.",
        headers={"WWW-Authenticate": "Bearer"}
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


async def check_tenant_access(
    tenant_id: str,
    user: dict = Security(get_current_user)
) -> bool:
    """
    Check if user has access to specific tenant.

    Args:
        tenant_id: Tenant ID to check access for
        user: Current authenticated user

    Returns:
        True if user has access

    Raises:
        HTTPException: If user doesn't have access
    """
    # TODO: Implement proper tenant access control
    # For now, allow all authenticated users

    if not user.get("authenticated"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to tenant"
        )

    return True
