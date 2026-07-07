# Project ATLAS

# Build Pack Roadmap

## BP-ROADMAP — Official Build Pack Roadmap

---

## Document Information

| Field | Value |
|--------|--------|
| Document ID | BP-ROADMAP |
| Title | Official Build Pack Roadmap |
| Version | 1.0.0 |
| Status | Approved |
| Repository | Project ATLAS |
| Document Owner | Chief Architecture Office |
| Product Owner | Anil Kumar |
| Repository Path | 04_Build_Packs/BP-ROADMAP.md |
| Depends On | MC-000, RTM-001, BP-000, BP-001, BP-002, ARCH-001 through ARCH-008, DOMAIN-001 through DOMAIN-010, ES-001 through ES-007, RA-001 through RA-012 |
| Last Updated | 2026-07-08 |

---

# 1. Purpose

BP-ROADMAP is the single authoritative source for the Project ATLAS Build Pack sequence.

It defines every registered Build Pack from BP-000 through BP-012, the primary Reference Architectures each Build Pack derives from, its Domain scope, its current lifecycle status, its inter-Build-Pack dependencies, and the planned implementation order.

BP-ROADMAP does not author Build Pack content. Each Build Pack remains an independent document. BP-ROADMAP only establishes the framing, sequence, and dependency graph that governs how Build Packs are authored and delivered.

Upon approval, BP-ROADMAP replaces the retired placeholder Build Pack titles previously recorded in MC-000 (prior to MC-000 v2.3.0) and becomes the sole roadmap reference for all future Build Pack authoring.

---

# 2. Scope

**In Scope:**

- Build Pack identifiers (BP-000 through BP-012)
- Build Pack titles
- Build Pack purposes derived exclusively from approved MC / ARCH / DOMAIN / ES / RA / prior BP sources
- Primary Reference Architecture bindings for each Build Pack
- Primary Domain bindings for each Build Pack
- Lifecycle status of each Build Pack
- Explicit inter-Build-Pack dependencies
- Planned implementation order and rationale

**Out of Scope:**

- Any implementation-level architecture, technology selection, or engineering decision. Those belong to Build Packs and Implementation Packs.
- Build Packs beyond BP-012. Any expansion of the Build Pack series requires a new roadmap version approved through repository governance.
- Implementation Pack sequencing. Implementation Pack ordering is governed by each Build Pack's Implementation Readiness Matrix.

---

# 3. Roadmap Format

Every Build Pack entry in this roadmap uses the following 7-field template:

1. Build Pack ID
2. Title
3. Purpose
4. Primary Reference Architectures
5. Primary Domains
6. Status
7. Dependencies

**Rules:**

- Titles for BP-000, BP-001, and BP-002 are frozen and reflect the authoritative Build Pack files.
- Titles for BP-003 through BP-012 are established by this roadmap. They shall be used verbatim when each Build Pack is authored.
- Purposes cite only approved repository documents. No external justification is admissible.
- Primary Reference Architectures shall be selected from RA-001 through RA-012.
- Primary Domains shall be selected from DOMAIN-001 through DOMAIN-010, or shall be "Cross-Cutting" for foundation Build Packs.
- Status values shall be one of: Approved, Draft (Engineering Review), Draft (Architecture Review), Planned.
- Dependencies shall list every prior Build Pack whose approval is required before the current Build Pack may enter engineering review.

---

# 4. Build Pack Roadmap Table

