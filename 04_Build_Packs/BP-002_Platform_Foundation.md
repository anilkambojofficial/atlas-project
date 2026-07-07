# Project ATLAS

# Build Pack

## BP-002 — Platform Foundation

---

# Document Information

| Field | Value |
|--------|--------|
| Document ID | BP-002 |
| Title | Platform Foundation |
| Version | 1.0.0 |
| Status | Draft (Engineering Review) |
| Repository | Project ATLAS |
| Owner | Anil Kumar |
| Classification | Implementation Specification |
| Depends On | BP-000, BP-001 |
| Next | BP-003 |
| Last Updated | 2026-07-08 |

---

# 1. Purpose

This Build Pack defines the implementation baseline for the Project ATLAS Platform Foundation.

It specifies the shared technical foundation on which every backend service, AI service, frontend workspace, integration, and workflow shall be built.

BP-002 is not architecture. It is an implementation contract derived from the approved architecture and reference architecture layers.

Every subsequent Build Pack, Implementation Pack, and production service shall conform to the standards defined in this document.

This Build Pack establishes:

- The canonical Platform Foundation
- Cross-cutting platform capabilities every service inherits
- Baseline services required before any domain module is implemented
- The bridge between the approved architecture layer and future domain Build Packs

---

# 2. Scope

BP-002 defines the implementation baseline for:

- Shared Platform Services
- Shared Platform Libraries
- Baseline Runtime
- Tenant-Aware Foundation
- Security Foundation
- Observability Foundation
- Event Foundation
- Configuration Foundation
- API Foundation
- Data Access Foundation
- AI Integration Foundation
- Deployment Foundation

BP-002 does not define:

- Domain-specific services (delivered by future domain Build Packs)
- Specific AI agents (delivered by AI Build Packs)
- Specific integrations (delivered by Integration Build Packs)
- User interface features (delivered by Frontend Build Packs)
- Business workflows (delivered by Workflow Build Packs)

Scope boundaries follow the layering rules in RA-001, RA-003, RA-005, RA-006, RA-009, RA-010, RA-011, and RA-012.

---

# 3. Dependencies

This Build Pack depends on the following approved repository documents.

**Master Context**

- MC-000 Repository Index
- MC-001 through MC-005

**Architecture**

- ARCH-001 through ARCH-008

**Domain Model**

- DOMAIN-001 through DOMAIN-010

**Engineering Standards**

- ES-001 through ES-007

**Reference Architecture**

- RA-001 Backend Reference Architecture
- RA-002 Frontend Reference Architecture
- RA-003 AI Platform Reference Architecture
- RA-004 Infrastructure Reference Architecture
- RA-005 Data Platform Reference Architecture
- RA-006 Event-Driven Reference Architecture
- RA-007 AI Agent Runtime Reference Architecture
- RA-008 RAG Platform Reference Architecture
- RA-009 Multi-Tenant Reference Architecture
- RA-010 Observability & Operations Reference Architecture
- RA-011 Security Reference Architecture
- RA-012 Integration Reference Architecture

**Preceding Build Packs**

- BP-000 Engineering Foundation
- BP-001 Product Foundation

No other repository documents are consumed by this Build Pack. The approved Project ATLAS repository is the sole authoritative source for this Build Pack.

---

# 4. Build Pack Objectives

BP-002 exists to translate the approved architecture and reference architecture into an implementation-ready platform foundation.

The objectives of this Build Pack are:

- Establish the canonical Platform Foundation before any domain Build Pack begins
- Define the shared runtime every backend, frontend, AI, integration, and workflow service consumes
- Define the shared libraries every service reuses without re-implementation
- Enforce architectural conformance across every service delivered downstream
- Provide a baseline that satisfies MC-000 governance, engineering standards, and reference architecture obligations
- Provide a stable contract between the architecture layer and the implementation layer
- Provide a foundation that is tenant-aware, secure by default, observable by default, event-aware by default, and AI-aware by default from the first commit
- Serve as the mandatory precursor for every subsequent Build Pack and every Implementation Pack

Objectives outside BP-002:

- Domain modelling (owned by DOMAIN-001 through DOMAIN-010)
- Reference architecture definition (owned by RA-001 through RA-012)
- Engineering standards definition (owned by ES-001 through ES-007)
- Product identity (owned by BP-001)
- Engineering rules (owned by BP-000)

---

## 4.1 Platform Capability Map

The Platform Foundation groups its cross-cutting capabilities into ten mandatory categories. Every downstream service inherits every category.

| Capability | Authoritative Source | Purpose |
|-----------|----------------------|---------|
| Backend Runtime | RA-001 | Canonical service scaffolding, lifecycle, and layering |
| Frontend Runtime | RA-002 | Canonical workspace, module federation, and rendering baseline |
| Data Foundation | RA-005 | Polyglot persistence, data access, data governance |
| Event Foundation | RA-006 | Event Bus, Outbox, Inbox, idempotency, replay |
| AI Foundation | RA-003, RA-007, RA-008 | AI Orchestrator, Agent Runtime, RAG access |
| Multi-Tenant Foundation | RA-009 | Tenant Registry, isolation, provisioning |
| Observability Foundation | RA-010 | Metrics, logging, tracing, incident lifecycle |
| Security Foundation | RA-011 | Identity, AuthN, AuthZ, Zero Trust, secrets |
| Integration Foundation | RA-012 | API Gateway, webhooks, connectors, AI providers |
| Infrastructure Foundation | RA-004 | Environments, compute, network, DR |

No downstream Build Pack shall re-declare a capability. Every capability shall be consumed from the Platform Foundation.

---

## 4.2 Platform Context

BP-002 sits inside the Project ATLAS repository governance chain.

The context flow is:

MC (Master Context)

↓

ARCH (Architecture)

↓

DOMAIN (Domain Model)

↓

ES (Engineering Standards)

↓

RA (Reference Architecture)

↓

BP (Build Pack)  ◀── BP-002 operates at this layer

↓

IP (Implementation Pack)

↓

Production

BP-002 is the first Build Pack that turns the frozen architecture and reference architecture layers into an executable platform contract. It does not modify any upstream layer. It does not skip downstream to Implementation Packs. It sits between them and enforces conformance in both directions.

---

# 5. Platform Responsibilities

The Platform Foundation is responsible for delivering the cross-cutting capabilities every Project ATLAS service inherits.

**Foundational Responsibilities**

- Provide the canonical backend runtime as defined in RA-001
- Provide the canonical frontend runtime as defined in RA-002
- Provide the tenant-aware execution context defined in RA-009
- Provide the security execution context defined in RA-011
- Provide the observability execution context defined in RA-010
- Provide the event execution context defined in RA-006
- Provide the API execution context defined in RA-012
- Provide the data access execution context defined in RA-005
- Provide the AI execution context defined in RA-003 and RA-007
- Provide the deployment execution context defined in RA-004

**Governance Responsibilities**

- Enforce engineering principles defined in BP-000
- Enforce product identity defined in BP-001
- Enforce Reference Architecture standards without deviation
- Enforce Definition of Done gates for every downstream service

**Delivery Responsibilities**

- Deliver a working baseline runtime that domain Build Packs consume
- Deliver reusable libraries so domain services do not re-implement cross-cutting concerns
- Deliver canonical repository skeletons per RA-001 and RA-002
- Deliver operational readiness aligned with RA-010

The Platform Foundation shall never contain domain business logic. Domain logic belongs to the domain Build Packs downstream of BP-002.

---

# 6. Platform Components

The Platform Foundation shall be delivered as the following components. Each component is bounded by an approved Reference Architecture. No component invents scope beyond its RA.

**Backend Platform Component**

- Source: RA-001
- Delivers: canonical service scaffolding, layered architecture, service lifecycle, standard health endpoints, dependency injection baseline, error contract, request context propagation

**Frontend Platform Component**

- Source: RA-002
- Delivers: canonical workspace scaffolding, shell application, module federation, design system integration point, tenant-aware routing

**Infrastructure Platform Component**

- Source: RA-004
- Delivers: environment topology, compute baseline, network baseline, secrets integration point, disaster recovery scaffolding

**Data Platform Component**

- Source: RA-005
- Delivers: polyglot persistence adapters, data access layer, migration baseline, data governance hooks

**Event Platform Component**

- Source: RA-006
- Delivers: Event Bus client, Outbox implementation, Inbox implementation, idempotency helpers, retry and DLQ scaffolding, Event Catalog binding

**AI Platform Component**

- Source: RA-003
- Delivers: AI Orchestrator client, Registry client, Model Router client, Context Engine client, Guardrails hook, FinOps hook

**AI Agent Runtime Component**

- Source: RA-007
- Delivers: Agent Runtime client, Agent lifecycle hooks, multi-agent collaboration bindings, human oversight hooks

**RAG Platform Component**

- Source: RA-008
- Delivers: ingestion client, retrieval client, reranking client, citation binding, trust score binding

**Multi-Tenant Component**

- Source: RA-009
- Delivers: Tenant Registry client, tenant context propagation, isolation enforcement, subscription and feature-flag binding

**Observability Component**

- Source: RA-010
- Delivers: metrics emitter, structured logger, distributed tracing baseline, dashboard binding, alert binding, incident hooks

**Security Component**

- Source: RA-011
- Delivers: identity client, authentication middleware, authorization middleware, secrets client, encryption client, session manager, audit logger

**Integration Component**

- Source: RA-012
- Delivers: API Gateway binding, webhook framework, connector registration, AI provider registration, integration observability hooks

Every downstream service shall consume every component listed above. Selective consumption is not permitted.

---

# 7. Repository Mapping

The Platform Foundation is expressed in the Project ATLAS repository as follows. Locations follow MC-000 and the canonical platform structures defined in the RA layer.

**Documentation Anchors**

| Repository Path | Owner | Source |
|------------------|-------|--------|
| `00_Master_Context/` | Governance | MC-000 through MC-005 |
| `01_Architecture/` | Architecture Office | ARCH-001 through ARCH-008 |
| `02_Domain_Model/` | Domain Office | DOMAIN-001 through DOMAIN-010 |
| `03_Engineering_Standards/` | Engineering Office | ES-001 through ES-007 |
| `04_Build_Packs/` | Build Pack Office | BP-000, BP-001, BP-002 (this document) |
| `05_Reference_Architecture/` | Reference Architecture Office | RA-001 through RA-012 |

