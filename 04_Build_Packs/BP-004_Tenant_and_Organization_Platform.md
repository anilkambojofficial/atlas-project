# Project ATLAS

# BP-004 — Tenant & Organization Platform

---

## Document Information

| Field | Value |
|--------|--------|
| Document ID | BP-004 |
| Title | Tenant & Organization Platform |
| Version | 1.0.0 |
| Status | Draft (Engineering Review) |
| Repository | Project ATLAS |
| Document Owner | Chief Architecture Office |
| Product Owner | Anil Kumar |
| Repository Path | 04_Build_Packs/BP-004_Tenant_and_Organization_Platform.md |
| Depends On | BP-000, BP-001, BP-002, BP-003, MC-000, MC-002, MC-004, ARCH-001, ARCH-002, ARCH-004, ARCH-005, DOMAIN-001, ES-003, ES-004, RA-009, RA-005, RA-001, RA-011, RA-006, BP-ROADMAP |
| Last Updated | 2026-07-08 |

---

# 1. Build Pack Objectives

BP-004 delivers the Tenant & Organization Platform for Project ATLAS.

The Tenant & Organization Platform is the root business ownership boundary of the platform. It establishes the tenant (Organization) as the authoritative multi-tenant container, defines the internal organizational structure (Departments and Teams), owns the subscription and entitlement model, enforces multi-tenant governance, and publishes the Organization lifecycle events that every downstream domain depends on.

Per DOMAIN-001, every business entity in the platform belongs to exactly one Organization. Per ARCH-002 and RA-009, tenant isolation is mandatory and applies to identity, data, events, configuration, storage, and AI context. Per BP-003, user-to-tenant binding is resolved by the Identity & Access Platform against the authoritative Tenant Registry established by BP-004.

**Objectives:**

- Establish the Tenant Registry as the authoritative source of Organization identity and lifecycle state
- Deliver the Organization lifecycle (Provisioning → Validation → Activation → Operational → Suspension → Reactivation → Archival → Retention → Deletion) with authorized and auditable transitions
- Deliver Organization structure (Department, Team) with tenant-scoped uniqueness and hierarchical inheritance
- Deliver the Subscription model with plan, billing cycle, renewal, user limits, storage limits, AI usage limits, API access, and integration access as first-class configuration
- Deliver Entitlement enforcement that resolves subscription features into runtime capability decisions consumed by every downstream Build Pack
- Deliver Organization configuration surfaces covering General, Business, Security, AI, and Notification categories
- Deliver Organization administration model (Organization Administrator role, delegated administration, admin audit)
- Deliver tenant isolation enforcement primitives consumed by BP-003 Identity & Access, BP-005 AI Platform, BP-006 Knowledge Platform, BP-007 Workflow Platform, and every subsequent Build Pack
- Deliver Organization storage allocation and quota metering aligned to ARCH-004 Data Architecture and RA-005 Data Platform
- Deliver Organization events (lifecycle, structure, subscription, entitlement, configuration, administration) via the platform event bus established in BP-002
- Deliver Organization audit as the authoritative record of every state transition, configuration change, subscription change, and administrative action

**Non-Objectives:**

- Deliver the Identity, Authentication, Authorization, Session, or Token surfaces (owned by BP-003)
- Deliver the AI Platform, Knowledge Platform, or downstream capability Build Packs
- Deliver billing execution, payment processing, invoicing, or dunning
- Deliver Project, Meeting, Decision, Action, SOP, or Notification capabilities (owned by BP-007, BP-008, BP-009, BP-010)
- Deliver cross-tenant analytics, cross-tenant reporting, or platform-operator surfaces (Implementation Defined During Engineering)

---

# 2. Scope

**In Scope:**

- Organization aggregate lifecycle and governance
- Tenant Registry as authoritative multi-tenant container
- Department and Team hierarchy under an Organization
- Subscription model, plan association, and entitlement resolution
- Organization configuration (General, Business, Security, AI, Notification)
- Organization branding surfaces (logo, display name, default language, time zone)
- Organization administration (Organization Administrator, delegated administrators, admin audit)
- Tenant isolation enforcement primitives consumed by all downstream Build Packs
- Organization storage allocation and quota metering
- Organization events (lifecycle, structure, subscription, entitlement, configuration, administration, storage, audit)
- Organization audit as the authoritative record for tenant state changes

**Out of Scope:**

- User identity, authentication, authorization, session, token, and federation (BP-003)
- Interactive login, machine authentication, agent authentication (BP-003)
- Billing execution, payment processing, invoicing (Implementation Defined During Engineering)
- Project, Meeting, Decision, Action, SOP capabilities (BP-007, BP-008, BP-009)
- Notification delivery (BP-010)
- Integration connectors (BP-011)
- Production operations, deployment, and infrastructure (BP-012)

---

# 3. Repository Alignment

BP-004 conforms to the canonical Build Pack template established by BP-002 and applied by BP-003.

**Authoritative Sources:**

- MC-002 Product Foundation — product definition of Organization as the customer tenant
- MC-004 Core Principles & Governance — repository governance for tenant isolation
- ARCH-001 System Architecture — platform structure and multi-tenant service placement
- ARCH-002 Multi-Tenant Architecture — tenant isolation, organization boundaries, subscription model, tenant lifecycle, multi-tenant governance
- ARCH-004 Data Architecture — tenant-scoped storage strategy and data isolation
- ARCH-005 Security Architecture — tenant-scoped access policy and audit logging
- DOMAIN-001 Organization Domain — Organization aggregate, Department, Team, Configuration, Subscription, Events, Business Rules, Lifecycle Governance, Constraints
- ES-003 Database Standards — tenant-scoped data model rules
- ES-004 Security Standards — tenant-scoped security enforcement
- RA-009 Multi-Tenant Reference Architecture — tenant isolation enforcement, organization provisioning
- RA-005 Data Platform Reference Architecture — tenant-scoped storage, quota, and metering
- RA-001 Backend Reference Architecture — service structure, event emission, audit trail
- RA-011 Security Reference Architecture — tenant-scoped policy enforcement (upstream from BP-003)
- RA-006 Event-Driven Reference Architecture — event contract publication for Organization lifecycle
- BP-002 Platform Foundation — event bus, observability, API gateway, configuration surfaces
- BP-003 Identity & Access Platform — user-to-tenant binding, tenant-scoped identity enforcement

---

# 4. Platform Context Diagram

## 4.1 Consumers of the Tenant & Organization Platform

- BP-003 Identity & Access Platform (tenant binding lookups, user-to-tenant resolution)
- BP-005 AI Platform (tenant-scoped AI configuration, AI usage limits, AI approval policies)
- BP-006 Knowledge Platform (tenant-scoped knowledge repository, storage allocation)
- BP-007 Workflow Platform (tenant-scoped project scoping)
- BP-008 Meeting Intelligence Platform (tenant-scoped meeting scoping)
- BP-009 Decision, Action & SOP Platform (tenant-scoped decision, action, SOP scoping)
- BP-010 Notification Platform (tenant-scoped notification preferences)
- BP-011 Integration Platform (tenant-scoped connector registration)
- BP-012 Production & Operations Platform (tenant-scoped observability, quota metering, audit)
- Platform Administrator surfaces (tenant provisioning, tenant governance, tenant audit review)

## 4.2 External Dependencies

- Platform Event Bus (BP-002) — publishes Organization lifecycle, subscription, entitlement, configuration, administration, storage, and audit events
- Identity & Access Platform (BP-003) — resolves administrator identity for tenant administration operations
- Data Platform (RA-005) — provides tenant-scoped storage substrate
- Secrets Management (BP-002) — houses tenant-scoped configuration secrets (Implementation Defined During Engineering)
- Configuration Service (BP-002) — houses tenant-scoped feature flags and platform configuration
- Observability Stack (RA-010, delivered by BP-012) — receives Tenant & Organization Platform telemetry
- Audit Store (BP-002) — receives Organization audit records

## 4.3 Tenant Isolation Boundary

The Tenant & Organization Platform defines the authoritative tenant isolation boundaries that every downstream Build Pack shall respect.

1. **Registry Boundary** — Every Organization identifier is globally unique and immutable. Organization identifier collisions are rejected at the Registry.
2. **Data Boundary** — Every business record shall carry the Organization identifier. Cross-tenant queries are prohibited unless authorized as platform-operator operations.
3. **Event Boundary** — Every event emitted by the Tenant & Organization Platform carries the Organization identifier. Downstream consumers shall filter by Organization identifier.
4. **Configuration Boundary** — Organization configuration is tenant-scoped. Configuration changes shall not propagate across Organization identifiers.
5. **Administration Boundary** — Organization administration operations shall be authorized against the Organization identifier of the acting administrator. Cross-tenant administration operations are prohibited unless performed by an authorized platform-operator role (Implementation Defined During Engineering).

