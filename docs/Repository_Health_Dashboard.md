# Project ATLAS — Repository Health Dashboard

| Field | Value |
|---|---|
| Document ID | HD-001 |
| Title | Repository Health Dashboard |
| Role | **Unique role:** the refreshable traffic-light view. Scores are baselined from MAT-001 (methodology + full evidence live there); this dashboard adds two operational lenses (Technical Debt management, Operational Readiness) and is refreshed at every audit/sprint close without re-issuing MAT editions |
| Edition | 1 — 2026-07-19 (Sprint-001 closure) |

## Dashboard

| # | Area | Score | Status | One-line state |
|---|---|---|---|---|
| 1 | Architecture | 8.5 | 🟢 Healthy | Layer-pure (mechanically verified), Protocol-seamed; unexercised by a real module until Identity |
| 2 | Documentation | 9.0 | 🟢 Healthy | 89 md documents, full governance corpus; known chain contradictions documented as tripwires |
| 3 | Governance | 8.5 | 🟢 Healthy | Constitution + ADRs + registers + gates exist; **ratifications pending** is the one open item |
| 4 | Testing | 4.5 | 🔴 Critical | 99.08% on `shared/`; zero elsewhere; gate-bound subset (ADR-002/003 tests) non-deferrable |
| 5 | Security | 4.0 | 🔴 Critical | Strong primitives; no authn/z (scheduled IP-002); anonymous surfaces are Category A |
| 6 | Scalability | 5.0 | 🟡 Needs Attention | Design-ready (stateless, UUID v7, tenant keying); ops posture absent (pagination, pools, topics) |
| 7 | Maintainability | 8.5 | 🟢 Healthy | Single-sourced vocabularies, citation docstrings, deterministic conventions |
| 8 | Reliability | 4.0 | 🔴 Critical | Event-loss window + non-healing producer (Category A, gate-owned ADR-002/003); no alerting |
| 9 | AI Readiness | 9.0 | 🟢 Healthy | Cold-start resumable; context/profiles/memory/navigation complete; cross-model rules in place |
| 10 | Developer Experience | 7.0 | 🟡 Needs Attention | One-command env, pinned toolchains; no CI feedback loop; Windows frictions documented |
| 11 | Technical Debt (management quality) | 7.5 | 🟡 Needs Attention | *Amount* is expected for a foundation; *management* is strong: 100% of known debt ID-registered, classified A–D, owner-assigned. Held below 🟢 only because Category A is non-empty |
| 12 | Operational Readiness | 3.5 | 🔴 Critical | No K8s, CI, alerting, runbooks, DR, or IP-011; containerized dev environment is the sole operational asset |

**Composite: 6.6/10** (matches MAT-001 across shared areas). Reds are concentrated, scheduled, and gate-owned — the dashboard's purpose is to keep them visibly red until discharged, not to average them away.

## Per-area detail (evidence · risk · target · plan)

Areas 1–10 inherit MAT-001 §1–§12 verbatim for current-state, evidence, risks, and improvement plans (do not duplicate; MAT-001 is authoritative). Deltas and the two new areas:

### 11. Technical Debt — 7.5 🟡 (target 8.5)
- **Evidence:** AUD-001/002 registers: 3 Critical + 6 High + 14 Medium + 13 Low findings, every one re-validated, classified (A/B/C/D), owner-assigned with permanent IDs; zero unregistered known debt; POL-001 forbids unregistered shortcuts (Emergency §6).
- **Risk:** register rot — findings fixed without status updates, or new debt accruing unregistered during implementation pressure.
- **Plan:** stage reports must update finding status when touching a registered area (POL-001 §7); AUD-003 at Sprint-002 close re-scores. **Target 8.5** = Category A empty + register verified current.

### 12. Operational Readiness — 3.5 🔴 (target 8.0)
- **Evidence:** absent: K8s manifests, CI/CD, alerting, dashboards, runbooks, backup/restore drills, DR posture, IP-011 (unauthored). Present: verified Compose environment, production-shaped images, truthful probes (ADR-007), redacted structured logs.
- **Risk:** operational work is the classic casualty of feature pressure; it is now *inherited* Sprint-002 scope competing with Identity.
- **Plan:** Sprint-002 platform-hardening stages (K8s per ADR-004/007 + M-12; CI gates); IP-011 authored before Sprint-011 planning; alerting on outbox-age with ADR-002. **Target 8.0** at production certification (CON-001 §15).

### Score deltas vs MAT-001
None — areas 1–10 carry MAT-001 baselines unchanged (same evidence date). First expected movement: Sprint-002 close (Testing ↑, Security ↑, Reliability ↑ if gates hold; Governance ↑ on ratification).

## Refresh protocol

At each audit or sprint close: update scores + one-liners here; record evidence deltas in the audit (AUD-00x); re-issue MAT as a new edition only when methodology or a majority of scores move. A dashboard edit outside an audit/closure event is a POL-001 §5 violation.
