#!/usr/bin/env bash
# =============================================================================
# Project ATLAS — start the development environment (Stage S1.6)
# Usage: scripts/dev-up.sh [infra|full]     (default: infra)
# Governing documents: IP-001 §16, ES-006 §11, approved S1.6 plan.
# =============================================================================
set -euo pipefail

PROFILE="${1:-infra}"
if [[ "$PROFILE" != "infra" && "$PROFILE" != "full" ]]; then
    echo "Usage: $0 [infra|full]" >&2
    exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/../deployment/compose/docker-compose.yml"

echo "Starting Project ATLAS development environment (profile: $PROFILE)…"
docker compose -f "$COMPOSE_FILE" --profile "$PROFILE" up -d --wait
docker compose -f "$COMPOSE_FILE" --profile "$PROFILE" ps