---

# 5. Organization Lifecycle

Per DOMAIN-001 §5 and §16, the Organization lifecycle is defined by the following stages. Every stage transition shall be authorized and auditable.

| Stage | Description | Authoritative Source |
|--------|-------------|---------------------|
| Provisioning | Organization record is created; identifiers assigned; tenant substrate allocated | DOMAIN-001 §16 |
| Validation | Provisioned Organization is validated for administrator, subscription, and configuration completeness | DOMAIN-001 §16 |
| Activation | Organization transitions to operational state; downstream Build Packs are notified via the Organization Activated event | DOMAIN-001 §5, §15 |
| Operational | Organization is Active; users, projects, meetings, knowledge, decisions, actions, and SOPs are accessible | DOMAIN-001 §5 |
| Suspension | Organization is suspended; operational access is revoked; data is retained | DOMAIN-001 §5, §16 |
| Reactivation | Suspended Organization is reactivated; operational access is restored | DOMAIN-001 §16 |
| Archival | Organization becomes read-only; write operations are rejected | DOMAIN-001 §5, §16 |
| Retention | Organization enters retention period per configured retention policy | DOMAIN-001 §16, ARCH-004 |
| Deletion | Organization is deleted at the end of the retention period; deletion is auditable | DOMAIN-001 §5, §16 |

Every stage transition emits an Organization lifecycle event on the platform event bus. Every stage transition is recorded in the Organization Audit Store.

---

# 6. Components

The Tenant & Organization Platform is composed of the following components. Every component is aligned to DOMAIN-001, ARCH-002, and RA-009.

## 6.1 Tenant Registry Service

Owns the authoritative Organization identifier, Organization Code, Organization Name, Display Name, Status, and creation metadata. Serves as the source of truth for tenant identity across the platform.

## 6.2 Tenant Lifecycle Service

Owns Organization lifecycle transitions (Provisioning, Validation, Activation, Suspension, Reactivation, Archival, Retention, Deletion). Emits lifecycle events. Enforces DOMAIN-001 lifecycle governance rules.

## 6.3 Organization Directory Service

Owns Department and Team entities. Enforces uniqueness of Department and Team names within an Organization. Publishes structure change events consumed by the Identity Domain and downstream Build Packs.

## 6.4 Subscription Service

Owns Subscription identifiers, plan association, billing cycle, renewal date, user limit, storage limit, AI usage limit, API access, and integration access flags. Publishes Subscription Changed events.

## 6.5 Entitlement Service

Resolves Subscription plans into runtime entitlement decisions consumed by every downstream Build Pack. Provides an Entitlement Query API that returns feature availability, quota, and policy decisions.

## 6.6 Organization Configuration Service

Owns Organization configuration categories (General, Business, Security, AI, Notification) and Organization branding. Enforces tenant-scoped configuration integrity. Publishes Configuration Updated events.

## 6.7 Organization Administration Service

Owns the Organization Administrator role, delegated administrator assignments, and administrative operation authorization. Consumes identity resolution from BP-003. Publishes Administration events.

## 6.8 Tenant Isolation Enforcement Library

Provides a shared library consumed by every service in the platform to enforce tenant isolation at the data access layer. Rejects cross-tenant read and write operations unless the caller is authorized as a platform operator.

## 6.9 Storage Allocation Service

Owns Organization storage quotas per storage category (Business Data, Documents, Meeting Recordings, Knowledge Repository, AI Embeddings, Search Indexes, Audit Logs) per DOMAIN-001 §11. Publishes Storage Threshold events.

## 6.10 Organization Event Emitter

Serializes Organization state changes into event contracts and publishes them on the platform event bus established in BP-002 §Event Bus. Ensures event ordering and idempotency.

## 6.11 Organization Audit Service

Records every Organization state transition, configuration change, subscription change, and administrative action as an immutable audit record. Provides audit query surfaces consumed by Organization administrators and platform operators.

## 6.12 Tenant Provisioning Orchestrator

Coordinates the end-to-end provisioning of a new Organization across the Tenant Registry, Organization Directory, Subscription Service, Entitlement Service, Configuration Service, Administration Service, and Storage Allocation Service. Ensures atomicity of tenant provisioning.

## 6.13 Tenant Deprovisioning Orchestrator

Coordinates the end-to-end deprovisioning of an Organization across all tenant-scoped stores per the configured retention policy. Ensures audit-complete deprovisioning aligned to ARCH-004 retention rules.

---

# 7. Repository Mapping

| Component | Owning Domain | Owning Reference Architecture | Owning Engineering Standard | Future Implementation Pack |
|-----------|--------------|-------------------------------|------------------------------|-----------------------------|
| Tenant Registry Service | DOMAIN-001 | RA-009, RA-001 | ES-003 | Implementation Defined During Engineering |
| Tenant Lifecycle Service | DOMAIN-001 | RA-009, RA-001 | ES-003 | Implementation Defined During Engineering |
| Organization Directory Service | DOMAIN-001 | RA-001 | ES-003 | Implementation Defined During Engineering |
| Subscription Service | DOMAIN-001 | RA-009, RA-001 | ES-003 | Implementation Defined During Engineering |
| Entitlement Service | DOMAIN-001 | RA-009, RA-001 | ES-003, ES-004 | Implementation Defined During Engineering |
| Organization Configuration Service | DOMAIN-001 | RA-001 | ES-003 | Implementation Defined During Engineering |
| Organization Administration Service | DOMAIN-001, DOMAIN-002 | RA-009, RA-011 | ES-004 | Implementation Defined During Engineering |
| Tenant Isolation Enforcement Library | DOMAIN-001 | RA-009, RA-011 | ES-003, ES-004 | Implementation Defined During Engineering |
| Storage Allocation Service | DOMAIN-001 | RA-005 | ES-003 | Implementation Defined During Engineering |
| Organization Event Emitter | DOMAIN-001 | RA-006 | ES-001 | Implementation Defined During Engineering |
| Organization Audit Service | DOMAIN-001 | RA-011, RA-010 | ES-004 | Implementation Defined During Engineering |
| Tenant Provisioning Orchestrator | DOMAIN-001 | RA-009, RA-001 | ES-001 | Implementation Defined During Engineering |
| Tenant Deprovisioning Orchestrator | DOMAIN-001 | RA-009, RA-005 | ES-003 | Implementation Defined During Engineering |

---

# 8. Service Inventory

Every service is defined using the 11-field canonical Service Inventory template established by BP-002.

## 8.1 Tenant Registry Service

| Field | Value |
|--------|--------|
| Service ID | SVC-BP004-001 |
| Service Name | Tenant Registry Service |
| Purpose | Owns authoritative Organization identifiers and registry metadata |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-009, RA-001 |
| Primary Consumers | BP-003, Tenant Lifecycle Service, Organization Directory Service, Subscription Service, Entitlement Service, Organization Administration Service, downstream Build Packs |
| Upstream Dependencies | Tenant Registry DB |
| Downstream Dependencies | Organization Event Emitter |
| Events Emitted | organization.registered.v1 |
| Events Consumed | none |
| Deployment Model | Implementation Defined During Engineering |

## 8.2 Tenant Lifecycle Service

| Field | Value |
|--------|--------|
| Service ID | SVC-BP004-002 |
| Service Name | Tenant Lifecycle Service |
| Purpose | Owns Organization lifecycle transitions with authorized and auditable state changes |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-009, RA-001 |
| Primary Consumers | Tenant Provisioning Orchestrator, Tenant Deprovisioning Orchestrator, Organization Administrator surfaces |
| Upstream Dependencies | Tenant Registry Service, Organization Audit Service |
| Downstream Dependencies | Organization Event Emitter |
| Events Emitted | organization.provisioning.v1, organization.validated.v1, organization.activated.v1, organization.suspended.v1, organization.reactivated.v1, organization.archived.v1, organization.retention_entered.v1, organization.deleted.v1 |
| Events Consumed | organization.registered.v1 |
| Deployment Model | Implementation Defined During Engineering |

## 8.3 Organization Directory Service

| Field | Value |
|--------|--------|
| Service ID | SVC-BP004-003 |
| Service Name | Organization Directory Service |
| Purpose | Owns Department and Team entities under an Organization |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-001 |
| Primary Consumers | BP-003, BP-007, BP-009, Organization Administrator surfaces |
| Upstream Dependencies | Tenant Registry Service, Organization Configuration DB |
| Downstream Dependencies | Organization Event Emitter |
| Events Emitted | organization.department_created.v1, organization.department_updated.v1, organization.department_removed.v1, organization.team_created.v1, organization.team_updated.v1, organization.team_removed.v1 |
| Events Consumed | organization.activated.v1, organization.suspended.v1, organization.archived.v1 |
| Deployment Model | Implementation Defined During Engineering |