| BP ID | Title | Status | Primary Reference Architectures | Primary Domains | Depends On |
|--------|--------|--------|--------|--------|--------|
| BP-000 | Engineering Foundation | Approved | n/a (governance) | Cross-Cutting | — |
| BP-001 | Product Foundation | Approved | n/a (product) | Cross-Cutting | BP-000 |
| BP-002 | Platform Foundation | Draft (Engineering Review) | RA-001, RA-002, RA-003, RA-004, RA-005, RA-006, RA-007, RA-008, RA-009, RA-010, RA-011, RA-012 | Cross-Cutting | BP-000, BP-001 |
| BP-003 | Identity & Access Platform | Planned | RA-011, RA-009, RA-001 | DOMAIN-002 | BP-000, BP-001, BP-002 |
| BP-004 | Tenant & Organization Platform | Planned | RA-009, RA-001, RA-005 | DOMAIN-001 | BP-000, BP-001, BP-002, BP-003 |
| BP-005 | AI Platform | Planned | RA-003, RA-007, RA-001 | DOMAIN-010 | BP-000, BP-001, BP-002, BP-003, BP-004 |
| BP-006 | Knowledge Platform | Planned | RA-005, RA-008, RA-001 | DOMAIN-005 | BP-000, BP-001, BP-002, BP-003, BP-004, BP-005 |
| BP-007 | Workflow Platform | Planned | RA-001, RA-002, RA-006 | DOMAIN-003 | BP-000, BP-001, BP-002, BP-003, BP-004 |
| BP-008 | Meeting Intelligence Platform | Planned | RA-003, RA-007, RA-008, RA-006 | DOMAIN-004 | BP-000, BP-001, BP-002, BP-003, BP-004, BP-005, BP-006, BP-007 |
| BP-009 | Decision, Action & SOP Platform | Planned | RA-001, RA-006 | DOMAIN-006, DOMAIN-007, DOMAIN-008 | BP-000, BP-001, BP-002, BP-003, BP-004, BP-007 |
| BP-010 | Notification Platform | Planned | RA-012, RA-006, RA-001 | DOMAIN-009 | BP-000, BP-001, BP-002, BP-003, BP-004 |
| BP-011 | Integration Platform | Planned | RA-012, RA-001, RA-006 | Cross-Cutting (ARCH-006) | BP-000, BP-001, BP-002, BP-003, BP-004 |
| BP-012 | Production & Operations Platform | Planned | RA-010, RA-004, RA-001 | Cross-Cutting | BP-000, BP-001, BP-002, BP-003, BP-004, BP-005, BP-006, BP-007, BP-008, BP-009, BP-010, BP-011 |

---

# 5. Build Pack Entries

## 5.1 BP-000 — Engineering Foundation

- **Title:** Engineering Foundation
- **Purpose:** Establish the Build Pack governance rules, format, traceability requirements, and repository conventions that every subsequent Build Pack shall follow.
- **Primary Reference Architectures:** Not applicable. BP-000 is a governance Build Pack.
- **Primary Domains:** Cross-Cutting.
- **Status:** Approved.
- **Dependencies:** None.
- **Source Authority:** BP-000 file (Approved), MC-004 Core Principles & Governance.

---

## 5.2 BP-001 — Product Foundation

- **Title:** Product Foundation
- **Purpose:** Establish the product identity, vision, mission, and business framing for Project ATLAS as the authoritative product-level context for all downstream Build Packs.
- **Primary Reference Architectures:** Not applicable. BP-001 is a product-level Build Pack.
- **Primary Domains:** Cross-Cutting.
- **Status:** Approved.
- **Dependencies:** BP-000.
- **Source Authority:** BP-001 file (Approved), MC-001 Vision, MC-002 Product Foundation, MC-003 Product Scope & Roadmap.

---

## 5.3 BP-002 — Platform Foundation

- **Title:** Platform Foundation
- **Purpose:** Establish the cross-cutting platform capabilities that every domain Build Pack depends on, including identity foundations, tenant registry foundations, event bus, observability, API gateway, AI orchestration, agent runtime, RAG foundations, notification dispatch, secrets, and configuration.
- **Primary Reference Architectures:** RA-001, RA-002, RA-003, RA-004, RA-005, RA-006, RA-007, RA-008, RA-009, RA-010, RA-011, RA-012.
- **Primary Domains:** Cross-Cutting.
- **Status:** Draft (Engineering Review).
- **Dependencies:** BP-000, BP-001.
- **Source Authority:** BP-002 file (Draft (Engineering Review)), ARCH-001 through ARCH-008, RA-001 through RA-012.

---

## 5.4 BP-003 — Identity & Access Platform

