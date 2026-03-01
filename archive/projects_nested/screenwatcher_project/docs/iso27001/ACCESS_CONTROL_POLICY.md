# ISO 27001 Access Control Policy - ScreenWatcher

## 1. Principles
- **Least Privilege**: Users are granted the minimum level of access required for their role.
- **Separation of Duties**: Administrative functions are separated from operational functions.

## 2. Roles & Permissions (RBAC)

| Role | Permissions | Scope |
| :--- | :--- | :--- |
| **Operator** | Read Registry, Write Telemetry | Machine-level operations |
| **Manager** | Manage Registry, Read Analytics | Factory/Line management |
| **Admin** | Full System Access | System-wide configuration |

## 3. Technical Implementation
- **Framework**: Casbin with `rbac_model.conf`.
- **Enforcement**: `CasbinPermission` class in `apps.rbac.permissions`.
- **Policy Storage**: Database-backed (Django ORM Adapter).

## 4. User Provisioning
- Users must be assigned to groups that correspond to RBAC roles.
- `apps.rbac` automatically maps groups (prefixed with `role:`) to Casbin policies.

## 5. Review Cycle
- Access rights must be reviewed quarterly.
