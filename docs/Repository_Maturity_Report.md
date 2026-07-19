# Project ATLAS — Repository Maturity Report

| Field | Value |
|---|---|
| Document ID | MAT-001 |
| Title | Engineering Maturity Report (pre-Sprint-002 baseline) |
| Date / Basis | 2026-07-19 · End of Sprint-001 (S1.1–S1.6); AUD-001/AUD-002 evidence; full repository review |
| Scoring stance | Conservative. Scores rate **what exists and is verified today**, not what is planned or documented as future intent. A pre-production foundation is *expected* to score low in operational areas — low scores below are sequencing facts, not indictments, except where noted |
| Refresh cadence | With each AUD-series review (Constitution §16.4) |

**Score summary**

| Area | Score | Target (Sprint-004 horizon) |
|---|---|---|
| Architecture | **8.5** | 9 |
| Scalability | **5** | 8 |
| Security | **4** | 8.5 |
| Reliability | **4** | 8.5 |
| Maintainability | **8.5** | 9 |
| Observability | **6.5** | 8.5 |
| Documentation | **9** | 9.5 |
| Testing | **4.5** | 8 |
| Deployment | **5** | 8 |
| AI Readiness | **9** | 9.5 |
| Developer Experience | **7** | 8.5 |
| Repository Governance | **8.5** | 9.5 |
| **Unweighted mean** | **6.6** | **8.7** |

---

## 1. Architecture — 8.5 / 10

- **Current state:** Clean Architecture + DDD skeleton with mechanically verified layer purity; DI via a single composition root; six Protocol seams ahead of need; sole-entry-point mandates encoded; event/envelope/error/config vocabularies single-sourced.
- **Evidence:** 0 forbidden imports (`shared→core/api/infrastructure`, `infrastructure→core/api` — grep-verified twice, AUD-001/AUD-002); 30-module import-integrity test; `core/container.py` structural Protocol binding; AUD-002 strengths §1–§3, §8.
- **Risks:** the architecture is unexercised by real business modules — Identity (Sprint-002) is the first stress test of the `apps/` pattern; `BaseHTTPMiddleware` (AUD H-5) is a known hot-path liability for future streaming.
- **Improvement plan:** implement Identity strictly on the documented module recipe (CTX-001 §13) and feed deviations back as ADRs; ASGI middleware rewrite before IP-004.
- **Why not higher:** unproven under a real module; two compatibility shims outstanding; H-5 pending.

## 2. Scalability — 5 / 10

- **Current state:** design-level scalability is strong (stateless pods, UUID v7 keys, per-tenant partition keying, async I/O); operational scalability is absent (no ordered/keyset pagination, no connection budget, no topic provisioning, no load evidence).
- **Evidence:** AUD-001 §6 ordered break-list; `repositories/base.py` 0 `order_by`; pool defaults 5+10; no declarative Kafka topic management; single Celery queue.
- **Risks:** the break order is known: event divergence → connection exhaustion → probe load → OFFSET depth. None is exotic; all are cheap now, expensive later.
- **Improvement plan:** ADR-005 (Sprint-002 gate); connection-budget math + statement timeout in S1.7 values; topic provisioning in S1.7/IP-011; first load test in S1.9/S1.10.
- **Why 5, not lower:** the expensive-to-retrofit half (statelessness, key design, tenancy affinity) is already right; what's missing is configuration and process, not redesign.

## 3. Security — 4 / 10

