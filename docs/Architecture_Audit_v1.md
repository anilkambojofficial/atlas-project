# Project ATLAS — Architecture Audit v1

| Field | Value |
|---|---|
| Document ID | AUD-001 |
| Title | Repository-Wide Architecture Audit v1 |
| Scope | Every implementation file as of end of Sprint-001 (S1.1–S1.6): `backend/`, `frontend/`, `configs/`, `deployment/`, `scripts/`, root tooling files |
| Method | Full-file review + mechanical verification (import-direction greps, pattern scans, targeted line-level evidence). No files modified |
| Baseline | Commit `dbe75eb` + S1.6 working tree; 86 unit tests passing, shared coverage 99.08% |
| Assumption | Platform must eventually serve **millions of users** across thousands of tenant organizations |
| Audit posture | Deliberately adversarial ("extremely critical"). Findings marked **(scheduled)** are gaps the sprint plan already assigns to a future stage — they are still listed, ranked, and given hard deadlines, because "scheduled" is not "safe" |
| Date / Auditor | 2026-07-19 / AI Lead Architect session |

**How to read severity:**

- **Critical** — would cause data loss, data divergence, security exposure, or unrecoverable outage in production; must be resolved before the first business feature (IP-002) ships on top of it.
- **High** — correctness or availability defect at scale; must be resolved within Sprint-001 remainder or as an explicit entry gate of the stage that first touches it.
- **Medium** — erodes consistency, operability, or security posture; schedule deliberately.
- **Low** — hygiene, debt, or documentation alignment; batch opportunistically.

---

## 0. Executive Summary

The foundation is **structurally sound where it matters most**: layer purity is mechanically clean (zero `shared→core/api/infrastructure` imports, zero `infrastructure→core/api` imports, no circular dependencies detected), tenancy/audit/soft-delete mixins exist before any business table does, envelopes and error taxonomy are single-sourced, and configuration is genuinely hierarchical with fail-fast validation. This is a better skeleton than most production systems ever retrofit.

The audit nevertheless finds **3 Critical, 6 High, 14 Medium, 13 Low** issues. The dominant theme: **the platform's reliability story is weaker than its structure story.** The event pipeline can silently lose events (C-1) and cannot heal itself after a broker outage (C-2); the highest-risk code (Unit of Work, middleware, Kafka manager) is precisely the code with zero test coverage (H-4); and several defaults that are harmless today (unordered pagination, uncached health probes, `BaseHTTPMiddleware`) become correctness or availability defects exactly when traffic grows. None of these are exotic — all have well-understood fixes, and most are already anticipated by the governing documents (RA-006 §10 outbox, RA-001 §14 resilience, ES-007 test strategy). The gap is sequencing: **several "scheduled" items must be re-classified as entry gates for IP-002**, because building identity — the first producer of real business events and real credentials — on top of C-1/C-2/H-4 would convert latent defects into production incidents.

---

## 1. Critical Findings

### C-1 — Events can be silently lost between commit and publish (no operational Outbox)

- **Category:** Event consistency / Missing abstraction · **Evidence:** `backend/infrastructure/database/unit_of_work.py:55–80` (publish-after-commit; `except Exception … logged` at line 73), `backend/infrastructure/messaging/outbox_model.py` (model exists, **nothing writes it**), no drain worker, no migration.
- **Problem:** `UnitOfWork.commit()` commits the DB transaction, then publishes collected events directly to Kafka. If the process dies, the broker is down, or publish raises between commit and acknowledgment, the state change is durable but the event is **gone forever** — logged, not recovered. RA-006 §10 mandates the transactional outbox precisely for this window. At millions of users this is not an edge case; it is a statistical certainty measured per deploy, per broker rebalance, per pod eviction — producing permanent divergence between services (e.g., an organization activated but downstream platforms never told).
- **Why Critical now:** IP-002 (identity) is the next sprint and produces security-relevant events whose loss is an auditable incident by BP-003 ED ("audit event drop = incident").
- **Fix:** Before the first business event: (1) Alembic migration for `platform_event_outbox`; (2) `UnitOfWork.commit()` writes envelopes to the outbox **inside** the transaction; (3) a Celery-beat (or dedicated loop) drain worker publishes with retry + exponential backoff, marks published, and alerts on age thresholds; (4) keep direct publish only for non-transactional system events. The seam (`UnitOfWork.event_publisher`, `OutboxStore` contract) already exists — this is wiring, not redesign. **Deadline: IP-002 entry gate.**

