# 07_ADRs — Architecture Decision Records

ADRs record architectural decisions not fully specified by the MC→IP documentation chain, and sanctioned deviations from it (Constitution §16.2). ADRs are superseded, never silently edited. Status values: Proposed → Accepted → Superseded.

| ADR | Title | Status | Binding effect |
|---|---|---|---|
| [ADR-001](ADR-001_Platform_Foundation_Engineering_Decisions.md) | Platform Foundation Engineering Decisions (Sprint-001 batch) | **Accepted** (PO, 2026-07-19) | Ratifies 12 implemented Sprint-001 conventions (event naming/versioning/stamping, error mapping, naming deviation, shared independence, …) |
| [ADR-002](ADR-002_Transactional_Outbox.md) | Transactional Outbox for Event Publication | **Accepted** (PO, 2026-07-19); **Sprint-002 completion gate** | Outbox-in-transaction + drain worker before first business event producer |
| [ADR-003](ADR-003_Kafka_Reliability_Strategy.md) | Kafka Reliability and Reconnection Strategy | **Accepted** (PO, 2026-07-19); **Sprint-002 completion gate** | Supervised producer re-establishment, error classification, readiness trip |
| [ADR-004](ADR-004_Production_Authentication_Enforcement.md) | Production Authentication Enforcement & Surface Gating | **Accepted** (PO, 2026-07-19); **Sprint-002 completion gate / Production Blocker** | Deny-by-default at `/api/v1`; fail closed; docs/metrics gating |
| [ADR-005](ADR-005_Pagination_Strategy.md) | Pagination Strategy (Deterministic Ordering + Keyset) | **Accepted** (PO, 2026-07-19); **Sprint-002 completion gate** | PK-ordered lists; keyset standard; bounded OFFSET |
| [ADR-006](ADR-006_CORS_Strategy.md) | CORS Strategy | **Accepted** (PO approved Option 1, 2026-07-19); implementation is a Sprint-002 completion gate | Permanent standard: same-origin-only production, allowlisted dev origins, wildcards prohibited everywhere |
| [ADR-007](ADR-007_Health_Check_Strategy.md) | Health, Readiness, and Liveness Strategy | **Accepted** (PO, 2026-07-19; ratifies implemented semantics) | Probe semantics law for S1.7; non-blocking optimization guidance |

Provenance: drafted 2026-07-19 by the pre-Sprint-002 governance review (AUD-002, CON-001, MAT-001).
