# Requirements Specification Document

## 1. Executive Summary

The project is a Python-based Model Context Protocol (MCP) service designed to extract and analyze Reddit content. The system supports searching subreddit posts and comments based on user queries, with optional user-level exploration. To ensure relevance and efficiency, queries are decomposed into semantically meaningful subqueries before execution. Retrieved results are indexed in a vector store for compact contextual retrieval. The system transparently manages data freshness by refreshing content when indexed results become outdated. Advanced features include hybrid retrieval strategies, temporal weighting, preprocessing, and post-processing with LLMs. Scalability and maintainability, including caching, expiration policies, and incremental updates, are essential design considerations.

---

## 2. Scope

The system will allow users to input a query and receive relevant Reddit content enriched with insights. The service is intended for information retrieval, trend discovery, and domain-specific research. Extensions such as expert user identification, community detection, and sentiment analysis are optional enhancements.

---

## 3. Functional Requirements

### 3.1 Core Functionality

* FR-1: The MCP shall be implemented in Python.
* FR-2: The system shall connect to Reddit and retrieve posts and comments from specific subreddits.
* FR-3: The system shall support optional retrieval of posts and comments from specific Reddit users.
* FR-4: The system shall decompose an initial user query into multiple subqueries before executing searches.
* FR-5: The system shall index retrieved content in a vector store to reduce contextual load.

### 3.2 Query Enrichment

* FR-6: The system shall support semantic expansion of queries (e.g., synonyms, related terms).
* FR-7: The system shall support entity-aware query splitting (NER-based).

### 3.3 Indexing and Retrieval

* FR-8: The system shall support hybrid retrieval combining lexical (BM25) and semantic (embeddings) search.
* FR-9: The system shall apply temporal weighting to prefer recent content.
* FR-10: The system shall support multi-vector indexing, separately embedding posts, comments, and users.

### 3.4 Preprocessing

* FR-11: The system shall chunk long posts and comments into coherent fragments before indexing.
* FR-12: The system shall deduplicate retrieved results.
* FR-13: The system shall generate short summaries for posts and discussion threads.

### 3.5 Post-processing and User Experience

* FR-14: The system shall re-rank results using an LLM based on contextual relevance.
* FR-15: The system shall generate structured outputs, including:

  * FR-15.1: Key arguments or perspectives (e.g., pros/cons)
  * FR-15.2: Trend identification
  * FR-15.3: Identification of relevant or authoritative users
* FR-16: The system shall provide both raw links and synthesized insights as output.

### 3.6 Scalability and Maintenance

* FR-17: The system shall implement caching for frequent or similar queries.
* FR-18: The system shall manage Reddit API rate limits using queues and backoff strategies.
* FR-19: The system shall support incremental vector store updates without full re-indexing.
* FR-20: The system shall enforce an expiration policy for indexed content.
  * FR-20.1: Each indexed item shall store a timestamp of retrieval.
  * FR-20.2: If indexed content exceeds a configurable expiration period, the system shall trigger a refresh from Reddit.
  * FR-20.3: The refresh shall request only new or updated content (filtered by date) and merge it with existing indexed data.

### 3.7 Extensions (Optional / Future Work)

* FR-21: The system may identify expert users within a domain.
* FR-22: The system may detect emerging communities (growing subreddits related to the query).
* FR-23: The system may perform sentiment analysis on retrieved content.

---

## 4. Non-Functional Requirements

* NFR-1: **Performance**: Query processing and indexing shall be efficient enough to handle multiple concurrent requests without significant latency.
* NFR-2: **Scalability**: The architecture shall support growth in the number of indexed posts/comments and the number of users.
* NFR-3: **Reliability**: The system shall handle Reddit API rate limits gracefully to avoid service disruption.
* NFR-4: **Maintainability**: The system shall be modular, allowing independent updates to the query, indexing, and post-processing components.
* NFR-5: **Extensibility**: The design shall allow new analysis features (e.g., sentiment, community detection) to be integrated with minimal rework.
* NFR-6: **Data Freshness**: The system shall prioritize recent and up-to-date Reddit content in responses.
* NFR-7: **Usability**: Results shall be presented in both raw (links) and synthesized (insights) forms for ease of use.

---

## 5. Related Documentation

- Configuration parameters: see `docs/5-configuration.md`.
- Technology choices and local stack: see `docs/4-technology.md`.
- Deployment view: see `docs/3-deployment-diagram.md`.