# reddit-mcp

## Quickstart

Ensure Docker Desktop is running and your `.env` exists (see `.env.example`). Make scripts executable:

```bash
chmod +x infra-only.sh infra-with-app.sh
```

Bring up only infrastructure (Qdrant, Meilisearch, Redis, Prometheus, Grafana):

```bash
./infra-only.sh
```

Bring up infrastructure + FastAPI app (profile `app`):

```bash
./infra-with-app.sh
```

Services:
- Qdrant: http://localhost:6333
- Meilisearch: http://localhost:7700
- Redis: redis://localhost:6379
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin by default)
- App: http://localhost:8000 (health: `/healthz`, metrics: `/metrics`)