## 8.4 Subscription Service

| Field | Value |
|--------|--------|
| Service ID | SVC-BP004-004 |
| Service Name | Subscription Service |
| Purpose | Owns Subscription plan association, billing cycle, and limits per Organization |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-009, RA-001 |
| Primary Consumers | Entitlement Service, Organization Administrator surfaces, downstream Build Packs |
| Upstream Dependencies | Tenant Registry Service, Subscription DB |
| Downstream Dependencies | Organization Event Emitter |
| Events Emitted | subscription.created.v1, subscription.updated.v1, subscription.plan_changed.v1, subscription.renewed.v1, subscription.expired.v1, subscription.canceled.v1 |
| Events Consumed | organization.activated.v1, organization.suspended.v1 |
| Deployment Model | Implementation Defined During Engineering |

## 8.5 Entitlement Service

| Field | Value |
|--------|--------|
| Service ID | SVC-BP004-005 |
| Service Name | Entitlement Service |
| Purpose | Resolves Subscription plans into runtime entitlement decisions for downstream Build Packs |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-009, RA-001 |
| Primary Consumers | BP-003, BP-005, BP-006, BP-007, BP-008, BP-009, BP-010, BP-011 |
| Upstream Dependencies | Subscription Service, Entitlement Cache |
| Downstream Dependencies | Organization Event Emitter |
| Events Emitted | entitlement.recomputed.v1, entitlement.violation_detected.v1 |
| Events Consumed | subscription.created.v1, subscription.updated.v1, subscription.plan_changed.v1, subscription.expired.v1, subscription.canceled.v1 |
| Deployment Model | Implementation Defined During Engineering |

## 8.6 Organization Configuration Service

| Field | Value |
|--------|--------|
| Service ID | SVC-BP004-006 |
| Service Name | Organization Configuration Service |
| Purpose | Owns Organization configuration surfaces (General, Business, Security, AI, Notification) and branding |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-001 |
| Primary Consumers | BP-003, BP-005, BP-006, BP-007, BP-008, BP-009, BP-010, Organization Administrator surfaces |
| Upstream Dependencies | Tenant Registry Service, Organization Configuration DB |
| Downstream Dependencies | Organization Event Emitter |
| Events Emitted | organization.configuration_updated.v1, organization.branding_updated.v1, organization.security_policy_updated.v1, organization.ai_configuration_updated.v1, organization.notification_preferences_updated.v1 |
| Events Consumed | organization.activated.v1 |
| Deployment Model | Implementation Defined During Engineering |

## 8.7 Organization Administration Service

| Field | Value |
|--------|--------|
| Service ID | SVC-BP004-007 |
| Service Name | Organization Administration Service |
| Purpose | Owns Organization Administrator role, delegated administrator assignments, and administrative authorization |
| Owning Domain | DOMAIN-001, DOMAIN-002 |
| Owning Reference Architecture | RA-009, RA-011 |
| Primary Consumers | Organization Administrator surfaces, BP-003 Authorization PDP |
| Upstream Dependencies | Tenant Registry Service, BP-003 Identity Directory, BP-003 Authorization PDP |
| Downstream Dependencies | Organization Event Emitter, Organization Audit Service |
| Events Emitted | organization.administrator_assigned.v1, organization.administrator_revoked.v1, organization.delegated_administrator_assigned.v1, organization.delegated_administrator_revoked.v1 |
| Events Consumed | organization.activated.v1, organization.suspended.v1, organization.archived.v1 |
| Deployment Model | Implementation Defined During Engineering |

## 8.8 Tenant Isolation Enforcement Library

| Field | Value |
|--------|--------|
| Service ID | SVC-BP004-008 |
| Service Name | Tenant Isolation Enforcement Library |
| Purpose | Provides shared enforcement primitives to reject cross-tenant read and write operations at every service boundary |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-009, RA-011 |
| Primary Consumers | Every platform service (BP-002 through BP-012) |
| Upstream Dependencies | Tenant Registry Service |
| Downstream Dependencies | Organization Audit Service |
| Events Emitted | tenant.isolation_violation_detected.v1 |
| Events Consumed | none |
| Deployment Model | Implementation Defined During Engineering (delivered as a shared library rather than a standalone service) |

## 8.9 Storage Allocation Service

| Field | Value |
|--------|--------|
| Service ID | SVC-BP004-009 |
| Service Name | Storage Allocation Service |
| Purpose | Owns Organization storage quotas per storage category and emits quota threshold events |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-005 |
| Primary Consumers | BP-006, BP-008, BP-010, Organization Administrator surfaces |
| Upstream Dependencies | Subscription Service, Storage Allocation DB |
| Downstream Dependencies | Organization Event Emitter |
| Events Emitted | storage.quota_updated.v1, storage.threshold_reached.v1, storage.quota_exceeded.v1 |
| Events Consumed | subscription.plan_changed.v1, subscription.updated.v1 |
| Deployment Model | Implementation Defined During Engineering |

## 8.10 Organization Event Emitter

| Field | Value |
|--------|--------|
| Service ID | SVC-BP004-010 |
| Service Name | Organization Event Emitter |
| Purpose | Serializes Organization state changes into event contracts and publishes them on the platform event bus |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-006 |
| Primary Consumers | BP-002 Event Bus, downstream Build Packs |
| Upstream Dependencies | Tenant Registry Service, Tenant Lifecycle Service, Organization Directory Service, Subscription Service, Entitlement Service, Organization Configuration Service, Organization Administration Service, Storage Allocation Service, BP-002 Outbox |
| Downstream Dependencies | BP-002 Event Bus |
| Events Emitted | all events listed under §8.1 through §8.9 |
| Events Consumed | none |
| Deployment Model | Implementation Defined During Engineering (delivered as a shared component using the outbox pattern established in BP-002) |

## 8.11 Organization Audit Service

| Field | Value |
|--------|--------|
| Service ID | SVC-BP004-011 |
| Service Name | Organization Audit Service |
| Purpose | Records every Organization state transition, configuration change, subscription change, and administrative action as an immutable audit record |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-011, RA-010 |
| Primary Consumers | Organization Administrator surfaces, platform operators, BP-012 |
| Upstream Dependencies | Tenant Lifecycle Service, Organization Configuration Service, Subscription Service, Organization Administration Service, Storage Allocation Service, Tenant Isolation Enforcement Library, Organization Audit Store |
| Downstream Dependencies | Organization Audit Store, Organization Event Emitter |
| Events Emitted | organization.audit_record_created.v1 |
| Events Consumed | organization.provisioning.v1, organization.activated.v1, organization.suspended.v1, organization.reactivated.v1, organization.archived.v1, organization.retention_entered.v1, organization.deleted.v1, organization.configuration_updated.v1, subscription.plan_changed.v1, organization.administrator_assigned.v1, organization.administrator_revoked.v1, tenant.isolation_violation_detected.v1 |
| Deployment Model | Implementation Defined During Engineering |

## 8.12 Tenant Provisioning Orchestrator

| Field | Value |
|--------|--------|
| Service ID | SVC-BP004-012 |
| Service Name | Tenant Provisioning Orchestrator |
| Purpose | Coordinates the end-to-end provisioning of a new Organization across Tenant Registry, Directory, Subscription, Entitlement, Configuration, Administration, and Storage Allocation |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-009, RA-001 |
| Primary Consumers | Organization Administrator surfaces, platform operators |
| Upstream Dependencies | Tenant Registry Service, Tenant Lifecycle Service, Organization Directory Service, Subscription Service, Entitlement Service, Organization Configuration Service, Organization Administration Service, Storage Allocation Service |
| Downstream Dependencies | Organization Event Emitter, Organization Audit Service |
| Events Emitted | organization.provisioning_started.v1, organization.provisioning_completed.v1, organization.provisioning_failed.v1 |
| Events Consumed | organization.registered.v1 |
| Deployment Model | Implementation Defined During Engineering |

## 8.13 Tenant Deprovisioning Orchestrator

| Field | Value |
|--------|--------|
| Service ID | SVC-BP004-013 |
| Service Name | Tenant Deprovisioning Orchestrator |
| Purpose | Coordinates end-to-end deprovisioning of an Organization across all tenant-scoped stores per configured retention policy |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-009, RA-005 |
| Primary Consumers | Platform operators, Organization Administrator surfaces |
| Upstream Dependencies | Tenant Registry Service, Tenant Lifecycle Service, Storage Allocation Service, Organization Audit Service, retention policy configuration |
| Downstream Dependencies | Organization Event Emitter, Organization Audit Service |
| Events Emitted | organization.deprovisioning_started.v1, organization.deprovisioning_completed.v1, organization.deprovisioning_failed.v1 |
| Events Consumed | organization.retention_entered.v1 |
| Deployment Model | Implementation Defined During Engineering |

