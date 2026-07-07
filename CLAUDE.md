# Project ATLAS — Claude Code Context

This file is auto-loaded by Claude Code when the project is opened. It carries all context needed to continue Build Pack authoring on any machine after cloning the repo from GitHub.

---

## 1. Project Identity

- **Repository:** Project ATLAS
- **Product Owner:** Anil Kumar (anilkamboj@vardhman.com)
- **Repository Root:** `E:\atlas-project` (Windows) — the folder structure is platform-independent; on any PC the working directory is the cloned repo root.
- **Primary Deliverable Series:** Build Packs BP-000 through BP-012 under `04_Build_Packs/`.
- **Authoritative Roadmap:** `04_Build_Packs/BP-ROADMAP.md` (v1.0.0, Approved).

---

## 2. Current State (as of 2026-07-08)

| BP | Title | Status |
|----|-------|--------|
| BP-000 | Engineering Foundation | Approved |
| BP-001 | Product Foundation | Approved |
| BP-002 | Platform Foundation | Draft (Engineering Review) |
| BP-003 | Identity & Access Platform | Draft (Engineering Review) |
| BP-004 | Tenant & Organization Platform | Draft (Engineering Review) |
| BP-005 | AI Platform | Draft (Engineering Review) |
| BP-006 | Knowledge Platform | Draft (Engineering Review) |
| **BP-007** | **Workflow Platform** | **NEXT — TO AUTHOR** |
| BP-008 | Meeting Intelligence Platform | Planned |
| BP-009 | Decision, Action & SOP Platform | Planned |
| BP-010 | Notification Platform | Planned |
| BP-011 | Integration Platform | Planned |
| BP-012 | Production & Operations Platform | Planned |

**When the user types `BP-007` (or any BP-XXX), begin authoring that Build Pack immediately using the rules in Sections 3–6 below.** Verify current state by listing `04_Build_Packs/` before starting.

---

## 3. BP-007 Authoring Directive

Source: `04_Build_Packs/BP-ROADMAP.md` §5.8.

- **Title (verbatim):** Workflow Platform
- **File Path:** `04_Build_Packs/BP-007_Workflow_Platform.md`
- **Purpose:** Deliver the workflow capability that carries Project structure, project membership, project lifecycle, and project-scoped resources as the shared workflow surface for meetings, decisions, actions, and SOPs, aligned to DOMAIN-003.
- **Primary Reference Architectures:** RA-001 Backend, RA-002 Frontend, RA-006 Event-Driven.
- **Primary Domains:** DOMAIN-003 Project.
- **Depends On:** BP-000, BP-001, BP-002, BP-003, BP-004.
- **Next:** BP-008.

**Upstream sources to read before drafting:**

1. `04_Build_Packs/BP-006_Knowledge_Platform.md` — most recent template exemplar; mirror its structure.
2. `02_Domains/DOMAIN-003_*.md` — primary domain authority.
3. `05_Reference_Architecture/RA-001_*.md`, `RA-002_*.md`, `RA-006_*.md` — capability authority.
4. `00_Master_Context/MC-000*` — repository index.
5. `04_Build_Packs/BP-003`, `BP-004` — dependency inputs (tenant scoping, identity binding).

---

## 4. Mandatory Build Pack Sections (BP-002 onward)

Every Build Pack must include these sections. Omission is a Blocking issue.

1. Build Pack Objectives
2. Platform Capability Map (capabilities → authoritative RA/upstream sources)
3. Platform Context Diagram (MC → ARCH → DOMAIN → ES → RA → BP → IP → Production; current BP layer marked)
4. Service Inventory
5. Implementation Readiness Matrix
6. Traceability Matrix

Use **"Service Inventory"** as the canonical name — never "Required Services".

---

## 5. Mandatory Templates

All templates below apply from BP-002 through BP-012. Any field not explicitly authorized by MC / ARCH / DOMAIN / ES / RA / prior BP shall be recorded as `"Implementation Defined During Engineering"` — never invented.

### 5.1 Service Inventory (11 fields per service)