**Implementation Anchors**

The Platform Foundation implementation shall follow the canonical structures declared in the Reference Architecture layer:

| Canonical Structure | Defined In | Section |
|---------------------|-----------|---------|
| Canonical Backend Structure | RA-001 | §22 |
| Canonical Frontend Structure | RA-002 | §22 |
| Canonical AI Platform Structure | RA-003 | §22 |
| Canonical Infrastructure Structure | RA-004 | §22 |
| Canonical Data Platform Structure | RA-005 | §22 |
| Canonical Event Platform Structure | RA-006 | §22 |
| Canonical Agent Runtime Structure | RA-007 | §22 |
| Canonical RAG Platform Structure | RA-008 | §22 |
| Canonical Multi-Tenant Structure | RA-009 | §22 |
| Canonical Observability Structure | RA-010 | §22 |
| Canonical Security Structure | RA-011 | §22 |
| Canonical Integration Structure | RA-012 | §22 |

BP-002 does not redefine these structures. It binds them into a single Platform Foundation contract.

---

# 8. Service Inventory

The Platform Foundation shall provide the following baseline services. Every service is described using the mandatory eleven-field Service Inventory template. Fields not explicitly declared by the approved repository are recorded as "Implementation Defined During Engineering".

---

## 8.1 Identity Service

- **Service Name:** Identity Service
- **Source Documents:** RA-011 §5 (Identity Platform), §6 (Authentication), §12 (Session Management)
- **Responsibilities:** identity issuance for humans, service accounts, AI agents, applications, external partners, and system processes (§5); authentication via SSO, MFA, passwordless, service authentication, API authentication, and federated identity (§6); session lifecycle (§12)
- **Inputs:** authentication credentials, federated identity assertions (§6); Implementation Defined During Engineering
- **Outputs:** authenticated sessions (§12), identity assertions, audit records (§20)
- **Dependencies:** Enterprise Identity Providers (RA-011 §24), Secrets Service (RA-011 §10), audit subsystem (RA-011 §20)
- **Consumers:** all Platform Services (RA-011 Referenced By), Authorization Service, API Gateway (RA-012 §5)
- **Failure Modes:** Implementation Defined During Engineering
- **Observability Requirements:** Authentication Events (RA-011 §14); further telemetry Implementation Defined During Engineering
- **Security Requirements:** identity verification, session protection, risk-based and continuous authentication (RA-011 §6); compliance with enterprise security policies (RA-011 §6)
- **Implementation Status:** Implementation Defined During Engineering.

---

## 8.2 Tenant Registry Service

- **Service Name:** Tenant Registry Service
- **Source Documents:** RA-009 (Tenant Registry, Provisioning, Isolation, Feature Management, Subscription Management)
- **Responsibilities:** tenant lifecycle, provisioning, isolation policy resolution, feature enablement, subscription resolution (RA-009)
- **Inputs:** tenant provisioning requests, feature and subscription configurations; Implementation Defined During Engineering
- **Outputs:** tenant context, isolation policies, feature entitlements
- **Dependencies:** Identity Service (RA-011), Configuration Service, Event Bus (RA-006 for tenant lifecycle events)
- **Consumers:** all Platform Services, API Gateway (RA-012 §5)
- **Failure Modes:** Implementation Defined During Engineering
- **Observability Requirements:** Implementation Defined During Engineering (must integrate with RA-010)
- **Security Requirements:** tenant isolation enforcement (RA-009), tenant-scoped audit logging (RA-011 §20)
- **Implementation Status:** Implementation Defined During Engineering.

---

## 8.3 Authorization Service

- **Service Name:** Authorization Service
- **Source Documents:** RA-011 §7 (Authorization)
- **Responsibilities:** policy evaluation for RBAC, ABAC, and policy-based access control (§7); centralized and auditable authorization decisions (§7)
- **Inputs:** identity context, resource references, requested actions; Implementation Defined During Engineering
- **Outputs:** authorization decisions, audit records (RA-011 §20)
- **Dependencies:** Identity Service, Tenant Registry Service, policy repository (Implementation Defined During Engineering)
- **Consumers:** all Platform Services, API Gateway (RA-012 §5)
- **Failure Modes:** Implementation Defined During Engineering
- **Observability Requirements:** Authorization Failures (RA-011 §14); Policy Violations (RA-011 §14)
- **Security Requirements:** least privilege, organization isolation, resource ownership, policy evaluation (RA-011 §7)
- **Implementation Status:** Implementation Defined During Engineering.

---

## 8.4 Secrets Service

- **Service Name:** Secrets Service
- **Source Documents:** RA-011 §10 (Secrets Management), §11 (Key Management)
- **Responsibilities:** central secret storage, rotation, audited retrieval (§10, §11)
- **Inputs:** secret storage requests, secret retrieval requests, rotation triggers
- **Outputs:** secret values (audited), key lifecycle events
- **Dependencies:** Key Management System (RA-011 §24)
- **Consumers:** all Platform Services (RA-011 Referenced By)
- **Failure Modes:** Implementation Defined During Engineering
- **Observability Requirements:** Secret Access events (RA-011 §14)
- **Security Requirements:** no secrets in source code or application configuration (§10); auditable key lifecycle (§11); encryption at rest and in transit (RA-011 §9)
- **Implementation Status:** Implementation Defined During Engineering.

---

## 8.5 Configuration Service

- **Service Name:** Configuration Service
- **Source Documents:** RA-001 (Backend Reference Architecture), RA-004 (Infrastructure Reference Architecture), RA-009 (tenant-scoped configuration)
- **Responsibilities:** environment-scoped configuration resolution, tenant-scoped configuration resolution
- **Inputs:** configuration lookup requests scoped by environment and tenant
- **Outputs:** configuration values
- **Dependencies:** Tenant Registry Service, Secrets Service (for secret-typed configuration)
- **Consumers:** all Platform Services
- **Failure Modes:** Implementation Defined During Engineering
- **Observability Requirements:** Implementation Defined During Engineering (must integrate with RA-010)
- **Security Requirements:** encryption of sensitive configuration (RA-011 §9); audit logging (RA-011 §20)
- **Implementation Status:** Implementation Defined During Engineering.

---

## 8.6 Event Bus Service

- **Service Name:** Event Bus Service
- **Source Documents:** RA-006 §5 (Event Bus), §10 (Outbox), §11 (Inbox), §14 (Retry Strategy), §15 (DLQ), §16 (Event Replay), §17 (Event Observability), §18 (Event Security)
- **Responsibilities:** publication, subscription, routing, retry, ordering, delivery tracking, dead letter queue (§5)
- **Inputs:** events from producers via Outbox (§10)
- **Outputs:** events delivered to consumers, DLQ entries (§15), replay streams (§16)
- **Dependencies:** Outbox implementations (§10), Inbox implementations (§11), Enterprise Event Catalog (§21), Schema Registry (§22)
- **Consumers:** all Platform Services, AI Platform, Workflow Engine, Notification Platform, Analytics Platform (RA-006 Referenced By)
- **Failure Modes:** transient failures handled via retry (§14); permanent failures routed to DLQ (§15); events shall never be silently discarded (§15)
- **Observability Requirements:** Published Events, Consumed Events, Failed Events, Retry Count, Processing Latency, Queue Depth, Consumer Lag (§17)
- **Security Requirements:** Authentication, Authorization, Encryption, Tenant Isolation, Payload Validation, Audit Logging (§18)
- **Implementation Status:** Implementation Defined During Engineering.

---

## 8.7 Observability Collector Service

- **Service Name:** Observability Collector Service
- **Source Documents:** RA-010 (Observability & Operations Reference Architecture)
- **Responsibilities:** ingestion of metrics, logs, and distributed traces; correlation across services
- **Inputs:** metric, log, and trace payloads from all Platform Services
- **Outputs:** aggregated telemetry, correlated traces, dashboard and alerting feeds
- **Dependencies:** metrics store, log store, trace store — Implementation Defined During Engineering
- **Consumers:** dashboards, alerting, SRE, incident management (RA-010)
- **Failure Modes:** Implementation Defined During Engineering
- **Observability Requirements:** self-observability — Implementation Defined During Engineering
- **Security Requirements:** tenant isolation, encryption in transit, audit logging (RA-011)
- **Implementation Status:** Implementation Defined During Engineering.

---

## 8.8 API Gateway Service

- **Service Name:** API Gateway Service
- **Source Documents:** RA-012 §5 (API Gateway), §6 (API Standards), §14 (Integration Observability), §15 (Integration Security)
- **Responsibilities:** Authentication, Authorization, Routing, Rate Limiting, API Versioning, Request Validation, Observability (§5); enforcement of enterprise integration policies (§5)
- **Inputs:** external and internal API requests
- **Outputs:** routed requests, rate-limit responses, validation errors
- **Dependencies:** Identity Service, Authorization Service, downstream Platform Services
- **Consumers:** all clients, all downstream Platform Services (RA-012 Referenced By)
- **Failure Modes:** Implementation Defined During Engineering
- **Observability Requirements:** API Availability, API Latency (RA-012 §14)
- **Security Requirements:** Authentication, Authorization, Encryption, Rate Limiting, Input Validation, Output Validation, Secret Management, Audit Logging (RA-012 §15)
- **Implementation Status:** Implementation Defined During Engineering.

---

## 8.9 AI Orchestrator Service

- **Service Name:** AI Orchestrator Service
- **Source Documents:** RA-003 (AI Platform Reference Architecture)
- **Responsibilities:** routing AI workloads across models, guardrail enforcement, FinOps enforcement, context assembly, model routing (RA-003)
- **Inputs:** AI request submissions, model routing rules, tenant context; Implementation Defined During Engineering
- **Outputs:** AI responses, telemetry, FinOps cost records
- **Dependencies:** Model Router, Registry, Context Engine, Enterprise Memory, Guardrails, FinOps (all RA-003); AI Provider Integrations (RA-012 §10)
- **Consumers:** Agent Runtime Service, RAG Service, all AI-consuming services
- **Failure Modes:** Implementation Defined During Engineering
- **Observability Requirements:** Implementation Defined During Engineering (must integrate with RA-010)
- **Security Requirements:** AI Security Policies (RA-011 §13); AI misuse detection (RA-011 §15); Guardrails (RA-003)
- **Implementation Status:** Implementation Defined During Engineering.

