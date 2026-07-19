# Project ATLAS — Repository Manifest

| Field | Value |
|---|---|
| Document ID | MAN-001 |
| Title | Repository Manifest (master metadata) |
| Role | The single at-a-glance metadata record. **Unique role:** facts and numbers only — depth lives in the documents it points to. Refreshed at every sprint close (with CTX-002) |
| Date | 2026-07-19 (Sprint-001 closure) |

## Identity

| Field | Value |
|---|---|
| Repository Name | **Project ATLAS** — AI-native, multi-tenant Enterprise Knowledge & Intelligence Platform (MC-001) |
| Repository Version | Baseline **v1.0.0-sprint001** (BAS-001; freeze commits + tag pending PO approval — last commit `dbe75eb`, 32 uncommitted paths comprising S1.6 + governance corpus) |
| Current Baseline | BAS-001 — Sprint-001 frozen scope; immutability terms in BAS-001 §Immutability |
| Current Sprint | Sprint-001 **CLOSED & FROZEN** (`baseline-v1.0.0-sprint001` → `d7293b0`) · Sprint-002 (Identity & Access) **IMPLEMENTED & CLOSURE-REVIEWED** — all five GOV-001 gates closed; READY TO FREEZE pending PO (CLS-002; recommended tag `baseline-v1.1.0-sprint002`); state authority LOG-S002 |
| Repository Status | Verified platform foundation; zero business features; **NOT production ready** (by declaration, CON-001 §15); **governance ratified 2026-07-19** — CON-001 in force (v1.0.0), ADR-001..007 all Accepted; freeze commits + baseline tag pending |
| Product Owner | Anil Kumar (anilkamboj@vardhman.com) — sole approval authority |

## Technology & Infrastructure Stack

| Layer | Stack (authoritative pins: `backend/uv.lock`, `frontend/pnpm-lock.yaml`) |
|---|---|
| Backend | Python 3.13 · FastAPI · Uvicorn · SQLAlchemy 2 (async) · Alembic · Pydantic v2 · Celery · uv 0.11.29 |
| Frontend | Next.js 15 (App Router) · React 19 · TypeScript strict · Tailwind + shadcn/ui · TanStack Query · Zustand · pnpm 10.14.0 |
| Data / messaging | PostgreSQL 17-alpine · Redis 7-alpine · Apache Kafka 3.9.1 (KRaft; single-node dev topology) |
| Containers | `python:3.13-slim` / `node:22-alpine` multi-stage non-root images · Compose profiles `infra`/`full` · `scripts/dev-{up,down}.sh` |
| Pending (deferred → Sprint-002) | Kubernetes manifests · CI/CD (GitHub Actions) · test pyramid beyond `shared/` |

## Repository Statistics (counted 2026-07-19)

| Metric | Count |
|---|---|
| Governed chain documents (00–06) | **68** — MC 6 · ARCH 8 · DOMAIN 10 · ES 7 · BP 14 (13 packs + roadmap) · RA 12 · IP 11 |
| ADRs | **7** (+ index) — **all Accepted** (PO ratification 2026-07-19; ADR-006 with CORS option selection) |
| Audits | **2** — AUD-001 (adversarial), AUD-002 (re-validation/reclassification) |
| Engineering Standards | **7** (ES-001..007) |
| Context documents (AI) | **2 core** (CTX-001 depth, CTX-002 entry) + this intelligence set (MAN/KG/AIL/NAV/MEM) |
| Sprint documents | **LOG-S001, CLS-001, BAS-001** (+ per-sprint logs going forward) |
| Governance/docs total in `docs/` | **20** (13 pre-existing + 7 intelligence documents) |
| Source files | Backend **65** Python files · Frontend **25** TS/TSX files |
| Tests / coverage | **86** collected unit tests · shared coverage **99.08%** (gate ≥95%, enforced) |

## Current State Summaries (pointers, not prose)

| Dimension | Value | Authority |
|---|---|---|
| Architecture | Clean Architecture + DDD; layer-pure (0 forbidden imports, mechanically verified); 6 Protocol seams; sole-entry-point mandates | CON-001 §3–5; AUD-002 Part 4 |
| Maturity | **6.6/10** (structure 8.5–9; operations 4–5) | MAT-001; refreshable view: HD-001 |
| Production status | NOT PRODUCTION READY; Category A open: {C-1 event loss, C-2 Kafka resilience, C-3/M-7 anonymous surfaces} | CON-001 §15; AUD-002 |
| Risks | Gate discipline; sprint overlap; single approver; AI-self-review limits; documented chain contradictions | CTX-002 §5 |
| Technical debt | Registered by permanent finding ID (C-1…L-13), classified A–D, all owned | AUD-002; CLS-001 §11 |
| AI status | Fully cold-start resumable; rules CON-001 §12; loading profiles AIL-001; memory map MEM-001 | CTX-002 |

## Document Loading Order (canonical; per-role variants in AIL-001/NAV-001)

1. `docs/Repository_Constitution.md` → 2. `docs/AI_Continuation_Pack.md` → 3. `docs/AI_Future_Context_Pack.md` → 4. sprint log(s) + `docs/Decision_Register.md` → 5. task-specific chain per CTX-001 §13 → 6. nearest analogous code → 7. `git log`/`git status`.

## Repository Navigation Index

| Need | Go to |
|---|---|
| What is this product? | `00_Master_Context/` (MC-001 first) |
| What is the law? | CON-001 · CTX-001 §3 invariants · POL-001 (changes) |
| What is decided? | REG-001 → `07_ADRs/` |
| Where are we? | CTX-002 · RMB-001 · current sprint log |
| What's wrong / debt? | AUD-002 · HD-001 |
| How do I build module X? | CTX-001 §13 (corrected mapping + recipe) → its IP/BP/DOMAIN |
| How healthy is it? | HD-001 (traffic lights) · MAT-001 (baseline scores) · CERT-001 (certification) |
| Document relationships | KG-001 (knowledge graph) |
| Who reads what, in what order? | NAV-001 (humans) · AIL-001 (AI profiles) |
| Fast mental rebuild | MEM-001 |