---

# 9. Required APIs

The following API surfaces shall be delivered. Specific API contracts (paths, request/response schemas, authentication) are Implementation Defined During Engineering and shall be recorded in the API specifications under `10_API/`.

**Tenant Registry APIs:**

- Register Organization
- Retrieve Organization by identifier
- Retrieve Organization by Organization Code
- List Organizations (platform-operator scope)

**Tenant Lifecycle APIs:**

- Transition Organization state (Provisioning → Validation → Activation → Suspension → Reactivation → Archival → Retention → Deletion)
- Retrieve Organization lifecycle history

**Organization Directory APIs:**

- Create, retrieve, update, remove Department
- Create, retrieve, update, remove Team
- List Departments within an Organization
- List Teams within a Department

**Subscription APIs:**

- Assign Subscription plan to Organization
- Update Subscription plan
- Retrieve Subscription for Organization
- Retrieve Subscription history

**Entitlement APIs:**

- Query Entitlement for a feature within an Organization
- Query quota status for a feature within an Organization
- Recompute entitlements for an Organization

**Organization Configuration APIs:**

- Retrieve Organization configuration (General, Business, Security, AI, Notification)
- Update Organization configuration (per category)
- Retrieve Organization branding
- Update Organization branding

**Organization Administration APIs:**

- Assign Organization Administrator
- Revoke Organization Administrator
- Assign delegated administrator
- Revoke delegated administrator
- List administrators for an Organization

**Storage Allocation APIs:**

- Retrieve storage allocation for an Organization
- Retrieve storage usage per category
- Update storage quota (platform-operator scope)

**Organization Audit APIs:**

- Query audit records for an Organization
- Query audit records by administrator
- Query audit records by event category

All APIs shall enforce tenant isolation via the Tenant Isolation Enforcement Library. All APIs shall be authenticated via BP-003 authentication surfaces and authorized via BP-003 Authorization PDP.

---

# 10. Required Databases

Every database is defined using the 11-field canonical Required Databases template established by BP-002.

## 10.1 Tenant Registry DB

| Field | Value |
|--------|--------|
| Database ID | DB-BP004-001 |
| Database Name | Tenant Registry DB |
| Purpose | Stores authoritative Organization identifiers, Organization Codes, Organization Names, Display Names, Status, and creation metadata |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-005, RA-009 |
| Storage Class | Relational |
| Tenant Isolation Model | Registry is cross-tenant by design (holds the identifier used for tenant isolation elsewhere); access is restricted to Tenant Registry Service and platform operators |
| Retention Policy | Retained indefinitely; deletion follows Tenant Deprovisioning Orchestrator per ARCH-004 retention rules |
| Backup Policy | Implementation Defined During Engineering |
| Consumers | Tenant Registry Service |
| Deployment Model | Implementation Defined During Engineering |

## 10.2 Organization Configuration DB

| Field | Value |
|--------|--------|
| Database ID | DB-BP004-002 |
| Database Name | Organization Configuration DB |
| Purpose | Stores Organization configuration (General, Business, Security, AI, Notification), branding, Departments, and Teams |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-005, RA-001 |
| Storage Class | Relational |
| Tenant Isolation Model | Every record carries Organization identifier; Tenant Isolation Enforcement Library rejects cross-tenant access |
| Retention Policy | Retained for the operational lifetime of the Organization; purged during Tenant Deprovisioning per configured retention policy |
| Backup Policy | Implementation Defined During Engineering |
| Consumers | Organization Configuration Service, Organization Directory Service |
| Deployment Model | Implementation Defined During Engineering |

## 10.3 Subscription DB

| Field | Value |
|--------|--------|
| Database ID | DB-BP004-003 |
| Database Name | Subscription DB |
| Purpose | Stores Subscription identifiers, plan association, billing cycle, renewal, and limits per Organization |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-005, RA-009 |
| Storage Class | Relational |
| Tenant Isolation Model | Every subscription record carries Organization identifier; access is restricted to Subscription Service and Entitlement Service |
| Retention Policy | Subscription history retained per configured retention policy; audit references retained beyond active subscription |
| Backup Policy | Implementation Defined During Engineering |
| Consumers | Subscription Service, Entitlement Service |
| Deployment Model | Implementation Defined During Engineering |

## 10.4 Entitlement Cache

| Field | Value |
|--------|--------|
| Database ID | DB-BP004-004 |
| Database Name | Entitlement Cache |
| Purpose | Stores precomputed entitlement decisions for low-latency lookup by downstream Build Packs |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-005, RA-001 |
| Storage Class | In-memory cache |
| Tenant Isolation Model | Cache keys carry Organization identifier; cache access is authorized via Tenant Isolation Enforcement Library |
| Retention Policy | Cache is transient; invalidated on subscription or plan change events |
| Backup Policy | Not applicable (cache is rebuildable from Subscription DB) |
| Consumers | Entitlement Service |
| Deployment Model | Implementation Defined During Engineering |

## 10.5 Storage Allocation DB

| Field | Value |
|--------|--------|
| Database ID | DB-BP004-005 |
| Database Name | Storage Allocation DB |
| Purpose | Stores Organization storage quotas per storage category and current usage measurements |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-005 |
| Storage Class | Relational |
| Tenant Isolation Model | Every record carries Organization identifier; Tenant Isolation Enforcement Library rejects cross-tenant access |
| Retention Policy | Retained for operational lifetime of the Organization |
| Backup Policy | Implementation Defined During Engineering |
| Consumers | Storage Allocation Service |
| Deployment Model | Implementation Defined During Engineering |

## 10.6 Organization Audit Store

| Field | Value |
|--------|--------|
| Database ID | DB-BP004-006 |
| Database Name | Organization Audit Store |
| Purpose | Stores immutable audit records for every Organization state transition, configuration change, subscription change, and administrative action |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-011, RA-010 |
| Storage Class | Append-only relational or object store (Implementation Defined During Engineering) |
| Tenant Isolation Model | Every record carries Organization identifier; audit queries are tenant-scoped for administrators; cross-tenant queries are restricted to platform operators |
| Retention Policy | Retained per compliance and regulatory requirements as configured in ARCH-004 retention policy |
| Backup Policy | Implementation Defined During Engineering |
| Consumers | Organization Audit Service |
| Deployment Model | Implementation Defined During Engineering |

---

# 11. Required Events

Every event category is defined using the 11-field canonical Required Events template established by BP-002. Every event carries the Organization identifier.

## 11.1 Organization Lifecycle Events

| Field | Value |
|--------|--------|
| Event Category ID | EVT-BP004-001 |
| Event Category Name | Organization Lifecycle Events |
| Purpose | Notifies downstream Build Packs of Organization lifecycle transitions |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-006 |
| Event Names | organization.provisioning.v1, organization.validated.v1, organization.activated.v1, organization.suspended.v1, organization.reactivated.v1, organization.archived.v1, organization.retention_entered.v1, organization.deleted.v1 |
| Producers | Tenant Lifecycle Service |
| Consumers | BP-003, BP-005, BP-006, BP-007, BP-008, BP-009, BP-010, BP-011, BP-012, Organization Audit Service |
| Ordering Guarantee | Ordered per Organization identifier |
| Delivery Semantics | At-least-once with idempotent consumers |
| Schema Location | Implementation Defined During Engineering |

## 11.2 Organization Structure Events

| Field | Value |
|--------|--------|
| Event Category ID | EVT-BP004-002 |
| Event Category Name | Organization Structure Events |
| Purpose | Notifies downstream Build Packs of Department and Team changes |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-006 |
| Event Names | organization.department_created.v1, organization.department_updated.v1, organization.department_removed.v1, organization.team_created.v1, organization.team_updated.v1, organization.team_removed.v1 |
| Producers | Organization Directory Service |
| Consumers | BP-003, BP-007, BP-009 |
| Ordering Guarantee | Ordered per Organization identifier |
| Delivery Semantics | At-least-once with idempotent consumers |
| Schema Location | Implementation Defined During Engineering |

## 11.3 Subscription Events

| Field | Value |
|--------|--------|
| Event Category ID | EVT-BP004-003 |
| Event Category Name | Subscription Events |
| Purpose | Notifies downstream Build Packs of Subscription and plan changes |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-006, RA-009 |
| Event Names | subscription.created.v1, subscription.updated.v1, subscription.plan_changed.v1, subscription.renewed.v1, subscription.expired.v1, subscription.canceled.v1 |
| Producers | Subscription Service |
| Consumers | Entitlement Service, BP-005, BP-006, BP-010, BP-011 |
| Ordering Guarantee | Ordered per Organization identifier |
| Delivery Semantics | At-least-once with idempotent consumers |
| Schema Location | Implementation Defined During Engineering |

## 11.4 Entitlement Events

