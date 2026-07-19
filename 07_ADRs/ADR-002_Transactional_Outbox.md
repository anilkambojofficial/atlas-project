# ADR-002 — Transactional Outbox for Event Publication

| Field | Value |
|---|---|
| Status | **Accepted** — Approved by Product Owner (Anil Kumar), 2026-07-19; implementation mandated as **Sprint-002 completion gate** (Governance Decision 1, 2026-07-19) |
| Date | 2026-07-19 |
| Deciders | Product Owner; drafted by pre-Sprint-002 governance review |
| Source | RA-006 §10, RA-001 §13, AUD-001 C-1/H-6/M-3, AUD-002, BP-003 (audit events must never be dropped) |

## Context

`UnitOfWork.commit()` currently commits the database transaction and then publishes collected events directly to Kafka; a publish failure after commit is logged and swallowed (`infrastructure/database/unit_of_work.py:73`). The loss window (process crash, broker unavailability, send timeout between commit and acknowledgment) produces permanent divergence between committed state and the event stream. The outbox ORM model exists (`infrastructure/messaging/outbox_model.py`) but has no migration, no writer, and no drain worker. No production code path emits business events yet — Sprint-002 (Identity) introduces the first producers, including security/audit events whose loss is an incident under BP-003.

## Decision

1. Business events are persisted to `platform_event_outbox` **inside** the same database transaction as the state change: `UnitOfWork.commit()` writes collected envelopes to the outbox before COMMIT; direct post-commit publishing is retired for transactional events.
2. A drain worker (Celery, `atlas.platform` queue) polls the outbox, publishes via the existing `EventPublisher` seam with capped exponential backoff, marks entries published, and surfaces age/failure metrics. Delivery guarantee: **at-least-once**; consumers must be idempotent (Inbox pattern, future consumer-side ADR).
3. `collect_event` is typed and fail-fast: signature narrows to `EventEnvelope`, with a `TypeError` raised at collection time (closes AUD-001 H-6's silent-discard path).
4. Non-transactional system events (no accompanying state change) may continue to publish directly through the container's publisher.
5. Bundled obligation: the drain worker runs under Celery, so structured JSON logging is enabled for workers in the same delivery (AUD-001 M-3).
6. The outbox ships with its tests in the same commits (Constitution §9.6): UoW-writes-outbox-in-transaction, drain retry/backoff, poison-entry handling, age alerting hook.

## Alternatives considered

- **Status quo (publish-after-commit)** — rejected: unrecoverable loss window; violates RA-006 §10.
- **Two-phase commit / transactional Kafka producer spanning DB+broker** — rejected: operational complexity, poor library support across the stack, RA-006 prescribes outbox.
- **CDC (Debezium) on the outbox table** — deferred: heavier operational footprint; the polling drain is sufficient at current scale and CDC can supersede it later without contract change.

## Consequences

- Broker outages degrade to "events delayed" (visible via outbox-age metric), never "events lost".
- Adds one polling worker and one table to operate; alerting on outbox age becomes a Production Ready requirement (Constitution §15).
- `UnitOfWork` contract change is internal; the `OutboxStore`/`EventPublisher` Protocols already anticipate it — no shared-contract break.
- Sprint-002 cannot be declared complete until this ADR is implemented and verified (gate register, AUD-002).
