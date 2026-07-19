# Project ATLAS — Sprint-002 Execution Log

| Field | Value |
|---|---|
| Document ID | LOG-S002 |
| Title | Sprint-002 Execution Log (Identity & Access) |
| Governing authority | Product Owner Sprint-002 directive of 2026-07-19 (inline scope — see ENG-005), BP-003, DOMAIN-002, CON-001, ADR-001..007 |
| Baseline | Continues from `baseline-v1.0.0-sprint001` |
| Owner | Anil Kumar |

## Stage Status

| Stage | Scope | Status | Verification |
|---|---|---|---|
| S2-01 | Platform completion gates: ADR-002 transactional outbox (UoW in-transaction staging, typed `collect_event`, Celery-beat drain worker with SKIP LOCKED + capped backoff + retry-budget escalation, migration 0001, worker JSON logging), ADR-003 Kafka supervised reconnection + error classification, ADR-005 PK-ordered `list()` + keyset `list_after()`, ADR-006 CORS (config allowlist, wildcards rejected, production same-origin validated), ADR-004 surface gating (docs off in production; ≥32-byte JWT secret enforced) | ✅ commit `eb21ff9` | 94 unit tests (8 new); validators exercised |
| S2-02/03 | Identity backend: 7 tables + migration 0002; Argon2id; JWT `TokenVerifier`; registration (+org bootstrap, seeded owner/admin/member roles); login w/ lockout + enumeration resistance; refresh rotation w/ family-revocation theft response; logout; profile; password-reset + email-verification frameworks (delivery feature-flagged off); PDP deny-by-default; ADR-004 deny-by-default mount gate + `public_endpoint` marker + `require_permission` PEP; httpOnly refresh cookie (M-5 closed); atomic audit rows + outbox events | ✅ commit `2dd3c6f` | 125 unit tests (31 new incl. real-ASGI 401/403/200 gate tests) |
| S2-04 | Live verification + defect fix | ✅ commit `b74cf40` | Migrations 0001+0002 applied to live PG first attempt. Full flow verified: anonymous 401 → register 201 → duplicate 409 → wrong-password 401 → login 200 (owner, 7 perms, httpOnly cookie) → `/users/me` 200 → rotation 200 → replay 401 → family survivor 401 → lockout persists and blocks correct password → logout idempotent. **Defect found & fixed:** UoW exception path rolled back theft-response revocation and lockout counters; services now commit security state before rejecting (regression tests added). Outbox: 9 events / 6 types staged by real use cases, drained 9/9 to Kafka, 0 pending |
| S2-05 | Frontend auth: in-memory access token (sessionStorage tokens removed), `withCredentials` client, auth store (login/logout/silent bootstrap/permissions), AuthProvider proactive rotation at 80% TTL, marker-cookie middleware layer, RHF+Zod login form with redirect handling, RouteGuard, dashboard user menu + sign-out, profile page | ✅ commit `a3cf263` | `tsc --noEmit` clean; production build 8/8 routes; live: login page 200 w/ form, `/` 307→login, `/dashboard` 307 w/ redirect param, marker path 200, `/api/health` 200; ADR-006 preflight: allowlisted origin echoed w/ credentials, foreign origin gets no CORS headers |
| S2-06 | Records + closure | ✅ this commit | This log; REG-001 ENG-004/005; CTX-002 refresh |

## Gate Register (GOV-001) — Sprint-002 completion gates

| Gate | Status |
|---|---|
| ADR-002 Transactional Outbox | ✅ Implemented, tested, live-verified (9/9 drained) |
| ADR-003 Kafka reliability | ✅ Implemented (supervised backoff, classification, readiness trip) |
| ADR-004 Production auth enforcement | ✅ Deny-by-default live at `/api/v1`; docs gated; fail closed |
| ADR-005 Ordered pagination | ✅ In repository base before first list endpoint |
| ADR-006 CORS | ✅ Live-verified allowlist + same-origin production validation |

## Decisions

- **ENG-004 — Identity tenancy layout:** `identity_users`/`identity_organizations` are platform-scoped aggregates (authentication is platform-wide, BP-003); tenancy binds via `identity_memberships`/`identity_roles` (org-scoped per ES-003 §9); sessions bind ≤1 active tenant. Recorded in REG-001.
- **ENG-005 — Sprint-002 scope authority:** IP-002 was unauthored at sprint start; the Product Owner's Sprint-002 directive (2026-07-19) is the interim scope authority. **Authoring the IP-002 document from the as-built state remains an open obligation.** Recorded in REG-001.
- **ENG-006 — Dev-machine build constraint:** Next.js build runs single-process with type/lint as dedicated standalone gates (`tsc --noEmit` clean); in-build duplicate phase OOMs on the 7.7 GB dev machine. S1.8-deferred CI must enforce type+lint as blocking checks.

## Known follow-ups (carried, not blocking)

Author IP-002 from as-built (ENG-005) · deferred Sprint-001 stages (K8s, CI, wider test pyramid) remain owned by this sprint's continuation per GOV-004 · email delivery integration (feature flag `identity_email_delivery`) awaits the Notification platform · org-switching endpoint (multi-membership) deferred to IP-003 · drain-worker/beat live soak under `full` compose profile.

## Version History

| Date | Entry |
|---|---|
| 2026-07-19 | Sprint-002 identity implementation: S2-01..S2-06 complete; all five GOV-001 completion gates closed; commits `eb21ff9`, `2dd3c6f`, `b74cf40`, `a3cf263` + this records commit |
