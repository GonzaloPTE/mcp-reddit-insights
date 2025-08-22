#!/usr/bin/env bash
# Purpose: Start infrastructure in containers, then run the app locally with
#          hot-reload using a Python virtualenv (development workflow).

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

"$SCRIPT_DIR/start-infra.sh"
"$SCRIPT_DIR/start-app-dev.sh"

echo "Infrastructure up + local dev app running."


