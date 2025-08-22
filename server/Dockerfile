FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

COPY server/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Configure spaCy models via build args (defaults: en,es and small size)
ARG NER_LANGUAGES=en,es
ARG SPACY_MODEL_SIZE=sm
ENV NER_LANGUAGES=${NER_LANGUAGES}
ENV SPACY_MODEL_SIZE=${SPACY_MODEL_SIZE}

# Install requested spaCy models
RUN python - <<'PY'
import os, sys, subprocess

languages = os.environ.get('NER_LANGUAGES', 'en,es')
size = os.environ.get('SPACY_MODEL_SIZE', 'sm')

lang_to_base = {
    'en': 'en_core_web_',
    'es': 'es_core_news_',
}

for raw in languages.split(','):
    code = raw.strip()
    base = lang_to_base.get(code)
    if not base:
        print(f"[warn] Unsupported spaCy language '{code}', skipping")
        continue
    pkg = f"{base}{size}"
    print(f"[info] Installing spaCy model: {pkg}")
    subprocess.check_call([sys.executable, '-m', 'spacy', 'download', pkg])
PY

COPY server /app

EXPOSE 8000

CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]
