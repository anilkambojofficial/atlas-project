# Project ATLAS — Product Roadmap Baseline (post-Sprint-001)

| Field | Value |
|---|---|
| Document ID | RMB-001 |
| Title | Product Roadmap Baseline at Sprint-001 Closure |
| Status | **Approved** (with CLS-001/BAS-001 under GOV-004, PO, 2026-07-19) |
| Authority note | This document *baselines* the roadmap state; sprint→IP sequencing authority remains IP-000, module authority remains BP-ROADMAP + the corrected mapping (CTX-001 §13). Divergence from IP-000 strict ordering is governed by GOV-004 |
| Legend | ✅ Completed · 🔵 In Progress / Authorized · ⏳ Planned · ⏸ Deferred |
| Date | 2026-07-19 |

## Sprint-001 — Repository Bootstrap (IP-001 Platform Foundation) — ✅ COMPLETED (closed at S1.6)

| Deliverable | Status |
|---|---|
| Repository skeleton; backend foundation (FastAPI, DI, config, logging, errors, health, /api/v1); infrastructure foundation (SQLAlchemy/Alembic/PG/Redis/Kafka/Celery); frontend foundation (Next 15); 12 shared libraries; configuration framework; containerized dev environment | ✅ Completed, verified (evidence: LOG-S001; baseline: BAS-001) |
| Governance apparatus: CTX-001, AUD-001/002, CON-001, MAT-001, ADR-001..007, closure set | ✅ Completed (ratification pending) |
| Kubernetes base manifests (was S1.7) | ⏸ Deferred → Sprint-002 |
| CI/CD pipeline (was S1.8) | ⏸ Deferred → Sprint-002 |
| Testing foundation beyond shared (was S1.9) | ⏸ Deferred → Sprint-002 (gate-bound subset) / Sprint-002+ |
| Sprint review (was S1.10) | Superseded by governance cycle |

## Sprint-002 — Identity & Access (IP-002 / BP-003 / DOMAIN-002) — 🔵 AUTHORIZED (READY WITH CONDITIONS)

**Note:** IP-002 is marked "NEXT — TO AUTHOR" — authoring IP-002 is Sprint-002's first work item, before implementation stages.

| Workstream | Status |
|---|---|
| Author IP-002 (Identity & Access Implementation Pack) | ⏳ First item |
| Identity module (`apps/identity`): users, credentials (Argon2id), JWT + refresh sessions, 3 identity classes, RBAC/ABAC PDP + PEP, identity events, first Alembic migrations | ⏳ Planned |
| **Completion gates (GOV-001, gate register AUD-002):** ADR-002 outbox (before first event producer) · ADR-003 Kafka resilience · ADR-004 auth enforcement · ADR-005 ordered pagination (before first list endpoint) · ADR-006 CORS (at first frontend integration) | ⏳ Gate-bound |
| Inherited deferred scope: K8s manifests (per ADR-004/007, M-12 rule), CI gates, priority test debt (UoW/handler/contract fixtures), httpOnly sessions, auth lockout, deep redaction, version-lock guard | ⏳ Planned within sprint |
| Readiness conditions 1–2: PO ratifies ADR set (+ ADR-006 selection) and CON-001 | 🔵 Pending PO |

## Sprint-003 — Tenant & Organization Platform (IP-003 / BP-004 / DOMAIN-001) — ⏳ PLANNED

Tenant Registry (sole org-identity source), organization lifecycle (11-state), subscription→entitlement with cached enforcement, Tenant Isolation Enforcement Library, storage quotas, org events (`atlas.organization`). Known tripwire: IP-003 "Workspace" entity lacks DOMAIN authority — stop-and-ask on encounter (CTX-001 §13).

## Sprint-004 — AI Platform (IP-004 / BP-005 / DOMAIN-010) — ⏳ PLANNED

AI Gateway as sole LLM entry; model/prompt/agent/tool registries; guardrails (pre+post); HITL approval surfaces; token/cost accounting; provider adapters in infrastructure layer only. Technical precondition from the audit trail: ASGI middleware rewrite (AUD H-5) lands before first streaming endpoint.

## Sprint-005 — Knowledge Platform (IP-005 / BP-006 / DOMAIN-005) — ⏳ PLANNED

Document ingestion pipeline (upload→scan→validate→chunk→embed→index), knowledge repository with all knowledge/vector storage ownership, hybrid permission-filtered search, citation-first retrieval.

## Sprint-006 → Sprint-011 — ⏳ PLANNED (per IP-000 sequence; titles per corrected mapping CTX-001 §13)

Workflow (IP-006 — ⚠ BP-007 scope ruling required first) → Meeting Intelligence (IP-007) → Decision & SOP (IP-008) → Notification (IP-009) → Integration (IP-010) → Production Operations (IP-011 — **must be authored**; production certification sprint against CON-001 §15).

## Future Vision (MC-003 phases — unchanged by this baseline)

- **Phase 1 (MVP):** Sprints 002–011 scope — multi-tenant orgs, identity, projects, meetings + transcription, AI summaries, decision/SOP/action intelligence, knowledge repository, search, reporting.
- **Phase 2:** Enterprise Knowledge Graph, cross-project intelligence, recommendations, workflow automation.
- **Phase 3:** Governed autonomous agents, predictive organizational intelligence.
- **Phase 4:** Ecosystem — ERP/CRM/HRMS connectors, marketplace, public APIs.
- **Explicitly ungoverned (no code without new governance):** Billing execution (excluded by BP-004; CON-001 §6.6).

## Standing roadmap risks

Gate discipline is the roadmap's single critical dependency (MAT-001 closing note); documentation reconciliation must precede its tripwire sprints (BP-007 before IP-006 work, off-by-one region before Sprint-008 planning); IP-011 authoring must precede Sprint-011 planning.