### C-2 — Kafka producer has no reconnection strategy: transient broker failure at startup = permanent publish outage

- **Category:** Missing abstraction / Scalability · **Evidence:** `backend/infrastructure/messaging/kafka.py` — producer created only in `connect()` at application startup; `grep retry|reconnect` → 0 hits; `publish()` raises `InfrastructureError` when the producer is absent; no re-establishment loop, no circuit breaker anywhere in the codebase.
- **Problem:** If Kafka is unavailable during startup (rolling restart, broker upgrade — routine at scale), the pod comes up degraded-by-design (correct per ARCH-001 §14) but **never recovers**: readiness stays red or, worse, the API serves traffic whose event publishes all fail until a human restarts the pod. RA-001 §14 requires retry/backoff/circuit-breaker resilience patterns; none are implemented for any infrastructure manager (PostgreSQL recovers via `pool_pre_ping`, redis-py reconnects per command — Kafka is the outlier with a connect-once lifecycle).
- **Fix:** Lazy producer (re)creation inside `publish()`/a supervisor task with capped exponential backoff and jitter; classify send-side errors (retriable vs fatal); a minimal circuit breaker that trips readiness. Combined with C-1's outbox, broker outages then degrade to "events delayed", never "events lost". **Deadline: with C-1, IP-002 entry gate.**

### C-3 — Zero authentication surface: every endpoint, `/metrics`, and interactive `/docs` are anonymous and unconditional

- **Category:** Security · **Evidence:** no auth dependency on any route; `backend/core/application.py:83` — `docs_url="/docs"` (and OpenAPI) enabled in **all** environments including production; `/metrics` (route inventory, error rates) unauthenticated; `settings.host` defaults to `0.0.0.0`.
- **Problem:** Sanctioned today (pre-IP-002, no business data exists, D-S001-class posture), but it is one merged business route away from being an exposure. `/metrics` and `/docs` leak internal topology to anyone who can reach the pod; at scale, "reachable" is guaranteed by accident (misconfigured ingress, port-forward left open).
- **Fix:** (1) Gate `docs_url`/`openapi_url`/`redoc_url` on `environment != "production"` (or gateway-authenticated) — one-line, do it in S1.7/S1.8 hardening; (2) restrict `/metrics` to the cluster-internal scrape network in the S1.7 manifests (NetworkPolicy) — never expose via ingress; (3) hard rule recorded now: **no business route merges before the IP-002 PDP/PEP dependency is enforceable on it.** Zero Trust (BP-003 ED-001/005) means the default answer to an unauthenticated request must become 401 the moment identity exists.

---

## 2. High Findings

### H-1 — Repository pagination has no ordering: pages are nondeterministic, and OFFSET pagination will not survive scale

- **Evidence:** `backend/infrastructure/repositories/base.py` — `grep order_by` → **0 hits**; `list()` applies limit/offset to an unordered SELECT.
- **Problem:** Without `ORDER BY`, PostgreSQL guarantees nothing: rows can repeat or vanish across pages as the planner changes. Every future business listing built on this base inherits silent pagination corruption. Separately, OFFSET-based pagination degrades linearly (`OFFSET 1_000_000` scans a million rows) — untenable at target scale.
- **Fix:** (1) Default deterministic ordering in the base — `order_by(model.id)` is ideal because UUID v7 PKs are time-ordered, giving stable, index-backed, creation-time ordering for free; (2) add a keyset (`WHERE id > :cursor LIMIT n`) variant to the base **before** the first business listing endpoint, and make offset mode a bounded convenience (cap already exists via `MAX_PAGE_SIZE`). **Deadline: before IP-002's first list endpoint.**

