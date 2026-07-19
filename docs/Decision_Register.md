# Project ATLAS — Decision Register

| Field | Value |
|---|---|
| Document ID | REG-001 |
| Title | Master Decision Register |
| Status | Living document — the master index of all architectural, engineering, and governance decisions from Sprint-001 onward |
| Maintenance | Appended at every stage gate that produces a decision (POL-001 §5); rows are never deleted, only status-updated |
| ID scheme | `D-SXXX-nn` sprint-scoped implementation decisions · `ADR-nnn[.k]` architecture decision records · `GOV-nnn` Product Owner governance rulings · `ENG-nnn` engineering interpretation decisions |

Statuses: **Accepted** (in force) · **Proposed** (awaiting PO ratification) · **Discharged** (obligation fulfilled, evidence recorded) · **Deferred** (owned, scheduled) · **Superseded** (replaced — pointer required).

---

## Governance Decisions (Product Owner)

| ID | Decision | Reason | Impact | Related ADR | Related Documents | Status |
|---|---|---|---|---|---|---|
| GOV-001 | Sprint-002 may begin; Outbox, Kafka resilience, auth enforcement, ordered pagination, CORS strategy are **Sprint-002 completion gates** (not entry gates) | Identity work need not idle behind platform hardening; gates close before first real producers/consumers exist | Defines the Sprint-002 exit bar; supersedes AUD-001's entry-gate recommendation | ADR-002..006 | AUD-002; CLS-001 §6 | Accepted (2026-07-19) |
| GOV-002 | Recognized production blockers: post-commit event loss; Kafka resilience; anonymous production business endpoints | Data-integrity and Zero-Trust failures cannot be remediated after the fact | Category A register; Definition of Production Ready §15 items | ADR-002/003/004 | AUD-002; CON-001 §15 | Accepted (2026-07-19) |
| GOV-003 | Health-probe optimization, expanded testing, frontend coverage are implementation improvements, not architecture failures | The abstractions are correctly shaped; the gaps are internal to them | Reclassified AUD H-3/H-4 to Category C/D | ADR-007 | AUD-002 | Accepted (2026-07-19) |
| GOV-004 | Sprint-001 is closed at S1.6; S1.7–S1.10 deferred to Sprint-002 ownership (S1.10 superseded by the governance cycle); Sprint-001 becomes the frozen baseline `baseline-v1.0.0-sprint001` | Foundation objective met; remaining stages benefit from ADR ratification preceding them | Baseline freeze; roadmap re-baseline; overlap supersedes IP-000 strict ordering | — | CLS-001; BAS-001; RMB-001 | **Accepted** (PO, 2026-07-19) — Sprint-001 CLOSED, baseline FROZEN; tag hash recorded below upon freeze execution |
| GOV-005 | Adoption of the 15 AI Development Rules + shared framework-independence rule for all implementation work | Bind AI-assisted development to traceability, verification, and stop-on-conflict discipline | Now constitutionalized | ADR-001 #12 | CON-001 §12; CTX-001 | Accepted (2026-07-18) |

## Sprint-001 Implementation Decisions

| ID | Decision | Reason | Impact | Related ADR | Related Documents | Status |
|---|---|---|---|---|---|---|
| D-S001-01 | Live PG/Redis/Kafka connectivity verification deferred from S1.2B to S1.6, with explicit discharge criteria | No container/runtime environment existed pre-S1.6; installing ahead of the governed stage would pre-empt scope | Model for all future deferrals (criteria + evidence + discharge) | — | LOG-S001 (full lifecycle + evidence) | **Discharged** (2026-07-19, S1.6) |
| ENG-001 | S1.4 interpretation set: monitoring=health vs telemetry=metrics; `shared/auth` interfaces-only; relocations via compatibility shims; pytest as dev dependency | IP-001 §9 package list required interpretation; PO approved the readings | Shaped the 12-package shared layout | ADR-001 #8/#12 | LOG-S001 S1.4 row; CTX-001 §6.3 | Accepted |
| ENG-002 | S1.6 set: dev-only single-node KRaft; dual Kafka listeners; Nginx deferred to ingress; image pins (postgres:17-alpine, redis:7-alpine, kafka:3.9.1, python:3.13-slim, node:22-alpine) | Dev-environment fidelity with production-shaped images without pre-empting S1.7 ingress design | Compose environment contract | — | LOG-S001 S1.6 row; BAS-001 | Accepted |
| ENG-003 | Health endpoints unenveloped; `/live` process-only; module checks via registry | Probe-tooling convention over ES-002 envelopes for operational surfaces | Now ratified as probe law | ADR-007 | AUD-002 | Accepted (ADR-007 ratified 2026-07-19) |