| Field | Value |
|--------|--------|
| Event Category ID | EVT-BP004-004 |
| Event Category Name | Entitlement Events |
| Purpose | Notifies downstream Build Packs of entitlement recomputations and violations |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-006, RA-009 |
| Event Names | entitlement.recomputed.v1, entitlement.violation_detected.v1 |
| Producers | Entitlement Service |
| Consumers | BP-003, BP-005, BP-006, BP-007, BP-008, BP-009, BP-010, BP-011 |
| Ordering Guarantee | Ordered per Organization identifier |
| Delivery Semantics | At-least-once with idempotent consumers |
| Schema Location | Implementation Defined During Engineering |

## 11.5 Configuration Events

| Field | Value |
|--------|--------|
| Event Category ID | EVT-BP004-005 |
| Event Category Name | Configuration Events |
| Purpose | Notifies downstream Build Packs of Organization configuration changes |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-006 |
| Event Names | organization.configuration_updated.v1, organization.branding_updated.v1, organization.security_policy_updated.v1, organization.ai_configuration_updated.v1, organization.notification_preferences_updated.v1 |
| Producers | Organization Configuration Service |
| Consumers | BP-003, BP-005, BP-006, BP-010 |
| Ordering Guarantee | Ordered per Organization identifier |
| Delivery Semantics | At-least-once with idempotent consumers |
| Schema Location | Implementation Defined During Engineering |

## 11.6 Administration Events

| Field | Value |
|--------|--------|
| Event Category ID | EVT-BP004-006 |
| Event Category Name | Administration Events |
| Purpose | Notifies downstream Build Packs of Organization administrator assignments and revocations |
| Owning Domain | DOMAIN-001, DOMAIN-002 |
| Owning Reference Architecture | RA-006, RA-011 |
| Event Names | organization.administrator_assigned.v1, organization.administrator_revoked.v1, organization.delegated_administrator_assigned.v1, organization.delegated_administrator_revoked.v1 |
| Producers | Organization Administration Service |
| Consumers | BP-003, Organization Audit Service |
| Ordering Guarantee | Ordered per Organization identifier |
| Delivery Semantics | At-least-once with idempotent consumers |
| Schema Location | Implementation Defined During Engineering |

## 11.7 Storage Events

| Field | Value |
|--------|--------|
| Event Category ID | EVT-BP004-007 |
| Event Category Name | Storage Events |
| Purpose | Notifies downstream Build Packs of storage quota updates and threshold breaches |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-006, RA-005 |
| Event Names | storage.quota_updated.v1, storage.threshold_reached.v1, storage.quota_exceeded.v1 |
| Producers | Storage Allocation Service |
| Consumers | BP-006, BP-008, BP-010, Organization Administrator surfaces |
| Ordering Guarantee | Ordered per Organization identifier |
| Delivery Semantics | At-least-once with idempotent consumers |
| Schema Location | Implementation Defined During Engineering |

## 11.8 Organization Audit Events

| Field | Value |
|--------|--------|
| Event Category ID | EVT-BP004-008 |
| Event Category Name | Organization Audit Events |
| Purpose | Notifies platform operators and Organization administrators of audit record creation and tenant isolation violations |
| Owning Domain | DOMAIN-001 |
| Owning Reference Architecture | RA-006, RA-011, RA-010 |
| Event Names | organization.audit_record_created.v1, tenant.isolation_violation_detected.v1 |
| Producers | Organization Audit Service, Tenant Isolation Enforcement Library |
| Consumers | Organization Administrator surfaces, BP-012 |
| Ordering Guarantee | Ordered per Organization identifier |
| Delivery Semantics | At-least-once with idempotent consumers |
| Schema Location | Implementation Defined During Engineering |

---

# 12. Required Configuration

The following tenant-scoped configuration surfaces shall be exposed. Specific configuration schemas are Implementation Defined During Engineering.

- Organization General (name, display name, code, time zone, default language, country, industry, organization size)
- Organization Business (working hours, fiscal year, holiday calendar)
- Organization Security (password policy, MFA policy, session timeout — federated to BP-003)
- Organization AI (default AI provider, AI usage limits, AI approval policies — federated to BP-005)
- Organization Notification (email preferences, push notifications, digest frequency — federated to BP-010)
- Organization Branding (logo, display name, colors, default language)
- Subscription (plan, billing cycle, renewal date, user limit, storage limit, AI usage limit, API access, integration access)
- Storage Allocation (per-category quotas)
- Retention Policy (per DOMAIN-001 §16 and ARCH-004)

---

# 13. Security

Aligned to ARCH-005, ES-004, and RA-011.

- Every API surface shall be authenticated via BP-003 authentication surfaces (Interactive, Machine, or Agent).
- Every API surface shall be authorized via BP-003 Authorization PDP against tenant-scoped policies.
- Every tenant-scoped data access shall pass through the Tenant Isolation Enforcement Library.
- Every configuration change, subscription change, and administrative action shall be recorded in the Organization Audit Store.
- Organization Administrator role assignments shall be authorized against the acting administrator's Organization identifier.
- Platform-operator operations that cross tenant boundaries shall be authorized against a distinct platform-operator role (Implementation Defined During Engineering) and shall be recorded in a platform-operator audit surface.
- Tenant isolation violations shall raise a `tenant.isolation_violation_detected.v1` event and shall be alerted through the observability stack established in BP-012.

---

# 14. Multi-Tenant

Aligned to ARCH-002 and RA-009.

- The Organization identifier is the authoritative tenant identifier used across the platform.
- Organization identifiers are globally unique and immutable per DOMAIN-001 §17.
- Every downstream Build Pack shall carry the Organization identifier on every business record, event, and API request.
- Cross-tenant read and write operations are prohibited except for authorized platform-operator surfaces.
- Tenant provisioning is coordinated by the Tenant Provisioning Orchestrator and shall be atomic across Registry, Directory, Subscription, Entitlement, Configuration, Administration, and Storage Allocation.
- Tenant deprovisioning is coordinated by the Tenant Deprovisioning Orchestrator and shall respect ARCH-004 retention policies.
- Suspended and Archived Organizations shall reject write operations at the Tenant Isolation Enforcement Library level.

---

# 15. AI Integration

Aligned to ARCH-003, DOMAIN-010, and BP-005.

- Organization AI configuration (default AI provider, AI usage limits, AI approval policies) is owned by the Organization Configuration Service and is federated to BP-005 AI Platform at runtime.
- AI usage quota decisions are resolved through the Entitlement Service.
- AI context shall never cross Organization boundaries per DOMAIN-001 §13.
- AI configuration change events are published on the platform event bus for BP-005 consumers.
- The Tenant & Organization Platform does not deliver AI capabilities directly; AI capabilities are delivered by BP-005.

---

# 16. Observability

Aligned to RA-010 and BP-012.

- Every service in BP-004 shall emit structured logs, metrics, and traces per the platform observability contract established in BP-002.
- Every event emission shall be traceable end-to-end via correlation identifiers.
- Organization lifecycle transitions shall be observable through dedicated metrics (provisioning duration, activation success rate, suspension count, deletion count).
- Subscription and entitlement recomputations shall be observable through dedicated metrics.
- Tenant isolation violation events shall be alerted through the observability stack.
- Organization audit records shall be queryable through the Organization Audit APIs and through platform-operator observability surfaces (Implementation Defined During Engineering).

---

# 17. Deployment

Aligned to ARCH-007, ES-006, and RA-004.

- Every service in BP-004 shall be deployable independently through the platform CI/CD pipelines established in BP-000 and BP-002.
- Every service shall respect the platform container, image, and configuration contract established in BP-002.
- Every database in BP-004 shall be provisioned through the platform data provisioning surfaces established in BP-002 (Implementation Defined During Engineering).
- Every service shall be observable, restartable, and rollback-safe.
- Tenant Registry Service, Tenant Lifecycle Service, and Subscription Service shall be highly available. Availability targets are Implementation Defined During Engineering.

---

# 18. Testing

Aligned to ES-007.

- Unit tests shall cover Organization lifecycle transitions, tenant isolation enforcement, entitlement resolution, and subscription plan changes.
- Integration tests shall cover Tenant Provisioning Orchestrator and Tenant Deprovisioning Orchestrator end-to-end paths.
- Contract tests shall cover every event emitted by BP-004 against downstream consumers (BP-003, BP-005, BP-006, BP-007, BP-008, BP-009, BP-010, BP-011).
- Tenant isolation tests shall verify that cross-tenant read and write operations are rejected at every service boundary.
- Audit tests shall verify that every state transition, configuration change, subscription change, and administrative action produces exactly one audit record.
- Load and performance tests are Implementation Defined During Engineering.

---

# 19. Implementation Readiness Matrix

Every capability is defined using the 9-field canonical Implementation Readiness Matrix template established by BP-002.

