# ADR-004 — Production Authentication Enforcement and Operational Surface Gating

| Field | Value |
|---|---|
| Status | **Accepted** — Approved by Product Owner (Anil Kumar), 2026-07-19; enforcement mandated as **Sprint-002 completion gate** and **Production Blocker** (Governance Decisions 1/2, 2026-07-19) |
| Date | 2026-07-19 |
| Deciders | Product Owner; drafted by pre-Sprint-002 governance review |
| Source | BP-003 ED-001/002/005 (Zero Trust, central PDP, fail-closed), ES-004, AUD-001 C-3/M-7/M-8, AUD-002 |

## Context

The Sprint-001 foundation intentionally ships with no authentication (identity is IP-002 scope). Interactive API docs are enabled unconditionally (`core/application.py:83`) and `/metrics` is unauthenticated. This posture is sanctioned scaffolding while no business data exists, but must not survive into production or outlive Sprint-002.

## Decision

1. **No anonymous business endpoint in production — constitutional rule** (Constitution §17.7). Every route mounted under `/api/v1` (other than explicitly catalogued public endpoints, currently none) requires an authenticated `Principal` once IP-002's verifier exists; authorization flows through the shared `PolicyDecisionPoint` contract — never inline permission logic (BP-003 ED-002).
2. **Fail closed:** if token verification or the PDP is unavailable, requests are rejected (401/403 per taxonomy), never allowed through (BP-003 ED-005).
3. **Enforcement mechanism:** a platform-level FastAPI dependency applied at the `/api/v1` router mount (deny-by-default), with an explicit opt-out marker for the catalogued public set — so forgetting to protect a new route is impossible, and unprotecting one is visible in review.
4. **Operational surfaces:** `docs_url`/`openapi_url`/`redoc_url` disabled when `environment == "production"`; `/metrics` restricted to the cluster-internal scrape network via S1.7 NetworkPolicy (never ingress-exposed); health endpoints remain unauthenticated by design (probe semantics, ADR-007).
5. **Rate limiting:** global rate limiting is owned by the API Gateway (ES-002 §18 direction); independently, IP-002 credential endpoints implement application-level lockout/backoff (brute-force defense is not delegated).
6. **Sequencing:** wiring lands with IP-002's identity service; the docs/metrics gating sub-items land earlier, in Sprint-001 S1.7/S1.8 hardening (Category B, AUD-002).

## Alternatives considered

- **Per-route auth dependencies added by each module** — rejected: opt-in security fails open on omission; deny-by-default at the mount fails closed.
- **Gateway-only authentication** — rejected as sole mechanism: Zero Trust requires service-level verification; the gateway is a layer, not the layer.
- **Basic-auth on `/docs` in production** — rejected: gating by environment is simpler and leaks nothing.

## Consequences

- Sprint-002 completion requires: enforcement dependency live, identity endpoints authenticated, placeholder anonymous access retired, sessionStorage token placeholder replaced with httpOnly cookies (BP-003 session design; AUD-001 M-5).
- Production deployment blocked until this ADR is verifiably enforced (Constitution §15).
- The public-endpoint catalogue becomes a reviewed artifact (initially empty).
