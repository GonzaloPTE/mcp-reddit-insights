#!/usr/bin/env bash
# Purpose: Start ONLY the FastAPI app container (Compose profile `app`).
# Note: This will also start dependent services (Qdrant, Meilisearch, Redis)
# via Docker Compose `depends_on` if they are not running yet.

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

docker-compose up -d mcp-reddit-insights

echo "App container (and dependencies if needed) is up."
