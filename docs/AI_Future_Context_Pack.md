# Project ATLAS — AI Future Context Pack

| Field | Value |
|---|---|
| Document ID | CTX-001 |
| Title | AI Future Context Pack |
| Classification | Permanent AI/engineering onboarding context |
| Audience | Every future AI coding model (Claude, GPT/Codex, others) and every human engineer |
| Authority | **Derivative.** This document summarizes the governing layers. If it ever conflicts with MC/ARCH/DOMAIN/ES/RA/BP/IP documents, **the governing documents win** and this file must be corrected |
| State captured | End of Sprint-001 (S1.1–S1.6 complete, runtime-verified); 2026-07-19 |
| Owner | Anil Kumar (Product Owner) |

> **How to use this file:** read it first, in full, before touching anything.
> Then read the governing documents for the layer you are about to work in.
> This file tells you *what exists and why*; the governing documents tell
> you *what is law*.

---

# 1. Project Vision

## Product purpose

Project ATLAS is an **AI-native, multi-tenant Enterprise Knowledge & Intelligence Platform** (SaaS). It continuously transforms organizational conversations, meetings, documents, decisions, and operational events into structured, governed, searchable, continuously evolving enterprise knowledge. It is the organization's **institutional memory and operational intelligence layer** — explicitly *not* another meeting recorder, wiki, ERP, CRM, chat tool, or office suite (MC-001 §15 product boundaries).

The functional heart is a pipeline:

```
Meeting → Recording → Transcript → AI analysis
   → extracted Decisions / Actions / Risks / SOP candidates / Knowledge objects
   → Enterprise Knowledge Graph → RAG-grounded search, chat, and recommendations
   → back into future meetings and decisions
```

## Long-term objectives (MC-001 §12, MC-003)

- Phase 1 (MVP): multi-tenant orgs, identity, projects, meetings (native + Zoom/Teams/Meet), transcription, AI summaries, decision/SOP/action intelligence, knowledge repository, enterprise search, reporting.
- Phase 2: Enterprise Knowledge Graph, cross-project intelligence, recommendations, workflow automation.
- Phase 3: autonomous-but-governed AI agents, predictive organizational intelligence.
- Phase 4: ecosystem — ERP/CRM/HRMS connectors, marketplace, public APIs.

## Design philosophy (constitutional — MC-001 §13, MC-004 §2)

1. **Enterprise before features** — long-term quality beats delivery speed.
2. **AI native** — AI is a platform capability, never a bolt-on feature.
3. **AI assists — humans decide** — nothing becomes official knowledge, an approved decision, or a published SOP without human approval (HITL).
4. **Every decision traceable** — in the product *and* in this repository.
5. **Knowledge never dies / everything is connected** — artifacts stay linked (meeting ↔ decision ↔ SOP ↔ action ↔ knowledge).
6. **Security by design; Zero Trust** — never assumed, always verified, fail-closed.
7. **Explainable AI** — every AI output carries evidence, citations, confidence.
8. **Documentation before implementation** — the repository is the single source of truth; code that contradicts approved documentation is a governance violation, not a shortcut.

---

# 2. Repository Architecture

## 2.1 The governance chain (memorize this)

```
MC (Master Context)            00_Master_Context/       business constitution
  ↓
ARCH (Architecture)            01_Architecture/         technical constitution (8 docs)
  ↓
DOMAIN (Domain Model, DDD)     02_Domains/              10 business domains
  ↓
ES (Engineering Standards)     03_Engineering_Standards/ 7 engineering laws
  ↓
RA (Reference Architecture)    05_Reference_Architecture/ 12 technology-NEUTRAL blueprints
  ↓
BP (Build Packs)               04_Build_Packs/          13 implementation contracts (BP-000..012)
  ↓
IP (Implementation Packs)      06_Implementation_Packs/ 11 executable specs (IP-000..010; IP-011 pending)
  ↓
Source code                    backend/ frontend/ agents/ …
```

**Conflict rule (ES-001 §5): the higher layer always wins.** No lower artifact may redefine a higher one. Deviations require a formal ADR in `07_ADRs/`.

## 2.2 Folder map