| Capability ID | Capability | Owning Domain | Owning RA | Owning ES | Status | Blockers | Verification Method | Notes |
|---------------|------------|----------------|-----------|-----------|--------|----------|----------------------|--------|
| CAP-BP004-001 | Tenant Registry | DOMAIN-001 | RA-009, RA-001 | ES-003 | Ready | None | Unit + Integration | Authoritative Organization identifier |
| CAP-BP004-002 | Tenant Lifecycle | DOMAIN-001 | RA-009 | ES-003 | Ready | None | Unit + Integration + Audit | Provisioning through Deletion |
| CAP-BP004-003 | Organization Directory | DOMAIN-001 | RA-001 | ES-003 | Ready | None | Unit + Integration | Departments and Teams |
| CAP-BP004-004 | Subscription Management | DOMAIN-001 | RA-009 | ES-003 | Ready | None | Unit + Integration | Plan, billing cycle, limits |
| CAP-BP004-005 | Entitlement Resolution | DOMAIN-001 | RA-009 | ES-003, ES-004 | Ready | None | Unit + Integration + Contract | Runtime entitlement decisions |
| CAP-BP004-006 | Organization Configuration | DOMAIN-001 | RA-001 | ES-003 | Ready | None | Unit + Integration | General/Business/Security/AI/Notification |
| CAP-BP004-007 | Organization Administration | DOMAIN-001, DOMAIN-002 | RA-009, RA-011 | ES-004 | Ready | BP-003 Authorization PDP available | Unit + Integration | Administrator role assignments |
| CAP-BP004-008 | Tenant Isolation Enforcement | DOMAIN-001 | RA-009, RA-011 | ES-003, ES-004 | Ready | None | Unit + Integration + Security | Shared enforcement library |
| CAP-BP004-009 | Storage Allocation | DOMAIN-001 | RA-005 | ES-003 | Ready | None | Unit + Integration | Quota per storage category |
| CAP-BP004-010 | Organization Event Emission | DOMAIN-001 | RA-006 | ES-001 | Ready | BP-002 Event Bus and Outbox available | Contract | Outbox-backed event emission |
| CAP-BP004-011 | Organization Audit | DOMAIN-001 | RA-011, RA-010 | ES-004 | Ready | None | Unit + Integration + Audit | Immutable audit record |
| CAP-BP004-012 | Tenant Provisioning Orchestration | DOMAIN-001 | RA-009 | ES-001 | Ready | Every dependent service available | Integration | Atomic tenant provisioning |
| CAP-BP004-013 | Tenant Deprovisioning Orchestration | DOMAIN-001 | RA-009, RA-005 | ES-003 | Ready | Retention policy configured | Integration | Retention-aligned deprovisioning |

---

# 20. Acceptance Criteria

BP-004 is considered ready for engineering review when:

- Every capability in §19 is documented and traceable
- Every service in §8 is documented using the 11-field template
- Every database in §10 is documented using the 11-field template
- Every event category in §11 is documented using the 11-field template
- Every Traceability Matrix row in §26 resolves to an authoritative source
- Every Engineering Decision in §27 is recorded with rationale and impact
- Every cross-reference in §28 resolves to an approved or draft repository document

---

# 21. Definition of Done

BP-004 is considered Done when:

- Engineering Review is complete and approved
- Every downstream Build Pack (BP-005 through BP-012) has confirmed compatibility with BP-004 tenant isolation and Organization events
- Every event contract in §11 is published in the platform event schema registry (Implementation Defined During Engineering)
- Every API surface in §9 has an approved API specification under `10_API/`
- Every database in §10 has an approved schema under `11_Database/`
- Every capability in §19 has an approved Implementation Pack under `06_Implementation_Packs/`

---

# 22. Engineering Checklist

- [ ] Tenant Registry Service implemented and integration-tested
- [ ] Tenant Lifecycle Service implemented and audit-verified
- [ ] Organization Directory Service implemented
- [ ] Subscription Service implemented
- [ ] Entitlement Service implemented and contract-tested against BP-005/BP-006/BP-007
- [ ] Organization Configuration Service implemented
- [ ] Organization Administration Service implemented and integrated with BP-003 Authorization PDP
- [ ] Tenant Isolation Enforcement Library implemented and consumed by every platform service
- [ ] Storage Allocation Service implemented
- [ ] Organization Event Emitter implemented on top of BP-002 Outbox
- [ ] Organization Audit Service implemented
- [ ] Tenant Provisioning Orchestrator implemented and integration-tested
- [ ] Tenant Deprovisioning Orchestrator implemented and retention-verified
- [ ] Every event contract registered in schema registry
- [ ] Every API surface specified under `10_API/`
- [ ] Every database schema specified under `11_Database/`
- [ ] Observability integration validated
- [ ] Security review approved
- [ ] Multi-tenant governance review approved

---

# 23. Risks

- **R-BP004-001** — Entitlement resolution latency may become a hot path for every downstream Build Pack. Mitigation: Entitlement Cache with event-driven invalidation.
- **R-BP004-002** — Tenant Provisioning Orchestrator failure may leave a partially provisioned Organization. Mitigation: idempotent provisioning steps and compensating deprovisioning path.
- **R-BP004-003** — Tenant Deprovisioning Orchestrator may miss tenant-scoped stores in downstream Build Packs authored after BP-004. Mitigation: mandatory tenant-scoped store registration contract enforced in every subsequent Build Pack.
- **R-BP004-004** — Configuration change events may bombard downstream consumers under heavy administration activity. Mitigation: debounce and coalesce configuration events at the Organization Event Emitter (Implementation Defined During Engineering).
- **R-BP004-005** — Cross-tenant queries by platform operators may inadvertently violate isolation contracts. Mitigation: distinct platform-operator role, explicit cross-tenant surfaces, and dedicated platform-operator audit trail.
- **R-BP004-006** — Subscription plan changes may leave downstream Build Packs operating with stale entitlement decisions. Mitigation: `entitlement.recomputed.v1` event and short-TTL Entitlement Cache.

---

# 24. Assumptions

- BP-000 governance and BP-001 product foundation are Approved and stable.
- BP-002 Platform Foundation is available and provides the Event Bus, Outbox, API Gateway, Observability, and Configuration surfaces.
- BP-003 Identity & Access Platform is available and provides administrator identity resolution and Authorization PDP surfaces.
- ARCH-002 Multi-Tenant Architecture defines tenant isolation contracts that are respected by every downstream Build Pack.
- RA-005 Data Platform Reference Architecture defines the tenant-scoped storage substrate consumed by BP-004.
- RA-006 Event-Driven Reference Architecture defines the event delivery contract consumed by BP-004.
- Retention policies for Organization deprovisioning are configurable at the platform level.

---

# 25. Out of Scope

- Billing execution, payment processing, invoicing, dunning
- Cross-tenant reporting, cross-tenant analytics, cross-tenant AI training
- User identity, authentication, authorization, session, token, federation (owned by BP-003)
- Project, Meeting, Decision, Action, SOP, Notification, Integration, Production capabilities
- Platform-operator surfaces beyond the tenant isolation boundary hooks called out in §4.3 and §13 (Implementation Defined During Engineering as part of BP-012)

---

# 26. Traceability Matrix

Every row is defined using the 8-column canonical Traceability Matrix template established by BP-002.