## Architecture Decision Records (see `07_ADRs/README.md` for the authoritative index)

| ID | Decision (compressed) | Reason | Impact | Related Documents | Status |
|---|---|---|---|---|---|
| ADR-001.1–.12 | Sprint-001 convention batch: `atlas.<domain>` topics; version-from-name; payloadSchema default; camelCase wire; tenant-stamping scope; org-ID keys; outbox schema; auth contract signatures; error→HTTP map; snake_case deviation; single env enumeration; shared framework-independence | Documentation deliberately deferred these; implementation required decisions; audit required their ratification | Binding conventions for every future module; items 1–6 are breaking-change-controlled | CTX-001 §6.4; AUD-002 | **Accepted** (PO, 2026-07-19) |
| ADR-002 | Transactional outbox in-transaction + Celery drain worker; typed `collect_event`; worker structured logging bundled | Post-commit publish has an unrecoverable loss window (AUD C-1) | **Sprint-002 completion gate**; retires Category A item C-1 | AUD-001/002; RA-006 §10 | **Accepted** (PO, 2026-07-19) |
| ADR-003 | Supervised Kafka producer re-establishment with backoff; error classification; readiness trip | Startup-connect failure is permanent today (AUD C-2, scope-corrected) | **Sprint-002 completion gate**; retires C-2 | AUD-002 | **Accepted** (PO, 2026-07-19) |
| ADR-004 | Deny-by-default auth at `/api/v1`; fail-closed; docs/metrics gating; gateway-owned rate limits + app-level lockout | Zero Trust (BP-003); anonymous production endpoints are a recognized blocker (GOV-002) | **Sprint-002 completion gate**; retires C-3/M-7 | AUD-002; CON-001 §10 | **Accepted** (PO, 2026-07-19) |
| ADR-005 | PK-ordered lists (UUID v7); keyset pagination standard; bounded OFFSET convenience | Unordered LIMIT/OFFSET is nondeterministic; OFFSET is linear-cost (AUD H-1) | **Sprint-002 completion gate** — before first list endpoint | AUD-002 | **Accepted** (PO, 2026-07-19) |
| ADR-006 | CORS permanent standard (Option 1 approved): production same-origin only (no CORS headers); development allowlisted origins only; **wildcards prohibited in all environments** | No policy existed; first browser integration is Sprint-002 (AUD H-2); PO selected Option 1 | **Sprint-002 completion gate** (implementation); policy decision closed | AUD-002 | **Accepted** (PO, 2026-07-19) |
| ADR-007 | Probe semantics ratified (`/live` process-only; `/ready` gating; `/health` diagnostic; `/metrics` internal); gather+TTL optimization guidance non-blocking | Implemented-but-undocumented semantics; GOV-003 reclassification | Law for S1.7-equivalent manifests | AUD-002 | **Accepted** (PO, 2026-07-19) |

## Standing Obligations Index (decisions that create future duties)

| Obligation | Source | Owner / due |
|---|---|---|
| ~~Ratify ADR-001..007 + CON-001~~ — **COMPLETE 2026-07-19**: CON-001 ratified; all seven ADRs Accepted (ADR-006 with CORS option selection). Sprint-002 readiness conditions 1–2 discharged | This governance cycle | Discharged |
| Five completion gates closed before Sprint-002 declared complete | GOV-001 | Sprint-002 plan |
| sessionStorage token placeholder retired (httpOnly sessions) | AUD M-5 / ADR-004 | Sprint-002 |
| Deferred S1.7/S1.8/S1.9 scope delivered | GOV-004 | Sprint-002(+) stages |
| IP-011 authored; documentation reconciliation batch; ES-001 §7 editorial; MC-000 refresh | CLS-001 §3 | Governance backlog (before Sprint-008 planning; BP-007 ruling before IP-006-adjacent work) |
| Independent human review before production | CON-001 §11.4 | Production Ready path |
| AUD-003 + MAT-002 refresh | CON-001 §16.4 | ≤ Sprint-002 close |