| Path | Contents | Notes |
|---|---|---|
| `00_Master_Context/` … `06_Implementation_Packs/` | The governance chain above | **Never modify without explicit Product Owner approval.** Some cross-references are stale — see §15.4 known inconsistencies |
| `07_ADRs/` | Architecture Decision Records | Currently empty; the repo's rules require ADRs for deviations. A batch "ADR-001 Platform Foundation Engineering Decisions" has been recommended (see §6.4) |
| `08_Templates/`, `09_Assets/`, `12_UI_UX/`, `99_Reference/` | Reserved, empty | Populated by future governance |
| `10_API/` | API specifications (OpenAPI) | Populated per IP (first: IP-002 identity APIs) |
| `11_Database/` | Database schema documentation | Populated when migrations land |
| `13_Testing/`, `14_Deployment/` | Test plans, deployment docs | Future stages |
| `docs/` | `Repository_Traceability_Matrix.md` (RTM-001), `Sprint-001_Execution_Log.md` (stage records + decisions like D-S001-01), this file | Execution log is the authoritative record of sprint state |
| `backend/` | Python 3.13 / FastAPI platform (see §2.3) | |
| `frontend/` | Next.js 15 App Router workspace (see §2.4) | |
| `agents/` | AI agent definitions | Empty until IP-004 |
| `configs/` | IP-001 §10 configuration hierarchy: `base/ development/ testing/ staging/ production/ local/` | `local/` is git-ignored (developer overrides + `secrets.json`) |
| `deployment/compose/` | Dev environment (`docker-compose.yml`, profiles `infra`/`full`) | K8s manifests arrive in S1.7 |
| `infrastructure/` | Terraform / IaC | Future |
| `database/` | Migration baselines / seed data | Alembic itself lives in `backend/` |
| `scripts/` | `dev-up.sh`, `dev-down.sh` | One-command dev environment |
| `tools/`, `.github/` | Tooling configs, CI | CI arrives in S1.8 |

## 2.3 Backend layout (`backend/`)

```
backend/
├── main.py                  # ASGI entrypoint: app = create_app()
├── pyproject.toml + uv.lock # uv project; pinned deps; pytest+coverage config
├── alembic.ini, migrations/ # async Alembic; URL via config hierarchy; versions/ empty until IP-002
├── Dockerfile               # multi-stage python:3.13-slim; also the worker image
├── core/                    # PLATFORM RUNTIME (no business logic, ever)
│   ├── application.py       #   composition root: create_app()
│   ├── container.py         #   DI container + Depends providers + startup/shutdown
│   ├── middleware.py        #   RequestContextMiddleware (correlation, metrics, logs)
│   ├── errors.py            #   HTTP exception handlers (+ re-exports of shared.exceptions)
│   └── health.py            #   compatibility shim → shared.monitoring
├── shared/                  # 12 FRAMEWORK-FREE packages (IP-001 §9) — see §2.5 rule
│   ├── auth/       contracts only: Principal, IdentityClass, TokenVerifier, PolicyDecisionPoint
│   ├── config/     Settings, hierarchy loader, SecretProvider chain, feature flags
│   ├── constants/  every platform literal (headers, pagination, env names, error codes…)
│   ├── contracts/  ES-002 API envelope builders (success_envelope / error_body)
│   ├── events/     EventEnvelope (RA-006 §8), naming, EventPublisher/MessageTransport
│   │               protocols, KafkaEventPublisher, Outbox contract
│   ├── exceptions/ AtlasError taxonomy (framework-free)
│   ├── logging/    JSON formatter, TRACE level, request contextvars
│   ├── monitoring/ HealthRegistry (sync+async checks)
│   ├── security/   redaction (SENSITIVE_KEYS), mask_secret, constant_time_equals…
│   ├── telemetry/  Prometheus-format MetricsRegistry
│   ├── utils/      uuid7() (RFC 9562)
│   └── validation/ parse_uuid, normalize_pagination, parse_iso8601, coerce_enum…
├── infrastructure/          # adapters (import shared; NEVER imported by shared)
│   ├── database/   AtlasBase + ES-003 mixins, DatabaseManager, session dep, UnitOfWork
│   ├── repositories/ SqlAlchemyRepository[ModelT] generic base
│   ├── cache/      RedisManager
│   └── messaging/  KafkaManager (satisfies MessageTransport), OutboxRecord model
├── api/                     # presentation: health.py (/health /ready /live /metrics),
│   └── v1/router.py         # /api/v1 mount point for service API groups
├── apps/                    # one modular service per platform — EMPTY until IP-002+
│   └── (identity/ tenant/ ai/ knowledge/ workflow/ meeting/ decision/ notification/ integration/)
├── workers/                 # Celery app (queue atlas.platform) + platform.ping task
└── tests/unit/shared/       # 86 unit tests; coverage gate ≥95% on shared (currently ~99%)
```

## 2.4 Frontend layout (`frontend/src/`)

`app/` (App Router; route groups `(auth)` → `/auth/login`, `(dashboard)` → `/dashboard`; root `error.tsx`, `loading.tsx`, `not-found.tsx`; `/api/health`) · `components/` (foundation/shared/domain/layout per RA-002) · `features/` (per-domain modules, empty until feature IPs) · `lib/` (`api/client.ts` — the ONLY path to the backend; `auth/`; `logging/`; `utils.ts` with uuid7) · `providers/` (Theme→Query→Auth) · `store/` (Zustand) · `hooks/` · `types/` (exact ES-002 envelope types) · `middleware.ts` (session-aware routing). Stack: TypeScript strict, Tailwind + shadcn/ui (CSS variables, light+dark), TanStack Query, Zustand, React Hook Form + Zod, Apache ECharts, axios, pnpm (corepack-pinned; `.npmrc node-linker=hoisted` for Windows).

## 2.5 Dependency direction (enforced)

