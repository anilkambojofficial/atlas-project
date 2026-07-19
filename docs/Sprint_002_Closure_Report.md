# Project ATLAS — Sprint-002 Closure Report

| Field | Value |
|---|---|
| Document ID | CLS-002 |
| Title | Sprint-002 "Identity & Access" — Engineering Closure |
| Status | Closure Pending Product Owner Approval |
| Review posture | Adversarial self-review with mechanical verification (author-bias disclosed; independent human review remains required pre-production, CON-001 §11.4) |
| Date | 2026-07-19 |

## 1. Completed (evidence per item in LOG-S002)

All five GOV-001 completion gates (ADR-002/003/004/005/006) closed and live-verified · identity backend (7 tables, migrations 0001–0002 applied first-attempt, Argon2id, JWT, rotation + theft response, lockout, PDP/PEP, atomic audit + outbox events) · ADR-004 deny-by-default live at `/api/v1` · frontend authentication (in-memory token, httpOnly refresh cookie, guards, login/profile) · 128 unit tests · one live-verification defect found and fixed with regression tests (fail-secure commits, `b74cf40`).

## 2. Acceptance-Criteria Verification (executed, not assumed)

| Criterion | Evidence |
|---|---|
| Authentication works | Live curl transcript: register 201 / duplicate 409 / wrong-pw 401 / login 200 (owner, 7 perms) / me 200 |
| Authorization works | PDP deny-default + cross-tenant tests; PEP 403→200 over real ASGI app (`test_enforcement.py`) |
| JWT | Round-trip, tamper, expiry, wrong-secret, wrong-issuer tests; ≥32-byte key enforced |
| Refresh + rotation | Live: rotate 200 → replay 401 → **family survivor 401** (post-fix) |
| Protected routes | Anonymous `/users/me` 401; frontend 307 guards + marker path verified |
| Permissions operational | Seeded roles; permissions in token; PEP verified |
| Migrations | `alembic upgrade head` → 0001, 0002 on live PG, first attempt |
| Frontend auth operational | Login page 200 with form, root/dashboard redirects, `/api/health` 200; `tsc --noEmit` clean; build 8/8 |
| Tests passing | **128 passed** (re-verified at closure via `python -m pytest`); zero removed |
| Architecture validation | Mechanical: `shared→outer` 0, `core→apps` 0, `infra→core/api/apps` 0, no web-storage tokens (0 hits), no secrets in code — one deviation, finding M-1 |

**Coverage:** shared 98.54% vs ≥95% enforced gate (delta from 99.08% = new settings validators; gate green). Identity module covered by 34 behavior tests; not yet under a numeric gate (M-6).

## 3. Independent-Review Findings

**Critical: none. High: none.** (Explicit statement per mandate.)

**Process — P-1:** a complete IP-002 specification (2026-07-08, 849 lines) existed but was believed unauthored; the sprint was executed solely against the Product Owner directive without loading it. No scope conflict resulted (the directive is a strict subset), and conformance was assessed at closure (IP-002 §31 addendum) — but the context-verification step failed and ENG-005 was recorded on a false premise (now corrected, REG-001). Root cause: stale "NEXT — TO AUTHOR" state in CLAUDE.md §2 trusted over a directory listing.

**Medium:**
- **M-1** `apps/identity/api.py:14` imports `api.v1.security` — `apps→api` is absent from CON-001 §4's allowed edges. Intra-presentation and cycle-free in practice, but a rule deviation. Fix: bind the verifier into the container at composition and move `get_current_principal`/`require_permission` into `core/`, or amend CON-001 §4 by ADR. Owner: Sprint-003 entry.
- **M-2** `PasswordService._all_user_sessions` runs an inline `select` on the UoW session — bypasses the repository layer (CON-001 anti-pattern). Fix: `SessionRepository.revoke_all_for_user`. Owner: Sprint-003.
- **M-3** Logout/lockout do not invalidate outstanding access JWTs (≤15-min exposure; stateless verify ignores `sid`). Diverges from IP-002 §14 "immediately invalidate" — ratified as divergence D-3 with the ED-005 Redis denylist as planned closure.
- **M-4** Concurrent refresh of one token: no row lock → optimistic-lock 500, and a client retry after a successful rotation triggers a false theft-positive (family logout). Fix: `FOR UPDATE` on session fetch + small reuse grace. Owner: Sprint-003 hardening.
- **M-5** Unknown-email login performs hash+verify (2 Argon2 ops) vs 1 for wrong-password — timing can distinguish account existence. Fix: single pre-computed dummy verify. Owner: Sprint-003.
- **M-6** No PostgreSQL-backed integration tests (fakes only) and no session/token cleanup worker (IP-002 §17) — unbounded table growth. Owner: testing-foundation stage / Sprint-003.

**Low:** L-1 IP-002 §9 divergences ratified as D-1/D-2/D-4 (JSONB permissions, merged session table, `identity_` prefix) · L-2 unverified-email users may log in (product decision recorded; flag-gated delivery pending Notification platform) · L-3 marker cookie fixed 30-day Max-Age · L-4 inline import in `api.refresh` · L-5 `created_by` unset on self-registration · L-6 drain worker starts/stops producer per run · L-7 no `expires_at` index on sessions · L-8 dev-machine single-process build (ENG-006) must not mask CI type/lint gates when S1.8-deferred CI lands.

## 4. Deferred (scope, not defects)

IP-002 §31.3 list: OIDC/OAuth2, MFA, API keys/service accounts (machine/agent classes), admin APIs (roles/permissions/sessions/audit), Redis session cache/denylist, password history, ABAC, cleanup worker, org switching. Plus inherited Sprint-001 deferrals (K8s, CI, test pyramid) per GOV-004.

## 5. Technical Debt & Risks

Debt: M-1..M-6, L-items above — all owner-assigned. Risks accepted: 15-minute access-token exposure window (M-3; short TTL mitigates); single-approver + AI-self-review (standing; CON-001 §11.4 gate holds); dev-machine memory ceiling (7.7 GB) distorting local builds (ENG-006); Application Control now blocks `.exe` shims in the venv (`python -m` path verified as the workaround — environment risk to watch).

## 6. Commits & Records

`eb21ff9` gates → `2dd3c6f` identity backend → `b74cf40` fail-secure fix → `a3cf263` frontend → `3f8249b` records → (this closure commit: IP-002 §31 addendum, CLS-002, record corrections). Records updated: LOG-S002, REG-001 (ENG-005 corrected + obligation discharged), CTX-002, MAN-001.

## 7. Next-Sprint Recommendations

1. Sprint-003 entry items: M-1 (enforcement relocation or CON-001 §4 ADR), M-2, M-4, M-5 — small, sharp fixes before Tenant work builds on identity.
2. Deliver the inherited platform stages (K8s per ADR-004/007, CI with type/lint/test/coverage gates, PG-backed integration harness) before or alongside IP-003.
3. IP-003 (Tenant) consumes `identity_organizations` as the registry seed — reconcile with BP-004's Tenant Registry ownership at planning; Workspace-entity tripwire remains (CTX-001 §13).
4. ED-005 Redis session cache/denylist closes M-3 naturally during IP-003's cache adoption.
5. Correct CLAUDE.md §2's stale IP status table (it caused P-1).

## 8. Freeze Recommendation

**READY TO FREEZE.** Zero Critical/High findings; every acceptance criterion evidenced by executed verification; all five completion gates closed; divergences ratified in IP-002 §31; all debt owner-assigned. The Mediums are hardening items that do not compromise the frozen surface's correctness for development use (production deployment remains separately gated by CON-001 §15, unchanged).
