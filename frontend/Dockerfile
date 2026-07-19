# syntax=docker/dockerfile:1
# =============================================================================
# Project ATLAS — Frontend image (Next.js 15 standalone)
#
# Governing documents:
# - IP-001 §16 — multi-stage, non-root, minimal base, health checks,
#   graceful shutdown; §16.1 — Node Alpine build/runtime. (Nginx from
#   §16.1 applies at the ingress layer — S1.7/K8s — because the app uses
#   SSR + middleware and requires the Node runtime; approved S1.6 plan.)
# - ES-006 §6 — reproducible install from pnpm-lock.yaml via the
#   packageManager-pinned pnpm (corepack).
#
# Build context: frontend/ (see deployment/compose/docker-compose.yml).
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1 — build
# ---------------------------------------------------------------------------
FROM node:22-alpine AS builder

WORKDIR /app
RUN corepack enable

# Dependency layer first for caching; frozen lockfile (ES-006 §6).
COPY package.json pnpm-lock.yaml .npmrc ./
RUN pnpm install --frozen-lockfile

COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN pnpm build

# ---------------------------------------------------------------------------
# Stage 2 — runtime
# ---------------------------------------------------------------------------
FROM node:22-alpine AS runtime

LABEL org.opencontainers.image.title="atlas-frontend" \
      org.opencontainers.image.description="Project ATLAS frontend (IP-001 §8)" \
      org.opencontainers.image.version="0.1.0" \
      org.opencontainers.image.vendor="Project ATLAS"

ENV NODE_ENV=production \
    PORT=3000 \
    HOSTNAME=0.0.0.0 \
    NEXT_TELEMETRY_DISABLED=1

WORKDIR /app

# Standalone server + static assets, owned by the built-in non-root user.
COPY --from=builder --chown=node:node /app/.next/standalone ./
COPY --from=builder --chown=node:node /app/.next/static ./.next/static
COPY --from=builder --chown=node:node /app/public ./public

USER node
EXPOSE 3000

HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=5 \
    CMD wget -qO /dev/null http://127.0.0.1:3000/api/health || exit 1

# Exec-form: node receives SIGTERM directly (graceful shutdown, IP-001 §16).
CMD ["node", "server.js"]