- **Title:** Identity & Access Platform
- **Purpose:** Deliver the Identity & Access capability for Project ATLAS, including user identity, authentication, authorization, session management, tenant identity binding, and Zero Trust enforcement points, aligned to DOMAIN-002 and RA-011.
- **Primary Reference Architectures:** RA-011 Security, RA-009 Multi-Tenant, RA-001 Backend.
- **Primary Domains:** DOMAIN-002 Identity & User.
- **Status:** Planned.
- **Dependencies:** BP-000, BP-001, BP-002.
- **Source Authority:** DOMAIN-002, ARCH-005, RA-011, RA-009, RA-001, ES-004 Security Standards.

---

## 5.5 BP-004 — Tenant & Organization Platform

- **Title:** Tenant & Organization Platform
- **Purpose:** Deliver tenant lifecycle, organization structure, department and team modeling, subscription and entitlement enforcement, and multi-tenant governance, aligned to DOMAIN-001 and RA-009.
- **Primary Reference Architectures:** RA-009 Multi-Tenant, RA-001 Backend, RA-005 Data Platform.
- **Primary Domains:** DOMAIN-001 Organization.
- **Status:** Planned.
- **Dependencies:** BP-000, BP-001, BP-002, BP-003.
- **Source Authority:** DOMAIN-001, ARCH-002, RA-009, RA-005, RA-001.

---

## 5.6 BP-005 — AI Platform

- **Title:** AI Platform
- **Purpose:** Deliver the AI Platform including prompt orchestration, AI Gateway, model routing, AI Agent Runtime, AI safety, and AI governance surfaces, aligned to DOMAIN-010, RA-003, and RA-007.
- **Primary Reference Architectures:** RA-003 AI Platform, RA-007 AI Agent Runtime, RA-001 Backend.
- **Primary Domains:** DOMAIN-010 AI.
- **Status:** Planned.
- **Dependencies:** BP-000, BP-001, BP-002, BP-003, BP-004.
- **Source Authority:** DOMAIN-010, ARCH-003, RA-003, RA-007, ES-005 AI Engineering Standards.

---

## 5.7 BP-006 — Knowledge Platform

- **Title:** Knowledge Platform
- **Purpose:** Deliver the Knowledge capability including knowledge repository, search, retrieval-augmented generation (RAG), knowledge graph, and enterprise memory taxonomy, aligned to DOMAIN-005, RA-005, and RA-008.
- **Primary Reference Architectures:** RA-005 Data Platform, RA-008 RAG Platform, RA-001 Backend.
- **Primary Domains:** DOMAIN-005 Knowledge.
- **Status:** Planned.
- **Dependencies:** BP-000, BP-001, BP-002, BP-003, BP-004, BP-005.
- **Source Authority:** DOMAIN-005, ARCH-004, RA-005, RA-008.

---

## 5.8 BP-007 — Workflow Platform

- **Title:** Workflow Platform
- **Purpose:** Deliver the workflow capability that carries Project structure, project membership, project lifecycle, and project-scoped resources as the shared workflow surface for meetings, decisions, actions, and SOPs, aligned to DOMAIN-003.
- **Primary Reference Architectures:** RA-001 Backend, RA-002 Frontend, RA-006 Event-Driven.
- **Primary Domains:** DOMAIN-003 Project.
- **Status:** Planned.
- **Dependencies:** BP-000, BP-001, BP-002, BP-003, BP-004.
- **Source Authority:** DOMAIN-003, RA-001, RA-002, RA-006.

---

## 5.9 BP-008 — Meeting Intelligence Platform

- **Title:** Meeting Intelligence Platform
- **Purpose:** Deliver the Meeting capability including meeting lifecycle, recording, transcription, and meeting intelligence (summaries, action extraction, decision extraction, knowledge extraction), aligned to DOMAIN-004.
- **Primary Reference Architectures:** RA-003 AI Platform, RA-007 AI Agent Runtime, RA-008 RAG Platform, RA-006 Event-Driven.
- **Primary Domains:** DOMAIN-004 Meeting.
- **Status:** Planned.
- **Dependencies:** BP-000, BP-001, BP-002, BP-003, BP-004, BP-005, BP-006, BP-007.
- **Source Authority:** DOMAIN-004, ARCH-003, RA-003, RA-007, RA-008, RA-006.

