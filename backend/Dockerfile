# syntax=docker/dockerfile:1
# =============================================================================
# Project ATLAS — Backend image (API + worker; one runtime, command-selected)
#
# Governing documents:
# - IP-001 §16 — multi-stage builds, non-root, minimal base images, health
#   checks, graceful shutdown, immutable versioned images; §16.1 — Python Slim.
# - ES-006 §6/§8 — reproducible builds from the lockfile; no secrets in
#   images; one service per container (the worker runs this same image with
#   a command override — one *runtime*, two containers).
# - IP-001 §10 — the configuration hierarchy ships with the image
#   (configs/ mounted at /app/configs, matching the loader's repo-root
#   resolution); secrets arrive only via environment at runtime.
#
# Build context: repository root (see deployment/compose/docker-compose.yml).
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1 — dependency builder
# ---------------------------------------------------------------------------
FROM python:3.13-slim AS builder

# Pinned toolchain (ES-006 §6)
RUN pip install --no-cache-dir uv==0.11.29

ENV UV_PROJECT_ENVIRONMENT=/opt/atlas/venv \
    UV_LINK_MODE=copy \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app/backend

# Dependency layer first for build caching; --frozen enforces the lockfile.
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev

# ---------------------------------------------------------------------------
# Stage 2 — runtime
# ---------------------------------------------------------------------------
FROM python:3.13-slim AS runtime

LABEL org.opencontainers.image.title="atlas-backend" \
      org.opencontainers.image.description="Project ATLAS backend platform (IP-001)" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.vendor="Project ATLAS"

# Non-root execution (IP-001 §16, ES-006 §8)
RUN groupadd --gid 10001 atlas \
    && useradd --uid 10001 --gid atlas --create-home atlas

ENV PATH="/opt/atlas/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --from=builder /opt/atlas/venv /opt/atlas/venv

WORKDIR /app/backend
COPY --chown=atlas:atlas backend/ /app/backend/
# Configuration hierarchy (IP-001 §10) — resolved relative to /app
COPY --chown=atlas:atlas configs/ /app/configs/

USER atlas
EXPOSE 8000

# Liveness-only probe (RA-001 §21): a failing dependency must gate
# readiness, not restart the process.
HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=5 \
    CMD ["python", "-c", "import urllib.request,sys;sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/live', timeout=3).status==200 else 1)"]

# Exec-form CMD so uvicorn receives SIGTERM directly (graceful shutdown,
# IP-001 §16); the worker container overrides this with the Celery command.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
