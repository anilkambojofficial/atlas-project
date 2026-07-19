# ADR-006 — CORS Strategy

| Field | Value |
|---|---|
| Status | **Accepted — Approved by Product Owner (Anil Kumar), 2026-07-19** (Option 1 selected); implementation remains a **Sprint-002 completion gate** (Governance Decision 1, 2026-07-19) |
| Date | 2026-07-19 |
| Deciders | Product Owner (Anil Kumar); analysis by pre-Sprint-002 governance review |
| Source | ARCH-005 (gateway direction), ES-002/ES-004, AUD-001 H-2, AUD-002 |

## Context

No CORS middleware exists; no CORS policy is recorded anywhere in the documentation chain. In local development the frontend (`:3000`) calls the backend (`:8000`) cross-origin — the first real browser call (Sprint-002 login) will be blocked. In deployed environments the topology is undecided: if frontend and API share an origin behind the gateway/ingress, production needs no CORS at all. AUD-001/AUD-002 classify this as a decision gap, not a code defect; per the no-invention rule the policy requires a Product Owner selection.

## Decision (Approved — permanent repository standard)

Per Product Owner approval of 2026-07-19, the permanent CORS policy is:

- **Production: Same-Origin Only** — no CORS headers are emitted in production.
- **Development: Allowlisted Origins** — explicit, config-driven origin list only.
- **Wildcards: Not Allowed** — wildcard origins are prohibited in every environment, unconditionally (not merely when credentials are enabled).

**Option 1 — Same-origin production, allowlisted development (APPROVED):**

1. Deployed environments serve frontend and API from one origin via the gateway/ingress (`/` → frontend, `/api` → backend). Production ships **no CORS headers** — the strongest posture, nothing to misconfigure.
2. A config-driven `cors_allowed_origins: list[str]` (default **empty** = middleware not installed) enables `CORSMiddleware` for local development only (`http://localhost:3000`), with credentials allowed, explicit method/header lists, and hard validation rules: **wildcard origins are rejected in all environments** (Product Owner mandate, 2026-07-19); production profile validation rejects any non-empty list unless explicitly overridden by a future superseding ADR.
3. The frontend API base URL becomes relative (`/api`) in deployed builds, absolute only in local dev — aligning with ADR-004's gateway-fronted enforcement.

**Option 2 — Cross-origin allowlist in all environments** (separate app/api domains): **NOT SELECTED.** Retained for the record; adopting it would require a superseding ADR.

## Alternatives rejected outright

- **Wildcard `*` CORS** — incompatible with credentialed requests and Zero Trust.
- **Ad-hoc per-route CORS handling** — unauditable; policy must be a single platform concern.

## Consequences

- Option 1 makes CORS a development-only concern and removes an entire production misconfiguration class; it commits S1.7+ ingress design to path-based routing.
- Either option is implementable in under a day on the existing `Settings` seam; the frontend change (relative base URL) is one configuration line.
- Gate discharge: the strategy decision is **made** (this approval); the gate closes when the implementation lands before Sprint-002 close (at first frontend↔backend integration) — no code change is authorized by this approval itself.