---

## 8.10 Agent Runtime Service

- **Service Name:** Agent Runtime Service
- **Source Documents:** RA-007 (AI Agent Runtime Reference Architecture)
- **Responsibilities:** Runtime Controller, Agent Lifecycle, Multi-Agent Collaboration, Human Oversight, Agent Registry Integration (RA-007)
- **Inputs:** agent invocation requests, agent definitions, human oversight callbacks
- **Outputs:** agent execution results, lifecycle events, oversight notifications
- **Dependencies:** AI Orchestrator Service, Agent Registry (RA-003), Event Bus Service (RA-006), Identity Service and Authorization Service (RA-011)
- **Consumers:** AI Platform, Workflow Engine, downstream domain services
- **Failure Modes:** Implementation Defined During Engineering
- **Observability Requirements:** agent lifecycle telemetry — Implementation Defined During Engineering (must integrate with RA-010)
- **Security Requirements:** authorization for agent execution (RA-011 §7), audit logging (RA-011 §20), AI security policies (RA-011 §13)
- **Implementation Status:** Implementation Defined During Engineering.

---

## 8.11 RAG Service

- **Service Name:** RAG Service
- **Source Documents:** RA-008 (RAG Platform Reference Architecture)
- **Responsibilities:** Ingestion, Chunking, Embedding, Hybrid Retrieval, Reranking, Citation, Trust Scoring (RA-008)
- **Inputs:** documents to ingest, retrieval queries, reranking requests
- **Outputs:** chunked and embedded documents, retrieved passages with citations, trust scores
- **Dependencies:** Vector platform and Search platform (RA-005), Embedding provider (RA-012 §10), AI Orchestrator Service (RA-003)
- **Consumers:** AI Orchestrator Service, Agent Runtime Service, knowledge-consuming domain services
- **Failure Modes:** Implementation Defined During Engineering
- **Observability Requirements:** Implementation Defined During Engineering (must integrate with RA-010)
- **Security Requirements:** tenant isolation, encryption, audit logging (RA-011)
- **Implementation Status:** Implementation Defined During Engineering.

---

## 8.12 Notification Dispatch Service

- **Service Name:** Notification Dispatch Service
- **Source Documents:** RA-006 (Notification Events category, §4), RA-012 §4 (Integration Types), RA-012 §7 (Webhooks)
- **Responsibilities:** dispatch of platform notifications through governed channels
- **Inputs:** notification events from Event Bus; Implementation Defined During Engineering for delivery preferences
- **Outputs:** dispatched notifications via governed channels; delivery telemetry
- **Dependencies:** Event Bus Service (RA-006), API Gateway Service (RA-012), Tenant Registry Service (RA-009)
- **Consumers:** end users, integration partners
- **Failure Modes:** transient webhook failures handled via retry, permanent failures routed to DLQ (RA-012 §7)
- **Observability Requirements:** Webhook Delivery, Event Delivery (RA-012 §14)
- **Security Requirements:** webhook signature verification (RA-012 §7); audit logging (RA-011 §20)
- **Implementation Status:** Implementation Defined During Engineering.

---

No downstream Build Pack shall implement an alternative to any service listed above. Extensions are governed under the extension points declared by the corresponding Reference Architecture.

---

# 9. Required APIs

The Platform Foundation shall expose the following baseline APIs. Every API shall be governed by RA-012 (API Gateway, API standards, API versioning) and secured under RA-011.

**Platform Health APIs**

- Liveness endpoint per service
- Readiness endpoint per service
- Startup endpoint per service
- Source: RA-001, RA-010

**Identity APIs**

- Authentication
- Token issuance and validation
- Session lifecycle
- Source: RA-011

**Tenant APIs**

- Tenant resolution
- Tenant context propagation
- Feature and subscription resolution
- Source: RA-009

**Authorization APIs**

- Policy evaluation
- Authorization decision retrieval
- Source: RA-011

**Configuration APIs**

- Environment-scoped configuration retrieval
- Tenant-scoped configuration retrieval
- Source: RA-001, RA-004

**Event APIs**

- Event publication
- Event subscription management
- Event replay control
- Source: RA-006

**Observability APIs**

- Metric submission
- Log submission
- Trace submission
- Source: RA-010

**AI Orchestration APIs**

- AI request submission
- Model routing status
- Guardrail evaluation
- Source: RA-003

**Agent Runtime APIs**

- Agent invocation
- Agent lifecycle control
- Human oversight callbacks
- Source: RA-007

**RAG APIs**

- Ingestion submission
- Retrieval query
- Reranking control
- Source: RA-008

**Integration APIs**

- Webhook registration
- Connector registration
- Partner registration
- Source: RA-012

All APIs shall follow the API Standards declared in RA-012 §6, be versioned per RA-012 §18, and expose observability per RA-010.

---

# 10. Required Databases

The Platform Foundation shall provide baseline data-storage capabilities under RA-005 (Data Platform). Every database is described using the mandatory eleven-field Required Databases template. Fields not explicitly declared by the approved repository are recorded as "Implementation Defined During Engineering".

---

## 10.1 Relational Store

- **Database Name:** Relational Store
- **Source Documents:** RA-005 (Polyglot Persistence — Relational platform)
- **Purpose:** transactional data, domain aggregates, workflow state
- **Ownership:** Implementation Defined During Engineering
- **Data Classification:** Implementation Defined During Engineering (RA-005 mandates data governance; specific classifications are downstream)
- **Tenant Isolation:** required per RA-009
- **Backup Responsibility:** Implementation Defined During Engineering (RA-004 mandates disaster recovery; per-store ownership assigned during engineering)
- **Retention Policy:** Implementation Defined During Engineering (RA-011 §16 mandates retention policies; specifics defined downstream)
- **Encryption Requirements:** at rest and in transit per RA-011 §9
- **Consumers:** all domain services, workflow engine; Implementation Defined During Engineering for specifics
- **Implementation Status:** Implementation Defined During Engineering.

---

## 10.2 Vector Store

- **Database Name:** Vector Store
- **Source Documents:** RA-005 (Polyglot Persistence — Vector platform), RA-008 (RAG Platform)
- **Purpose:** embedding storage, semantic retrieval
- **Ownership:** Implementation Defined During Engineering
- **Data Classification:** Implementation Defined During Engineering
- **Tenant Isolation:** required per RA-009
- **Backup Responsibility:** Implementation Defined During Engineering
- **Retention Policy:** Implementation Defined During Engineering
- **Encryption Requirements:** at rest and in transit per RA-011 §9
- **Consumers:** RAG Service (RA-008), AI Orchestrator Service (RA-003)
- **Implementation Status:** Implementation Defined During Engineering.

---

## 10.3 Search Store

- **Database Name:** Search Store
- **Source Documents:** RA-005 (Polyglot Persistence — Search platform), RA-008 (Hybrid Retrieval)
- **Purpose:** keyword and hybrid retrieval
- **Ownership:** Implementation Defined During Engineering
- **Data Classification:** Implementation Defined During Engineering
- **Tenant Isolation:** required per RA-009
- **Backup Responsibility:** Implementation Defined During Engineering
- **Retention Policy:** Implementation Defined During Engineering
- **Encryption Requirements:** at rest and in transit per RA-011 §9
- **Consumers:** RAG Service (RA-008), search-consuming domain services
- **Implementation Status:** Implementation Defined During Engineering.

---

## 10.4 Object / Document Store

- **Database Name:** Object / Document Store
- **Source Documents:** RA-005 (Polyglot Persistence), RA-008 (Ingestion)
- **Purpose:** raw source documents, ingestion artifacts, exports
- **Ownership:** Implementation Defined During Engineering
- **Data Classification:** Implementation Defined During Engineering
- **Tenant Isolation:** required per RA-009
- **Backup Responsibility:** Implementation Defined During Engineering
- **Retention Policy:** Implementation Defined During Engineering
- **Encryption Requirements:** at rest and in transit per RA-011 §9
- **Consumers:** RAG Service (RA-008), Integration Platform (RA-012), export consumers
- **Implementation Status:** Implementation Defined During Engineering.

---

## 10.5 Event Store / Log Store

- **Database Name:** Event Store / Log Store
- **Source Documents:** RA-005 (AI Data Pipeline), RA-006 §16 (Event Replay), RA-010 (Logging)
- **Purpose:** persistence of platform events for replay (RA-006 §16) and audit (RA-011 §20)
- **Ownership:** Implementation Defined During Engineering
- **Data Classification:** Implementation Defined During Engineering
- **Tenant Isolation:** required per RA-009
- **Backup Responsibility:** Implementation Defined During Engineering
- **Retention Policy:** Implementation Defined During Engineering (RA-011 §16 governs)
- **Encryption Requirements:** at rest and in transit per RA-011 §9; audit records protected against unauthorized modification (RA-011 §20)
- **Consumers:** Event Bus Service (RA-006), audit consumers, Observability Collector (RA-010)
- **Implementation Status:** Implementation Defined During Engineering.

---

## 10.6 Cache

- **Database Name:** Cache
- **Source Documents:** RA-005 (Polyglot Persistence)
- **Purpose:** performance acceleration for platform services
- **Ownership:** Implementation Defined During Engineering
- **Data Classification:** Implementation Defined During Engineering
- **Tenant Isolation:** required per RA-009
- **Backup Responsibility:** Implementation Defined During Engineering
- **Retention Policy:** Implementation Defined During Engineering
- **Encryption Requirements:** in transit per RA-011 §9; at rest Implementation Defined During Engineering
- **Consumers:** all Platform Services
- **Implementation Status:** Implementation Defined During Engineering.

---

Specific engines, vendors, storage tiers, and replication topologies are Implementation Defined During Engineering. All stores shall conform to RA-005 governance and RA-011 encryption mandates.

---

# 11. Required Events

The Platform Foundation shall support every event category declared in RA-006 §4. Every event category is described using the mandatory eleven-field Required Events template. Fields not explicitly declared by the approved repository are recorded as "Implementation Defined During Engineering". Every event shall follow the Event Contract in RA-006 §8 and be registered in the Enterprise Event Catalog (RA-006 §21).

---

## 11.1 Domain Events

