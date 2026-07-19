# ADR-001 — Platform Foundation Engineering Decisions (Sprint-001 Ratification Batch)

| Field | Value |
|---|---|
| Status | **Accepted** — Approved by Product Owner (Anil Kumar), 2026-07-19 |
| Date | 2026-07-19 |
| Deciders | Product Owner (Anil Kumar); drafted by pre-Sprint-002 governance review |
| Source | Documentation Consistency Audit (S1.4), CTX-001 §6.4 register, AUD-002 |
| Supersedes / Superseded by | — / — |

## Context

Sprint-001 implementation required a set of concrete engineering decisions in areas the approved documentation deliberately left as `"Implementation Defined During Engineering"` or did not fully specify. Each was implemented, verified, and recorded in session registers, but none had a formal ADR — a gap flagged by the S1.4 Documentation Consistency Audit and AUD-001/AUD-002. This ADR ratifies them as a batch; each item is already load-bearing in verified code.

## Decisions (ratifying implemented state)

| # | Decision | Where implemented | Rationale / authority |
|---|---|---|---|
| 1 | Kafka topic naming: one topic per domain, `atlas.<domain>` (e.g. `atlas.organization`) | `shared/events/naming.py`, `shared/constants` | RA-006 leaves physical topology open; per-domain topics give per-domain retention/scaling with bounded topic count |
| 2 | Event version is derived from the `.v<n>` suffix of the event type; no separate version field is authored | `shared/events/envelope.py` | Single source of truth; prevents name/version divergence; BP-004 §11 naming pattern |
| 3 | `payloadSchema` defaults to the event type string until a schema registry exists | `shared/events/envelope.py` | RA-006 §8 requires the field; registry is future scope (RA-006 §21) |
| 4 | Event wire keys are camelCase (`eventId`, `organizationId`, …) | `shared/events/envelope.py` | Consistency with ES-002 API wire format |
| 5 | Tenant stamping: `organizationId` **mandatory** for `domain` and `integration` categories; nullable for platform categories (`system`, `ai`, `security`, `audit`, `notification`) where no tenant context exists | `shared/events/envelope.py` validation | Reconciles BP-002 §14 ("every event tenant-stamped") with RA-006 §4 (platform categories); fail-closed where tenancy applies |
| 6 | Kafka message key = `organization_id` → per-tenant partition ordering | `shared/events/publisher.py` | BP-004 tenant affinity; ordering guarantees are per-key (RA-006) |
| 7 | Outbox table schema `platform_event_outbox` (envelope JSON + status/attempt/timestamps columns) | `infrastructure/messaging/outbox_model.py` | RA-006 §10; operationalization governed by ADR-002 |
| 8 | `shared/auth` contract signatures: `Principal`, `IdentityClass{HUMAN,MACHINE,AGENT}`, `AccessDecision`, `TokenVerifier`, `PolicyDecisionPoint` Protocols — interfaces only until IP-002 | `shared/auth/contracts.py` | BP-003 ED-003 (three identity classes), ED-002 (central PDP) |
| 9 | Error-category → HTTP status mapping, incl. `BusinessError → 409` | `shared/exceptions/errors.py` | ES-002 standard-codes rule; 409 for business-rule conflicts |
| 10 | Python code uses idiomatic snake_case functions/variables, deviating from ES-001 §7 camelCase; wire formats remain camelCase | Entire backend | PEP 8 ecosystem consistency; ES-001 §7 to be editorially amended rather than code changed |
| 11 | Single environment enumeration: `development, testing, staging, production` (constants + Settings literal to be derived from one source) | `shared/constants`, `shared/config` | IP-001 §10; removes dual-definition risk (AUD-001 L-2) |
| 12 | Shared-library framework independence: `shared/*` never imports `core/api/infrastructure/apps`/frontend (Product Owner rule, S1.4) | Verified by grep + import-integrity test | Enables Clean Architecture domain layers to use shared safely |

## Alternatives considered

Per-item alternatives were evaluated during S1.4/S1.6 (e.g. per-event topics — rejected: topic explosion; separate version field — rejected: divergence risk; camelCase Python — rejected: ecosystem friction). Recorded here in aggregate; none warrant individual ADRs at current scale.

## Consequences

- These conventions are binding for all future modules (Constitution §6/§7).
- ES-001 §7 requires an editorial amendment (naming); MC-000 refresh recommended.
- Any change to items 1–6 is a breaking event-contract change requiring a superseding ADR.
