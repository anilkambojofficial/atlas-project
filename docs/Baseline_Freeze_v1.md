# Project ATLAS — Baseline Freeze v1 (Sprint-001)

| Field | Value |
|---|---|
| Document ID | BAS-001 |
| Title | Sprint-001 Baseline Freeze |
| Status | **APPROVED — Baseline FROZEN** (GOV-004 Accepted by Product Owner, 2026-07-19; Freeze Procedure executed same day) |
| Effective upon | Product Owner approval of CLS-001 + this document, execution of the Freeze Procedure below — **both satisfied 2026-07-19** |
| Change control after freeze | POL-001 (Repository Change Policy). Sprint-001 scope becomes immutable except critical bug fixes per POL-001 §Hotfix |
| Date | 2026-07-19 |

## Freeze Procedure (required to make this freeze real)

The working tree currently holds **uncommitted Sprint-001 material**: the entire S1.6 containerization delivery and the governance/closure document set (last commit: `dbe75eb`, S1.5). The freeze is effective only after, upon approval:

1. Commit S1.6 (recommended message previously approved-pending: `feat(platform): add containerized development environment per IP-001 §16 (S1.6)`).
2. Commit the governance + closure document set (`docs(governance): …`).
3. Tag the resulting commit: **`baseline-v1.0.0-sprint001`** (annotated tag; the tag commit is the immutable baseline referent).
4. Record the tag hash in LOG-S001 and in REG-001 entry GOV-004.

## Baseline Identity

| Dimension | Frozen value |
|---|---|
| **Repository Version** | Baseline **v1.0.0-sprint001**; backend package `atlas-backend 0.1.0`; frontend package `0.1.0`; commit series `20b8d85 → dbe75eb` + the two freeze commits above |
| **Architecture Version** | MC/ARCH/DOMAIN/ES/RA chain as committed (ARCH-001..008; RA-001..012); BP-000/001 Approved, BP-002..012 Draft (Engineering Review); IP-000..010 Draft; IP-011 unauthored (registered debt). Layering law: CON-001 §3–§5 |
| **ADR Version** | ADR-001 through ADR-007, all **Proposed (PO ratification pending)**; ratification is Sprint-002 readiness condition 1 — the *set membership* is frozen; status flips to Accepted upon ratification without re-freeze |
| **Engineering Standard Version** | ES-001..007 as committed, with one ratified deviation register (ADR-001 #10 snake_case) pending editorial amendment |
| **Framework Version** | Backend: FastAPI ≥0.115<1.0, Uvicorn ≥0.32<1.0, Pydantic ≥2.9<3.0, SQLAlchemy ≥2.0<3.0, Alembic ≥1.14<2.0, asyncpg ≥0.30, redis ≥5.2<7.0, aiokafka ≥0.12<1.0, Celery ≥5.4<6.0 (`backend/pyproject.toml`; exact resolutions frozen in `backend/uv.lock`). Frontend: Next ^15, React ^19, TanStack Query ^5, Zustand ^5, RHF ^7.54, Zod ^3.23, axios ^1.7, ECharts ^5.5, next-themes ^0.4.6, jose ^5.9, Radix set, Tailwind + shadcn/ui (`frontend/package.json`; exact resolutions in `pnpm-lock.yaml`) |
| **Configuration Version** | IP-001 §10 hierarchy as implemented in S1.5: profiles `configs/{base,development,testing,staging,production}` + git-ignored `local/`; priority env > secrets (`ATLAS_SECRET_*` / `configs/local/secrets.json`) > local > env-profile > base; `ATLAS_FEATURE_*` flags; production guards active |
| **Dependency Versions** | Authoritative: **`backend/uv.lock`** and **`frontend/pnpm-lock.yaml`** at the freeze tag — the lockfiles, not this table, are the byte-level truth (ES-006 §6) |
| **Technology Stack** | Python 3.13 (dev-verified 3.13.14) · TypeScript strict / Node 22 LTS · package managers uv 0.11.29, pnpm 10.14.0 (corepack-pinned) · PostgreSQL · Redis · Kafka · Celery — locked per IP-001; changes require ADR (CON-001 §4.5) |
| **Infrastructure Stack** | PostgreSQL 17-alpine · Redis 7-alpine · Apache Kafka 3.9.1 (KRaft, single-node **dev-only topology**, dual listeners `kafka:19092`/`localhost:9092`) · named volumes `atlas_{postgres,redis,kafka}-data` · bridge network `atlas` |
| **Docker Stack** | `backend/Dockerfile` (multi-stage `python:3.13-slim`, uv `--frozen`, non-root uid 10001, `/live` healthcheck; doubles as worker image) · `frontend/Dockerfile` (multi-stage `node:22-alpine`, Next standalone, non-root) · `deployment/compose/docker-compose.yml` (profiles `infra`/`full`) · `scripts/dev-{up,down}.sh` |
| **Testing Baseline** | 86 collected unit tests (67 functions); shared coverage **99.08%** vs enforced ≥95% gate (`pyproject.toml [tool.coverage.report] fail_under=95`); deterministic/network-free; scope: `shared/` only (boundary registered: AUD H-4) |
| **Documentation Baseline** | 68-document chain + LOG-S001 + CTX-001 + docs/ governance set (AUD-001, AUD-002, CON-001, MAT-001, CLS-001, BAS-001, POL-001, REG-001, RMB-001, CTX-002) + `07_ADRs/` (7 ADRs + index). Known chain defects frozen *as documented* in CTX-001 §15.4 — fixing them is a governed change, not a freeze violation |
| **Audit Baseline** | AUD-001 (adversarial audit: 3C/6H/14M/13L) + AUD-002 (re-validation, A–D reclassification, gate register) — finding IDs (C-1…L-13) are permanent references |
| **Governance Baseline** | CON-001 (Constitution, ratification pending) · Governance Decisions 1–4 (REG-001 GOV-001..004) · Category A register {C-1, C-2, C-3/M-7} · Sprint-002 completion-gate register {ADR-002, ADR-003, ADR-004, ADR-005, ADR-006} · maturity baseline **6.6/10** (MAT-001) |

## Immutability Terms

1. After approval + tagging, Sprint-001 scope (everything above) is modified only per POL-001: critical bug fixes (hotfix rules), governed deprecations, or superseding ADRs.
2. The baseline is a **reference point, not a development branch**: Sprint-002 work proceeds on `main` per normal stage gates; "immutable" binds the *decisions and contracts*, not the file bytes — e.g., ADR-002 will lawfully rewrite `UnitOfWork` internals because ADR-002 is part of the frozen decision set.
3. Frozen contracts that no future change may break without a superseding ADR + version bump: ES-002 envelope shapes, RA-006 §8 event envelope fields, ADR-001 conventions 1–6, ES-003 mixin semantics, config priority order, `/live|/ready|/health|/metrics` semantics (ADR-007).
4. Baseline references in future documents use the tag `baseline-v1.0.0-sprint001` and document IDs (CLS-001/BAS-001), never "the old code".
