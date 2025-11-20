"""
RBAC Service - Role-Based Access Control
"""

from typing import Optional, List
from uuid import UUID
import structlog

from apps.memory_api.models.rbac import Role, UserRole, AccessLog

logger = structlog.get_logger(__name__)


class RBACService:
    """Service for managing roles and permissions"""

    def __init__(self):
        # In production, this would use database
        # For now, using in-memory storage
        self._user_roles: dict[str, UserRole] = {}

    async def get_user_role(self, user_id: str, tenant_id: UUID) -> Optional[UserRole]:
        """Get user's role for tenant"""
        key = f"{user_id}:{tenant_id}"
        return self._user_roles.get(key)

    async def assign_role(
        self,
        user_id: str,
        tenant_id: UUID,
        role: Role,
        assigned_by: str,
        project_ids: List[str] = None
    ) -> UserRole:
        """Assign role to user"""
        from uuid import uuid4

        user_role = UserRole(
            id=uuid4(),
            user_id=user_id,
            tenant_id=tenant_id,
            role=role,
            assigned_by=assigned_by,
            project_ids=project_ids or []
        )

        key = f"{user_id}:{tenant_id}"
        self._user_roles[key] = user_role

        logger.info(
            "role_assigned",
            user_id=user_id,
            tenant_id=str(tenant_id),
            role=role.value,
            assigned_by=assigned_by
        )

        return user_role

    async def revoke_role(self, user_id: str, tenant_id: UUID):
        """Revoke user's role"""
        key = f"{user_id}:{tenant_id}"
        if key in self._user_roles:
            del self._user_roles[key]

            logger.info(
                "role_revoked",
                user_id=user_id,
                tenant_id=str(tenant_id)
            )

    async def list_tenant_users(self, tenant_id: UUID) -> List[UserRole]:
        """List all users with roles in tenant"""
        return [
            role for role in self._user_roles.values()
            if role.tenant_id == tenant_id
        ]

    async def log_access(
        self,
        tenant_id: UUID,
        user_id: str,
        action: str,
        resource: str,
        allowed: bool,
        denial_reason: Optional[str] = None
    ):
        """Log access attempt for audit"""
        from uuid import uuid4

        log_entry = AccessLog(
            id=uuid4(),
            tenant_id=tenant_id,
            user_id=user_id,
            action=action,
            resource=resource,
            allowed=allowed,
            denial_reason=denial_reason
        )

        logger.info(
            "access_logged",
            tenant_id=str(tenant_id),
            user_id=user_id,
            action=action,
            allowed=allowed
        )

        return log_entry