### H-2 — No CORS policy: the browser cannot call the backend cross-origin at all

- **Evidence:** `grep -ri cors backend --include=*.py` → 6 hits, all in comments/constants — **no `CORSMiddleware` installed**; frontend client targets `http://localhost:8000` from origin `:3000`.
- **Problem:** The first real `fetch` from the frontend will be blocked by the browser. This is simultaneously a functional blocker and an unmade security decision — CORS is an allowlist policy, and ES-002/ARCH-005 leave the topology (same-origin-via-gateway vs. cross-origin allowlist) undecided.
- **Fix:** Decide the topology explicitly (recommended: same-origin through the gateway/ingress in deployed environments — no CORS at all — plus a config-driven `cors_allowed_origins` list, empty by default, for local dev). Wire `CORSMiddleware` from `Settings`, never wildcard with credentials. Needs a documented decision (ADR-001 batch or IP-002 §) — **flagging per the stop-on-gap rule rather than inventing the policy.**

### H-3 — Health endpoints do live, sequential, uncached dependency round-trips on every probe

- **Evidence:** `backend/shared/monitoring/health.py:52–58` — `run_all` awaits each check **serially**; `grep gather` → 0 hits; `/health` and `/ready` both invoke it per request; no TTL cache.
- **Problem:** Worst case latency is the *sum* of dependency timeouts (~12s with all deps down) — Kubernetes probe timeouts will fire on slowness of a *single* dependency. At scale: `replicas × 2 endpoints × probe frequency × 3 dependencies` = a permanent synthetic load storm against PostgreSQL/Redis/Kafka, and a thundering-herd amplifier exactly when a dependency is already sick.
- **Fix:** `asyncio.gather` the checks (bounds latency to the slowest single check); add a short TTL cache (2–5 s) on registry results; keep `/live` process-only (already correct); consider `/ready` consuming cached state while `/health` (ops/diagnostic) may force refresh. **Deadline: S1.7, before Kubernetes probes exist.**

### H-4 — The highest-risk code has zero tests; frontend has zero tests of any kind

- **Evidence:** `find tests -name "test_*.py" | grep -v unit/shared` → **0**; frontend `*.test.*|*.spec.*` → **0**. Untested: `UnitOfWork` (commit/rollback/event collection — the C-1 code path), `RequestContextMiddleware` (correlation propagation, the exception path that was already bug-fixed once in S1.2A), exception handlers (envelope byte-exactness), `SqlAlchemyRepository`, Kafka/Redis/Database managers, Celery tasks, the entire frontend including the ES-002 client that **already drifted once** in S1.3.
- **Problem:** Coverage gates protect `shared/` only. The proven failure mode of this repo (S1.3 envelope drift, S1.2A middleware bug) is exactly in the untested layers. "Scheduled for S1.9" is too late for the pieces IP-002 will immediately build on.
- **Fix:** Pull forward into S1.9-minimum (or earlier): UoW unit tests with fake session/publisher (no infra needed); handler tests via `TestClient` asserting envelope bytes; middleware correlation tests; a frontend↔backend **envelope contract test** (shared JSON fixtures consumed by both pytest and Vitest — see M-13). Full pyramid remains S1.9 scope.

### H-5 — `BaseHTTPMiddleware` is the wrong foundation for a platform that will stream AI responses