- **Event Category:** Domain Events
- **Source Documents:** RA-006 §4, §6
- **Producer:** domain services, published only after successful business transactions (RA-006 §6)
- **Consumer:** subscribers to domain events including AI Platform, Workflow Engine, Notification Platform, Analytics Platform (RA-006 Referenced By)
- **Purpose:** represent completed business facts (RA-006 §6)
- **Delivery Guarantee:** reliable delivery via Outbox Pattern (RA-006 §10) with idempotent consumers (RA-006 §12)
- **Ordering Requirements:** aggregate, workflow, or partition ordering as required; global ordering shall not be assumed (RA-006 §13)
- **Retry Strategy:** immediate retry, exponential backoff, configurable retry limits, circuit breaker integration, retry audit logging (RA-006 §14)
- **Dead Letter Strategy:** failed events routed to Dead Letter Queue with failure classification, manual review, replay support, and root cause analysis (RA-006 §15)
- **Observability Requirements:** Published Events, Consumed Events, Failed Events, Retry Count, Processing Latency, Queue Depth, Consumer Lag (RA-006 §17)
- **Implementation Status:** Implementation Defined During Engineering.

---

## 11.2 Integration Events

- **Event Category:** Integration Events
- **Source Documents:** RA-006 §4, §7; RA-012 §8 (Event Integrations)
- **Producer:** platform services acting as integration producers (RA-006 §7)
- **Consumer:** external systems, other bounded contexts (RA-006 §7)
- **Purpose:** communicate across bounded contexts and external systems (RA-006 §7)
- **Delivery Guarantee:** reliable delivery via Outbox Pattern (RA-006 §10) with idempotent consumers (RA-006 §12)
- **Ordering Requirements:** aggregate, workflow, or partition ordering as required (RA-006 §13)
- **Retry Strategy:** RA-006 §14
- **Dead Letter Strategy:** RA-006 §15
- **Observability Requirements:** RA-006 §17
- **Implementation Status:** Implementation Defined During Engineering.

---

## 11.3 System Events

- **Event Category:** System Events
- **Source Documents:** RA-006 §4
- **Producer:** Platform Foundation components
- **Consumer:** Observability Collector Service (RA-010), platform operators
- **Purpose:** platform-level operational signals
- **Delivery Guarantee:** Outbox / Inbox reliability per RA-006 §10 §11 §12
- **Ordering Requirements:** RA-006 §13
- **Retry Strategy:** RA-006 §14
- **Dead Letter Strategy:** RA-006 §15
- **Observability Requirements:** RA-006 §17; RA-010
- **Implementation Status:** Implementation Defined During Engineering.

---

## 11.4 AI Events

- **Event Category:** AI Events
- **Source Documents:** RA-006 §4; RA-003, RA-007
- **Producer:** AI Orchestrator Service (RA-003), Agent Runtime Service (RA-007), RAG Service (RA-008)
- **Consumer:** audit consumers, observability, downstream domain services, FinOps consumers (RA-003)
- **Purpose:** AI operation lifecycle telemetry and coordination
- **Delivery Guarantee:** Outbox / Inbox reliability per RA-006 §10 §11 §12
- **Ordering Requirements:** RA-006 §13
- **Retry Strategy:** RA-006 §14
- **Dead Letter Strategy:** RA-006 §15
- **Observability Requirements:** RA-006 §17; RA-010
- **Implementation Status:** Implementation Defined During Engineering.

---

## 11.5 Security Events

- **Event Category:** Security Events
- **Source Documents:** RA-006 §4; RA-011 §14 (Security Monitoring), §15 (Threat Detection)
- **Producer:** Identity Service, Authorization Service, Secrets Service, Security Monitoring components (RA-011)
- **Consumer:** SIEM platforms (RA-011 §24), Security Incident Response (RA-011 §17), audit consumers
- **Purpose:** authentication, authorization, privileged operations, policy violations, secret access, threat indicators (RA-011 §14)
- **Delivery Guarantee:** Outbox / Inbox reliability per RA-006 §10 §11 §12
- **Ordering Requirements:** RA-006 §13
- **Retry Strategy:** RA-006 §14
- **Dead Letter Strategy:** RA-006 §15; security events shall never be silently discarded
- **Observability Requirements:** RA-006 §17; RA-011 §14
- **Implementation Status:** Implementation Defined During Engineering.

---

## 11.6 Audit Events

- **Event Category:** Audit Events
- **Source Documents:** RA-006 §4; RA-011 §20 (Security Auditing)
- **Producer:** all Platform Services emitting audit-relevant activity (RA-011 §20)
- **Consumer:** audit store, compliance systems (RA-011 §16), Governance Platforms (RA-011 §24)
- **Purpose:** authentication, authorization, configuration changes, secret access, administrative actions, AI operations, compliance activities (RA-011 §20)
- **Delivery Guarantee:** Outbox / Inbox reliability per RA-006 §10 §11 §12; audit records protected against unauthorized modification (RA-011 §20)
- **Ordering Requirements:** RA-006 §13
- **Retry Strategy:** RA-006 §14
- **Dead Letter Strategy:** RA-006 §15; audit events shall never be silently discarded
- **Observability Requirements:** RA-006 §17; RA-011 §20
- **Implementation Status:** Implementation Defined During Engineering.

---

## 11.7 Notification Events

- **Event Category:** Notification Events
- **Source Documents:** RA-006 §4; RA-012 §4 (Integration Types)
- **Producer:** notification-emitting domain services
- **Consumer:** Notification Dispatch Service (§8.12)
- **Purpose:** trigger governed notifications to users and systems
- **Delivery Guarantee:** Outbox / Inbox reliability per RA-006 §10 §11 §12
- **Ordering Requirements:** RA-006 §13
- **Retry Strategy:** RA-006 §14
- **Dead Letter Strategy:** RA-006 §15
- **Observability Requirements:** RA-006 §17; Webhook Delivery, Event Delivery (RA-012 §14)
- **Implementation Status:** Implementation Defined During Engineering.

---

**Baseline Domain Events referenced by the repository** (RA-006 §6): MeetingCreated, DecisionApproved, SOPPublished, ActionAssigned, KnowledgeGenerated.

**Baseline Integration Events referenced by the repository** (RA-006 §7): UserProvisioned, EmailDispatched, CRMUpdated, ERPOrderCreated, AnalyticsExportCompleted.

**Event Contract Fields (mandatory, RA-006 §8):** Event ID, Event Type, Event Version, Event Timestamp, Organization ID, Correlation ID, Producer, Payload Schema, Metadata.

Concrete event payload schemas beyond the Event Contract are Implementation Defined During Engineering and shall be authored during domain Build Packs.

---

# 12. Required Configuration

The Platform Foundation shall expose configuration under RA-001 and RA-004, resolved by the Configuration Service (§8.5).

**Configuration Scopes**

- Platform scope (RA-001, RA-004)
- Environment scope (RA-004 Environment Strategy)
- Tenant scope (RA-009)
- Service scope (per service consumer)

**Configuration Categories**

- Runtime configuration (RA-001)
- Infrastructure configuration (RA-004)
- Data platform configuration (RA-005)
- Event platform configuration (RA-006)
- AI platform configuration (RA-003, RA-007, RA-008)
- Multi-tenant configuration (RA-009)
- Observability configuration (RA-010)
- Security configuration (RA-011)
- Integration configuration (RA-012)

**Configuration Governance**

- All configuration shall be version-controlled
- Sensitive configuration shall be resolved through the Secrets Service (RA-011 §10)
- Configuration changes shall be audited (RA-011 §20)
- No secrets or credentials in source code or application configuration (RA-011 §10)

Specific configuration keys, defaults, and schemas are Implementation Defined During Engineering.

---

# 13. Security Requirements

The Platform Foundation shall comply with every mandate in RA-011.

**Foundational Controls**

- Zero Trust across every request (RA-011 §8)
- Least Privilege for every identity (RA-011 §2)
- Defense in Depth (RA-011 §2)
- Continuous Verification (RA-011 §2)
- Encryption Everywhere (RA-011 §2, §9)
- Identity First (RA-011 §2, §5)
- Security Automation (RA-011 §2)

**Mandatory Capabilities**

- Authentication with SSO, MFA, passwordless, service, API, federated (RA-011 §6)
- Authorization with RBAC, ABAC, policy-based (RA-011 §7)
- Encryption at rest and in transit (RA-011 §9)
- Centralized Secrets Management (RA-011 §10)
- Independent Key Management (RA-011 §11)
- Session Management (RA-011 §12)
- Central Security Policies (RA-011 §13)
- Security Monitoring (RA-011 §14)
- Threat Detection (RA-011 §15)
- Compliance evidence (RA-011 §16)
- Security Incident Response (RA-011 §17)
- Secure SDLC (RA-011 §18)
- Vulnerability Management (RA-011 §19)
- Security Auditing (RA-011 §20)
- Risk Management (RA-011 §21)

**Prohibited Practices (RA-011 §25)**

- Hard-coded credentials
- Shared administrator accounts
- Missing encryption
- Excessive privileges
- Disabled audit logging
- Direct database access without authorization
- Unmanaged secrets
- AI access without policy validation

Deviations require an approved Architecture Decision Record (RA-011 §25).

---

# 14. Multi-Tenant Requirements

The Platform Foundation shall comply with every mandate in RA-009.

**Foundational Capabilities**

- Tenant Registry as authoritative tenant record (RA-009)
- Tenant Provisioning
- Tenant Isolation across identity, data, events, storage, AI context, and observability
- Feature Management (feature flags scoped by tenant)
- Subscription Management
- Billing integration
- Compliance controls per tenant

**Mandatory Behaviors**

- Every request shall carry tenant context (RA-009, RA-011 §7)
- Every persistence operation shall be tenant-scoped (RA-005, RA-009)
- Every event shall carry Organization ID (RA-006 §8)
- Every log, metric, and trace shall carry tenant identifiers (RA-010)
- Every AI operation shall be tenant-scoped (RA-003, RA-007, RA-008)
- Every integration shall respect tenant policies (RA-012)

**Prohibited Practices**

- Cross-tenant data access without explicit governed authorization
- Tenant identifiers absent from persistence, events, telemetry, or AI context
- Shared secrets across tenants (RA-011 §10)

Tenant lifecycle events (creation, suspension, termination) shall be published through the Event Bus (RA-006) and consumed by all tenant-aware components.

---

# 15. AI Integration Requirements

The Platform Foundation shall comply with every mandate in RA-003 (AI Platform), RA-007 (AI Agent Runtime), and RA-008 (RAG Platform).

