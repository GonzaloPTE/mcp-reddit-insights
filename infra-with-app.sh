#!/usr/bin/env bash
set -euo pipefail

# Bring up infra first for clearer logs and readiness
./infra-only.sh

# Then bring up the app container (profile `app`)
./app-only.sh
echo "Infrastructure + app are up."