```
ALLOWED:                                    FORBIDDEN:
api ──────► core ──► shared                 shared → core | api | infrastructure
api ──────► shared                          shared → frontend | apps | any business module
core ─────► infrastructure ──► shared       infrastructure → core | api
apps/* ───► shared, infrastructure(core-    core → apps/*
            provided deps via DI), core     any circular import
workers ──► shared (+ own app config)       UI components → backend calls (must use lib/api)
frontend/features ──► lib, shared, components   frontend business logic in components
```

- `shared/*` may depend only on: other shared packages, the Python stdlib, approved third-party libs (pydantic), and **Protocol abstractions**. Cross-boundary wiring happens in `core/container.py` via structural typing (e.g., `KafkaManager` satisfies `shared.events.MessageTransport` without shared importing infrastructure).
- Future `apps/<service>/` internals follow RA-001 Clean Architecture: `api → application → domain`, `infrastructure` implements domain-defined interfaces, domain imports **nothing** from outer layers (it may import `shared.exceptions`, `shared.events`, `shared.validation` — those are framework-free by rule).

---

# 3. Repository Invariants — NEVER change these

1. **The governance chain and its conflict rule** (§2.1). Code never overrides documents.
2. **Tenant isolation**: every business table carries `organization_id` (ES-003 §9, `OrganizationScopedMixin`); every domain/integration event carries `organizationId`; every query is tenant-filtered; AI context never crosses organizations (DOMAIN-001 §13). Cross-tenant access is **fail-closed** and a Critical defect (ES-007 §9).
3. **Identifiers**: UUID v7 (RFC 9562) everywhere — `shared.utils.uuid7` (Python) and `lib/utils.ts uuid7()` (TS). Primary keys are immutable and carry no business meaning (ES-003 §5).
4. **Time**: UTC, ISO-8601, timezone-aware (`DateTime(timezone=True)`, `datetime.now(timezone.utc)`).
5. **API envelopes** (ES-002 §7/§17 — byte-exact, mirrored in `shared/contracts/api.py` and `frontend/src/types`):
   - Success: `{"success": true, "data", "metadata", "timestamp", "correlationId"}`
   - Error: `{"success": false, "error": {"code", "message", "details", "correlationId", "timestamp"}}`
   - Correlation header: `X-Correlation-ID` (accepted inbound, echoed outbound, generated UUID v7 when absent).
6. **Error taxonomy** (`shared.exceptions`): `AtlasError` base + Validation(422)/Authentication(401)/Authorization(403)/NotFound(404)/Business(409)/Infrastructure(503)/ExternalService(502)/AI(502). Standard HTTP codes only; internals never leak to clients.
7. **Event contract** (RA-006 §8, `shared.events.EventEnvelope`): nine wire fields `eventId, eventType, eventVersion, timestamp, organizationId, correlationId, producer, payloadSchema, metadata` (+ `payload`, `category`). Event types match `<domain>.<event>.v<n>` (BP-004 §11). Topics are `atlas.<domain>`. Events are **immutable facts**, published **only after successful commit** (RA-001 §13) through the Event Bus — never point-to-point where events are appropriate (BP-002 ED-011).
8. **Persistence rules** (ES-003): soft delete by default (`deleted_at/by/delete_reason`; hard delete requires architectural approval); mandatory audit columns (`created_at/by, updated_at/by, version` with optimistic locking); forward-only reviewed Alembic migrations; parameterized queries only; each service exclusively owns its tables — **no cross-service database writes, ever** (access via APIs/events).
9. **Configuration priority** (IP-001 §10): Environment variables > Secret store > Environment config (`local` above `<env>` above `base`) > code defaults. No hard-coded values; no secrets in git or images (`configs/local/` is ignored and dockerignored).
10. **Sole-entry-point decisions** (BP-002 ED-009/010/011/012): API Gateway is the only ingress; the AI Orchestrator will be the only path to any LLM; the Event Bus is the only event distribution; the Tenant Registry will be the only source of org identity. Do not create parallel paths.
11. **Coverage gates** (ES-001 §14): domain ≥95, business ≥90, API ≥85, infra ≥80, shared libs ≥95 (enforced in `pyproject.toml`, `fail_under=95`). Below gate blocks merge.
12. **Technology stack** (IP-001, locked by lockfiles): Python 3.13+/FastAPI/SQLAlchemy 2 async/Alembic/Pydantic v2/uv · PostgreSQL/Redis/Kafka/Celery · Next.js 15/React 19/TypeScript/pnpm · Docker/K8s/Helm/Terraform/GitHub Actions. Changing any of these requires an ADR + Product Owner approval.
13. **Definition of Done** (ES-001 §21): no TODO/placeholder code in production paths; tests+security+observability+docs before "complete".
14. **The literal string `"Implementation Defined During Engineering"`** is the sanctioned marker for deliberately-deferred specifics in documentation — use it; never invent values to fill documentation gaps.
15. **Conventional commits** `type(scope): summary`; no direct commits to main; every stage/commit is proposed to the Product Owner before executing.

---

# 4. Engineering Principles

