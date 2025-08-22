#!/usr/bin/env bash
# Purpose: Start infrastructure in containers, then run the app locally with
#          hot-reload using a Python virtualenv (development workflow).

set -euo pipefail

./infra-only.sh
./app-only-dev.sh

echo "Infrastructure up + local dev app running."