- **Evidence:** `backend/core/middleware.py:25,49` — `RequestContextMiddleware(BaseHTTPMiddleware)`.
- **Problem:** Starlette's `BaseHTTPMiddleware` buffers via an internal task/queue, adds measurable per-request overhead, has a history of breaking streaming responses and background-task semantics, and degrades under high concurrency. BP-005/IP-004 mandate streamed LLM output; the request-context middleware wraps **every** request on the hot path.
- **Fix:** Reimplement as a pure ASGI middleware (`__call__(scope, receive, send)`), preserving behavior: contextvars binding, UUID v7 generation, metrics on the `send` of `http.response.start`, and the deliberate no-clear-on-exception rule (regression test it — that bug already happened once). Mechanical rewrite, ~1 day with tests. **Deadline: before IP-004; recommended S1.9 alongside its new tests.**

### H-6 — `collect_event(event: Any)` accepts garbage and drops it silently at publish time

- **Evidence:** `backend/infrastructure/database/unit_of_work.py:50–53` (`event: Any`, appended unvalidated); non-envelope objects are filtered post-commit with only an error log.
- **Problem:** A typo'd or hand-rolled event object survives the transaction and disappears with a log line — the *silent-loss* failure mode again, but caused by developer error and invisible in tests that don't read logs. Fail-fast is free here.
- **Fix:** Type and enforce at collection: `collect_event(self, event: EventEnvelope)` with an `isinstance` raise (`TypeError`) *before* the transaction commits, so bad events fail the use case loudly in development. One-line behavior change + tests.

---

## 3. Medium Findings

| ID | Category | Finding (evidence) | Impact at scale | Recommended fix | When |
|---|---|---|---|---|---|
| M-1 | Config consistency | `Settings(BaseModel)` is **mutable** — no `model_config = ConfigDict(frozen=True)` (`shared/config/settings.py:70`) | Any code can flip `settings.debug` at runtime; config stops being trustworthy state | Freeze the model; tests that mutate must build new instances (they already mostly do) | S1.9 |
| M-2 | Logging consistency / Security | Redaction in the JSON formatter applies `is_sensitive_key` to **top-level extra keys only**; a dict passed as an extra value (e.g. `extra={"payload": {"password": …}}`) is serialized unredacted (`shared/logging/logger.py:22–23` + format body) | One careless log line leaks a credential to the log pipeline | Run `redact_mapping` (already exists in `shared.security`) recursively over dict-valued extras in the formatter | S1.9 |
| M-3 | Logging consistency | Celery workers never call `configure_logging` (`grep workers/*.py` → 0) — worker logs are **not** structured JSON and lack correlation fields | Half the platform's execution (async work) invisible to structured log tooling | `setup_logging`/`worker_process_init` signal in `workers/app.py` invoking the shared `configure_logging`; carry correlation IDs in task headers | S1.9 |
| M-4 | Logging consistency | Duplicate per-request logging: uvicorn access lines *and* middleware request logs both emitted | 2× log volume at millions of requests = real money; noise in analysis | Disable uvicorn access logs (`access_log=False` / log-config) — middleware log is the canonical record | S1.7/S1.8 |
| M-5 | Security | Access/refresh tokens in `sessionStorage` (`frontend/src/lib/api/client.ts:87`, `lib/auth/session.ts:19–20`) — readable by any XSS payload; also tab-scoped (multi-tab logout UX debt) | Token exfiltration is the canonical SaaS breach | IP-002 must deliver httpOnly, Secure, SameSite session cookies via backend (per BP-003 session design); the current storage module is acceptable **only** as a pre-identity placeholder — record that constraint in IP-002's plan | IP-002 |
| M-6 | Security / Frontend | Root error boundary renders `error.message` to end users (`frontend/src/app/error.tsx:26`) | Client-side error internals (API URLs, state) shown to users | Generic message + `error.digest` reference; log the real message via the frontend logger only | S1.9 |
| M-7 | API consistency / Security | `/docs`, `/openapi.json` unconditional (`core/application.py:83`) — subset of C-3, listed for its own one-line fix | Schema disclosure in production | Env-gate; production serves 404 for docs endpoints | S1.7 |
| M-8 | Security / Scalability | No rate limiting anywhere (ES-002 §18 requires it) | Brute-force and scrape exposure the day auth endpoints exist | Confirm the gateway-owns-rate-limiting decision in writing (ADR-001 batch); IP-002 auth endpoints additionally need app-level lockout/backoff regardless of gateway | ADR + IP-002 |
| M-9 | Performance | Container startup connects PG→Redis→Kafka **serially**; worst case ~12 s of stacked timeouts before the app serves `/live` | Slow cold starts × autoscaling = capacity lag during incidents (exactly the wrong moment) | `asyncio.gather` the three `connect()`s with per-dependency timeout | S1.7 |
| M-10 | Code smell / Persistence | `AuditColumnsMixin` injects optimistic locking via `declared_attr __mapper_args__` (`infrastructure/database/base.py:96`); any model that declares its own `__mapper_args__` **silently disables versioning** | Lost-update protection evaporates without warning | Document the merge pattern (`{**AuditColumnsMixin.__mapper_args__(cls), …}`) in the base module; add a CI check/unit test asserting `version_id_col` present on every registered business model | S1.8 (CI) |
| M-11 | Scalability | No DB scale posture beyond defaults: pool 5+10 per pod, no statement timeout, no `pgbouncer` plan, OFFSET pagination (see H-1), no read-replica seam | Connection exhaustion is the classic first scaling wall (pods × pool > PG max_connections) | Record the connection-budget math in IP-011/S1.7 values; add configurable `statement_timeout`; adopt keyset pagination (H-1); plan pooler in IP-011 | S1.7/IP-011 |
| M-12 | Config consistency / Security | Compose falls back to default credentials `:-atlas` (`deployment/compose/docker-compose.yml:38,117,141`) — sanctioned for dev, but the **pattern** must not leak into S1.7 manifests | Default creds in staging/prod = incident | S1.7 rule: Kubernetes manifests take secrets only from `Secret` objects; no defaulted credential fallbacks; add a manifest lint | S1.7 |
| M-13 | API consistency / Tests | No contract test binding `frontend/src/types` to `shared/contracts` — the two ES-002 implementations already diverged once (S1.3) | Envelope drift recurs silently as endpoints multiply | Shared JSON fixture files (golden envelopes) asserted byte-exact by both pytest and Vitest; later, generate TS types from OpenAPI | S1.9 |
| M-14 | Docker / Security | Backend image `COPY`s the whole source tree including `tests/` (root `.dockerignore` has no `tests` entry — grep → 0) | Larger image, larger attack/scan surface, slower pulls at fleet scale | Exclude `backend/tests`, `migrations/README`-class files via `.dockerignore`, or COPY explicit dirs | S1.8 |

