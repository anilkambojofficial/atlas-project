# Project ATLAS — Repository Change Policy

| Field | Value |
|---|---|
| Document ID | POL-001 |
| Title | Repository Change Policy (post-Baseline-Freeze v1) |
| Status | Effective upon BAS-001 approval |
| Authority | CON-001 (Constitution); this policy operationalizes its §11 (Review), §16 (Evolution), §17 (Non-Negotiables) |
| Owner | Anil Kumar (Product Owner) |

All changes, of every class below, share the invariant floor: stage-gated approval (CON-001 §11.1), Conventional Commits, executed verification, no secrets, no placeholder code, and the Non-Negotiable Rules (CON-001 §17), which no change class — including Emergency — may violate.

## 1. Allowed Changes (normal development)

- New modules/features under an approved IP, following the module recipe (CON-001 §6; CTX-001 §13), inside an approved sprint stage.
- Additive, non-breaking extensions: new endpoints/events/tables/config keys/shared utilities that respect frozen contracts (BAS-001 §Immutability 3).
- Category C/D debt retirement per the AUD-002 register, scheduled in sprint plans.
- Test additions, documentation additions, tooling that doesn't alter runtime behavior.
- Process: stage plan → implementation → executed verification → report → PO approval → commit.

## 2. Breaking Changes

A change is breaking if it alters a frozen contract (envelopes, event fields, ADR-001 conventions 1–6, mixin semantics, config priority, probe semantics) or any published API/event consumed by another component.

- Require: a superseding or amending ADR **before** implementation; a version increment at the contract's granularity (event `.v<n+1>`, API version path, package version); a migration/coexistence plan (old and new versions coexist until consumers migrate — events are never mutated in place, new versions are added); explicit PO approval.
- Prohibited outright: breaking a wire contract silently, editing a published event schema, renaming frozen titles/markers.

## 3. Architecture Changes

Changes to layering, dependency direction, sole-entry-point paths, module boundaries, or the technology stack:

- Require an ADR (Proposed → PO-Accepted) before any code; AUD-style impact note if they touch Category A/B areas; update to CTX-001/CTX-002 in the same delivery.
- The mechanical checks (import-direction greps, import-integrity tests) must remain green and must be extended to cover the changed rule — an architecture change that cannot be mechanically enforced needs an explicit enforcement plan in its ADR.

## 4. ADR Changes

- ADRs are immutable once Accepted: never edited into new meaning. Corrections of typos/links are allowed; changes of substance require a **superseding ADR** with a `Superseded by` back-link (CON-001 §16.2).
- Status transitions (Proposed → Accepted / Rejected / Superseded) are PO-only and recorded in the ADR header and `07_ADRs/README.md` index and REG-001.
- New ADRs are numbered sequentially; batch ADRs (ADR-001 pattern) are permitted for ratifying implemented-convention sets.

## 5. Documentation Changes

- Approved chain documents (MC/ARCH/DOMAIN/ES/RA/BP/IP): PO approval required for any edit; substantive edits also require a version-row entry and, where they change engineering law, an ADR.
- Living operational documents (LOG-*, CTX-*, REG-001, RMB-001, `07_ADRs/README.md`): updated as part of normal stage gates by standing rule — each update listed in the stage report.
- Frozen governance records (AUD-*, CLS-*, BAS-*, MAT-* editions): never edited; corrected or updated only by issuing a successor edition (AUD-003, MAT-002, BAS-002…).
- Known-defect reconciliation (CTX-001 §15.4 items) is a governed editorial batch requiring PO approval — not opportunistic edits.

## 6. Emergency Changes

Definition: active production incident (data integrity, security breach, total outage) requiring immediate action. (Note: until first production deployment, **nothing qualifies** — pre-production urgency uses the normal process, same day if needed.)

- Authorized deviations: implementation may precede full documentation; approval may be verbal/synchronous with written confirmation within 24 h.
- Never authorized: violating Non-Negotiables (tenant isolation, secrets hygiene, audit-event integrity), skipping verification of the fix itself, or leaving the change undocumented — a retroactive record (decision entry + tests + ADR if architectural) is due within one working day, and the debt of any shortcut is registered.

## 7. Hotfix Rules (critical bug fixes against the frozen baseline)

- Scope: minimal diff that corrects the defect — no opportunistic refactoring, no feature smuggling.
- Every hotfix: reproducing regression test in the same commit (CON-001 §9.4); severity + root cause recorded in the active sprint log; AUD register updated if it invalidates or confirms a finding.
- If the defect is in a frozen contract, the fix must preserve wire/schema compatibility or follow §2 (breaking) even under time pressure.

## 8. Migration Rules

- Database: Alembic, forward-only, reviewed; every migration reversible in design (documented `downgrade`) even if rollback is operationally discouraged; no destructive column drops in the same release that stops writing them (expand → migrate → contract).
- Data migrations are separate, idempotent, tenant-scoped steps with progress observability.
- Event consumers must tolerate one version older/newer during rollout windows (§2 coexistence).
- Code relocations use the established shim pattern: compatibility re-export → migrate importers → remove, each step logged (precedent: `core/health.py`).

## 9. Deprecation Rules

- Deprecation is declared (ADR or stage report), aliased/shimmed, telemetry-observable where feasible, and removed only after: all in-repo importers migrated + one full sprint of coexistence, or PO waiver.
- The deprecation register lives in REG-001 (status `Deprecated` entries). Nothing is deleted while any consumer, test, or document references it.

## 10. Versioning Rules

- **Baseline tags:** `baseline-v<major>.<minor>.<patch>-sprint<NNN>` at each sprint close (BAS-001 procedure); baselines are annotated tags, never moved.
- **Packages:** SemVer; backend/frontend `0.x` until Definition of Production Ready is met, `1.0.0` at first production certification.
- **Events:** version-in-name `.v<n>` (ADR-001 #2); additive payload fields do not bump, semantic changes do.
- **APIs:** path-versioned `/api/v<n>`; `v<n+1>` opens only via ADR; two live versions maximum.
- **Documents:** version rows in headers; frozen-record documents version by edition (§5).
- **Lockfiles are the dependency truth**; dependency bumps are normal changes (patch/minor within pinned ranges) or breaking-change process (major bumps of frameworks in BAS-001's table).