**Mandatory AI Foundation Capabilities**

- AI Orchestrator (RA-003) is the sole entry point for platform AI workloads
- Registry Architecture governs all AI assets — models, agents, tools, prompts, capabilities (RA-003)
- Model Router determines model selection per request (RA-003)
- Context Engine assembles tenant-aware context for every AI operation (RA-003)
- Enterprise Memory provides persistent, governed AI memory (RA-003)
- Guardrails apply to every AI request and response (RA-003)
- FinOps tracks and enforces cost per tenant and per capability (RA-003)
- Agent Runtime (RA-007) governs agent lifecycle, multi-agent collaboration, and human oversight
- RAG Platform (RA-008) governs ingestion, chunking, embedding, retrieval, reranking, citation, and trust scoring
- AI Provider Integrations shall be routed through the AI Platform (RA-012 §10)

**Mandatory Behaviors**

- Every AI request shall carry tenant context (RA-009, RA-003)
- Every AI request shall be authenticated and authorized (RA-011)
- Every AI response shall pass Guardrails (RA-003)
- Every AI operation shall emit AI Events (§11.4)
- Every AI operation shall be observable per RA-010
- Every AI operation shall respect FinOps budgets (RA-003)
- Every agent shall be registered before execution (RA-007, RA-003 Registry)
- Human oversight hooks shall be available to every agent (RA-007)

**Prohibited Practices**

- Direct integration with AI providers outside the AI Orchestrator (RA-012 §10; RA-011 §25 "AI access without policy validation")
- Untenanted AI context (RA-009)
- Unregistered agents (RA-007)
- AI operations without audit logging (RA-011 §20)

---

# 16. Observability Requirements

The Platform Foundation shall comply with every mandate in RA-010 (Observability & Operations).

**Mandatory Telemetry**

- Metrics from every service
- Structured logging from every service
- Distributed tracing across every request
- Correlation identifiers propagated end to end

**Mandatory Signals**

- Platform health per service
- Request latency and error rates
- Event platform telemetry per RA-006 §17
- Integration telemetry per RA-012 §14
- Security telemetry per RA-011 §14
- AI operation telemetry per RA-003 (Implementation Defined During Engineering for specifics)

**Mandatory Operational Practices**

- Dashboards for platform health (RA-010)
- Alerting on defined thresholds (RA-010)
- Incident Management lifecycle (RA-010)
- SRE practices (RA-010)
- Platform Health Score (RA-010)

**Tenant Awareness**

- Every metric, log, and trace shall carry tenant identifiers (RA-009, RA-010)
- Every dashboard and alert shall be tenant-aware where applicable

Vendor selection for metrics, logs, and traces is Implementation Defined During Engineering.

---

# 17. Deployment Requirements

The Platform Foundation shall comply with every mandate in RA-004 (Infrastructure Reference Architecture).

**Mandatory Deployment Capabilities**

- Environment Strategy across development, testing, staging, and production (RA-004)
- Compute baseline (RA-004)
- Networking baseline (RA-004)
- Secrets integration point (RA-004, RA-011 §10)
- Disaster Recovery scaffolding (RA-004)

**Mandatory Deployment Behaviors**

- Every service shall be deployable independently (RA-001)
- Every service shall expose liveness, readiness, and startup endpoints (RA-001, RA-010)
- Every service shall be observable from first deployment (RA-010)
- Every service shall be tenant-aware from first deployment (RA-009)
- Every service shall be secure from first deployment (RA-011)
- Every deployment shall be reversible
- Every deployment shall be audited (RA-011 §20)

**Environment Isolation**

- No production data in non-production environments unless explicitly governed
- No shared secrets across environments (RA-011 §10)
- No shared tenant data across environments (RA-009)

Specific deployment tooling, orchestration platforms, and topology are Implementation Defined During Engineering under RA-004.

---

# 18. Testing Requirements

The Platform Foundation shall be validated before any downstream Build Pack begins implementation. Testing shall conform to BP-000 engineering rules and to ES-001 through ES-007.

**Mandatory Test Categories**

- Unit testing for every module
- Contract testing for every API (RA-012 §19)
- Integration testing for every service (RA-012 §19)
- End-to-end testing across critical flows (RA-012 §19)
- Performance testing for critical paths (RA-012 §19)
- Security testing per RA-011 §18 (Secure SDLC — Static Analysis, Dynamic Analysis, Dependency Scanning, Security Testing)
- Failure testing including retry, DLQ, replay behavior (RA-006, RA-012 §19)
- Multi-tenant isolation testing (RA-009)
- Observability validation (RA-010)

**Mandatory Test Behaviors**

- Tests shall be automated wherever practical (RA-012 §19)
- Tests shall run in isolated environments (RA-004)
- Tests shall not depend on production data
- Tests shall validate tenant isolation
- Tests shall validate security controls
- Tests shall validate observability signals
- Test results shall be recorded and auditable

Concrete test frameworks and coverage thresholds are Implementation Defined During Engineering under ES-001 through ES-007.

---

# 19. Implementation Readiness Matrix

The Implementation Readiness Matrix is the engineering handoff between BP-002 and its downstream Implementation Packs. Every major platform capability is described using the mandatory nine-field template. Fields not explicitly declared by the approved repository are recorded as "Implementation Defined During Engineering".

---

## 19.1 Backend Runtime

- **Capability:** Backend Runtime
- **Primary Build Pack:** BP-002 Platform Foundation
- **Primary Reference Architecture:** RA-001 Backend Reference Architecture
- **Implementation Pack(s):** Implementation Defined During Engineering
- **Primary Owner:** Chief Platform Architecture Office (per RA-001 Document Owner)
- **Implementation Status:** Implementation Defined During Engineering
- **Dependencies:** MC-000 through MC-005, ARCH-001 through ARCH-008, DOMAIN-001 through DOMAIN-010, ES-001 through ES-007 (per RA-001 Depends On)
- **Downstream Consumers:** all Platform Services and downstream Build Packs (per RA-001 Referenced By)
- **Notes:** Canonical service scaffolding and lifecycle per RA-001 §22

---

## 19.2 Frontend Runtime

- **Capability:** Frontend Runtime
- **Primary Build Pack:** BP-002 Platform Foundation
- **Primary Reference Architecture:** RA-002 Frontend Reference Architecture
- **Implementation Pack(s):** Implementation Defined During Engineering
- **Primary Owner:** Chief Frontend Architecture Office (per RA-002 Document Owner)
- **Implementation Status:** Implementation Defined During Engineering
- **Dependencies:** MC-000 through MC-005, ARCH-001 through ARCH-008, DOMAIN-001 through DOMAIN-010, ES-001 through ES-007 (per RA-002 Depends On)
- **Downstream Consumers:** all Frontend workspaces and downstream Build Packs (per RA-002 Referenced By)
- **Notes:** Canonical workspace scaffolding per RA-002 §22

---

## 19.3 AI Foundation

- **Capability:** AI Foundation
- **Primary Build Pack:** BP-002 Platform Foundation
- **Primary Reference Architecture:** RA-003 AI Platform Reference Architecture (with RA-007 AI Agent Runtime and RA-008 RAG Platform)
- **Implementation Pack(s):** Implementation Defined During Engineering
- **Primary Owner:** Chief AI Platform Architecture Office (per RA-003 Document Owner); Chief AI Runtime Architecture Office (per RA-007 Document Owner); Chief AI Knowledge Architecture Office (per RA-008 Document Owner)
- **Implementation Status:** Implementation Defined During Engineering
- **Dependencies:** RA-003 upstream (MC / ARCH / DOMAIN / ES); RA-007 adds RA-001 through RA-006; RA-008 adds RA-001 through RA-007
- **Downstream Consumers:** all AI-consuming Platform Services, Agent Runtime consumers, RAG consumers (per RA-003 / RA-007 / RA-008 Referenced By)
- **Notes:** Registry Architecture governs all AI assets per RA-003; provider integrations routed via RA-012 §10

---

## 19.4 Infrastructure Foundation

- **Capability:** Infrastructure Foundation
- **Primary Build Pack:** BP-002 Platform Foundation
- **Primary Reference Architecture:** RA-004 Infrastructure Reference Architecture
- **Implementation Pack(s):** Implementation Defined During Engineering
- **Primary Owner:** Chief Infrastructure Architecture Office (per RA-004 Document Owner)
- **Implementation Status:** Implementation Defined During Engineering
- **Dependencies:** MC-000 through MC-005, ARCH-001 through ARCH-008, DOMAIN-001 through DOMAIN-010, ES-001 through ES-007 (per RA-004 Depends On)
- **Downstream Consumers:** all Platform Services and deployment pipelines (per RA-004 Referenced By)
- **Notes:** Cloud-independent environment strategy per RA-004

---

## 19.5 Data Foundation

- **Capability:** Data Foundation
- **Primary Build Pack:** BP-002 Platform Foundation
- **Primary Reference Architecture:** RA-005 Data Platform Reference Architecture
- **Implementation Pack(s):** Implementation Defined During Engineering
- **Primary Owner:** Chief Data Architecture Office (per RA-005 Document Owner)
- **Implementation Status:** Implementation Defined During Engineering
- **Dependencies:** MC-000 through MC-005, ARCH-001 through ARCH-008, DOMAIN-001 through DOMAIN-010, ES-001 through ES-007 (per RA-005 Depends On)
- **Downstream Consumers:** all Platform Services, AI Foundation, RAG Service, Analytics consumers (per RA-005 Referenced By)
- **Notes:** Polyglot persistence per RA-005; every store shall be tenant-scoped per RA-009

---

## 19.6 Event Foundation

- **Capability:** Event Foundation
- **Primary Build Pack:** BP-002 Platform Foundation
- **Primary Reference Architecture:** RA-006 Event-Driven Reference Architecture
- **Implementation Pack(s):** Implementation Defined During Engineering
- **Primary Owner:** Chief Platform Architecture Office (per RA-006 Document Owner)
- **Implementation Status:** Implementation Defined During Engineering
- **Dependencies:** RA-001 through RA-005 (per RA-006 Depends On)
- **Downstream Consumers:** all Backend Services, AI Platform, Workflow Engine, Notification Platform, Analytics Platform (per RA-006 Referenced By)
- **Notes:** Outbox / Inbox / Idempotency / DLQ / Replay mandatory per RA-006 §10 through §16

