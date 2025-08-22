#!/usr/bin/env bash
set -euo pipefail

docker-compose up -d qdrant meilisearch redis prometheus grafana
echo "Infrastructure is up."