---

## 4. Low Findings

| ID | Category | Finding | Recommended fix |
|---|---|---|---|
| L-1 | Naming consistency | ES-001 §7 prescribes camelCase Python methods; the codebase (correctly) uses idiomatic snake_case. An undocumented standing deviation from an ES-layer document | Editorial ES-001 amendment or entry in the ADR-001 batch; do **not** change code |
| L-2 | Config consistency | `Environment` `Literal` in `settings.py` duplicates `VALID_ENVIRONMENTS` in `shared/constants` — two sources for one enumeration | Derive one from the other |
| L-3 | Code smell | `core/health.py` and parts of `core/errors.py` are S1.4 compatibility shims | Migrate importers to `shared.monitoring`/`shared.exceptions`; retire shims by Sprint-002 close |
| L-4 | Layering (judgment) | `KafkaEventPublisher` — a concrete publisher — lives in `shared/events`. Protocol-clean (depends only on `MessageTransport`), but "shared" now hosts an implementation | Acceptable; revisit if it ever grows Kafka-specific logic (then move to `infrastructure/messaging`) |
| L-5 | Code smell | `workers/app.py` calls `load_settings()` at module import (file I/O as an import side effect); `main.py` similarly builds the app at import (conventional for uvicorn) | Wrap worker settings in a lazy accessor; document the `main.py` convention |
| L-6 | Event consistency | `EventEnvelope.timestamp` is an unvalidated `str` on the inbound/parse path | Validate ISO-8601 in a field validator when consumers (Inbox) are built |
| L-7 | Consistency | Two independent `uuid7()` implementations (Python + TypeScript) with no cross-checking | Add both to the M-13 contract fixtures (version/variant bit assertions) |
| L-8 | Frontend | Several canonical deps installed but unused as of S1.6 (ECharts, RHF, Zod, most Radix) — intentional per IP-001, zero bundle cost until imported | None; note for dependency-audit hygiene in S1.8 CI |
| L-9 | Security (doc) | `secure_random_string` truncates `token_urlsafe` output — entropy is ample (~6 bits/char) but the reasoning is undocumented | One docstring sentence stating the entropy math |
| L-10 | Performance | `MetricsRegistry` uses `threading.Lock` on the async hot path — held for dict updates only; correct and cheap today | Acceptable; revisit only if scrape/label volume grows |
| L-11 | Code smell | `SqlAlchemyRepository.get_by_id`/soft-delete filter assume `id`/`deleted_at` attributes without binding the generic to the mixins | Bind `ModelT` to a protocol/base intersection or assert at subclass definition |
| L-12 | Security | Dev default `host="0.0.0.0"` binds all interfaces on developer machines | Default `127.0.0.1` for `development`; containers override via env (already do) |
| L-13 | Tooling | No enforced lint/type toolchain (ruff/mypy config exist-ish but no gate; frontend has ESLint but no CI) | S1.8 CI: ruff + mypy + eslint + `tsc --noEmit` as merge gates |

