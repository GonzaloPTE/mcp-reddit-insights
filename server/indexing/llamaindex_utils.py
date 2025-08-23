"""LlamaIndex utility helpers.

This module contains small, focused helpers used to translate internal
domain objects into LlamaIndex primitives.
"""

from __future__ import annotations

from typing import List

from llama_index.core.schema import TextNode

from ..connectors.reddit import RedditSearchResult


class LlamaIndexUtils:
    """Namespace for reusable LlamaIndex-related utilities."""

    @staticmethod
    def map_reddit_results_to_text_nodes(
        results: List[RedditSearchResult], query: str
    ) -> List[TextNode]:
        """Convert Reddit search results into LlamaIndex ``TextNode`` objects.

        Each node carries the post title as text and attaches structured
        metadata that will be persisted to the vector store as payload.

        Parameters
        ----------
        results:
            Collection of ``RedditSearchResult`` items produced by the connector.
        query:
            Original user query, attached as provenance in metadata.

        Returns
        -------
        List[TextNode]
            A list of LlamaIndex nodes ready for embedding and upsert.
        """
        nodes: List[TextNode] = []
        for r in results:
            text = r.title or ""
            node = TextNode(
                text=text,
                id_=r.id,
                metadata={
                    "url": r.url,
                    "score": r.score,
                    "num_comments": r.num_comments,
                    "created_utc": r.created_utc,
                    "subreddit": r.subreddit,
                    "author": r.author,
                    "query": query,
                    "source": "reddit",
                },
            )
            nodes.append(node)
        return nodes
