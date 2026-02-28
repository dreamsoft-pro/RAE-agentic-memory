# ISO 27001 Implementation Plan for ScreenWatcher

## 1. Objective
To align the ScreenWatcher project (Application & Infrastructure) with ISO/IEC 27001:2022 standards, focusing on information security, access control, and auditability.

## 2. Scope
- **Application**: ScreenWatcher Django Backend (Core, API, RBAC).
- **Infrastructure**: Deployment configurations (Docker, settings).
- **Processes**: Development lifecycle (CI/CD, Code Review).

## 3. Gap Analysis & Action Plan

### A.5.15 Access Control
**Requirement**: Rules to control physical and logical access to information and other associated assets.
**Current Status**: RBAC app exists (`apps.rbac`), Casbin integration present.
**Action**:
- Review `apps.rbac` configuration.
- Ensure strict separation of duties (Admin vs Operator).
- **Task**: Implement "Least Privilege" principle in Casbin policies.

### A.8.12 Data Leakage Prevention
**Requirement**: Measures to prevent unauthorized disclosure of data.
**Current Status**: `CORS_ALLOW_ALL_ORIGINS = True` (Critical Risk).
**Action**:
- Restrict CORS to trusted origins.
- Review API endpoints for excessive data exposure.

### A.8.15 Logging
**Requirement**: Event logs recording user activities, exceptions, faults, and information security events.
**Current Status**: Basic logging configured. Telemetry exists but focused on metrics.
**Action**:
- Implement **Audit Logging** for all write operations (create, update, delete).
- Log: `Who` (User), `What` (Resource), `When` (Timestamp), `Action` (Type), `Changes` (Diff).
- **Task**: Create `apps.audit` or integrate `django-easy-audit` / `django-auditlog`.

### A.8.26 Application Security Requirements
**Requirement**: Security requirements for development and acquisition.
**Current Status**: `settings.py` needs hardening.
**Action**:
- Fix duplicate configurations in `settings.py`.
- Enforce HTTPS (HSTS, SSL Redirect) in production.
- Secure Cookies (`HttpOnly`, `Secure`).

## 4. Implementation Phase 1: Hardening (Immediate)
- [ ] Fix `settings.py` duplicates (Channels, Auth classes).
- [ ] Restrict `CORS_ALLOW_ALL_ORIGINS`.
- [ ] Ensure `SECURE_SSL_REDIRECT` is environment-controlled.

## 5. Implementation Phase 2: Audit Logging
- [ ] Design Audit Model (likely in `apps.telemetry` or new `apps.audit`).
- [ ] Implement Middleware to capture requests.
- [ ] Store logs in a separate, immutable table (or append-only).

## 6. Implementation Phase 3: Documentation
- [ ] Create `docs/iso27001/ACCESS_CONTROL_POLICY.md`.
- [ ] Create `docs/iso27001/LOGGING_POLICY.md`.