---

## 5.10 BP-009 — Decision, Action & SOP Platform

- **Title:** Decision, Action & SOP Platform
- **Purpose:** Deliver the unified operational execution surface covering the Decision capability (decision lifecycle, approvals, history, traceability), the Action capability (assignments, status, tracking), and the SOP capability (generation, versioning, publication), aligned to DOMAIN-006, DOMAIN-007, and DOMAIN-008.
- **Primary Reference Architectures:** RA-001 Backend, RA-006 Event-Driven.
- **Primary Domains:** DOMAIN-006 Decision, DOMAIN-007 SOP, DOMAIN-008 Action.
- **Status:** Planned.
- **Dependencies:** BP-000, BP-001, BP-002, BP-003, BP-004, BP-007.
- **Source Authority:** DOMAIN-006, DOMAIN-007, DOMAIN-008, RA-001, RA-006.

---

## 5.11 BP-010 — Notification Platform

- **Title:** Notification Platform
- **Purpose:** Deliver the Notification capability including email, push, in-app, and webhook delivery channels, notification templates, and delivery guarantees, aligned to DOMAIN-009 and RA-012.
- **Primary Reference Architectures:** RA-012 Integration, RA-006 Event-Driven, RA-001 Backend.
- **Primary Domains:** DOMAIN-009 Notification.
- **Status:** Planned.
- **Dependencies:** BP-000, BP-001, BP-002, BP-003, BP-004.
- **Source Authority:** DOMAIN-009, RA-012, RA-006.

---

## 5.12 BP-011 — Integration Platform

- **Title:** Integration Platform
- **Purpose:** Deliver the enterprise integration capability including the connector framework, external system integrations, webhook framework, and AI provider integrations, aligned to ARCH-006 and RA-012.
- **Primary Reference Architectures:** RA-012 Integration, RA-001 Backend, RA-006 Event-Driven.
- **Primary Domains:** Cross-Cutting (ARCH-006 Integration Architecture).
- **Status:** Planned.
- **Dependencies:** BP-000, BP-001, BP-002, BP-003, BP-004.
- **Source Authority:** ARCH-006, RA-012, RA-006, RA-001.

---

## 5.13 BP-012 — Production & Operations Platform

- **Title:** Production & Operations Platform
- **Purpose:** Deliver the production readiness, observability, deployment, disaster recovery, and operational excellence capability that carries all preceding Build Pack outputs into production, aligned to RA-010 Observability & Operations and RA-004 Infrastructure.
- **Primary Reference Architectures:** RA-010 Observability & Operations, RA-004 Infrastructure, RA-001 Backend.
- **Primary Domains:** Cross-Cutting (ARCH-007 Deployment Architecture, ARCH-008 Non-Functional Architecture).
- **Status:** Planned.
- **Dependencies:** BP-000, BP-001, BP-002, BP-003, BP-004, BP-005, BP-006, BP-007, BP-008, BP-009, BP-010, BP-011.
- **Source Authority:** ARCH-007, ARCH-008, RA-010, RA-004, RA-001, ES-006 DevOps Standards.

---

# 6. Planned Implementation Order

The following order shall be observed unless amended through repository governance. The order reflects the dependency graph declared in Section 4 and Section 5.

**Foundation Layer (Complete or In Review):**

1. BP-000 — Engineering Foundation (Approved)
2. BP-001 — Product Foundation (Approved)
3. BP-002 — Platform Foundation (Draft (Engineering Review))

**Access & Tenant Layer:**

4. BP-003 — Identity & Access Platform
5. BP-004 — Tenant & Organization Platform

**Core Capability Layer:**

6. BP-005 — AI Platform
7. BP-006 — Knowledge Platform
8. BP-007 — Workflow Platform

**Applied Intelligence Layer:**

9. BP-008 — Meeting Intelligence Platform

**Operational Execution Layer:**

10. BP-009 — Decision, Action & SOP Platform