- Architecture first; read before writing (§15.2 reading order).
- Priority order: Correctness → Maintainability → Readability → Security → Scalability → Performance (ES-001 §1). Optimization never reduces maintainability.
- Clean Architecture + DDD: business rules only in domain layers; application services coordinate and own transaction boundaries; controllers/UI are thin.
- Event-driven where cross-service or asynchronous; direct calls for synchronous request/response.
- Everything observable from the first commit: structured logs, metrics, health checks are part of any new service's skeleton, not a follow-up (BP-002 ED-014).
- Graceful degradation (ARCH-001 §14): infrastructure outage → log + unhealthy readiness, never process crash; `/live` stays green so orchestrators don't restart-loop.
- Every stage/PR ends with: **verification (actually run it), explanation, git commit recommendation** — and stops for approval.
- If documentation conflicts with itself or with instructions: **stop and ask**; never resolve silently (record the ruling in the execution log/ADR).
- Production quality only; no placeholders; interfaces (typed Protocols) are legitimate deliverables, stubs are not.

---

# 5. Coding Standards

**Naming** (ES-001 §7): Python — PascalCase classes, camelCase *documented* but the implemented codebase uses idiomatic snake_case functions/variables (accepted engineering interpretation; keep consistent with existing code), UPPER_SNAKE constants; DB — snake_case plural tables; TS — camelCase, PascalCase components; wire formats — camelCase keys. Unit tests: `test_<behavior>` inside `Test<Subject>` classes; ES-007 naming intent `method_condition_expectedResult`.

**Typing**: Python `from __future__ import annotations`, full annotations, `Mapped[]` ORM types, `Protocol` + `@runtime_checkable` for contracts, `TypeVar` generics for repositories. TypeScript `strict` mode, no `any` (warn-level lint), discriminated unions for envelopes.

**Logging** (`shared.logging` / `frontend lib/logging`): one JSON object per line — `timestamp, severity, service, logger, message, correlationId, requestId, tenantId, userId` + context fields. TRACE(5) supported. **Never log values of keys in `shared.security.SENSITIVE_KEYS`** (auto-redacted, but don't rely on it — don't pass secrets). Request logs are emitted by middleware; don't duplicate. Uvicorn/Celery loggers route through the platform formatter.

**Errors**: raise `shared.exceptions` types with machine-readable `code` + optional `details=[{field, issue}]`. Handlers in `core/errors.py` render the envelope — never build error JSON by hand. Unexpected exceptions: log with stack, client gets generic 500.

**Validation**: at the boundary, before business logic. FastAPI/Pydantic for request bodies; `shared.validation` for primitives; frontend mirrors with Zod. Reject don't sanitize-and-continue.

**Async rules**: FastAPI handlers and infrastructure I/O are async; SQLAlchemy via `AsyncSession` only; never block the event loop (no sync DB/HTTP in handlers). Celery tasks are sync functions (worker context), must be idempotent and retry-safe. Health checks may be sync or async — the registry handles both.

**Dependency Injection** (IP-001 §11): the `ApplicationContainer` composes everything once; handlers receive dependencies via `Depends(get_settings|get_database|get_redis|get_kafka|get_unit_of_work|get_db_session)`. Handlers never construct managers/clients. New injectable categories get a container attribute + provider function. Bind implementations to shared Protocols in the container, not in shared.

**Events**: create via `EventEnvelope.create(event_type=…, category=…, producer=settings.service_name, organization_id=…, payload=…)` — version derives from the name, correlation from context, tenant enforcement automatic. Publish post-commit via `UnitOfWork.collect_event(envelope)` inside a `async with uow:` block, or directly through the container's publisher for non-transactional (system) events. Register every new event name in the docs of its IP; the Enterprise Event Catalog (RA-006 §21) will formalize this.

**DTOs / wire models**: Pydantic models with camelCase aliases (`populate_by_name=True`); frozen where they represent facts. Success responses built with `success_envelope(data, metadata)`.

**Repositories** (RA-001 §9): subclass `SqlAlchemyRepository[Model]`, declare `model`, add business-oriented queries. Soft-deleted rows are excluded by the base statement; `list()` is pagination-capped; **no business rules in repositories**, no raw SQL string interpolation.

**Services (application layer, future apps/)**: one use case = one transaction = one `UnitOfWork`; publish events by collecting them; call repositories, never sessions of other services; enforce authorization through the shared PDP contract (post-IP-002), never inline permission logic (BP-003 ED-002).

---

# 6. Architecture Decision Summary (reflected in code today)

## 6.1 From the Build Packs (frozen)
- BP-002 ED-001..014: RA layer consumed verbatim; 11-field/9-field/8-column documentation templates; **vendor selection deferred to IPs**; AI Orchestrator sole AI entry; API Gateway sole ingress; Event Bus sole distribution; Tenant Registry authoritative; Zero Trust on every request; every service tenant-aware/secure/observable/event-aware from first deployment.
- BP-003 ED-001..014: Zero Trust posture; central PDP + embedded PEPs; **three identity classes (human/machine/agent)**; cross-tenant assertions default-reject; **fail-closed on authorization unavailability**; Outbox for identity events; immutable audit (audit drop = incident); 11-stage identity lifecycle; five trust boundaries.
- BP-004 ED-001..014: Tenant Registry sole identifier source; org IDs immutable; tenant isolation as a shared library; entitlement cache w/ event invalidation; suspended orgs reject writes / archived read-only at the enforcement layer; AI context never crosses orgs.

