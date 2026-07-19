# ADR-003 — Kafka Reliability and Reconnection Strategy

| Field | Value |
|---|---|
| Status | **Accepted** — Approved by Product Owner (Anil Kumar), 2026-07-19; implementation mandated as **Sprint-002 completion gate** (Governance Decision 1/2, 2026-07-19) |
| Date | 2026-07-19 |
| Deciders | Product Owner; drafted by pre-Sprint-002 governance review |
| Source | RA-001 §14 (resilience patterns), ARCH-001 §14 (graceful degradation), AUD-001 C-2, AUD-002 (scope correction) |

## Context

`KafkaManager` creates its producer once during application startup; there is no retry, reconnection, or circuit-breaker logic (`infrastructure/messaging/kafka.py`). AUD-002's corrected scope: after a *successful* start, the aiokafka client self-heals from broker outages (per-send timeouts, then recovery); the unrecoverable case is **startup-connect failure**, which leaves the pod permanently unable to publish until manually restarted — unacceptable under routine rolling restarts and broker upgrades at scale. Current settings already include `acks=all` with the idempotent producer (correct; retained).

## Decision

1. **Lazy producer establishment with supervised retry:** if the producer is absent (startup failure or fatal producer error), `KafkaManager` attempts re-establishment on demand and via a background supervisor loop with capped exponential backoff + jitter; startup failure no longer condemns the pod.
2. **Error classification:** send-side errors are classified retriable (broker unavailable, timeouts — retried per policy / absorbed by the ADR-002 outbox) vs fatal (serialization, authorization — surfaced immediately as `InfrastructureError`).
3. **Readiness integration (minimal circuit breaker):** repeated failures trip the existing Kafka health check to unhealthy (readiness-visible) and back on recovery; no bespoke breaker framework is introduced.
4. **Division of labor with ADR-002:** the outbox owns *durability* (no loss); this ADR owns *liveness* (the pipeline heals itself). Direct-publish system events rely on this ADR alone and remain best-effort.
5. Producer settings ratified: `acks=all`, idempotence on, org-ID keying (ADR-001 #6); throughput tuning (linger/compression/partitioning) is deferred until profiling justifies it.

## Alternatives considered

- **Fail-fast startup (crash if Kafka absent)** — rejected: violates ARCH-001 §14 graceful degradation; couples API availability to broker availability.
- **Full circuit-breaker library** — rejected for now: the health-check trip achieves the operational goal without a new dependency; revisit if breaker semantics are needed for other dependencies.
- **Rely solely on the outbox** — rejected: the outbox needs a healing publisher underneath it; system events bypass the outbox.

## Consequences

- Broker unavailability at any lifecycle point becomes self-healing; readiness truthfully reflects the degradation window.
- Adds a supervisor task to the manager lifecycle (shutdown must cancel it cleanly — test required).
- Sprint-002 completion gate; tests ship with the implementation (Constitution §9.6).