---

## 19.7 Multi-Tenant Foundation

- **Capability:** Multi-Tenant Foundation
- **Primary Build Pack:** BP-002 Platform Foundation
- **Primary Reference Architecture:** RA-009 Multi-Tenant Reference Architecture
- **Implementation Pack(s):** Implementation Defined During Engineering
- **Primary Owner:** Chief SaaS Architecture Office (per RA-009 Document Owner)
- **Implementation Status:** Implementation Defined During Engineering
- **Dependencies:** RA-001 through RA-008 (per RA-009 Depends On)
- **Downstream Consumers:** all Platform Services and downstream Build Packs (per RA-009 Referenced By)
- **Notes:** Tenant context propagation is mandatory across every service, event, log, and AI operation

---

## 19.8 Observability Foundation

- **Capability:** Observability Foundation
- **Primary Build Pack:** BP-002 Platform Foundation
- **Primary Reference Architecture:** RA-010 Observability & Operations Reference Architecture
- **Implementation Pack(s):** Implementation Defined During Engineering
- **Primary Owner:** Chief Site Reliability Engineering Office (per RA-010 Document Owner)
- **Implementation Status:** Implementation Defined During Engineering
- **Dependencies:** RA-001 through RA-009 (per RA-010 Depends On)
- **Downstream Consumers:** all Platform Services, SRE, incident management, dashboards, alerting (per RA-010 Referenced By)
- **Notes:** Metrics, structured logging, distributed tracing mandatory from first deployment

---

## 19.9 Security Foundation

- **Capability:** Security Foundation
- **Primary Build Pack:** BP-002 Platform Foundation
- **Primary Reference Architecture:** RA-011 Security Reference Architecture
- **Implementation Pack(s):** Implementation Defined During Engineering
- **Primary Owner:** Chief Information Security Office (per RA-011 Document Owner)
- **Implementation Status:** Implementation Defined During Engineering
- **Dependencies:** RA-001 through RA-010 (per RA-011 Depends On)
- **Downstream Consumers:** all Platform Services, AI Platform, Infrastructure, Build Packs, Implementation Packs (per RA-011 Referenced By)
- **Notes:** Zero Trust and Least Privilege enforced across every request per RA-011 §2, §8

---

## 19.10 Integration Foundation

- **Capability:** Integration Foundation
- **Primary Build Pack:** BP-002 Platform Foundation
- **Primary Reference Architecture:** RA-012 Integration Reference Architecture
- **Implementation Pack(s):** Implementation Defined During Engineering
- **Primary Owner:** Chief Integration Architecture Office (per RA-012 Document Owner)
- **Implementation Status:** Implementation Defined During Engineering
- **Dependencies:** RA-001 through RA-011 (per RA-012 Depends On)
- **Downstream Consumers:** all Platform Services, External Integrations, Enterprise Connectors, Build Packs, Implementation Packs (per RA-012 Referenced By)
- **Notes:** API Gateway is the sole ingress; provider integrations governed via RA-012 §10

---

This matrix constitutes the authoritative engineering handoff between BP-002 and the Implementation Packs that will operationalize each capability. Implementation Packs shall update the Implementation Status field as each capability transitions from "Implementation Defined During Engineering" to "In Implementation" to "Implemented" per repository governance.

---

# 20. Acceptance Criteria

BP-002 is considered accepted when all of the following are true.

**Documentation Acceptance**

- BP-002 is present in `04_Build_Packs/BP-002_Platform_Foundation.md`
- BP-002 is registered in MC-000
- BP-002 is traced in RTM-001
- BP-002 references only approved MC, ARCH, DOMAIN, ES, RA, and preceding BP documents

**Structural Acceptance**

- All mandatory Build Pack sections are present, including Build Pack Objectives, Platform Capability Map, Platform Context Diagram, Service Inventory, Implementation Readiness Matrix, and Traceability Matrix
- Service Inventory follows the mandatory eleven-field template for every service
- Required Databases follows the mandatory eleven-field template for every database
- Required Events follows the mandatory eleven-field template for every event category
- Implementation Readiness Matrix follows the mandatory nine-field template for every capability
- Traceability Matrix follows the mandatory eight-column format
- Engineering Decisions follows the mandatory eight-field template for every decision

**Governance Acceptance**

- No invented architecture is present
- Every dependency cites an approved repository document
- Every unknown field is recorded as "Implementation Defined During Engineering"
- No downstream implementation guidance conflicts with any RA §25 anti-pattern

**Readiness Acceptance**

- The Platform Foundation contract is sufficient to begin authoring subsequent Build Packs
- The Service Inventory unambiguously enumerates every baseline service
- The Required Events section unambiguously enumerates every mandatory event category
- The Required Databases section unambiguously enumerates every baseline storage capability
- The Implementation Readiness Matrix unambiguously enumerates every major platform capability

Once all four acceptance categories are satisfied, BP-002 shall be marked Approved and frozen under §30 (Build Pack Freeze Declaration).

---

# 21. Definition of Done

BP-002 is considered Done only when all of the following are simultaneously true.

**Content Done**

- Every mandatory section is present and complete
- Every service in the Service Inventory uses the mandatory eleven-field template
- Every database in Required Databases uses the mandatory eleven-field template
- Every event category in Required Events uses the mandatory eleven-field template
- Every capability in the Implementation Readiness Matrix uses the mandatory nine-field template
- Every unknown field is recorded as "Implementation Defined During Engineering"

**Traceability Done**

- Every claim is traceable to MC-000 through MC-005, ARCH-001 through ARCH-008, DOMAIN-001 through DOMAIN-010, ES-001 through ES-007, RA-001 through RA-012, BP-000, or BP-001
- No content is invented outside the approved repository
- The Traceability Matrix (§26) enumerates every upstream dependency

**Governance Done**

- MC-000 registers BP-002
- RTM-001 records BP-002 traceability
- CHANGELOG records BP-002 addition
- VERSION reflects the repository advance
- The document is committed with the format `docs(bp-002): add build pack` per BP-000 Git Rules

**Engineering Done**

- Acceptance Criteria (§20) are satisfied
- No anti-pattern from any RA §25 is present in BP-002 guidance
- No downstream Build Pack, Implementation Pack, or production service can proceed without conforming to BP-002

Only when every category is satisfied shall BP-002 be marked Approved.

---

# 22. Engineering Checklist

The following checklist shall be executed before BP-002 is submitted for approval.

**Structural Checklist**

- [ ] Document Information header present and correct
- [ ] All 30 mandatory sections present in the specified order
- [ ] Section numbering consistent with the approved list
- [ ] Build Pack Objectives (§4) present
- [ ] Platform Capability Map (§4.1) present
- [ ] Platform Context (§4.2) present
- [ ] Service Inventory (§8) uses eleven-field template
- [ ] Required Databases (§10) uses eleven-field template
- [ ] Required Events (§11) uses eleven-field template
- [ ] Implementation Readiness Matrix (§19) uses nine-field template
- [ ] Traceability Matrix (§26) uses eight-column format
- [ ] Engineering Decisions (§27) uses eight-field template
- [ ] Build Pack Freeze Declaration (§30) present

**Content Checklist**

- [ ] Every capability is bound to an authoritative Reference Architecture
- [ ] Every service cites its Source Documents
- [ ] Every database cites its Source Documents
- [ ] Every event category cites its Source Documents
- [ ] Every unknown field is marked "Implementation Defined During Engineering"
- [ ] No invented architecture is present
- [ ] No prohibited practice from any RA §25 is present

**Traceability Checklist**

- [ ] MC-000 references verified
- [ ] MC-001 through MC-005 references verified
- [ ] ARCH-001 through ARCH-008 references verified
- [ ] DOMAIN-001 through DOMAIN-010 references verified
- [ ] ES-001 through ES-007 references verified
- [ ] RA-001 through RA-012 references verified
- [ ] BP-000 references verified
- [ ] BP-001 references verified

**Governance Checklist**

- [ ] MC-000 updated to register BP-002
- [ ] RTM-001 updated to trace BP-002
- [ ] CHANGELOG updated
- [ ] VERSION updated
- [ ] Git commit prepared per BP-000 Git Rules

Every checklist item shall be satisfied before Approval.

---

# 23. Risks

The following risks are recorded for BP-002. Mitigation strategies are Implementation Defined During Engineering and shall be authored under RA-011 §21 (Risk Management).

**Governance Risks**

- Downstream Build Packs may attempt to redefine platform capabilities that are owned by BP-002. Mitigation: Reference Architecture conformance gates.
- Upstream architecture may evolve after BP-002 is frozen. Mitigation: ADR workflow declared by BP-000 and each RA §27.

**Engineering Risks**

- Implementation may drift from the RA layer if Implementation Packs are authored without BP-002 consultation. Mitigation: Implementation Readiness Matrix (§19) as mandatory handoff.
- Service Inventory items may be re-implemented locally by downstream services. Mitigation: prohibition declared in §8.

**Security Risks**

- Prohibited practices from RA-011 §25 (hard-coded credentials, shared administrator accounts, missing encryption, excessive privileges, disabled audit logging, direct database access without authorization, unmanaged secrets, AI access without policy validation) may re-appear during rapid implementation. Mitigation: Secure SDLC per RA-011 §18 and Security Auditing per RA-011 §20.

**Multi-Tenant Risks**

- Tenant identifiers may be missing from persistence, events, telemetry, or AI context. Mitigation: mandatory behaviors declared in §14.

**AI Risks**

- AI provider integrations may bypass the AI Orchestrator. Mitigation: prohibition declared in §15.
- Unregistered agents may execute. Mitigation: Registry Architecture per RA-003 and RA-007.

**Operational Risks**

- Observability signals may be inconsistent across services. Mitigation: RA-010 conformance and §16 mandates.
- Deployments may proceed without required tenant, security, or observability posture. Mitigation: Deployment behaviors declared in §17.

Concrete risk-scoring, likelihood, and impact assessments are Implementation Defined During Engineering under RA-011 §21.

---

# 24. Assumptions

BP-002 is authored under the following assumptions. Each assumption is anchored in the approved repository.

