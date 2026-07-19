# Project ATLAS

# Implementation Pack

## IP-002 — Identity & Access Platform

---

# Document Information

| Field | Value |
|--------|--------|
| Document ID | IP-002 |
| Title | Identity & Access Platform |
| Version | 1.0.0 |
| Status | Draft (Engineering Review) |
| Repository | Project ATLAS |
| Owner | Anil Kumar |
| Classification | Engineering Implementation Specification |
| Depends On | IP-000, IP-001, BP-003, RA-001, RA-009, RA-011 |
| Next | IP-003 |
| Last Updated | 2026-07-08 |

---

# 1. Purpose

IP-002 defines the implementation specification for the Project ATLAS Identity & Access Platform.

This document translates BP-003 Identity & Access Platform into executable engineering guidance.

It specifies the implementation of authentication, authorization, user identity, service identity, tenant-aware identity, session management, token management, and access governance.

The Identity & Access Platform shall become the single source of truth for authentication and authorization across Project ATLAS.

No downstream Implementation Pack shall implement an independent identity solution.

---

# 2. Scope

This Implementation Pack governs:

- User Management
- Role Management
- Permission Management
- Authentication
- Authorization
- OAuth2
- OpenID Connect
- JWT
- Refresh Tokens
- API Keys
- Service Accounts
- Session Management
- Password Policy
- MFA Foundation
- Audit Logging

Excluded:

- Tenant business logic
- AI identities
- Workflow permissions
- External integrations

These are implemented in later Implementation Packs.

---

# 3. Dependencies

Implementation depends upon:

## Master Context

MC-000 through MC-005

## Architecture

ARCH-001

ARCH-005

ARCH-008

## Engineering Standards

ES-001

ES-002

ES-006

ES-007

## Reference Architecture

RA-001 Backend

RA-009 Multi-Tenant

RA-011 Security

## Build Packs

BP-003 Identity & Access Platform

## Previous Implementation Packs

IP-000

IP-001

Only approved repository documents may be used as implementation inputs.

---

# 4. Implementation Objectives

Implementation shall provide:

- Identity Service
- Authentication Service
- Authorization Service
- Token Service
- Session Service
- Role Service
- Permission Service
- API Key Service
- Service Account Service
- Audit Service

Every authentication mechanism shall share a common identity model.

---

# 5. Engineering Deliverables

Completion of IP-002 shall produce:

- Identity Microservice
- Authentication APIs
- Authorization Engine
- JWT Infrastructure
- Refresh Token Service
- Session Manager
- RBAC Framework
- ABAC Foundation
- API Key Management
- Service Account Management
- Identity Audit Framework
- MFA Foundation

These components become mandatory dependencies for all future platform services.

---

# 6. Backend Module Structure

```text
backend/apps/identity/

├── api/
│
├── application/
│
├── domain/
│
├── infrastructure/
│
├── repositories/
│
├── services/
│
├── security/
│
├── tokens/
│
├── sessions/
│
├── permissions/
│
├── audit/
│
├── events/
│
├── workers/
│
└── tests/
```

Each module shall have clearly separated Domain, Application, and Infrastructure responsibilities.

No business logic shall exist inside API controllers.

---

# 7. Service Architecture

The Identity Platform shall expose the following internal services.

| Service | Responsibility |
|----------|----------------|
| Identity Service | User lifecycle |
| Authentication Service | Login and authentication |
| Authorization Service | Access decisions |
| Token Service | JWT issuance and validation |
| Session Service | Session lifecycle |
| Role Service | Role management |
| Permission Service | Permission management |
| API Key Service | Machine authentication |
| Service Account Service | Service identities |
| Identity Audit Service | Security audit |

Every service shall expose versioned APIs and publish security events through the Event Platform.

---
---

# 8. API Specification

The Identity Platform shall expose versioned REST APIs.

Base URL

```text
/api/v1/identity
```

Mandatory API groups:

| API Group | Purpose |
|-----------|---------|
| Authentication API | User authentication |
| User API | User lifecycle |
| Role API | Role management |
| Permission API | Permission management |
| Session API | Session management |
| Token API | JWT management |
| API Key API | Machine authentication |
| Service Account API | Service identities |
| MFA API | Multi-factor authentication |
| Audit API | Identity audit |

No API shall bypass the Authorization Service.

---

# 9. Database Design

The Identity Platform shall own the following tables.

```text
identity/

├── users
├── roles
├── permissions
├── role_permissions
├── user_roles
├── sessions
├── refresh_tokens
├── api_keys
├── service_accounts
├── mfa_devices
├── password_history
├── login_history
└── audit_logs
```

Ownership of these tables belongs exclusively to the Identity Platform.

No external service shall modify these tables directly.

---

# 10. Repository Layer

