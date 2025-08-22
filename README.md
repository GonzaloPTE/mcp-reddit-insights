# reddit-mcp

## Quickstart

Ensure Docker Desktop is running and your `.env` exists (see `.env.example`). Make scripts executable:

```bash
chmod +x infra-only.sh infra-with-app.sh app-only.sh app-only-dev.sh infra-with-app-dev.sh
```

Bring up only infrastructure (Qdrant, Meilisearch, Redis, Prometheus, Grafana):

```bash
./infra-only.sh
```

Bring up infrastructure + FastAPI app (profile `app`):

```bash
./infra-with-app.sh
```

Local development (infra in Docker + app with hot-reload locally):

```bash
./infra-with-app-dev.sh
```

Services:
- Qdrant: http://localhost:6333
- Meilisearch: http://localhost:7700
- Redis: redis://localhost:6379
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin by default)
- App: http://localhost:8000 (health: `/healthz`, metrics: `/metrics`)

LLMs and embeddings:
- See `llms.txt` for current defaults and how to override via environment variables.

## Container image (GHCR)

On pushes to `main/master` and tags, CI builds and publishes a Docker image to GitHub Container Registry.

- Image: `ghcr.io/<owner>/<repo>:<tag>` (e.g., `ghcr.io/GonzaloPTE/mcp-reddit-insights:latest`)
- Pull:

```bash
docker pull ghcr.io/GonzaloPTE/mcp-reddit-insights:latest
```

- Run (example):

```bash
docker run --rm -p 8000:8000 \
  -e QDRANT_URL=http://host.docker.internal:6333 \
  -e MEILI_URL=http://host.docker.internal:7700 \
  -e REDIS_URL=redis://host.docker.internal:6379 \
  -e OPENAI_API_KEY=... \
  ghcr.io/GonzaloPTE/mcp-reddit-insights:latest
```

## LLMs

This repo includes an `llms.txt` at the root, following the emerging community proposal for LLM-friendly context files ([Answer.AI proposal](https://raw.githubusercontent.com/AnswerDotAI/llms-txt/refs/heads/main/nbs/index.qmd)).

- Summary: concise project context for inference-time use by LLMs
- Directives (permissive by default):
  - `LLM: *`, `$trainingAllowed: true`, `$chatAllowed: true`, `$embedded: allowed`, `$responseLength: 250`
- Links: curated references to `docs/*.md` for deeper detail

Customize `llms.txt` to fit your policy (e.g., disable training, adjust response length) and keep links current.