- MC-000 through MC-005 are the sole authoritative Master Context for Project ATLAS.
- ARCH-001 through ARCH-008 are the sole authoritative Architecture documents.
- DOMAIN-001 through DOMAIN-010 are the sole authoritative Domain Model documents.
- ES-001 through ES-007 are the sole authoritative Engineering Standards.
- RA-001 through RA-012 are the sole authoritative Reference Architecture documents.
- BP-000 and BP-001 are the sole preceding Build Packs.
- No repository document outside those listed above is authoritative for BP-002 content.
- The Reference Architecture layer is technology-neutral and shall not be superseded by BP-002.
- Implementation Packs will operationalize each capability listed in the Implementation Readiness Matrix (§19) under separate governance.
- The Product Owner is Anil Kumar as declared in every upstream document.
- Deviations from BP-002 require an approved Architecture Decision Record per BP-000 AI Development Rules.

---

# 25. Out of Scope

BP-002 does not define any of the following. Each item is delegated to the identified authority.

- Domain business logic — delegated to future domain Build Packs
- Specific AI agents — delegated to AI-domain Build Packs and RA-007 Registry Architecture
- Specific integrations — delegated to Integration Build Packs and RA-012 Enterprise Integration Catalog
- Specific user interface features — delegated to Frontend Build Packs and RA-002
- Specific business workflows — delegated to Workflow Build Packs
- Specific vendors, cloud providers, or products — delegated to Implementation Packs under the RA extension points
- Specific data schemas beyond the Event Contract (RA-006 §8) — delegated to domain Build Packs
- Specific test frameworks and coverage thresholds — delegated to ES-001 through ES-007
- Specific deployment tooling and orchestration topology — delegated to RA-004 and Implementation Packs
- Specific risk-scoring methodologies — delegated to RA-011 §21
- Specific compliance certifications — delegated to RA-011 §16 and organizational governance

BP-002 shall not be interpreted as defining, superseding, or altering any item in this list. Any downstream authority shall conform to BP-002 without expanding its scope.

---

# 26. Traceability Matrix

Every BP-002 section is mapped to its upstream authority. Verification Method describes how conformance is proven.

| BP Section | MC Reference | ARCH Reference | DOMAIN Reference | ES Reference | RA Reference | BP Reference | Verification Method |
|-----------|-------------|---------------|-----------------|-------------|-------------|-------------|--------------------|
| §1 Purpose | MC-000 | ARCH-001..008 | DOMAIN-001..010 | ES-001..007 | RA-001..012 | BP-000, BP-001 | Repository governance rule |
| §2 Scope | MC-000 | n/a | n/a | n/a | RA-001, RA-003, RA-005, RA-006, RA-009, RA-010, RA-011, RA-012 | BP-000 | Reference Architecture citation |
| §3 Dependencies | MC-000..005 | ARCH-001..008 | DOMAIN-001..010 | ES-001..007 | RA-001..012 | BP-000, BP-001 | Direct upstream enumeration |
| §4 Build Pack Objectives | MC-000 | n/a | n/a | n/a | RA-001..012 | BP-000 | Repository governance rule |
| §4.1 Platform Capability Map | MC-000 | n/a | n/a | n/a | RA-001..012 | n/a | Reference Architecture binding table |
| §4.2 Platform Context | MC-000 | n/a | n/a | n/a | n/a | n/a | Repository governance chain |
| §5 Platform Responsibilities | n/a | n/a | n/a | n/a | RA-001..012 | BP-000, BP-001 | Reference Architecture citation |
| §6 Platform Components | n/a | n/a | n/a | n/a | RA-001..012 | n/a | Reference Architecture citation |
| §7 Repository Mapping | MC-000 | n/a | n/a | n/a | RA-001..012 §22 | BP-000, BP-001 | Canonical structure cross-check |
| §8 Service Inventory | n/a | n/a | n/a | n/a | RA-003, RA-006, RA-007, RA-008, RA-009, RA-010, RA-011, RA-012 | n/a | Eleven-field template conformance |
| §9 Required APIs | n/a | n/a | n/a | n/a | RA-001, RA-006, RA-009, RA-010, RA-011, RA-012 | n/a | Reference Architecture citation |
| §10 Required Databases | n/a | n/a | n/a | n/a | RA-005, RA-008, RA-009, RA-011 | n/a | Eleven-field template conformance |
| §11 Required Events | n/a | n/a | n/a | n/a | RA-006, RA-011, RA-012 | n/a | Eleven-field template conformance |
| §12 Required Configuration | n/a | n/a | n/a | n/a | RA-001, RA-004, RA-009, RA-011 | n/a | Reference Architecture citation |
| §13 Security Requirements | n/a | n/a | n/a | n/a | RA-011 | n/a | Reference Architecture citation |
| §14 Multi-Tenant Requirements | n/a | n/a | n/a | n/a | RA-009 | n/a | Reference Architecture citation |
| §15 AI Integration Requirements | n/a | n/a | n/a | n/a | RA-003, RA-007, RA-008, RA-011, RA-012 | n/a | Reference Architecture citation |
| §16 Observability Requirements | n/a | n/a | n/a | n/a | RA-010 | n/a | Reference Architecture citation |
| §17 Deployment Requirements | n/a | n/a | n/a | n/a | RA-004 | n/a | Reference Architecture citation |
| §18 Testing Requirements | n/a | n/a | n/a | ES-001..007 | RA-011 §18, RA-012 §19 | BP-000 | Engineering Standard cross-check |
| §19 Implementation Readiness Matrix | n/a | n/a | n/a | n/a | RA-001..012 | n/a | Nine-field template conformance |
| §20 Acceptance Criteria | MC-000 | n/a | n/a | n/a | n/a | BP-000 | Repository governance rule |
| §21 Definition of Done | MC-000 | n/a | n/a | n/a | n/a | BP-000 | Repository governance rule |
| §22 Engineering Checklist | n/a | n/a | n/a | ES-001..007 | n/a | BP-000 | Engineering Standard cross-check |
| §23 Risks | n/a | n/a | n/a | n/a | RA-011 §21 | n/a | Reference Architecture citation |
| §24 Assumptions | MC-000..005 | ARCH-001..008 | DOMAIN-001..010 | ES-001..007 | RA-001..012 | BP-000, BP-001 | Repository governance chain |
| §25 Out of Scope | n/a | n/a | n/a | ES-001..007 | RA-004, RA-006 §8, RA-011 §16 §21 | BP-001 §12 | Delegation citation |
| §26 Traceability Matrix | MC-000 | n/a | n/a | n/a | n/a | n/a | Eight-column template conformance |
| §27 Engineering Decisions | n/a | n/a | n/a | n/a | RA-001..012 §27 pattern | BP-000 | Eight-field template conformance |
| §28 Cross References | MC-000 | ARCH-001..008 | DOMAIN-001..010 | ES-001..007 | RA-001..012 | BP-000, BP-001 | Direct enumeration |
| §29 Version History | n/a | n/a | n/a | n/a | n/a | BP-000 | Repository convention |
| §30 Build Pack Freeze Declaration | MC-000 | n/a | n/a | n/a | RA-001..012 §30 pattern | BP-000 | Repository governance rule |

Every claim in BP-002 is traceable through this matrix. Rows with "Repository governance rule" as Verification Method correspond to standards adopted during BP-002 authoring.

---

# 27. Engineering Decisions

BP-002 records the following engineering decisions. Every decision follows the mandatory eight-field template. Rationale references only approved repository documents.

---

## 27.1 ED-001 — Consume Reference Architecture verbatim

- **Decision ID:** ED-001
- **Decision:** BP-002 shall consume the Reference Architecture layer verbatim and shall not redefine any Reference Architecture capability, principle, or structure.
- **Source Documents:** BP-000 (Build Rules, AI Development Rules), RA-001..012 §25 (Anti-Patterns), RA-001..012 §30 (Freeze Declarations)
- **Rationale:** BP-000 forbids silent architectural change; every RA §30 declares its architecture frozen; every RA §25 prohibits deviations without an ADR.
- **Impact:** Downstream Build Packs and Implementation Packs are bound to the Reference Architecture through BP-002.
- **Alternatives Considered:** None admissible under BP-000 governance.
- **Status:** Accepted
- **Future ADR Required:** No

---

## 27.2 ED-002 — Service Inventory eleven-field template

- **Decision ID:** ED-002
- **Decision:** Every service in the Service Inventory shall use the mandatory eleven-field template (Service Name, Source Documents, Responsibilities, Inputs, Outputs, Dependencies, Consumers, Failure Modes, Observability Requirements, Security Requirements, Implementation Status).
- **Source Documents:** Repository governance rule adopted during BP-002 authoring.
- **Rationale:** Ensures uniform service description, prevents omission of security and observability fields, and forces explicit acknowledgment of unknowns via "Implementation Defined During Engineering".
- **Impact:** Every Build Pack from BP-002 through BP-012 shall conform.
- **Alternatives Considered:** Free-form service description — rejected because it permits inconsistency and omission.
- **Status:** Accepted
- **Future ADR Required:** No

---

## 27.3 ED-003 — Required Databases eleven-field template

- **Decision ID:** ED-003
- **Decision:** Every database in the Required Databases section shall use the mandatory eleven-field template (Database Name, Source Documents, Purpose, Ownership, Data Classification, Tenant Isolation, Backup Responsibility, Retention Policy, Encryption Requirements, Consumers, Implementation Status).
- **Source Documents:** Repository governance rule adopted during BP-002 authoring; RA-005 (Data governance), RA-009 (Tenant isolation), RA-011 §9 (Encryption).
- **Rationale:** Data stores require explicit ownership, classification, isolation, and encryption declarations; the template prevents omission.
- **Impact:** Every Build Pack from BP-002 through BP-012 shall conform.
- **Alternatives Considered:** Free-form database description — rejected on the same grounds as ED-002.
- **Status:** Accepted
- **Future ADR Required:** No

---

## 27.4 ED-004 — Required Events eleven-field template

- **Decision ID:** ED-004
- **Decision:** Every event category in the Required Events section shall use the mandatory eleven-field template (Event Category, Source Documents, Producer, Consumer, Purpose, Delivery Guarantee, Ordering Requirements, Retry Strategy, Dead Letter Strategy, Observability Requirements, Implementation Status).
- **Source Documents:** Repository governance rule adopted during BP-002 authoring; RA-006 (Event architecture).
- **Rationale:** Event categories require explicit delivery, ordering, retry, and DLQ declarations to satisfy RA-006 §10 through §17.
- **Impact:** Every Build Pack from BP-002 through BP-012 shall conform.
- **Alternatives Considered:** Free-form event description — rejected on the same grounds as ED-002.
- **Status:** Accepted
- **Future ADR Required:** No

