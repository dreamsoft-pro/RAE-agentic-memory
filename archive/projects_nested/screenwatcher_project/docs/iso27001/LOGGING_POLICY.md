# ISO 27001 Logging & Monitoring Policy - ScreenWatcher

## 1. Objectives
To ensure all security-relevant events are recorded and stored securely to facilitate incident detection and forensic analysis.

## 2. Scope of Logging
The following events MUST be logged:
- User Authentication (Success, Failure, Logout).
- Data Modification (Create, Update, Delete) on critical assets (Users, Registry, Rules).
- System Configuration Changes.

## 3. Data Recorded
Each log entry must include:
- **Who**: Actor (User ID / Username).
- **What**: Action and target resource.
- **When**: UTC Timestamp.
- **Where**: Source IP address.
- **Outcome**: Success or Failure details.

## 4. Technical Implementation
- **Application**: `apps.audit` using Django Signals and Middleware.
- **Storage**: `AuditLog` table in PostgreSQL.
- **Immutability**: Log entries cannot be edited or deleted through the application interface (Admin view set to Read-Only).

## 5. Retention
- Audit logs are retained for at least 12 months.