## 6.2 From IP-001 (technology)
FastAPI, Next.js App Router, PostgreSQL, Redis, Kafka, Docker, Kubernetes, GitHub Actions, structured logging, health endpoint convention — all "Approved" and implemented.

## 6.3 Sprint-001 session decisions (approved by Product Owner, recorded in the execution log)
- **D-S001-01**: live-infra verification deferred from S1.2B → **discharged in S1.6** (all green-path checks passed).
- S1.4 interpretations: monitoring=health vs telemetry=metrics; `shared/auth` interfaces-only; exceptions relocated with re-exports; pytest(+asyncio,+cov) allowed; **shared/* framework-independence rule** (see §2.5).
- S1.6: dev-only single-node KRaft; dual Kafka listeners (`kafka:19092` internal, `localhost:9092` host); Nginx deferred to ingress; image pins postgres:17-alpine / redis:7-alpine / apache/kafka:3.9.1 / python:3.13-slim / node:22-alpine.

## 6.4 Implemented but not yet ADR-documented (audit findings — write ADR-001 when authorized)
Topic convention `atlas.<domain>`; event version derived from name suffix; `payloadSchema` defaults to event type; camelCase event wire keys; tenant-stamping scope (domain+integration mandatory, platform categories nullable — reconciles BP-002 §14 with RA-006 §4); Kafka message key = organization_id; outbox table schema; auth Protocol signatures; SENSITIVE_KEYS membership; error-category→HTTP-status mapping; pytest companion packages. **Do not silently change any of these; they are load-bearing.**

---

# 7. Configuration Philosophy

- One loader: `shared.config.load_settings()`. Resolution: `configs/base/backend.json` → `configs/<environment>/backend.json` → `configs/local/backend.json` → **Secret layer** (`LocalFileSecretProvider` reading `configs/local/secrets.json`, then `EnvironmentSecretProvider` reading `ATLAS_SECRET_<FIELD>`) → environment variables (`ATLAS_<FIELD>`, plus canonical `DATABASE_URL`/`REDIS_URL`/`KAFKA_BROKER` from IP-002 §18; prefixed beats canonical).
- Environments: exactly `development | testing | staging | production` (selected by `ATLAS_ENVIRONMENT`).
- Validation is fail-fast at load: URL schemes enforced (`postgresql+asyncpg://`, `redis(s)://`); **production refuses `debug=true` or `database_echo=true`**.
- Feature flags: platform-scoped `features` map + `ATLAS_FEATURE_<NAME>` overrides + `settings.feature_enabled(name)`. Tenant-scoped flags belong to IP-003's Entitlement service — do not build them into Settings.
- Introspection: `settings.safe_dump()` only (masks credential fields). Never log raw settings.
- **Never change**: the priority order; the environment set; the no-secrets-in-git/images rule; the injectable `SecretProvider` seam (the future vault provider plugs in there — replace providers, not the loader).

---

# 8. Security Principles

Zero Trust (verify every request; fail-closed — BP-003 ED-005) · least privilege · defense in depth · TLS 1.3 / AES-256 targets (ES-004 §13) · Argon2id for passwords when IP-002 lands · secrets only via the secret layer/vault; never in code, git, images, or logs · redaction via `shared.security` (single authoritative `SENSITIVE_KEYS`) · immutable audit (audit event drop = incident) · security tests block release (SAST/dependency/secret scans arrive with CI in S1.8) · prompt-injection defense and permission-aware RAG are mandatory once AI features land (ES-004 §16–§18) · every identity is one of HUMAN/MACHINE/AGENT (`shared.auth.IdentityClass`) — agents are never disguised as users.

# 9. Multi-tenancy Principles

Organization = tenant = root ownership boundary. Every business object belongs to exactly one organization forever (no transfers). Compose new models with `OrganizationScopedMixin`. Every event (domain/integration), log line (`tenantId`), cache key, metric, and AI context is tenant-stamped. Tenant filtering will be centralized in the Tenant Isolation Enforcement Library (BP-004/IP-003) — until it exists, every query in `apps/*` must filter by organization explicitly, and **isolation tests are mandatory per feature; a failure is a Critical, release-blocking defect** (ES-007 §9). Suspended orgs reject writes; archived orgs are read-only. Authentication is platform-wide; authorization is tenant-scoped; a session binds to exactly one active tenant.

# 10. Event Architecture

Categories (RA-006 §4): domain, integration, system, ai, security, audit, notification. Names: `<domain>.<event>.v<n>` — concrete catalog examples live in BP-004 §11 (`organization.activated.v1`, `subscription.plan_changed.v1`, `tenant.isolation_violation_detected.v1`, …). Envelope + publisher: §3.7/§5. Reliability: acks=all idempotent producer today; the **transactional outbox** (`platform_event_outbox` model exists; migration + drain worker pending) supersedes direct post-commit publishing when a service needs exactly-once-relative-to-state — wire it through the existing `UnitOfWork.event_publisher` seam. Consumers (future) use the Inbox pattern + idempotent processing; never assume global ordering (per-key ordering only); DLQ never silently discards; **audit/security events must never be dropped**.

# 11. Testing Strategy

Pyramid: many unit, fewer integration, few E2E (ES-001 §14). Unit tests: deterministic, no network, no shared mutable state; fakes/doubles for transports (see `FakeTransport` in `tests/unit/shared/test_events.py`). Coverage gates as in §3.11 — enforced by `uv run pytest --cov=shared` (gate hard-fails <95). Integration/E2E/API-contract/performance harnesses arrive in S1.9; OpenAPI is the authoritative API test contract (ES-002 §22); tenant-isolation tests mandatory per business feature; every fixed defect adds a regression test; flaky tests are quarantined and fixed, not deleted. Frontend: Vitest + Playwright (S1.9), accessibility target WCAG 2.2 AA.

# 12. Docker Strategy

Backend image: multi-stage `python:3.13-slim`, `uv sync --frozen`, non-root uid 10001, ships `configs/` (minus `local/`), HEALTHCHECK = `/live` only, exec-form CMD. Worker = same image, Celery command override. Frontend: `node:22-alpine`, corepack-pinned pnpm, Next standalone output, non-root `node`. Dev environment: `deployment/compose/docker-compose.yml`, profiles `infra` (PG 17-alpine, Redis 7-alpine, Kafka 3.9.1 single-node KRaft with dual listeners) and `full` (+ backend, worker, frontend); named volumes; health-gated `depends_on`; canonical env vars; `scripts/dev-up.sh [infra|full]` / `dev-down.sh [--volumes]`. Host tools connect via `localhost:5432/6379/9092`; containers via `postgres:5432 / redis:6379 / kafka:19092`. Production topology, scanning, signing: CI (S1.8) and IP-011 — not compose.

---

# 13. Future Module Guidelines

**Universal recipe for any new platform service (`backend/apps/<name>/`):**

1. Read its governing chain: DOMAIN-xxx → BP-xxx → IP-xxx (mapping below) + RA-001 + relevant ES docs.
2. Module skeleton per its IP §6: `api/ application/ domain/ infrastructure/ repositories/ services/ … events/ workers/ tests/`. Business rules **only** in `domain/`.
3. Models: compose `UUIDPrimaryKeyMixin + OrganizationScopedMixin + AuditColumnsMixin + SoftDeleteMixin` on `AtlasBase`; tables owned exclusively; Alembic migration reviewed.
4. APIs: mount an APIRouter group on `api/v1/router.py` at `/api/v1/<name>`; envelopes via `shared.contracts`; auth via the shared PDP/PEP contracts (post-IP-002); OpenAPI documented in `10_API/`.
5. Events: define names per pattern, publish via UoW collection; consume via idempotent handlers; document producer/consumer in the IP's event tables.
6. Workers: register task modules in `workers/app.py` include list; tasks idempotent.
7. Health: register dependency checks on the container's `HealthRegistry` — do not modify `api/health.py`.
8. Tests: unit + isolation + contract; coverage gates.
9. Frontend feature: `frontend/src/features/<name>/`, backend access only through `lib/api/client`, components from the design system.

**Module → governing documents map (correcting the known off-by-one — trust THIS table):**

| Module | Domain | Build Pack | Impl. Pack | Notes / cautions |
|---|---|---|---|---|
| Authentication / Identity | DOMAIN-002 | **BP-003** | **IP-002** | Implements `shared/auth` Protocols inside `apps/identity`; Argon2id; JWT+refresh; RBAC+ABAC PDP; 3 identity classes; owns `identity/*` tables. First Alembic revision lands here |
| Organizations / Tenancy | DOMAIN-001 | **BP-004** | **IP-003** | Tenant Registry, lifecycle orchestrators, subscription→entitlement, Tenant Isolation Enforcement Library, storage quotas. IP-003 adds "Workspace" — not a DOMAIN entity; flag to Product Owner before modeling it |
| RBAC (authorization) | DOMAIN-002 | BP-003 §8.9/8.10 | IP-002 | Central PDP; PEP library embedded everywhere; deny-by-default; never inline permission checks |
| Meetings | DOMAIN-004 | **BP-008** | **IP-007** | Never calls AI providers directly — everything through the AI platform; transcripts immutable; extraction publishes to decision/knowledge platforms via events |
| Knowledge | DOMAIN-005 | **BP-006** | **IP-005** | Owns ALL knowledge/document/chunk/embedding/vector/citation storage; AI platform consumes, never owns |
| Documents | DOMAIN-005 | BP-006 | IP-005 | Part of Knowledge: ingestion pipeline upload→scan→validate→metadata→chunk→embed→index |
| Search | DOMAIN-005 + RA-008 | BP-006 | IP-005 | Hybrid (semantic+keyword+metadata), permission-filtered, citation-first |
| AI | DOMAIN-010 | **BP-005** | **IP-004** | AI Gateway sole entry; model/prompt/agent/tool registries; guardrails pre+post; HITL; token/cost accounting; provider SDKs only in infrastructure layer |
| Workflow | DOMAIN-003(!) | **BP-007** | **IP-006** | ⚠ BP-007 as authored is a generic workflow engine but BP-ROADMAP assigns it the Project/workspace capability (DOMAIN-003 Project). **Stop and get a governance ruling before implementing** — see §15.4 |
| Notifications | DOMAIN-009 | **BP-010** | **IP-009** | Sole notification path; templates, preferences, retries, escalation; providers behind connectors |
| Integrations | ARCH-006 | **BP-011** | **IP-010** | Connector framework; core never calls third-party APIs directly |
| Billing | — | — | — | ⚠ **No approved documentation exists.** BP-004 explicitly excludes billing execution/payment/invoicing ("Implementation Defined During Engineering"). Do NOT invent a billing module; request governance (new BP/ADR) first. Only the Subscription/Entitlement surfaces of BP-004/IP-003 exist |

# 14. Anti-patterns (prohibited; from RA §25 lists + session rules)

Business logic in controllers/UI/repositories/shared · direct DB access across services or from presentation · hard-coded configuration or secrets · cross-tenant data access · direct LLM/AI-provider calls from business code · hard-coded prompts or model selection outside registries · mutable events, unversioned events, ungoverned event names · bypassing API Gateway / Event Bus / (future) AI Orchestrator or Tenant Registry · framework imports in domain or shared layers · circular dependencies · global mutable state · `SELECT *` / unparameterized SQL / N+1 patterns · hard deletes without approval · silent exception swallowing; error JSON built by hand · logging secrets or full tokens · placeholder code, TODO stubs, "temporary" hacks in production paths · skipping verification ("it should work") · re-implementing anything the platform already provides (config, logging, errors, health, metrics, UoW, repositories, envelopes, uuid7) · inventing features, fields, endpoints, or architecture not present in the governing documents · modifying approved documentation without explicit Product Owner approval · treating this file as authoritative over the governing documents.

---

# 15. AI Prompting Guidelines (for future AI sessions)

## 15.1 Operating contract
Work **stage-gated**: the Product Owner approves each stage before code is written and approves results before the next stage. Every stage ends with (a) real runtime verification you executed, (b) a plain-language explanation of every file/folder touched, (c) a recommended `type(scope): summary` commit message — then **stop and wait**. Never commit/push unless told. Never overwrite files you didn't just create without instruction. If anything conflicts — documents vs documents, documents vs instructions, documents vs code — stop and present the conflict with options.

## 15.2 Context loading order (do this at session start)
1. This file (`docs/AI_Future_Context_Pack.md`) and `CLAUDE.md`.
2. `docs/Sprint-001_Execution_Log.md` (+ later sprint logs) — the authoritative "where are we" record, including decisions like D-S001-01.
3. For the task's layer: its IP → its BP → its DOMAIN → relevant ES → relevant RA. (Use the corrected mapping table in §13, not the stale cross-references.)
4. The existing code you'll extend — read `core/container.py`, `shared/` package `__init__`s, and the nearest analogous implementation before writing anything.
5. `git log --oneline -15` for recent trajectory.

## 15.3 Prompting / execution style that works in this repo
- One stage, one objective, explicit "Do NOT implement" exclusions — honor them literally.
- Derive every design element from a citable source; docstrings in this codebase cite their governing sections (e.g. "IP-001 §14") — continue that practice.
- Prefer extending the platform seams (container providers, health registry, event publisher seam, secret providers, v1 router) over inventing parallel mechanisms.
- Verify by running: start the stack (`scripts/dev-up.sh`), hit endpoints, run `uv run pytest`, check the structured logs. "Compiles" is not verification.
- Report failures honestly, including environment blockers; propose options rather than silently working around them.

## 15.4 Known documentation inconsistencies (do not "fix" silently; ask)
1. **BP↔IP numbering off-by-one** from IP-008 onward (IP-008 mislabels BP-010, IP-009 mislabels BP-011, IP-010 mislabels BP-012; BP-005..008 IRMs point one IP too high; BP-012 cites nonexistent IP-012). Use §13's table.
2. **BP-007 vs BP-ROADMAP §5.8**: authored BP-007 = generic workflow engine; roadmap assigns Project/workspace (DOMAIN-003). Unresolved — needs a governance ruling before IP-006-adjacent work.
3. **MC-000 Repository Index is stale** (old BP statuses, retired IP titles). BP-ROADMAP v1.0.0 and the actual files are authoritative.
4. Minor: domain-title mislabels in BP-008/009/011; ARCH/DOMAIN cross-refs to retired BP names; BP-002 §14 vs RA-006 §4 tenant-stamping tension (reconciled in code per §6.4).
5. `07_ADRs/` empty while rules require ADRs — see §6.4 backlog.

## 15.5 Session hygiene
Update the sprint execution log at stage gates; keep this Context Pack current when invariants/decisions change (with approval); leave the machine clean (stop servers/containers you started); never install software or modify system state without explicit approval.

# 16. Sprint Implementation Rules

Sprints follow IP-000: dependency-first, one IP per sprint (Sprint-002 = IP-002 Identity, … Sprint-011 = IP-011 Production Operations — IP-011 must be authored first). Within a sprint: plan → approval → incremental stages (each: implement → verify → report → approval) → sprint review against the IP's Acceptance Criteria + quality gates 1–5 (IP-000 §16) → execution-log update → commit(s). Deferred verifications get a recorded decision (D-Sxxx-nn pattern) with explicit discharge criteria attached to a later stage. No stage skipping; no starting an IP whose dependencies aren't approved.

# 17. Review Checklist (before every commit)

- [ ] Traceable: every new element cites its governing document/section
- [ ] Layering: no forbidden imports (grep `shared/` for `core|api|infrastructure`); business rules only in domain
- [ ] Tenancy: org scoping on models/queries/events/logs where applicable
- [ ] Envelopes/errors/events use the shared builders — nothing hand-rolled
- [ ] No secrets, no hard-coded config, no TODO/placeholder, no dead code
- [ ] Naming/typing per §5; docstrings with governing citations
- [ ] Tests added/updated; coverage gates pass locally (`uv run pytest --cov=shared`)
- [ ] Backward compatibility preserved (re-exports where things moved)
- [ ] Execution log updated if a stage gate; commit message `type(scope): summary`

# 18. Verification Checklist (before every merge)

- [ ] Full unit suite green; coverage gates met
- [ ] Backend boots: `/live` 200; `/health` `/ready` reflect true dependency state (200 with dev stack up via `scripts/dev-up.sh`; 503 with accurate detail when down)
- [ ] `/metrics` exposes counters; correlation ID propagates (send `X-Correlation-ID`, see it echoed + logged)
- [ ] Error envelope exact on a 404; structured logs are valid JSON with mandatory fields, secrets redacted
- [ ] Alembic migrations apply forward cleanly (when models exist)
- [ ] Kafka publish acknowledged / Celery `platform.ping` round-trip (when eventing/worker paths touched)
- [ ] Frontend: `pnpm type-check` + `pnpm build` clean; `/api/health` 200; affected routes render (when frontend touched)
- [ ] Docker images build; containers healthy (when images/compose touched)
- [ ] No regressions vs the previous stage's verification report

# 19. Common Mistakes (learned in this repository — don't repeat)

1. **Route groups don't create URL segments** — `(auth)/login` serves `/login`, not `/auth/login`; two pages can collide on `/`. Put real segments inside groups.
2. **Envelope drift**: inventing `{meta, errors[], request_id}`-style shapes instead of the exact ES-002 contract broke the first frontend client. Mirror `shared/contracts` exactly.
3. **pytest can't find modules** without `pythonpath=["."]` in `pyproject.toml` — it's already set; don't remove it.
4. **Windows specifics**: pnpm needs `.npmrc node-linker=hoisted` (symlink EPERM); `uv`/`python`/`docker` are not on Git Bash PATH by default (`export PATH="$HOME/.local/bin:/c/Program Files/Docker/Docker/resources/bin:$PATH"`); killed shells can orphan `node`/`uvicorn` processes that squat ports — check `netstat` and `taskkill` stale PIDs before assuming a bind failure is a code bug.
5. **Clearing request context before the outermost error handler runs** strips the correlation ID from 500 envelopes — the middleware intentionally does NOT clear context on the exception path.
6. **`.gitignore` patterns can swallow files you need** (`.env.*` almost excluded `.env.local.example`). Check `git status` actually lists what you created.
7. **Kafka in compose needs dual listeners** — advertising only `localhost:9092` breaks containers; advertising only `kafka:19092` breaks host tools. Both are configured; keep them.
8. **Old servers serving stale builds** during re-verification — always confirm the process you're curling is the one you just built.
9. **peer-dependency drift** (next-themes 0.3 vs React 19) — check peer warnings at install; don't ship with them.
10. **Trusting stale documentation cross-references** (§15.4) instead of the corrected mapping.
11. Forgetting that `/live` must check nothing but the process — putting dependency checks in liveness causes restart loops.
12. Writing "verification" claims without executing them. Every claim in a verification report must correspond to a command actually run.

# 20. Final Repository Philosophy

This repository is built on one bet: **that disciplined, documented, traceable engineering compounds** — the same bet the product itself makes about organizational knowledge. The documentation layer is not bureaucracy; it is the product's memory, and the code is its execution. Every future contributor — human or AI — inherits both the freedom and the constraint that follow: you never need to guess (the answer is written down, or the gap is explicitly marked "Implementation Defined During Engineering"), and you are never entitled to improvise architecture (if it isn't written, you propose, get approval, and write it down first).

When in doubt: read up the chain, ask the Product Owner, record the decision, then build it well — verified, observable, tenant-safe, and traceable. Leave the repository the way you'd want to find it: **more knowledge, zero drift.**

---

*Maintenance: update this document at every sprint close and whenever an invariant, decision, or inconsistency changes state — with Product Owner approval, like any other documentation change.*