---

## 27.5 ED-005 — Implementation Readiness Matrix nine-field template

- **Decision ID:** ED-005
- **Decision:** The Implementation Readiness Matrix shall use the mandatory nine-field template (Capability, Primary Build Pack, Primary Reference Architecture, Implementation Pack(s), Primary Owner, Implementation Status, Dependencies, Downstream Consumers, Notes) and shall be placed immediately before Acceptance Criteria.
- **Source Documents:** Repository governance rule adopted during BP-002 authoring; RA-001..012 Document Owner declarations.
- **Rationale:** The matrix formalizes the engineering handoff between Build Packs and Implementation Packs and prevents implementation drift.
- **Impact:** Every Build Pack from BP-002 through BP-012 shall include this matrix. Implementation Packs shall update Implementation Status.
- **Alternatives Considered:** Deferring the handoff artifact to Implementation Packs — rejected because it removes upstream traceability.
- **Status:** Accepted
- **Future ADR Required:** No

---

## 27.6 ED-006 — Traceability Matrix eight-column format

- **Decision ID:** ED-006
- **Decision:** The Traceability Matrix shall use the mandatory eight-column format (BP Section, MC Reference, ARCH Reference, DOMAIN Reference, ES Reference, RA Reference, BP Reference, Verification Method).
- **Source Documents:** Repository governance rule adopted during BP-002 authoring.
- **Rationale:** Explicit column-per-layer traceability proves that every Build Pack section is grounded in an authoritative repository document.
- **Impact:** Every Build Pack from BP-002 through BP-012 shall conform.
- **Alternatives Considered:** Free-form traceability paragraph — rejected because it defeats column-per-layer auditability.
- **Status:** Accepted
- **Future ADR Required:** No

---

## 27.7 ED-007 — Engineering Decisions Register eight-field template

- **Decision ID:** ED-007
- **Decision:** The Engineering Decisions section shall be structured as a register using the mandatory eight-field template (Decision ID, Decision, Source Documents, Rationale, Impact, Alternatives Considered, Status, Future ADR Required).
- **Source Documents:** Repository governance rule adopted during BP-002 authoring; RA-001..012 §27 pattern.
- **Rationale:** A decision register with explicit rationale and impact prevents opaque architectural drift and preserves the reasoning for future ADRs.
- **Impact:** Every Build Pack from BP-002 through BP-012 shall conform.
- **Alternatives Considered:** Simple decision list without rationale — rejected because it loses reasoning and blocks ADR authoring.
- **Status:** Accepted
- **Future ADR Required:** No

---

## 27.8 ED-008 — Vendor and product selection deferred

- **Decision ID:** ED-008
- **Decision:** Every vendor, product, and specific technology selection is deferred to Implementation Packs.
- **Source Documents:** RA-001..012 §24 (Technology Mapping — technology-neutral); RA-001..012 §30 (Freeze Declarations).
- **Rationale:** The Reference Architecture layer is explicitly technology-neutral; premature vendor lock-in violates each RA §24.
- **Impact:** Decision Deferred to Implementation Pack for every technology-specific decision.
- **Alternatives Considered:** Selecting vendors in BP-002 — rejected because it contradicts every RA §24.
- **Status:** Accepted
- **Future ADR Required:** No

---

## 27.9 ED-009 — AI Orchestrator is the sole AI entry point

- **Decision ID:** ED-009
- **Decision:** The AI Orchestrator Service (§8.9) is the sole entry point for platform AI workloads.
- **Source Documents:** RA-003 (AI Platform Architecture); RA-012 §10 (AI Provider Integrations); RA-011 §25 ("AI access without policy validation" prohibited).
- **Rationale:** Centralizing AI ingress enforces Guardrails, FinOps, tenant scoping, and Registry conformance for every AI request.
- **Impact:** No service shall integrate directly with an AI provider.
- **Alternatives Considered:** Per-service direct AI integration — rejected under RA-011 §25 and RA-012 §10.
- **Status:** Accepted
- **Future ADR Required:** No

---

## 27.10 ED-010 — API Gateway is the sole ingress

- **Decision ID:** ED-010
- **Decision:** The API Gateway Service (§8.8) is the sole ingress for external and governed internal API traffic.
- **Source Documents:** RA-012 §5 (API Gateway); RA-011 (Authentication and Authorization).
- **Rationale:** Centralized ingress enforces authentication, authorization, rate limiting, versioning, and validation uniformly.
- **Impact:** No service shall accept ungoverned inbound traffic.
- **Alternatives Considered:** Per-service ingress — rejected under RA-012 §5 and RA-012 §25 anti-patterns ("Bypassing API Gateway").
- **Status:** Accepted
- **Future ADR Required:** No

---

## 27.11 ED-011 — Event Bus is the sole event distribution mechanism

- **Decision ID:** ED-011
- **Decision:** The Event Bus Service (§8.6) is the sole mechanism for platform event distribution.
- **Source Documents:** RA-006 (Event Bus, Outbox, Inbox, DLQ, Replay); RA-006 §25 anti-patterns ("Direct service-to-service dependencies where events are appropriate").
- **Rationale:** Centralized event distribution enforces Outbox reliability, idempotency, DLQ, replay, and observability.
- **Impact:** No service shall bypass the Event Bus for cross-service communication where events are appropriate.
- **Alternatives Considered:** Point-to-point service integrations — rejected under RA-006 §25.
- **Status:** Accepted
- **Future ADR Required:** No

---

## 27.12 ED-012 — Tenant Registry is the authoritative tenant record

- **Decision ID:** ED-012
- **Decision:** The Tenant Registry Service (§8.2) is the sole authoritative source of tenant records.
- **Source Documents:** RA-009 (Multi-Tenant Reference Architecture).
- **Rationale:** A single tenant registry enforces consistent isolation, subscription, feature, and lifecycle behavior across every service.
- **Impact:** No service shall maintain a parallel tenant record.
- **Alternatives Considered:** Per-service tenant records — rejected under RA-009.
- **Status:** Accepted
- **Future ADR Required:** No

---

## 27.13 ED-013 — Zero Trust across every request

- **Decision ID:** ED-013
- **Decision:** Zero Trust and Least Privilege shall apply to every request in the Platform Foundation.
- **Source Documents:** RA-011 §2 (Security Principles), §8 (Zero Trust Architecture).
- **Rationale:** RA-011 mandates continuous verification; trust shall never be assumed based on network location.
- **Impact:** Every request shall be authenticated, authorized, and auditable.
- **Alternatives Considered:** Perimeter-based trust — rejected under RA-011 §8.
- **Status:** Accepted
- **Future ADR Required:** No

---

## 27.14 ED-014 — Every service is tenant-aware, secure, observable, and event-aware from first deployment

- **Decision ID:** ED-014
- **Decision:** Every Platform Service shall be tenant-aware, secure, observable, and event-aware from first deployment.
- **Source Documents:** RA-006, RA-009, RA-010, RA-011.
- **Rationale:** Retro-fitting these capabilities has been declared out of scope; downstream Build Packs consume them from BP-002 as preconditions.
- **Impact:** No downstream service shall enter deployment without these capabilities.
- **Alternatives Considered:** Progressive enablement per capability — rejected because it permits gaps that violate RA-011 §25.
- **Status:** Accepted
- **Future ADR Required:** No

---

# 28. Cross References

**Preceding Build Packs**

- BP-000 Engineering Foundation
- BP-001 Product Foundation

**Reference Architecture**

- RA-001 Backend Reference Architecture
- RA-002 Frontend Reference Architecture
- RA-003 AI Platform Reference Architecture
- RA-004 Infrastructure Reference Architecture
- RA-005 Data Platform Reference Architecture
- RA-006 Event-Driven Reference Architecture
- RA-007 AI Agent Runtime Reference Architecture
- RA-008 RAG Platform Reference Architecture
- RA-009 Multi-Tenant Reference Architecture
- RA-010 Observability & Operations Reference Architecture
- RA-011 Security Reference Architecture
- RA-012 Integration Reference Architecture

**Engineering Standards**

- ES-001 through ES-007

**Domain Model**

- DOMAIN-001 through DOMAIN-010

**Architecture**

- ARCH-001 through ARCH-008

**Master Context**

- MC-000 Repository Index
- MC-001 through MC-005

**Future Related Documents**

- BP-003 and subsequent Build Packs
- All Implementation Packs
- RTM-001 Repository Traceability Matrix

---

# 29. Version History

- 1.0.0 — Initial Build Pack. Establishes the canonical Platform Foundation for Project ATLAS. Adopts the mandatory Build Pack section standards (Objectives, Capability Map, Context Diagram, Service Inventory, Implementation Readiness Matrix, Traceability Matrix) and the mandatory templates (Service Inventory 11-field, Required Databases 11-field, Required Events 11-field, Implementation Readiness Matrix 9-field, Traceability Matrix 8-column, Engineering Decisions Register 8-field) for BP-002 through BP-012.

---

# 30. Build Pack Freeze Declaration

Upon approval, BP-002 becomes the authoritative Platform Foundation for Project ATLAS.

The following standards are considered frozen until amended through formal repository governance:

- Platform Capability Map (§4.1)
- Platform Context (§4.2)
- Platform Responsibilities (§5)
- Platform Components (§6)
- Repository Mapping (§7)
- Service Inventory template (§8)
- Required APIs baseline (§9)
- Required Databases template (§10)
- Required Events template (§11)
- Required Configuration governance (§12)
- Security Requirements binding (§13)
- Multi-Tenant Requirements binding (§14)
- AI Integration Requirements binding (§15)
- Observability Requirements binding (§16)
- Deployment Requirements binding (§17)
- Testing Requirements binding (§18)
- Implementation Readiness Matrix template (§19)
- Acceptance Criteria (§20)
- Definition of Done (§21)
- Traceability Matrix format (§26)
- Engineering Decisions Register format (§27)

All future Build Packs, Implementation Packs, platform services, AI services, integrations, and production systems shall conform to BP-002 without deviation.

Changes affecting BP-002 require an approved Architecture Decision Record per BP-000 AI Development Rules.

---

# End of Document