**Distribution & Extension Layer:**

11. BP-010 — Notification Platform
12. BP-011 — Integration Platform

**Production & Operations Layer:**

13. BP-012 — Production & Operations Platform

**Rationale for Ordering:**

- Foundation Layer must precede all others because every downstream Build Pack depends on BP-000, BP-001, and BP-002.
- BP-003 precedes BP-004 because tenant identity binding depends on the identity foundation established in BP-003.
- BP-005 precedes BP-006 and BP-008 because Knowledge Platform and Meeting Intelligence Platform consume AI Platform surfaces.
- BP-006 precedes BP-008 because Meeting Intelligence Platform consumes Knowledge Platform retrieval and enterprise memory surfaces.
- BP-007 precedes BP-008 and BP-009 because Workflow Platform provides the project scoping model for meetings, decisions, actions, and SOPs.
- BP-009 consolidates the operational execution surface (decisions, actions, SOPs) into a single Build Pack, executing after Workflow Platform is available.
- BP-010 and BP-011 may execute in parallel after BP-004 because they are distribution and extension layers that only require identity, tenant, and platform foundations.
- BP-012 executes last because Production & Operations Platform depends on every preceding Build Pack having reached engineering-ready state; the roadmap ends with production readiness so the platform can transition into operated service.

---

# 7. Governance Rules

- BP-ROADMAP is the sole authoritative roadmap for Build Packs BP-000 through BP-012.
- Retired placeholder titles from MC-000 prior to v2.3.0 are superseded by this roadmap.
- Every Build Pack authored from BP-003 onward shall use the title recorded in this roadmap verbatim.
- Every Build Pack authored from BP-003 onward shall respect the dependency graph declared in Section 4 and Section 5.
- Every Build Pack shall include the mandatory Build Pack sections established by BP-002: Build Pack Objectives, Platform Capability Map, Platform Context Diagram, Service Inventory, Implementation Readiness Matrix, Traceability Matrix.
- Every change to BP-ROADMAP requires a Product Owner approval and shall be recorded in Section 8 Version History.
- Changes that alter Build Pack titles, dependencies, or implementation order shall additionally require an Architecture Decision Record.

---

# 8. Version History

**Version 1.0.0 — 2026-07-08**

Initial Build Pack Roadmap.

- Established BP-000 through BP-012 as the authoritative Build Pack series
- Recorded frozen titles and statuses for BP-000, BP-001, BP-002
- Recorded Product Owner directed titles for BP-003 (Identity & Access Platform), BP-007 (Workflow Platform), BP-009 (Decision, Action & SOP Platform), and BP-012 (Production & Operations Platform)
- Consolidated the operational execution surface (decisions, actions, SOPs) into BP-009
- Positioned Integration Platform at BP-011 and Production & Operations Platform at BP-012 so the roadmap ends with production readiness
- Established titles, purposes, primary Reference Architectures, primary Domains, statuses, and dependencies for BP-004 through BP-012, derived exclusively from approved repository documents
- Established planned implementation order and dependency rationale
- Established roadmap governance rules

---

# 9. Roadmap Freeze Declaration

Upon approval, BP-ROADMAP becomes the authoritative Build Pack roadmap for Project ATLAS.

All Build Pack authoring from BP-003 onward shall conform to this roadmap.

Retired placeholder titles from MC-000 prior to v2.3.0 are superseded and shall not be used.

No Build Pack authoring shall commence without alignment with BP-ROADMAP.

BP-ROADMAP shall remain stable unless amended through formal repository governance and an approved Architecture Decision Record.

---

# 10. Cross References

- MC-000 Repository Index (v2.3.0)
- RTM-001 Repository Traceability Matrix (v1.2.1)
- BP-000 Engineering Foundation (Approved)
- BP-001 Product Foundation (Approved)
- BP-002 Platform Foundation (Draft (Engineering Review))
- ARCH-001 through ARCH-008 (Approved Repository Baseline)
- DOMAIN-001 through DOMAIN-010
- ES-001 through ES-007
- RA-001 through RA-012 (Draft (Architecture Review))

---
