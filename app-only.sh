#!/usr/bin/env bash
# Purpose: Start ONLY the FastAPI app container (Compose profile `app`).
# Note: This will also start dependent services (Qdrant, Meilisearch, Redis)
# via Docker Compose `depends_on` if they are not running yet.

set -euo pipefail

docker-compose --profile app up -d app
echo "App container (and dependencies if needed) is up."
