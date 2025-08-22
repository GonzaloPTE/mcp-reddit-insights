# Technology Choices

This document outlines the selected open-source technologies for local development and deployment of the Reddit MCP service.

## Service and Language

- Python service using FastAPI + Uvicorn.
- Configuration via environment variables and/or `.env` using Pydantic Settings.
- Retries/backoff handled with `tenacity` or `asyncio` + custom backoff.

## Vector Store (Semantic Search)

- Qdrant (containerized) as the primary vector database.
- Pros: fast HNSW ANN, filters, simple API, good local/prod parity.
- Default HTTP port: 6333 (gRPC: 6334).

## Lexical Search (BM25)

- Meilisearch (containerized) for BM25-based lexical retrieval.
- Pros: lightweight, fast, easy setup.
- Default port: 7700.

## Cache

- Redis (containerized) for caching query results, simple queues, and rate limiting support.
- Default port: 6379.

## Metrics and Visualization

- Prometheus for metrics collection.
- Grafana for dashboarding and visualization.
- Initial scrape targets include Prometheus itself; application and service exporters can be added later.

## LLM and Embeddings (External Provider)

- OpenAI as the initial external provider.
- LLM: `gpt-5-nano`.
- Embeddings: OpenAI embeddings model (e.g., `text-embedding-3-large`).
- API keys provided via environment variables.

## Work Queue

- Simple local queue using `asyncio` with backoff for transient failures (no external broker in local dev).

## NLP Preprocessing

- spaCy with NER enabled for entity-aware query splitting and preprocessing.

## Local Orchestration

- Docker Compose to provision Qdrant, Meilisearch, Redis, Prometheus, and Grafana locally.
- Persist data with named volumes.

### Quickstart

1. Ensure Docker Desktop is running.
2. From the repository root:

```bash
docker-compose up -d
```

Services:
- Qdrant: http://localhost:6333
- Meilisearch: http://localhost:7700
- Redis: redis://localhost:6379
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (default user: admin / admin)

Environment:
- Use `.env` (see `.env.example`) for secrets like `OPENAI_API_KEY`, `MEILI_MASTER_KEY`, optional `REDIS_PASSWORD`, `QDRANT_API_KEY`.
- Helper scripts: `infra-only.sh` (infra only) and `infra-with-app.sh` (infra + app profile).

Notes:
- Add application metrics endpoints and exporters as needed and update Prometheus scrape configs accordingly.