---

## 5. Clean-Bill Categories (verified, with evidence)

| Requested category | Verdict |
|---|---|
| **Layer violations** | **None found.** Mechanical scan: `shared/` importing `core|api|infrastructure` → 0 hits; `infrastructure/` importing `core|api` → 0 hits. The S1.4 framework-independence rule holds. (Judgment note: L-4.) |
| **Circular dependencies** | **None found.** Import graph is a DAG: `api → core → infrastructure → shared`, with intra-`shared` edges acyclic (`config→security/features/secrets`, `logging→security`, `events→logging/utils` — no back-edges). 30-module import integrity test passes. |
| **Missing interfaces** | Largely satisfied: `SecretProvider`, `MessageTransport`, `EventPublisher`, `OutboxStore`, `TokenVerifier`, `PolicyDecisionPoint` Protocols all exist. Gaps are *implementations*, not interfaces (C-1, C-2) — plus no cache-abstraction protocol yet (Redis is accessed as a manager; acceptable until a second cache consumer exists). |
| **Exception consistency** | Strong. Single taxonomy (`shared.exceptions`), single handler set rendering ES-002 envelopes, no hand-built error JSON found, stack traces log-only. Only note: `BusinessError→409` mapping is an undocumented decision (ADR-001 batch, already registered in CTX-001 §6.4). |
| **API consistency** | Strong within scope: both implemented enveloped surfaces byte-match ES-002; health endpoints unenveloped by documented decision. Open items are H-2 (CORS) and M-7 (docs exposure), not envelope drift. |
| **Naming consistency** | Internally consistent per surface (snake_case Python/DB, camelCase wire/TS, `atlas.<domain>` topics, `<domain>.<event>.v<n>` events). The only defect is standards-vs-code (L-1) and dual enumeration (L-2). |

---

## 6. Scalability Assessment (millions-of-users lens)

**What is already right:** stateless API pods (all state in PG/Redis/Kafka) → horizontal scaling works; UUID v7 keys (no hotspot sequences, time-ordered index locality); tenant column + event keying by `organization_id` (partition-affinity per tenant); async I/O throughout the request path; graceful-degradation startup; images are non-root, slim, health-checked.

**What will break, in the order it will break:**

