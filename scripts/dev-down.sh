#!/usr/bin/env bash
# =============================================================================
# Project ATLAS — stop the development environment (Stage S1.6)
# Usage: scripts/dev-down.sh [--volumes]   (--volumes also removes data)
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/../deployment/compose/docker-compose.yml"

ARGS=(down --remove-orphans)
if [[ "${1:-}" == "--volumes" ]]; then
    ARGS+=(--volumes)
fi

docker compose -f "$COMPOSE_FILE" --profile infra --profile full "${ARGS[@]}"