Repositories shall encapsulate persistence logic.

Mandatory repositories:

- UserRepository
- RoleRepository
- PermissionRepository
- SessionRepository
- RefreshTokenRepository
- ApiKeyRepository
- ServiceAccountRepository
- AuditRepository

Repositories shall never contain business rules.

---

# 11. Domain Layer

Domain entities include:

- User
- Role
- Permission
- Session
- RefreshToken
- ApiKey
- ServiceAccount
- MFADevice

Business rules shall reside only inside the Domain Layer.

---

# 12. Application Layer

Application services shall coordinate domain behavior.

Application services include:

- CreateUser
- UpdateUser
- DeleteUser
- AuthenticateUser
- LogoutUser
- AssignRole
- RemoveRole
- CreatePermission
- RotateApiKey
- CreateServiceAccount
- RegisterMFA
- VerifyMFA

Application services shall remain transaction boundaries.

---

# 13. Security Implementation

Authentication mechanisms:

- Username & Password
- OAuth2
- OpenID Connect
- JWT
- Refresh Token
- API Keys
- Service Accounts

Authorization mechanisms:

- RBAC
- ABAC
- Policy Evaluation

Passwords shall be hashed using Argon2id.

Refresh tokens shall be securely stored.

JWT signing keys shall never be hardcoded.

---

# 14. Session Management

Every authenticated user shall receive:

- Access Token
- Refresh Token
- Session Record

Session lifecycle:

Created

↓

Authenticated

↓

Active

↓

Refreshed

↓

Expired

↓

Archived

Session revocation shall immediately invalidate authentication.

---
---

# 15. Event Architecture

The Identity Platform shall publish and consume events through the Project ATLAS Event Platform.

## Published Events

| Event | Description |
|--------|-------------|
| User.Created | New user created |
| User.Updated | User profile updated |
| User.Deleted | User removed |
| User.Activated | User activated |
| User.Deactivated | User disabled |
| User.LoggedIn | Successful authentication |
| User.LoggedOut | Session terminated |
| Password.Changed | Password updated |
| Password.Reset | Password reset completed |
| Role.Assigned | Role assigned to user |
| Role.Removed | Role removed from user |
| Permission.Granted | Permission granted |
| Permission.Revoked | Permission revoked |
| MFA.Enabled | MFA activated |
| MFA.Disabled | MFA removed |
| ApiKey.Created | API key created |
| ApiKey.Rotated | API key rotated |
| ServiceAccount.Created | Service account created |

All published events shall include:

- Event ID
- Correlation ID
- Tenant ID
- Timestamp
- Actor ID
- Event Version

---

## Consumed Events

The Identity Platform shall consume:

- Tenant.Created
- Tenant.Disabled
- Tenant.Deleted
- Notification.Delivered
- Integration.AuthenticationUpdated

Consumed events shall never modify identity state without authorization validation.

---

# 16. Redis Strategy

Redis shall be used only for transient identity data.

Redis keys:

```text
identity:

session:{sessionId}

refresh:{tokenId}

mfa:{userId}

login_attempt:{userId}

permission_cache:{userId}

role_cache:{userId}

token_blacklist:{jwtId}
```

Redis shall never become the system of record.

The database remains authoritative.

---

# 17. Background Workers

Identity workers shall execute asynchronous operations.

Worker responsibilities:

- Expire sessions
- Revoke expired tokens
- Clean refresh tokens
- Rotate API keys
- Process audit events
- Process login history
- Publish identity events
- Synchronize permission cache

Workers shall remain idempotent.

---

# 18. Environment Variables

Mandatory environment variables:

```text
DATABASE_URL

REDIS_URL

KAFKA_BROKER

JWT_PRIVATE_KEY

JWT_PUBLIC_KEY

JWT_EXPIRATION

REFRESH_TOKEN_EXPIRATION

ARGON_MEMORY_COST

ARGON_TIME_COST

SESSION_TIMEOUT

MFA_ENABLED

API_KEY_LENGTH

AUDIT_RETENTION_DAYS
```

Secrets shall be loaded from the platform secret manager.

No production secret shall exist inside source code.

---

# 19. External Interfaces

The Identity Platform shall expose services to:

- Tenant Platform
- Workflow Platform
- AI Platform
- Knowledge Platform
- Meeting Platform
- Notification Platform
- Integration Platform

Every external interaction shall occur through approved APIs or events.

Direct database access is prohibited.

---

# 20. Observability

Identity telemetry shall include:

Metrics

- Login Success Rate
- Login Failure Rate
- Token Issuance
- Active Sessions
- Session Expiration
- MFA Success Rate
- API Key Usage
- Authorization Decisions

Logs

- Authentication
- Authorization
- Session Creation
- Token Refresh
- Permission Changes
- Security Events