1. **Event loss/divergence under normal operational churn** (C-1/C-2) — breaks *correctness*, the worst kind of scale failure.
2. **PostgreSQL connection exhaustion** (M-11) — `pods × (5+10)` crosses `max_connections` at modest replica counts; needs budgeted pools + pooler.
3. **Probe-induced dependency load and probe flapping** (H-3).
4. **OFFSET pagination on large tenant datasets** (H-1).
5. **Kafka topology defaults** — no declarative topic provisioning exists; topics materialize via broker auto-creation with default partition counts, so consumer parallelism is accidentally 1. Fix: declarative topic management (partitions/replication/retention per topic) in S1.7/IP-011; single-node KRaft remains dev-only by decision.
6. **Single Celery queue** (`atlas.platform`) — fine now; per-domain queues + priority classes needed as IPs land (each IP should declare its queues).
7. **Middleware overhead** (H-5) on every request.
8. **No caching strategy** — Redis is connected but unused by design; the entitlement cache (BP-004) will be the first consumer; define key-namespace + TTL conventions before two services invent their own (`atlas:<domain>:<org>:<…>` recommended, decide in IP-003).

---

## 7. Remediation Roadmap

| Window | Items | Rationale |
|---|---|---|
| **S1.7 (Kubernetes)** | H-3 (parallel+cached health), M-7 (gate docs), M-4 (uvicorn access logs), M-9 (parallel startup), M-12 (no default creds in manifests), M-11 partial (connection budget, statement timeout), C-3 partial (`/metrics` NetworkPolicy) | These are properties the manifests bake in — cheapest to fix while writing them |
| **S1.8 (CI/CD)** | L-13 (lint/type gates), M-10 (version-lock CI check), M-14 (image trim), L-8 (dep audit) | CI is the natural enforcement point |
| **S1.9 (Testing)** | H-4 (core/infra/frontend tests), H-5 (ASGI middleware rewrite + tests), H-6 (typed `collect_event`), M-1 (frozen Settings), M-2 (deep redaction), M-3 (worker logging), M-6 (error boundary), M-13 (contract fixtures) | Highest-risk-first test debt + the two behavior changes that need tests to land safely |
| **IP-002 entry gate (blocking)** | **C-1 (outbox operational), C-2 (Kafka resilience), H-1 (ordered/keyset pagination), H-2 (CORS decision), C-3 rule (no unauthenticated business routes)** | Identity is the first producer of real events, real lists, real credentials — these must precede it |
| **IP-002 scope** | M-5 (httpOnly sessions), M-8 (auth lockout) | Belong to identity design itself |
| **Governance (ADR-001 batch + editorial)** | L-1, L-2, M-8 decision record, existing CTX-001 §6.4 register | One approval cycle clears all documentation debt |

---

## 8. Category → Findings Index

| Requested category | Findings |
|---|---|
| Layer violations | §5 clean (note L-4) |
| Circular dependencies | §5 clean |
| Code smells | M-10, L-3, L-5, L-11, H-6 |
| Missing abstractions | C-1 (outbox impl), C-2 (resilience), H-1 (keyset pagination), §6.8 (cache conventions) |
| Missing interfaces | §5 (protocols present; C-1/C-2 are missing implementations) |
| Missing tests | H-4, M-13 |
| Security issues | C-3, M-2, M-5, M-6, M-7, M-8, M-12, M-14, L-9, L-12 |
| Performance concerns | H-3, H-5, M-4, M-9, L-10 |
| Scalability concerns | §6; C-1, C-2, H-1, H-3, M-11 |
| Event consistency | C-1, H-6, L-6, §6.5 (topic provisioning) |
| Configuration consistency | M-1, M-12, L-2, L-5 |
| Naming consistency | L-1, L-2, L-7 |
| Logging consistency | M-2, M-3, M-4 |
| Exception consistency | §5 clean (ADR note) |
| API consistency | H-2, M-7, M-13, §5 |

---

*This audit reports state; it changes nothing. Each fix follows the normal stage/approval/verification cadence. Findings C-1, C-2, and the IP-002 entry-gate row of §7 are the audit's headline recommendation.*
