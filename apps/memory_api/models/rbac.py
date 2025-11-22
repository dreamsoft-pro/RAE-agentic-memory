"""
Role-Based Access Control (RBAC) models
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional
from uuid import UUID


class Role(str, Enum):
    """User roles in order of privilege"""
    OWNER = "owner"          # Full access, can delete tenant
    ADMIN = "admin"          # Manage users, settings, billing
    DEVELOPER = "developer"  # Full API access, read/write memories
    ANALYST = "analyst"      # Analytics and read-only access
    VIEWER = "viewer"        # Read-only access

    @property
    def level(self) -> int:
        """Get numeric privilege level"""
        levels = {
            Role.OWNER: 5,
            Role.ADMIN: 4,
            Role.DEVELOPER: 3,
            Role.ANALYST: 2,
            Role.VIEWER: 1
        }
        return levels[self]

    def can_perform(self, action: str) -> bool:
        """Check if role can perform action"""
        permissions = {
            Role.OWNER: ["*"],  # All actions
            Role.ADMIN: [
                "users:read", "users:write", "users:delete",
                "settings:read", "settings:write",
                "billing:read", "billing:write",
                "memories:read", "memories:write", "memories:delete",
                "analytics:read"
            ],
            Role.DEVELOPER: [
                "memories:read", "memories:write", "memories:delete",
                "graph:read", "graph:write",
                "reflections:read", "reflections:write",
                "analytics:read"
            ],
            Role.ANALYST: [
                "memories:read",
                "analytics:read",
                "graph:read"
            ],
            Role.VIEWER: [
                "memories:read"
            ]
        }

        role_perms = permissions.get(self, [])

        # Owner has all permissions
        if "*" in role_perms:
            return True

        return action in role_perms or action.split(":")[0] + ":*" in role_perms


class Permission(BaseModel):
    """Individual permission"""
    resource: str = Field(..., description="Resource type (memories, users, settings, etc.)")
    action: str = Field(..., description="Action (read, write, delete)")

    def __str__(self) -> str:
        return f"{self.resource}:{self.action}"


class UserRole(BaseModel):
    """User role assignment"""

    id: UUID
    user_id: str = Field(..., description="User identifier")
    tenant_id: UUID = Field(..., description="Tenant this role applies to")
    role: Role = Field(..., description="Assigned role")

    # Scope restrictions (optional)
    project_ids: List[str] = Field(default_factory=list, description="Restrict to specific projects (empty = all)")

    # Metadata
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_by: Optional[str] = Field(None, description="Who assigned this role")
    expires_at: Optional[datetime] = Field(None, description="Role expiration (optional)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user_123",
                "tenant_id": "tenant_abc",
                "role": "developer",
                "project_ids": []
            }
        }
    )

    def is_expired(self) -> bool:
        """Check if role assignment has expired"""
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at

    def has_access_to_project(self, project_id: str) -> bool:
        """Check if user has access to specific project"""
        # Empty list means access to all projects
        if not self.project_ids:
            return True
        return project_id in self.project_ids

    def can_perform(self, action: str, project_id: Optional[str] = None) -> bool:
        """Check if user can perform action"""
        # Check expiration
        if self.is_expired():
            return False

        # Check project access
        if project_id and not self.has_access_to_project(project_id):
            return False

        # Check role permissions
        return self.role.can_perform(action)


class RoleHierarchy:
    """Helper class for role hierarchy checks"""

    @staticmethod
    def is_higher_or_equal(role1: Role, role2: Role) -> bool:
        """Check if role1 >= role2 in hierarchy"""
        return role1.level >= role2.level

    @staticmethod
    def can_assign_role(assigner_role: Role, target_role: Role) -> bool:
        """Check if assigner can assign target role"""
        # Owners can assign any role
        if assigner_role == Role.OWNER:
            return True

        # Admins can assign roles below them
        if assigner_role == Role.ADMIN:
            return target_role.level < Role.ADMIN.level

        # Others cannot assign roles
        return False

    @staticmethod
    def can_modify_user(modifier_role: Role, target_user_role: Role) -> bool:
        """Check if modifier can modify target user"""
        # Can only modify users with lower role
        return modifier_role.level > target_user_role.level


class AccessLog(BaseModel):
    """Audit log entry for access control"""

    id: UUID
    tenant_id: UUID
    user_id: str
    action: str
    resource: str
    resource_id: Optional[str] = None

    # Result
    allowed: bool
    denial_reason: Optional[str] = None

    # Context
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Metadata
    metadata: dict = Field(default_factory=dict)


async def check_permission(
    user_id: str,
    tenant_id: UUID,
    action: str,
    project_id: Optional[str] = None
) -> tuple[bool, Optional[str]]:
    """
    Check if user has permission to perform action.

    Returns:
        (allowed, denial_reason)
    """
    # Import here to avoid circular dependency
    from apps.memory_api.services.rbac_service import RBACService

    service = RBACService()
    user_role = await service.get_user_role(user_id, tenant_id)

    if not user_role:
        return False, "User has no role in this tenant"

    if user_role.is_expired():
        return False, "Role assignment has expired"

    if project_id and not user_role.has_access_to_project(project_id):
        return False, f"No access to project {project_id}"

    if not user_role.can_perform(action):
        return False, f"Role {user_role.role.value} cannot perform {action}"

    return True, None


async def require_permission(
    user_id: str,
    tenant_id: UUID,
    action: str,
    project_id: Optional[str] = None
):
    """
    Decorator/function to require permission.
    Raises HTTPException if permission denied.
    """
    from fastapi import HTTPException, status

    allowed, reason = await check_permission(user_id, tenant_id, action, project_id)

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied: {reason}"
        )
