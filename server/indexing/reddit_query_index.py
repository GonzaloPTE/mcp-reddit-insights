"""Reddit query indexing via LlamaIndex + Qdrant.

This module provides a small façade class, ``RedditQueryIndex``, that:
1) fetches posts via the Reddit connector,
2) converts them to LlamaIndex ``TextNode`` objects,
3) embeds and upserts them into a Qdrant collection via ``QdrantVectorStore``.

"""

from __future__ import annotations

from typing import Any, List, Optional

import meilisearch
import qdrant_client
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore

from ..config import settings
from ..connectors.reddit import RedditConnector
from .reddit_index_utils import RedditIndexUtils


class RedditQueryIndex:
    """Index Reddit search results into Qdrant using LlamaIndex.

    Parameters
    ----------
    collection_name:
        Qdrant collection name. Keep consistent per-embedding-dimension.
    embed_model:
        Optional embedding model override. If omitted, the value is derived from
        ``settings.embedding_model_id``. Accepts either a LlamaIndex embedding
        instance or a string alias (e.g., ``"local:BAAI/bge-small-en-v1.5"`` or
        an OpenAI model id).
    """

    def __init__(
        self,
        collection_name: str = "reddit_mcp_posts",
        embed_model: Optional[Any] = None,
    ) -> None:
        self._collection_name = collection_name
        self._client = qdrant_client.QdrantClient(url=settings.qdrant_url)
        # Resolve embed model from config unless explicitly overridden (tests may override).
        # If config contains an HF model id (e.g., "BAAI/bge-small-en-v1.5"),
        # convert to the local alias so LlamaIndex loads the local provider.
        if embed_model is not None:
            self._embed_model = embed_model
        else:
            model_id = settings.embedding_model_id
            if isinstance(model_id, str) and model_id.startswith("local:"):
                self._embed_model = model_id
            elif isinstance(model_id, str) and "/" in model_id:
                # Heuristic: looks like a HF model id -> use local provider
                self._embed_model = f"local:{model_id}"
            else:
                # Could be "default" (Mock/OpenAI in tests) or an OpenAI model id
                self._embed_model = model_id

    def upsert(self, query: str, subreddit: Optional[str] = None, limit: int = 10) -> List[object]:
        """Fetch Reddit results and upsert them into Qdrant and Meilisearch.

        The function is idempotent with respect to repeated titles/IDs being
        embedded; Qdrant will upsert by point id. Caller is responsible for
        choosing ``collection_name`` consistent with the embedding dimension.

        Returns the list of results that were indexed (useful for downstream logs/tests).
        """
        if not query or not query.strip():
            return []

        reddit = RedditConnector(
            client_id=settings.reddit_client_id,
            client_secret=settings.reddit_client_secret,
            user_agent=settings.reddit_user_agent,
        )
        results = reddit.search(
            query=query,
            subreddit=subreddit,
            limit=limit,
            include_comments=True,
            comments_limit=50,
            replace_more_limit=None,
        )
        if not results:
            return []

        # Convert domain objects to LlamaIndex nodes with structured metadata.
        nodes = RedditIndexUtils.map_submissions_to_text_nodes(results, query)

        # Ensure collection exists and upsert using the configured embedding model.
        vector_store = QdrantVectorStore(client=self._client, collection_name=self._collection_name)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        VectorStoreIndex.from_documents(
            nodes, storage_context=storage_context, embed_model=self._embed_model
        )

        # Also index into Meilisearch (BM25) for lexical search.
        # Use the same collection/index name for parity with Qdrant.
        try:
            meili_client = meilisearch.Client(settings.meili_url, settings.meili_master_key)
            index = meili_client.index(self._collection_name)
            documents = RedditIndexUtils.map_submissions_to_meili_documents(results, query)
            task = index.add_documents(documents, "id")
            # Wait for task completion so tests can assert immediate availability.
            task_uid = None
            if isinstance(task, dict):
                task_uid = task.get("taskUid") or task.get("uid")
            else:
                # Support SDKs that return a Task object
                task_uid = (
                    getattr(task, "taskUid", None)
                    or getattr(task, "uid", None)
                    or getattr(task, "task_uid", None)
                )
            if task_uid is not None:
                meili_client.wait_for_task(task_uid)
        except Exception:
            # Best-effort: do not fail the overall indexing if Meilisearch is unavailable.
            pass

        return results