Tracing

- Login Flow
- Token Validation
- Authorization Pipeline
- Session Validation
- MFA Verification

Every request shall contain a Correlation ID.

---
---

# 21. Testing Strategy

The Identity Platform shall implement comprehensive automated testing.

## Unit Testing

Coverage shall include:

- User Domain
- Role Domain
- Permission Domain
- Authentication Logic
- Authorization Policies
- Session Management
- Token Management
- MFA Validation

Minimum coverage:

- Domain Layer ≥ 95%
- Application Layer ≥ 90%
- API Layer ≥ 85%

---

## Integration Testing

Integration tests shall validate:

- PostgreSQL
- Redis
- Kafka
- JWT Authentication
- OAuth2
- OpenID Connect
- API Keys
- Service Accounts

---

## Security Testing

Mandatory security validation:

- Password Hashing
- JWT Validation
- Refresh Token Rotation
- Replay Attack Prevention
- Brute Force Protection
- MFA Validation
- Session Hijacking Protection
- API Key Validation
- Authorization Policy Testing

---

## Performance Testing

Performance validation shall include:

- Concurrent Authentication
- Token Generation
- Permission Evaluation
- Session Validation
- Role Resolution
- MFA Verification

Authentication latency targets shall comply with repository performance objectives.

---

# 22. Deployment Strategy

Identity services shall support:

- Stateless Deployment
- Horizontal Scaling
- Rolling Updates
- Zero-Downtime Deployment
- Automatic Rollback
- Health Verification

Deployment order:

```text
Database Migration

↓

Configuration Validation

↓

Application Deployment

↓

Health Validation

↓

Traffic Routing

↓

Monitoring Verification
```

---

# 23. Acceptance Criteria

IP-002 shall be considered complete when:

- Authentication service is operational.
- Authorization engine functions correctly.
- RBAC implementation is complete.
- ABAC foundation is operational.
- JWT authentication is functional.
- Session management is operational.
- MFA foundation is implemented.
- Audit logging is functional.
- Events are published successfully.
- Repository traceability is complete.

---

# 24. Definition of Done

Implementation shall be complete when:

- Code review approved.
- Static analysis passed.
- Unit tests passed.
- Integration tests passed.
- Security validation completed.
- Performance validation completed.
- Documentation updated.
- API documentation generated.
- Deployment validated.
- Engineering approval completed.

---

# 25. Engineering Checklist

Before approval verify:

- Identity Service implemented
- Authentication Service implemented
- Authorization Service implemented
- JWT implemented
- OAuth2 implemented
- OIDC implemented
- Session management operational
- API Keys operational
- Service Accounts operational
- MFA operational
- Audit logging verified
- Events verified
- Redis caching verified
- Health endpoints verified

---

# 26. Risks

Primary implementation risks include:

- Credential compromise
- Token leakage
- Session hijacking
- Privilege escalation
- Incorrect authorization policies
- Cache inconsistency
- Identity synchronization failures
- Key rotation failures
- Authentication bottlenecks
- Audit log integrity issues

Mitigation strategies shall be documented before production deployment.

---

# 27. Traceability Matrix

| Implementation Area | Governing Documents |
|---------------------|---------------------|
| Identity Service | BP-003 |
| Authentication | RA-011 |
| Authorization | RA-011 |
| Multi-Tenant Identity | RA-009 |
| Backend Implementation | RA-001 |
| Security | ES-006 |
| Testing | ES-007 |
| Platform Foundation | IP-001 |

Every implementation artifact shall remain traceable to approved repository documents.

---

# 28. Engineering Decisions Register

| ID | Decision | Source | Status |
|----|----------|--------|--------|
| ED-001 | FastAPI Identity Service | RA-001 | Approved |
| ED-002 | JWT Authentication | RA-011 | Approved |
| ED-003 | OAuth2 / OIDC Support | RA-011 | Approved |
| ED-004 | Argon2id Password Hashing | RA-011 | Approved |
| ED-005 | Redis Session Cache | RA-005 | Approved |
| ED-006 | Kafka Security Events | RA-006 | Approved |
| ED-007 | RBAC + ABAC Authorization | BP-003 | Approved |
| ED-008 | Immutable Identity Audit | RA-010 | Approved |

Implementation-specific changes require repository governance approval.

---

# 29. Cross References

Primary references include:

- MC-000 through MC-005
- ARCH-001
- ARCH-005
- ARCH-008
- ES-001
- ES-002
- ES-006
- ES-007
- RA-001
- RA-009
- RA-011
- BP-003
- IP-000
- IP-001

---

# 30. Version History

| Version | Date | Description |
|----------|------|-------------|
| 1.0.0 | 2026-07-08 | Initial implementation specification |

---

# 31. Freeze Declaration

