# ADR-005 — Pagination Strategy (Deterministic Ordering + Keyset)

| Field | Value |
|---|---|
| Status | **Accepted** — Approved by Product Owner (Anil Kumar), 2026-07-19; implementation mandated as **Sprint-002 completion gate** (Governance Decision 1, 2026-07-19) |
| Date | 2026-07-19 |
| Deciders | Product Owner; drafted by pre-Sprint-002 governance review |
| Source | ES-003 (UUID v7 PKs), ES-002 (pagination metadata), AUD-001 H-1, AUD-002 |

## Context

`SqlAlchemyRepository.list()` applies LIMIT/OFFSET with no ORDER BY (`infrastructure/repositories/base.py`) — PostgreSQL then guarantees no row order, so pages can repeat or skip rows nondeterministically. Separately, OFFSET pagination scans and discards all preceding rows, degrading linearly with depth — untenable at millions-of-users data volumes. No caller of `list()` exists yet; Sprint-002 (Identity) introduces the first list endpoints.

## Decision

1. **Deterministic default ordering:** the repository base orders every list query by primary key (`ORDER BY id`). Because primary keys are UUID v7 (time-ordered, ES-003/ADR-001), this yields stable, index-backed, creation-time ordering at zero additional cost. Business-specific orderings append `id` as the final tiebreaker to remain total.
2. **Keyset (cursor) pagination is the platform standard** for unbounded collections: `WHERE (sort_key, id) > (:cursor_key, :cursor_id) ORDER BY sort_key, id LIMIT :n`, exposed in the repository base alongside the existing method. Cursors are opaque strings on the wire (encoded key material), carried in ES-002 `metadata`.
3. **OFFSET mode is retained as a bounded convenience** (small, admin-style listings), capped by the existing `MAX_PAGE_SIZE` and a maximum page depth; it must not back any customer-facing unbounded collection.
4. **Timing:** the ordered default + keyset method must exist in the repository base **before the first business list endpoint merges** (Sprint-002); every Identity list endpoint uses the standard from day one.

## Alternatives considered

- **ORDER BY created_at** — rejected as primary: non-unique (ties), redundant with UUID v7 id ordering, second index dependency.
- **OFFSET everywhere with caps** — rejected: still nondeterministic without ordering (fixed here anyway) and still linear-cost at depth.
- **Third-party cursor library** — rejected: the pattern is ~30 lines in the existing base; no dependency warranted.

## Consequences

- All list responses become deterministic and replay-stable; pagination cost becomes O(page) regardless of depth.
- Wire contract gains a cursor convention (documented with IP-002's first endpoints; mirrored in frontend types — contract-fixture coverage per Constitution §9.5).
- Existing `list()` signature keeps compatibility; ordering addition is behaviorally breaking only for code depending on undefined order (none exists).