| Row | Requirement / Capability | Master Context | Architecture | Domain | Engineering Standard | Reference Architecture | Downstream Consumer |
|-----|--------------------------|-----------------|---------------|--------|----------------------|-------------------------|---------------------|
| 1 | Tenant Registry as authoritative identifier | MC-002, MC-004 | ARCH-002 | DOMAIN-001 §4, §17 | ES-003 | RA-009 | BP-003, all downstream BPs |
| 2 | Organization identifier globally unique and immutable | MC-004 | ARCH-002 | DOMAIN-001 §17 | ES-003 | RA-009 | All downstream BPs |
| 3 | Organization lifecycle Provisioning → Deletion | MC-002 | ARCH-002 | DOMAIN-001 §5, §16 | ES-003 | RA-009 | BP-012 |
| 4 | Department and Team hierarchy | MC-002 | ARCH-002 | DOMAIN-001 §6, §7, §8 | ES-003 | RA-001 | BP-003, BP-007, BP-009 |
| 5 | Subscription plan association | MC-002 | ARCH-002 | DOMAIN-001 §10 | ES-003 | RA-009 | BP-005, BP-006, BP-010 |
| 6 | Entitlement resolution for downstream capabilities | MC-002 | ARCH-002 | DOMAIN-001 §10 | ES-003, ES-004 | RA-009 | BP-005, BP-006, BP-007, BP-008, BP-009, BP-010, BP-011 |
| 7 | Organization Configuration surfaces (General/Business/Security/AI/Notification) | MC-002 | ARCH-002 | DOMAIN-001 §9 | ES-003 | RA-001 | BP-003, BP-005, BP-006, BP-010 |
| 8 | Organization Branding | MC-002 | ARCH-002 | DOMAIN-001 §9 | ES-003 | RA-001 | Frontend surfaces (RA-002) |
| 9 | Organization Administrator role | MC-002 | ARCH-005 | DOMAIN-001 §12 | ES-004 | RA-011 | BP-003 Authorization PDP |
| 10 | Delegated administrator model | MC-002 | ARCH-005 | DOMAIN-001 §12 | ES-004 | RA-011 | BP-003 Authorization PDP |
| 11 | Tenant isolation across identity | MC-004 | ARCH-002, ARCH-005 | DOMAIN-001 §13, §17 | ES-004 | RA-009, RA-011 | BP-003 |
| 12 | Tenant isolation across data | MC-004 | ARCH-002, ARCH-004 | DOMAIN-001 §13, §17 | ES-003 | RA-009, RA-005 | All downstream BPs |
| 13 | Tenant isolation across events | MC-004 | ARCH-002 | DOMAIN-001 §13, §15 | ES-001 | RA-009, RA-006 | All downstream BPs |
| 14 | Tenant isolation across configuration | MC-004 | ARCH-002 | DOMAIN-001 §13 | ES-003 | RA-009 | All downstream BPs |
| 15 | Tenant isolation across administration | MC-004 | ARCH-002, ARCH-005 | DOMAIN-001 §12, §13 | ES-004 | RA-009, RA-011 | BP-012 |
| 16 | Organization storage allocation | MC-002 | ARCH-004 | DOMAIN-001 §11 | ES-003 | RA-005 | BP-006, BP-008, BP-010 |
| 17 | Storage quota threshold events | MC-002 | ARCH-004 | DOMAIN-001 §11 | ES-001 | RA-005, RA-006 | BP-006, BP-008, BP-010 |
| 18 | Organization lifecycle events | MC-002 | ARCH-002 | DOMAIN-001 §15 | ES-001 | RA-006 | All downstream BPs |
| 19 | Organization structure events | MC-002 | ARCH-002 | DOMAIN-001 §15 | ES-001 | RA-006 | BP-003, BP-007, BP-009 |
| 20 | Subscription events | MC-002 | ARCH-002 | DOMAIN-001 §15 | ES-001 | RA-006 | BP-005, BP-006, BP-010, BP-011 |
| 21 | Entitlement events | MC-002 | ARCH-002 | DOMAIN-001 §15 | ES-001 | RA-006 | BP-003, BP-005, BP-006, BP-007, BP-008, BP-009, BP-010, BP-011 |
| 22 | Configuration events | MC-002 | ARCH-002 | DOMAIN-001 §15 | ES-001 | RA-006 | BP-003, BP-005, BP-006, BP-010 |
| 23 | Administration events | MC-002 | ARCH-005 | DOMAIN-001 §15 | ES-001 | RA-006, RA-011 | BP-003, Organization Audit Service |
| 24 | Organization audit as authoritative record | MC-004 | ARCH-005 | DOMAIN-001 §16 | ES-004 | RA-011, RA-010 | BP-012 |
| 25 | Audit record immutability | MC-004 | ARCH-005 | DOMAIN-001 §17 | ES-004 | RA-011 | BP-012 |
| 26 | Tenant provisioning atomicity | MC-004 | ARCH-002 | DOMAIN-001 §16 | ES-001 | RA-009 | All downstream BPs |
| 27 | Tenant deprovisioning retention alignment | MC-004 | ARCH-004 | DOMAIN-001 §16, §17 | ES-003 | RA-009, RA-005 | All downstream BPs |
| 28 | Suspended organizations reject write operations | MC-002 | ARCH-002 | DOMAIN-001 §5 | ES-003 | RA-009 | All downstream BPs |
| 29 | Archived organizations become read-only | MC-002 | ARCH-002 | DOMAIN-001 §5 | ES-003 | RA-009 | All downstream BPs |
| 30 | AI context never crosses Organization boundaries | MC-004 | ARCH-002, ARCH-003 | DOMAIN-001 §13 | ES-005 | RA-009, RA-003 | BP-005, BP-006, BP-008 |
| 31 | Tenant Isolation Enforcement Library as shared primitive | MC-004 | ARCH-002 | DOMAIN-001 §13, §17 | ES-003, ES-004 | RA-009, RA-011 | All platform services |
| 32 | Organization Administrator authorization via BP-003 PDP | MC-004 | ARCH-005 | DOMAIN-002 | ES-004 | RA-011 | BP-003 |
| 33 | Cross-tenant operations restricted to platform-operator role | MC-004 | ARCH-002, ARCH-005 | DOMAIN-001 §12, §13 | ES-004 | RA-009, RA-011 | BP-012 |

---

# 27. Engineering Decisions Register

Every entry is defined using the 8-field canonical Engineering Decisions Register template established by BP-002.

## ED-001 Tenant Registry as authoritative identifier source

- **Decision:** The Tenant Registry Service is the sole authoritative source of Organization identifiers across the platform.
- **Status:** Accepted
- **Rationale:** DOMAIN-001 §17 mandates globally unique and immutable Organization identifiers; a single authoritative source is required to prevent identifier collisions.
- **Consequences:** Every service that consumes Organization identifiers shall resolve them through the Tenant Registry Service; no service may mint Organization identifiers independently.
- **Alternatives Considered:** Distributed identifier issuance was rejected because it does not satisfy immutability and uniqueness at platform scale.
- **Owning Reference Architecture:** RA-009
- **Owning Engineering Standard:** ES-003
- **Related Traceability Rows:** 1, 2

## ED-002 Organization identifier immutability

- **Decision:** Organization identifiers are immutable after Provisioning.
- **Status:** Accepted
- **Rationale:** DOMAIN-001 §17 declares Organization identifiers immutable to preserve downstream referential integrity across every business record and event.
- **Consequences:** Renaming or reassigning Organization identifiers requires deprovisioning and reprovisioning.
- **Alternatives Considered:** Reassignable identifiers were rejected because they would invalidate downstream references and audit history.
- **Owning Reference Architecture:** RA-009
- **Owning Engineering Standard:** ES-003
- **Related Traceability Rows:** 2

## ED-003 Tenant isolation as a shared library

- **Decision:** Tenant isolation is enforced through a shared Tenant Isolation Enforcement Library rather than reimplemented in each service.
- **Status:** Accepted
- **Rationale:** A single shared library ensures uniform enforcement, uniform violation detection, and consistent audit events.
- **Consequences:** Every service in the platform shall consume the library at every data access path.
- **Alternatives Considered:** Per-service tenant enforcement was rejected because it drifts over time and hides violations.
- **Owning Reference Architecture:** RA-009, RA-011
- **Owning Engineering Standard:** ES-003, ES-004
- **Related Traceability Rows:** 11, 12, 13, 14, 15, 31

## ED-004 Entitlement Service as runtime resolver

- **Decision:** Entitlement decisions are resolved at runtime by the Entitlement Service against precomputed Subscription plan mappings.
- **Status:** Accepted
- **Rationale:** Downstream Build Packs require low-latency entitlement lookups; centralized resolution prevents each Build Pack from independently interpreting Subscription plans.
- **Consequences:** Every downstream Build Pack shall consume the Entitlement Query API; entitlement policy changes propagate through Subscription and Entitlement events.
- **Alternatives Considered:** Distributing entitlement logic to each Build Pack was rejected because it fragments plan interpretation.
- **Owning Reference Architecture:** RA-009
- **Owning Engineering Standard:** ES-003, ES-004
- **Related Traceability Rows:** 6, 21

## ED-005 Entitlement Cache with event-driven invalidation

- **Decision:** Entitlement decisions are cached in an in-memory Entitlement Cache and invalidated by Subscription and Entitlement events.
- **Status:** Accepted
- **Rationale:** Runtime entitlement lookups occur on every downstream API path; caching reduces load on the Subscription DB. Event-driven invalidation preserves correctness on plan changes.
- **Consequences:** Consumers may observe short-lived stale entitlement decisions bounded by cache TTL and event delivery latency; both are Implementation Defined During Engineering.
- **Alternatives Considered:** Non-cached resolution was rejected on performance grounds; time-based-only cache invalidation was rejected because it does not react to Subscription plan changes.
- **Owning Reference Architecture:** RA-009, RA-005
- **Owning Engineering Standard:** ES-003
- **Related Traceability Rows:** 6, 20, 21

## ED-006 Tenant provisioning orchestration