IP-002 establishes the canonical implementation specification for the Project ATLAS Identity & Access Platform.

The Identity Platform is the single owner of authentication, authorization, user identity, service identity, session management, token management, API keys, service accounts, multi-factor authentication, and identity auditing.

All downstream Implementation Packs shall consume Identity Platform services through approved APIs and events rather than implementing independent identity functionality.

Implementation shall remain fully traceable to BP-003, RA-001, RA-009, RA-011, and the Engineering Standards.

---

# 31. As-Built Addendum — Sprint-002 (2026-07-19)

> Appended by the Sprint-002 Engineering Closure. The specification above
> (2026-07-08) is preserved unmodified; this addendum records what was
> **actually built**, where it diverges, and what remains. Reality below
> supersedes intention above wherever they conflict (CLS-002 authority).
> Process note: Sprint-002 was executed against the Product Owner's inline
> scope directive; this document's §1–§30 were not loaded during
> implementation (process finding P-1, CLS-002) — conformance was
> assessed at closure.

## 31.1 Delivered (verified live; evidence in LOG-S002 / CLS-002)

- Module `backend/apps/identity/` per §6 layering intent: `models`,
  `domain` (framework-free policies/permissions), `repositories`,
  `services`, `schemas`, `security`, `api`; enforcement in
  `backend/api/v1/security.py`.
- **Tables (migration 0002, prefix `identity_`):** users, organizations,
  roles, memberships, sessions, verification_tokens, audit_log (append-only).
- **Auth:** Argon2id (ED-004 ✓); HS256 JWT ≥32-byte key, 15-min TTL
  (ED-002 ✓); opaque refresh tokens SHA-256-at-rest, httpOnly cookie,
  rotation with family-revocation theft response; login lockout
  (5 attempts / 15 min); enumeration-resistant responses.
- **Authorization (ED-007 partial):** RBAC via org-scoped roles with
  permission strings; PDP deny-by-default + cross-tenant deny
  (`shared.auth.PolicyDecisionPoint` implementation); `require_permission`
  PEP; ADR-004 deny-by-default gate at `/api/v1` with explicit
  `public_endpoint` markers. ABAC: deferred.
- **APIs (§8 subset):** Authentication API + User API
  (`/api/v1/identity/auth/*`, `/users/me`). Registration optionally
  bootstraps an organization with seeded system roles (owner/admin/member).
- **Frameworks:** email verification + password reset (token issuance,
  hashed at rest; delivery behind feature flag `identity_email_delivery`).
- **Events (ED-006 ✓ via ADR-002 outbox):** identity.user.registered.v1
  (audit), organization.created.v1 (domain), identity.user.logged_in.v1,
  identity.user.locked.v1, identity.session.revoked.v1,
  identity.session.reuse_detected.v1, identity.password.reset_completed.v1
  (security). Atomic audit rows per use case (ED-008 ✓).
- **Frontend:** login (RHF+Zod), logout, RouteGuard + middleware marker
  layer, in-memory access token + silent rotation at 80% TTL, profile.

## 31.2 Ratified divergences from §9/§14 (design decisions, as-built)

| # | Specification | As-built | Rationale |
|---|---|---|---|
| D-1 | `permissions`, `role_permissions`, `user_roles` join tables | Permission strings as JSONB array on org-scoped `identity_roles`; single role per membership | Simpler at current scale; join-table normalization deferred until custom-role editing (IP-003+) |
| D-2 | Separate `sessions` + `refresh_tokens` | Merged `identity_sessions` (session ≡ refresh lineage; `family_id`, `replaced_by`) | Rotation lineage and revocation live on one row; no dual-write |
| D-3 | §14 "revocation shall immediately invalidate authentication" | Refresh invalidation immediate; outstanding access JWTs live ≤15 min | Stateless verification; ED-005 Redis denylist is the planned closure (CLS-002 M-3) |
| D-4 | Bare table names | `identity_<name>` prefix | Module-ownership visibility in a shared schema (CON-001 §6.2) |

## 31.3 Deferred to future stages (never silently dropped)

OAuth2/OIDC (ED-003) · MFA API/devices · API keys + service accounts
(machine/agent identity classes — contracts exist in `shared.auth`) ·
Role/Permission/Session/Token/Audit admin APIs · Redis session cache +
revocation denylist (ED-005) · password history · login-history table
(partially covered by audit_log) · ABAC policies · session/token cleanup
worker (§17) · org switching (multi-membership).

## 31.4 Traceability

BP-003 §8 (identity classes, PDP/PEP, fail-closed) · ADR-001..007 (all
enforced; gate evidence LOG-S002) · ES-003 mixins on all tables ·
ES-002 envelopes/errors · ENG-004 tenancy layout (REG-001).
