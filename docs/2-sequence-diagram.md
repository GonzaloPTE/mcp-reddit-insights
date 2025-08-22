# Sequence Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant S as MCP Service
    participant RC as Reddit Connector
    participant PP as Preprocessor
    participant VS as Vector Store Index
    participant LLM as Post Processor
    participant MON as Prometheus/Grafana
    participant O as Output Layer

    U->>S: Submit query
    S->>VS: Check existing context
    alt Context sufficient and fresh
        VS-->>S: Return relevant results
    else Context missing or stale
        S->>RC: Fetch new data from Reddit (filtered by date if stale)
        RC->>PP: Return new posts and comments
        PP->>VS: Preprocess and index new content
        VS-->>S: Return combined results
    end
    S->>LLM: Refine and structure response
    LLM->>O: Prepare insights and links
    O->>U: Deliver final answer
    Note over S,MON: Expose /metrics; Prometheus scrapes app:8000
```