1. Service Name
2. Source Documents
3. Responsibilities
4. Inputs
5. Outputs
6. Dependencies
7. Consumers
8. Failure Modes
9. Observability Requirements
10. Security Requirements
11. Implementation Status *(initial value: "Implementation Defined During Engineering")*

### 5.2 Required Databases (11 fields per database)

1. Database Name
2. Source Documents
3. Purpose
4. Ownership
5. Data Classification
6. Tenant Isolation
7. Backup Responsibility
8. Retention Policy
9. Encryption Requirements
10. Consumers
11. Implementation Status

### 5.3 Required Events (11 fields per event category)

1. Event Category
2. Source Documents
3. Producer
4. Consumer
5. Purpose
6. Delivery Guarantee
7. Ordering Requirements
8. Retry Strategy
9. Dead Letter Strategy
10. Observability Requirements
11. Implementation Status

### 5.4 Engineering Decisions Register (8 fields per decision)

1. Decision ID
2. Decision
3. Source Documents
4. Rationale *(cite only approved repository documents)*
5. Impact
6. Alternatives Considered *(or "Decision Deferred to Implementation Pack")*
7. Status *(Accepted | Proposed | Deferred | Superseded)*
8. Future ADR Required (Yes/No)

### 5.5 Traceability Matrix (8 columns; one row per BP section)

1. BP Section
2. MC Reference
3. ARCH Reference
4. DOMAIN Reference
5. ES Reference
6. RA Reference
7. BP Reference
8. Verification Method

Use `"n/a"` where a column does not apply.

### 5.6 Implementation Readiness Matrix (9 fields per capability)

Placed immediately before Acceptance Criteria.

1. Capability
2. Primary Build Pack
3. Primary Reference Architecture
4. Implementation Pack(s) *(initial: "Implementation Defined During Engineering")*
5. Primary Owner *(cite the Document Owner from the source RA; never invent)*
6. Implementation Status *(initial: "Implementation Defined During Engineering")*
7. Dependencies
8. Downstream Consumers
9. Notes

---

## 6. Authoring Cadence (BP-003 onward)

- Parts 1 and 2 (typically §§1–7 and §8 Service Inventory) may be presented incrementally to lock scope and vocabulary.
- **From Part 3 onward, draft all remaining sections in a single continuous pass** and write the assembled file to disk. Present a completion summary — do not gate on part-by-part approval.
- **Interrupt authoring only for:**
  - Missing or contradictory RA / DOMAIN / ES / ARCH / MC source
  - An ADR-level decision surfacing mid-draft
  - A mandatory section rule (Section 4 above) that cannot be satisfied
- Do **not** interrupt for stylistic, naming, or organizational refinements — handle those as editorial deltas after the file is assembled.

---

## 7. Document Header Format

Every Build Pack starts with:

```
# Project ATLAS

# Build Pack

## BP-XXX — <Title Verbatim from BP-ROADMAP>

---

# Document Information

| Field | Value |
|--------|--------|
| Document ID | BP-XXX |
| Title | <Title> |
| Version | 1.0.0 |
| Status | Draft (Engineering Review) |
| Repository | Project ATLAS |
| Owner | Anil Kumar |
| Classification | Implementation Specification |
| Depends On | <from BP-ROADMAP> |
| Next | BP-<XXX+1> |
| Last Updated | <YYYY-MM-DD> |
```

---

## 8. Hard Rules

- Titles for BP-003 through BP-012 are **frozen** in BP-ROADMAP.md — use verbatim.
- No invented capabilities, services, dependencies, or owners. Every claim must trace to an approved upstream document.
- No external justification. Rationale cites only MC / ARCH / DOMAIN / ES / RA / prior BP.
- Do not skip mandatory sections on stylistic grounds. Only formal repository governance (an ADR or MC update) may supersede.

---

## 9. Quick-Start Protocol

When user says `BP-007` (or the next BP in sequence):

1. Confirm current state: list `04_Build_Packs/` and read `BP-ROADMAP.md` §5.<n>.
2. Read the primary Domain file, primary RAs, and the most recent completed Build Pack for template shape.
3. Draft Part 1 (§§1–7) and Part 2 (§8 Service Inventory) with brief user confirmation gates.
4. Draft Parts 3+ in one continuous pass; write the file; report the completion summary.
