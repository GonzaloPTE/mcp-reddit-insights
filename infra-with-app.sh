#!/usr/bin/env bash
set -euo pipefail

docker-compose --profile app up -d
echo "Infrastructure + app profile is up."

