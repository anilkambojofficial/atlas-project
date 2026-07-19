# ADR-007 — Health, Readiness, and Liveness Strategy

| Field | Value |
|---|---|
| Status | **Accepted** — Approved by Product Owner (Anil Kumar), 2026-07-19 — ratifies implemented semantics; optimization guidance non-blocking (Governance Decision 3, 2026-07-19) |
| Date | 2026-07-19 |
| Deciders | Product Owner; drafted by pre-Sprint-002 governance review |
| Source | IP-001 §14, ARCH-001 §14, AUD-001 H-3/M-9, AUD-002 |

## Context

The platform exposes four operational endpoints implemented in S1.2A/S1.2B and verified green in S1.6. Their semantics were an implemented-but-undocumented decision set; AUD-001 additionally flagged the serial, uncached execution of dependency checks as a scale concern (severity revised down in AUD-002 per Governance Decision 3: implementation improvement, not architecture failure).

## Decision (ratifying implemented semantics)

1. **`/live`** — process liveness only; checks **nothing** external. Kubernetes livenessProbe target. A sick dependency must never restart-loop the pods (ARCH-001 §14).
2. **`/ready`** — dependency readiness via the shared `HealthRegistry`; 200 only when required dependencies are healthy, 503 otherwise with per-check detail. Kubernetes readinessProbe target; traffic-gating semantics.
3. **`/health`** — diagnostic aggregate for humans/monitors; same registry, full detail. Not a Kubernetes probe target.
4. **`/metrics`** — Prometheus text format; cluster-internal only (ADR-004 §4).
5. These endpoints are **unenveloped** (industry-standard probe payloads; ES-002 envelopes govern business APIs) and **unauthenticated** (probe reachability; `/metrics` protected at the network layer). Health endpoints live outside `/api/v1` and outside ADR-004's deny-by-default scope.
6. Every module registers its dependency checks on the container's `HealthRegistry`; `api/health.py` is never modified per-module (Constitution §6.5).

## Optimization guidance (non-blocking, Category C — target S1.7 alongside probe definitions)

- Execute registered checks **concurrently** (`asyncio.gather`), bounding worst-case latency to the slowest single check instead of the sum of timeouts.
- Add a short **TTL cache** (2–5 s) on registry results so `replicas × probes × dependencies` synthetic load stays constant under probe frequency; `/health` may force refresh.
- Startup dependency connects may parallelize with per-dependency timeouts (AUD-001 M-9) — same pattern, same seam.
- S1.7 probe parameters (periods, thresholds, timeouts) must be derived from the measured check latencies, with probe timeout > slowest single check timeout.

## Alternatives considered

- **Deep checks in liveness** — rejected: converts dependency outages into restart storms.
- **Static "ok" readiness** — rejected: defeats traffic gating; readiness must be truthful (verified truthful in S1.2B failure-path and S1.6 green-path testing).

## Consequences

- Probe semantics are now citable law for S1.7 manifests and every future module.
- The optimization items are internal to `shared/monitoring` — no endpoint contract change when they land.