- **Decision:** Tenant provisioning is coordinated by a dedicated Tenant Provisioning Orchestrator that ensures atomicity across Registry, Directory, Subscription, Entitlement, Configuration, Administration, and Storage Allocation.
- **Status:** Accepted
- **Rationale:** Partial provisioning would leave the platform in an inconsistent tenant state; atomic orchestration prevents this.
- **Consequences:** Every service that participates in tenant provisioning shall expose idempotent operations; failed provisioning shall trigger compensating deprovisioning.
- **Alternatives Considered:** Ad hoc provisioning workflows were rejected because they do not guarantee atomicity or compensating actions.
- **Owning Reference Architecture:** RA-009, RA-001
- **Owning Engineering Standard:** ES-001
- **Related Traceability Rows:** 26

## ED-007 Tenant deprovisioning retention alignment

- **Decision:** Tenant deprovisioning is coordinated by a dedicated Tenant Deprovisioning Orchestrator aligned to the configured retention policy defined in ARCH-004 and DOMAIN-001 §16.
- **Status:** Accepted
- **Rationale:** Deprovisioning must respect retention periods, audit preservation, and downstream Build Pack tenant-scoped stores.
- **Consequences:** Every downstream Build Pack shall register its tenant-scoped stores with the deprovisioning contract; deprovisioning shall not proceed without confirmation from every registered store.
- **Alternatives Considered:** Immediate hard-delete was rejected because it violates retention and compliance requirements.
- **Owning Reference Architecture:** RA-009, RA-005
- **Owning Engineering Standard:** ES-003
- **Related Traceability Rows:** 27

## ED-008 Outbox-backed Organization Event Emission

- **Decision:** Organization events are emitted through the outbox pattern established in BP-002 to ensure exactly-once relative to the source of truth.
- **Status:** Accepted
- **Rationale:** Consumers require reliable delivery of Organization lifecycle events; the outbox pattern ensures event durability aligned to source-of-truth state transitions.
- **Consequences:** Every service that publishes Organization events shall write to its outbox as part of the same transaction as its state change; the Organization Event Emitter drains the outbox to the Event Bus.
- **Alternatives Considered:** Direct event publication was rejected because it does not guarantee durability relative to the source of truth.
- **Owning Reference Architecture:** RA-006
- **Owning Engineering Standard:** ES-001
- **Related Traceability Rows:** 18, 19, 20, 21, 22, 23

## ED-009 Organization Audit immutability

- **Decision:** Organization audit records are immutable and stored in an append-only store.
- **Status:** Accepted
- **Rationale:** DOMAIN-001 §17 declares audit records non-deletable outside approved retention procedures; append-only storage enforces this at the data layer.
- **Consequences:** Audit records cannot be updated in place; corrections are captured as new audit records referencing the original.
- **Alternatives Considered:** Mutable audit records were rejected because they undermine compliance and non-repudiation.
- **Owning Reference Architecture:** RA-011
- **Owning Engineering Standard:** ES-004
- **Related Traceability Rows:** 24, 25

## ED-010 Organization administration authorized via BP-003 PDP

- **Decision:** Organization administrative operations are authorized through the BP-003 Authorization PDP rather than a BP-004-local authorization mechanism.
- **Status:** Accepted
- **Rationale:** Consolidating authorization in BP-003 preserves a single source of truth for policy decisions and avoids duplicate policy engines.
- **Consequences:** BP-004 depends on BP-003 Authorization PDP being operational; administrative authorization policies are recorded in BP-003 policy stores.
- **Alternatives Considered:** A dedicated BP-004 authorization mechanism was rejected because it would fragment policy governance.
- **Owning Reference Architecture:** RA-011
- **Owning Engineering Standard:** ES-004
- **Related Traceability Rows:** 9, 10, 32

## ED-011 Cross-tenant operations restricted to platform-operator role

- **Decision:** Cross-tenant operations are restricted to a distinct platform-operator role and recorded in a dedicated platform-operator audit surface.
- **Status:** Accepted
- **Rationale:** Tenant isolation is a foundational invariant; cross-tenant operations must be explicitly authorized and auditable.
- **Consequences:** The platform-operator role is defined separately from Organization Administrator; cross-tenant operations produce distinct audit records.
- **Alternatives Considered:** Extending Organization Administrator to cross-tenant scope was rejected because it violates the tenant isolation boundary.
- **Owning Reference Architecture:** RA-009, RA-011
- **Owning Engineering Standard:** ES-004
- **Related Traceability Rows:** 15, 33

## ED-012 Suspended organizations reject write operations at enforcement layer

- **Decision:** Suspended organizations reject write operations at the Tenant Isolation Enforcement Library layer.
- **Status:** Accepted
- **Rationale:** DOMAIN-001 §5 mandates that Suspended organizations lose operational access; enforcing this at the shared library layer applies the rule uniformly across every service.
- **Consequences:** Every service that performs writes shall consult tenant status before writing; the enforcement library provides a shared status check.
- **Alternatives Considered:** Per-service suspension checks were rejected because they drift and produce inconsistent behavior across the platform.
- **Owning Reference Architecture:** RA-009
- **Owning Engineering Standard:** ES-003
- **Related Traceability Rows:** 28

## ED-013 Archived organizations become read-only at enforcement layer

- **Decision:** Archived organizations become read-only at the Tenant Isolation Enforcement Library layer.
- **Status:** Accepted
- **Rationale:** DOMAIN-001 §5 mandates that Archived organizations be read-only; enforcing this at the shared library layer applies the rule uniformly across every service.
- **Consequences:** Every service shall consult tenant status before writing; archived state produces predictable read-only behavior downstream.
- **Alternatives Considered:** Per-service archival checks were rejected on drift grounds.
- **Owning Reference Architecture:** RA-009
- **Owning Engineering Standard:** ES-003
- **Related Traceability Rows:** 29

## ED-014 AI context never crosses Organization boundaries

- **Decision:** AI context, embeddings, retrieval results, and prompt inputs shall never cross Organization boundaries.
- **Status:** Accepted
- **Rationale:** DOMAIN-001 §13 declares that AI context shall never cross Organization boundaries; this invariant is foundational to multi-tenant AI trust.
- **Consequences:** BP-005 AI Platform and BP-006 Knowledge Platform shall scope every AI context to the acting Organization identifier; BP-004 exposes the Organization identifier through Entitlement and Configuration surfaces to enforce this.
- **Alternatives Considered:** Cross-tenant AI context sharing was rejected because it violates DOMAIN-001 and undermines tenant trust.
- **Owning Reference Architecture:** RA-009, RA-003
- **Owning Engineering Standard:** ES-005
- **Related Traceability Rows:** 30

---

# 28. Cross References

- MC-000 Repository Index
- MC-002 Product Foundation
- MC-004 Core Principles & Governance
- ARCH-001 System Architecture
- ARCH-002 Multi-Tenant Architecture
- ARCH-004 Data Architecture
- ARCH-005 Security Architecture
- DOMAIN-001 Organization Domain
- ES-001 Engineering Standards
- ES-003 Database Standards
- ES-004 Security Standards
- ES-005 AI Engineering Standards
- RA-001 Backend Reference Architecture
- RA-005 Data Platform Reference Architecture
- RA-006 Event-Driven Reference Architecture
- RA-009 Multi-Tenant Reference Architecture
- RA-010 Observability & Operations Reference Architecture
- RA-011 Security Reference Architecture
- BP-000 Engineering Foundation
- BP-001 Product Foundation
- BP-002 Platform Foundation
- BP-003 Identity & Access Platform
- BP-ROADMAP Official Build Pack Roadmap

---

# 29. Version History

**Version 1.0.0 — 2026-07-08**

Initial Tenant & Organization Platform Build Pack.

- Established Build Pack Objectives aligned to DOMAIN-001 and RA-009
- Established Tenant Isolation Boundary (Registry, Data, Event, Configuration, Administration)
- Established Organization Lifecycle mapping (Provisioning through Deletion)
- Established 13 platform services in the Service Inventory
- Established 6 databases in Required Databases
- Established 8 event categories in Required Events
- Established 13 capabilities in the Implementation Readiness Matrix
- Established 33-row Traceability Matrix
- Established 14 Engineering Decisions (ED-001 through ED-014)
- Aligned with BP-ROADMAP.md v1.0.0 sequencing
- Consumes BP-002 Platform Foundation and BP-003 Identity & Access Platform

---

# 30. Build Pack Freeze Declaration

Upon Engineering Review approval, BP-004 becomes the authoritative Tenant & Organization Platform Build Pack for Project ATLAS.

Every downstream Build Pack (BP-005 through BP-012) shall respect the tenant isolation boundary, entitlement resolution surface, Organization event contracts, and Organization audit contract established by BP-004.

Retired placeholder titles for BP-004 from prior repository versions are superseded and shall not be used.

BP-004 shall remain stable unless amended through formal repository governance and an approved Architecture Decision Record.

---
