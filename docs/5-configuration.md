# Configuration

This document lists configurable parameters for the Reddit MCP service. Parameters should be adjustable via environment variables and/or a configuration file to tune freshness, performance, retrieval quality, and optional features.

| Parameter | Default | Range/Type | Description | Related Requirements |
|---|---|---|---|---|
| EXPIRATION_DAYS | 14 | int ≥ 0 | Expiration threshold for indexed content; triggers refresh when exceeded. | FR-20, FR-20.1–20.3, NFR-6 |
| CACHE_TTL_SECONDS | 3600 | int ≥ 0 | TTL for query-result cache entries. | FR-17, NFR-1 |
| CACHE_MAX_ENTRIES | 10000 | int ≥ 0 | Max items stored in cache to prevent unbounded growth. | FR-17, NFR-2 |
| MAX_CONTEXT_SIZE_TOKENS | 4000 | int ≥ 512 | Upper bound for tokens returned to LLM/ranking. | FR-14, FR-16, NFR-1 |
| QUERY_MAX_SUBQUERIES | 5 | int ≥ 1 | Maximum number of subqueries generated per user query. | FR-4 |
| QUERY_ENABLE_SEMANTIC_EXPANSION | true | bool | Toggle semantic expansion (synonyms/related terms). | FR-6 |
| QUERY_ENABLE_ENTITY_SPLIT | true | bool | Toggle entity-aware query splitting (NER). | FR-7 |
| SUBREDDITS_ALLOWLIST | [] | list[str] | Restrict searches to specific subreddits if provided. | FR-2, NFR-5 |
| USERS_ALLOWLIST | [] | list[str] | Optional list of Reddit users to include. | FR-3 |
| MAX_REDDIT_ITEMS_PER_REQUEST | 100 | 1–100 | Cap on items fetched per API request. | FR-2, FR-3, NFR-1 |
| RATE_LIMIT_MAX_CALLS_PER_MINUTE | 60 | int ≥ 1 | Client-side throttle to respect Reddit rate limits. | FR-18, NFR-3 |
| RATE_LIMIT_WINDOW_SECONDS | 60 | int ≥ 1 | Time window for the above throttle. | FR-18, NFR-3 |
| BACKOFF_INITIAL_SECONDS | 1 | float ≥ 0 | Initial backoff delay for retry strategy. | FR-18, NFR-3 |
| BACKOFF_MAX_SECONDS | 60 | float ≥ 0 | Maximum backoff delay. | FR-18, NFR-3 |
| RETRY_MAX_ATTEMPTS | 5 | int ≥ 0 | Maximum retry attempts for transient failures. | FR-18, NFR-3 |
| QUEUE_CONCURRENCY | 4 | int ≥ 1 | Parallelism for Reddit fetch and indexing tasks. | NFR-1, NFR-2 |
| CHUNK_MAX_TOKENS | 512 | int ≥ 64 | Max chunk size for posts/comments before indexing. | FR-11 |
| CHUNK_OVERLAP_TOKENS | 64 | int ≥ 0 | Overlap between contiguous chunks. | FR-11 |
| DEDUP_SIMILARITY_THRESHOLD | 0.92 | 0–1 | Similarity threshold for deduplication. | FR-12 |
| SUMMARIZATION_MAX_TOKENS | 128 | int ≥ 16 | Target length for generated summaries. | FR-13 |
| EMBEDDING_MODEL_ID | text-embedding-3-large | str | Embedding model identifier. | FR-5, FR-8, FR-10 |
| EMBEDDING_DIM | 3072 | int ≥ 128 | Dimensionality of embedding vectors. | FR-5, FR-10 |
| BM25_TOP_K | 200 | int ≥ 1 | Number of documents considered by BM25. | FR-8 |
| SEMANTIC_TOP_K | 200 | int ≥ 1 | Number of documents considered by embedding search. | FR-8 |
| HYBRID_ALPHA | 0.5 | 0–1 | Weight between lexical and semantic scores. | FR-8 |
| TEMPORAL_DECAY_HALF_LIFE_DAYS | 7 | float > 0 | Half-life for recency weighting of results. | FR-9, NFR-6 |
| MULTIVECTOR_ENABLE_USERS | true | bool | Toggle separate user-level embeddings. | FR-10 |
| MULTIVECTOR_ENABLE_POSTS | true | bool | Toggle separate post-level embeddings. | FR-10 |
| MULTIVECTOR_ENABLE_COMMENTS | true | bool | Toggle separate comment-level embeddings. | FR-10 |
| RERANK_TOP_K | 20 | int ≥ 1 | Items passed to LLM for re-ranking. | FR-14, NFR-1 |
| LLM_MODEL_ID | gpt-5-nano | str | LLM used for re-ranking and insight generation. | FR-14, FR-15, FR-16 |
| LLM_TEMPERATURE | 0.2 | 0–2 | Creativity for LLM post-processing. | FR-14, FR-15, FR-16 |
| VECTOR_STORE_PROVIDER | qdrant | enum[faiss,qdrant,pgvector,...] | Vector index backend. | FR-5, FR-19, NFR-2 |
| VECTOR_STORE_COLLECTION_PREFIX | reddit_mcp | str | Prefix/namespace for collections. | FR-5, FR-19 |
| INDEX_BATCH_SIZE | 128 | int ≥ 1 | Batch size for indexing operations. | FR-19, NFR-1 |
| INDEX_REFRESH_CRON | 0 */6 * * * | cron str | Periodic job to refresh stale indices. | FR-20, NFR-6 |
| LOG_LEVEL | INFO | enum[DEBUG,INFO,WARN,ERROR] | Logging verbosity. | NFR-4 |
| ENABLE_METRICS | true | bool | Expose performance/usage metrics. | NFR-1, NFR-2 |
| METRICS_EXPORTER | prometheus | enum[prometheus,otlp,none] | Metrics sink. | NFR-1, NFR-2 |
| ENABLE_TRACING | false | bool | Distributed tracing toggle. | NFR-1, NFR-4 |
| USER_AGENT | reddit-mcp/0.1 | str | Client user agent for Reddit API. | FR-18, NFR-3 |

Notes:
- Defaults are indicative and may be tuned during implementation and benchmarking.
- When a parameter toggles an optional feature (e.g., expert detection, sentiment), it shall default to disabled unless explicitly enabled.

### Service Endpoints and Secrets

| Parameter | Default | Type | Description |
|---|---|---|---|
| QDRANT_URL | http://localhost:6333 | str | Qdrant HTTP endpoint |
| QDRANT_API_KEY | (empty) | str | Optional API key for Qdrant |
| MEILI_URL | http://localhost:7700 | str | Meilisearch HTTP endpoint |
| MEILI_MASTER_KEY | dev-master-key | str | Master key for Meilisearch (dev) |
| REDIS_URL | redis://localhost:6379 | str | Redis connection URL |
| OPENAI_API_KEY | (empty) | str | API key for OpenAI |