- **Current state:** excellent primitives (taxonomy'd redaction, secret-provider chain, production config guards, non-root containers, parameterized-only data access, identity-class contracts) with **no authentication or authorization anywhere** — sanctioned pre-IP-002 scaffolding.
- **Evidence:** `shared/security`, `shared/config` validators, Dockerfiles (uid 10001/node), AUD C-3/M-5/M-7 (docs unconditional at `application.py:83`; sessionStorage placeholder; anonymous `/metrics`); no SAST/dependency scanning yet (S1.8).
- **Risks:** the score is structural until IP-002; the specific hazard is *schedule slip* — every sprint that adds surface before ADR-004 enforcement widens exposure.
- **Improvement plan:** ADR-004 enforcement + httpOnly sessions + lockout in Sprint-002; scanning gates in S1.8; vault provider + independent security review on the Production Ready path (Constitution §15).
- **Why 4, not lower:** fail-closed design intent is already encoded in contracts and constitution; primitives mean IP-002 assembles rather than invents.

## 4. Reliability — 4 / 10

- **Current state:** graceful degradation verified (S1.2B failure paths, S1.6 green paths); but the event pipeline has an unrecoverable loss window and a non-healing producer, and no retry/backoff/alerting exists anywhere.
- **Evidence:** AUD C-1 (`unit_of_work.py:73`; outbox model unwired), C-2 as re-scoped in AUD-002 (startup-connect failure is permanent); no alerting; single-node dev Kafka (sanctioned).
- **Risks:** the two Category A items concentrate here; both are latent (zero business events exist) but Sprint-002 arms them.
- **Improvement plan:** ADR-002 + ADR-003 (Sprint-002 gates) with tests-in-same-commit; outbox-age alerting as Production Ready requirement; DR/backup posture via IP-011.
- **Why 4:** reliability is the report's weakest *architecture-adjacent* area and the reason the governance review exists; honesty demands the low score even though fixes are fully designed.

## 5. Maintainability — 8.5 / 10

- **Current state:** single-sourced vocabularies, citation-bearing docstrings, framework-free shared core at 99% coverage, deterministic conventions, small composition root, compatibility-shim deprecation discipline.
- **Evidence:** 12 shared packages; `shared/constants` as single literal source; docstring citations throughout ("IP-001 §14" pattern); AUD-002 strengths §3; both historical defects were drift *prevented from recurring* by centralization + planned contract fixtures.
- **Risks:** maintainability outside `shared/` is asserted, not test-protected (H-4) until S1.9; shims linger.
- **Improvement plan:** S1.9 test expansion per AUD priorities; retire shims by Sprint-002 close (Constitution §16.5).

## 6. Observability — 6.5 / 10

- **Current state:** structured JSON logs with correlation/tenant fields, TRACE level, request middleware logging, Prometheus metrics with bounded label cardinality, four-endpoint health model with truthful readiness.
- **Evidence:** `shared/logging`, `shared/telemetry`, ADR-007 semantics verified in S1.2B (failure) and S1.6 (green); correlation echo verified.
- **Risks:** no distributed tracing (deliberately deferred), no alerting, Celery workers log unstructured (M-3), double request logging (M-4), shallow redaction depth (M-2), no log pipeline/retention decisions.
- **Improvement plan:** M-3 with ADR-002 delivery; M-2/M-4 per AUD schedule; tracing + alerting + dashboards via S1.7/IP-011.
- **Why 6.5:** unusually strong for a foundation sprint, but observability is only real once something alerts a human — nothing does yet.

## 7. Documentation — 9 / 10

- **Current state:** 68-document governed chain with explicit precedence; sprint execution log with decision IDs and discharge evidence; CTX-001 onboarding pack; AUD/ADR/CON/MAT governance set produced pre-Sprint-002; honest defect and deferral records.
- **Evidence:** the chain itself; LOG-S001 D-S001-01 lifecycle (recorded → discharged with evidence); CTX-001 §15.4 documenting the repo's *own* documentation defects; 7 ADRs now covering the undocumented-decision register.
- **Risks:** known cross-reference defects (BP↔IP off-by-one, BP-007 scope conflict, stale MC-000) are documented-but-unfixed; IP-011 unauthored; documentation volume itself is a consistency liability as layers multiply.
- **Improvement plan:** editorial reconciliation batch (needs PO approval — flagged since the consistency audit); author IP-011 before Sprint-011 planning; MC-000 refresh.
- **Why not 10:** a 10 requires the chain to be internally contradiction-free; it currently is not (documented in CTX-001 §15.4).

## 8. Testing — 4.5 / 10

- **Current state:** exemplary depth on `shared/` (86 tests, 99.08% vs ≥95% gate, deterministic, fake-based); zero automated tests for `core/`, `api/`, `infrastructure/`, `workers/`, and the entire frontend; no integration/E2E/contract/load layers.
- **Evidence:** `find tests` results (AUD-verified: 0 non-shared backend tests; 0 frontend test files); the two historical defects both occurred in untested layers.
- **Risks:** the untested code is precisely the risk-bearing code (UoW, middleware exception path, envelope handlers, ES-002 client); reclassified as implementation improvement per Governance Decision 3, but outbox tests are non-deferrable (bound to ADR-002).
- **Improvement plan:** ADR-002/003 tests in Sprint-002 (gate-bound); S1.9 delivers the pyramid: UoW/middleware/handler units, TestClient envelope tests, FE↔BE golden contract fixtures, frontend Vitest+Playwright, isolation-test harness ahead of Identity data.
- **Why 4.5:** average of a 9 (shared) and near-0 (everything else), weighted toward risk location.

## 9. Deployment — 5 / 10

- **Current state:** production-shaped containerization verified end-to-end (multi-stage, non-root, healthchecked images; profiled Compose; one-command scripts; standalone Next build); nothing beyond a developer laptop — no Kubernetes, no CI/CD, no environments.
- **Evidence:** S1.6 verification (6 containers healthy first attempt; 13/13 checks); `deployment/compose/`; absent `.github/workflows`; S1.7/S1.8 planned.
- **Risks:** manifests will bake in security/probe/credential posture — S1.7 must consume ADR-004/007 and the M-12 rule or the debt compounds; image ships `tests/` (M-14).
- **Improvement plan:** S1.7 manifests per ADRs; S1.8 CI with the full gate set; IP-011 for production operations doctrine.
- **Why 5:** the hard container groundwork is done and verified; everything environment-shaped is absent by schedule.

## 10. AI Readiness — 9 / 10

- **Current state:** the repository is explicitly engineered for cross-model continuation: CTX-001 (invariants, corrected mappings, trap list, session protocol), Constitution §12 (AI rules), deterministic conventions that make generated code converge, memory/log discipline, citation-bearing code.
- **Evidence:** CTX-001; CON-001 §12; this governance cycle itself — executed by an AI under the documented protocol, producing evidence-cited, self-challenging review artifacts (AUD-001 → AUD-002 revision trail).
- **Risks:** context documents can drift from code if the sprint-close refresh discipline lapses; AI self-review has inherent author-bias limits (mitigated by Constitution §11.4 independent-human requirement).
- **Improvement plan:** maintain refresh cadence; add CI check that CTX-001/ADR index reference existing files; first cross-model handoff (e.g., a Codex/GPT session) as a live validation exercise.

## 11. Developer Experience — 7 / 10

- **Current state:** one-command environment (`dev-up.sh`), pinned toolchains (uv, corepack/pnpm), hierarchical config with local overrides, fast test suite, honest docs of Windows quirks.
- **Evidence:** S1.6 first-attempt green environment; `scripts/`; `.npmrc`/`packageManager` pins; CTX-001 §19 known-mistakes list.
- **Risks:** no CI feedback loop (all verification manual); Windows PATH friction documented but unautomated; no pre-commit hooks; onboarding depends on reading discipline.
- **Improvement plan:** S1.8 CI + pre-commit (lint/type/test on changed scope); a `make`/task-runner façade for common flows; devcontainer definition as an option.

## 12. Repository Governance — 8.5 / 10

- **Current state:** layered authority with precedence law; stage-gated execution with recorded approvals; decision registry with IDs and discharge criteria; adversarial audit + re-validation cycle; from this review: a Constitution, 7 ADRs, and classification machinery (A–D categories, gate registers).
- **Evidence:** LOG-S001; D-S001-01 lifecycle; AUD-001→AUD-002 challenge trail; CON-001; `07_ADRs/` populated after being an empty required directory since inception.
- **Risks:** governance artifacts await PO ratification (all Proposed); the process depends on a single approver (bus factor — acceptable at current team size, noted); documentation-fix backlog needs a governance slot.
- **Improvement plan:** ratification of CON-001 + ADR-001..007 (Sprint-002 readiness condition 1–2); recurring audit cadence per Constitution §16.4; editorial reconciliation batch scheduled.
- **Why not higher:** governance that hasn't been ratified or survived a second sprint is still provisional by its own standards.

---

## Reading the scores together

The profile is deliberately lopsided: **structure, documentation, governance, and AI-continuity score 8.5–9; operations, security, reliability, and testing score 4–5.** That is the correct shape for a foundation-sprint repository — the high-scoring areas are the ones that are prohibitively expensive to retrofit, and the low-scoring areas all have designed, scheduled, gate-bound remediations (ADR-002..006, S1.7–S1.9, IP-002). The governance risk to watch is singular: **the low scores rise only if the Sprint-002 completion gates hold.** If gate discipline slips, the platform accumulates business features on top of a 4-scored reliability core — the one trajectory this report exists to prevent.
