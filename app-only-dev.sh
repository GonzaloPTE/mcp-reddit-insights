#!/usr/bin/env bash
# Purpose: Run the MCP app locally with hot-reload while using the already-running
#          infrastructure (Qdrant, Meilisearch, Redis). This speeds up development
#          loops versus running everything in containers.

set -euo pipefail

# Load environment variables from .env if present (for OPENAI_API_KEY, etc.)
if [ -f ./.env ]; then
  set -a
  . ./.env
  set +a
fi

# Sensible local defaults if not provided
export QDRANT_URL="${QDRANT_URL:-http://localhost:6333}"
export MEILI_URL="${MEILI_URL:-http://localhost:7700}"
export REDIS_URL="${REDIS_URL:-redis://localhost:6379}"
export LOG_LEVEL="${LOG_LEVEL:-DEBUG}"
export PORT="${PORT:-8000}"
export NER_LANGUAGES="${NER_LANGUAGES:-en,es}"

# Create and activate a Python virtual environment
if [ ! -d .venv ]; then
  echo "[info] Creating virtual environment at .venv"
  python -m venv .venv
fi
# shellcheck disable=SC1091
if [ -f .venv/bin/activate ]; then
  . .venv/bin/activate
elif [ -f .venv/Scripts/activate ]; then
  . .venv/Scripts/activate
else
  echo "[error] Could not find virtualenv activate script (.venv/bin/activate or .venv/Scripts/activate)" >&2
  exit 1
fi

python -m pip install --upgrade pip >/dev/null

# Ensure Python deps available
python -m pip install -r server/requirements.txt

# Ensure spaCy models for configured languages
IFS=',' read -r -a __NER_LANGS <<<"${NER_LANGUAGES}"
for lang in "${__NER_LANGS[@]}"; do
  lang_trimmed=$(echo "$lang" | xargs)
  case "$lang_trimmed" in
    en)
      pkg="en_core_web_sm"
      ;;
    es)
      pkg="es_core_news_sm"
      ;;
    *)
      echo "[warn] Unsupported NER language: $lang_trimmed (skipping)"
      continue
      ;;
  esac
  python - <<PY
import spacy
try:
    spacy.load("${pkg}")
    print("[ok] spaCy model ${pkg} is available")
except Exception:
    import sys, subprocess
    print("[info] Installing spaCy model ${pkg}...")
    code = subprocess.call([sys.executable, "-m", "spacy", "download", "${pkg}"])
    sys.exit(code)
PY

done

echo "[run] Starting FastAPI with reload on port ${PORT}"
exec uvicorn server.main:app --host 0.0.0.0 --port "${PORT}" --reload
