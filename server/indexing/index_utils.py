"""LlamaIndex utility helpers.

This module contains small, focused helpers used to translate internal
domain objects into LlamaIndex primitives.
"""

from __future__ import annotations

from typing import List

from llama_index.core.schema import TextNode

from ..connectors.reddit import RedditComment, RedditSearchResult


class IndexUtils:
    """Namespace for reusable indexing utilities.

    This helper consolidates transformations between internal domain objects
    (e.g., ``RedditSearchResult``) and concrete index payloads for:
    - LlamaIndex ``TextNode`` objects (for Qdrant vector store)
    - Meilisearch documents (for BM25/lexical search)

    The goal is to keep mapping logic centralized, consistent, and easily
    testable, so additions to captured Reddit metadata automatically flow to
    both vector and lexical indices.
    """

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

        Notes
        -----
        The attached metadata includes a broad subset of PRAW ``Submission``
        attributes (e.g., permalink, flair, moderation flags, counts). See
        PRAW ``Submission`` reference for details.
        """
        nodes: List[TextNode] = []
        for r in results:
            # Use the submission body (selftext) as the node content for vector search
            text = getattr(r, "selftext", "") or ""
            node = TextNode(
                text=text,
                id_=r.id,
                metadata={
                    # Preserve the title in metadata for display
                    "title": getattr(r, "title", None),
                    "url": getattr(r, "url", None),
                    "permalink": getattr(r, "permalink", None),
                    "score": getattr(r, "score", None),
                    "num_comments": getattr(r, "num_comments", None),
                    "created_utc": getattr(r, "created_utc", None),
                    "created": getattr(r, "created", None),
                    "edited_ts": getattr(r, "edited_ts", None),
                    "subreddit": getattr(r, "subreddit", None),
                    "subreddit_id": getattr(r, "subreddit_id", None),
                    "author": getattr(r, "author", None),
                    "author_fullname": getattr(r, "author_fullname", None),
                    "is_self": getattr(r, "is_self", None),
                    "over_18": getattr(r, "over_18", None),
                    "stickied": getattr(r, "stickied", None),
                    "locked": getattr(r, "locked", None),
                    "spoiler": getattr(r, "spoiler", None),
                    "upvote_ratio": getattr(r, "upvote_ratio", None),
                    "link_flair_text": getattr(r, "link_flair_text", None),
                    "link_flair_template_id": getattr(r, "link_flair_template_id", None),
                    "num_crossposts": getattr(r, "num_crossposts", None),
                    "gilded": getattr(r, "gilded", None),
                    "thumbnail": getattr(r, "thumbnail", None),
                    "domain": getattr(r, "domain", None),
                    "fullname": getattr(r, "fullname", None),
                    "query": query,
                    "source": "reddit",
                },
            )
            nodes.append(node)
            # Also map any fetched comments into additional nodes
            comments = getattr(r, "comments", None)
            if comments:
                nodes.extend(IndexUtils.map_reddit_comments_to_text_nodes(comments, query))
        return nodes

    @staticmethod
    def map_reddit_results_to_meili_documents(
        results: List[RedditSearchResult], query: str
    ) -> List[dict]:
        """Convert Reddit search results into Meilisearch documents.

        Parameters
        ----------
        results:
            Collection of ``RedditSearchResult`` items produced by the connector.
        query:
            Original user query, attached as provenance in the document payload.

        Returns
        -------
        List[dict]
            A list of plain JSON-serializable dictionaries ready for Meilisearch
            ``add_documents`` ingestion. Documents include:

            - Identity: ``id`` (primary key), ``fullname``
            - Content: ``title``, ``selftext``, ``url``, ``permalink``, ``domain``
            - Subreddit/author: ``subreddit``, ``subreddit_id``, ``author``, ``author_fullname``
            - Timestamps: ``created_utc``, ``created``, ``edited_ts``
            - Moderation/flags: ``over_18``, ``stickied``, ``locked``, ``spoiler``
            - Flair: ``link_flair_text``, ``link_flair_template_id``
            - Counters/scores: ``score``, ``num_comments``, ``num_crossposts``,
              ``gilded``, ``upvote_ratio``
            - Media hints: ``thumbnail``
            - Provenance: ``query``, ``source`` (``"reddit"``)

        Notes
        -----
        These attributes are chosen to support rich filtering/sorting in
        Meilisearch (e.g., by subreddit, author, NSFW flag) and future
        analytical use-cases.
        """
        docs: List[dict] = []
        for r in results:
            docs.append(
                {
                    "id": getattr(r, "id", None),
                    "title": getattr(r, "title", None),
                    "url": getattr(r, "url", None),
                    "permalink": getattr(r, "permalink", None),
                    "score": getattr(r, "score", None),
                    "num_comments": getattr(r, "num_comments", None),
                    "created_utc": getattr(r, "created_utc", None),
                    "created": getattr(r, "created", None),
                    "edited_ts": getattr(r, "edited_ts", None),
                    "subreddit": getattr(r, "subreddit", None),
                    "subreddit_id": getattr(r, "subreddit_id", None),
                    "author": getattr(r, "author", None),
                    "author_fullname": getattr(r, "author_fullname", None),
                    "is_self": getattr(r, "is_self", None),
                    "selftext": getattr(r, "selftext", None),
                    "over_18": getattr(r, "over_18", None),
                    "stickied": getattr(r, "stickied", None),
                    "locked": getattr(r, "locked", None),
                    "spoiler": getattr(r, "spoiler", None),
                    "upvote_ratio": getattr(r, "upvote_ratio", None),
                    "link_flair_text": getattr(r, "link_flair_text", None),
                    "link_flair_template_id": getattr(r, "link_flair_template_id", None),
                    "num_crossposts": getattr(r, "num_crossposts", None),
                    "gilded": getattr(r, "gilded", None),
                    "thumbnail": getattr(r, "thumbnail", None),
                    "domain": getattr(r, "domain", None),
                    "fullname": getattr(r, "fullname", None),
                    "query": query,
                    "source": "reddit",
                }
            )
            # Also map any fetched comments into additional documents
            comments = getattr(r, "comments", None)
            if comments:
                docs.extend(IndexUtils.map_reddit_comments_to_meili_documents(comments, query))
        return docs

    @staticmethod
    def map_reddit_comments_to_text_nodes(
        comments: List[RedditComment], query: str
    ) -> List[TextNode]:
        """Convert Reddit comments into LlamaIndex ``TextNode`` objects.

        The node text contains the comment body. Threading and provenance
        details are attached in metadata for downstream use.
        """
        nodes: List[TextNode] = []
        for c in comments:
            text = getattr(c, "body", "") or ""
            link_id = getattr(c, "link_id", None)
            submission_id = None
            if isinstance(link_id, str) and "_" in link_id:
                try:
                    submission_id = link_id.split("_", 1)[1]
                except Exception:
                    submission_id = None

            node = TextNode(
                text=text,
                id_=getattr(c, "id", None),
                metadata={
                    "kind": "comment",
                    "parent_id": getattr(c, "parent_id", None),
                    "link_id": link_id,
                    "submission_id": submission_id,
                    "author": getattr(c, "author", None),
                    "score": getattr(c, "score", None),
                    "created_utc": getattr(c, "created_utc", None),
                    "is_submitter": getattr(c, "is_submitter", None),
                    "depth": getattr(c, "depth", None),
                    "controversiality": getattr(c, "controversiality", None),
                    "stickied": getattr(c, "stickied", None),
                    "locked": getattr(c, "locked", None),
                    "distinguished": getattr(c, "distinguished", None),
                    "subreddit": getattr(c, "subreddit", None),
                    "subreddit_id": getattr(c, "subreddit_id", None),
                    "query": query,
                    "source": "reddit",
                },
            )
            nodes.append(node)
        return nodes

    @staticmethod
    def map_reddit_comments_to_meili_documents(
        comments: List[RedditComment], query: str
    ) -> List[dict]:
        """Convert Reddit comments into Meilisearch documents.

        Includes threading identifiers and basic moderation/score metadata.
        """
        docs: List[dict] = []
        for c in comments:
            link_id = getattr(c, "link_id", None)
            submission_id = None
            if isinstance(link_id, str) and "_" in link_id:
                try:
                    submission_id = link_id.split("_", 1)[1]
                except Exception:
                    submission_id = None

            docs.append(
                {
                    "id": getattr(c, "id", None),
                    "body": getattr(c, "body", None),
                    "kind": "comment",
                    "parent_id": getattr(c, "parent_id", None),
                    "link_id": link_id,
                    "submission_id": submission_id,
                    "author": getattr(c, "author", None),
                    "score": getattr(c, "score", None),
                    "created_utc": getattr(c, "created_utc", None),
                    "is_submitter": getattr(c, "is_submitter", None),
                    "depth": getattr(c, "depth", None),
                    "controversiality": getattr(c, "controversiality", None),
                    "stickied": getattr(c, "stickied", None),
                    "locked": getattr(c, "locked", None),
                    "distinguished": getattr(c, "distinguished", None),
                    "subreddit": getattr(c, "subreddit", None),
                    "subreddit_id": getattr(c, "subreddit_id", None),
                    "query": query,
                    "source": "reddit",
                }
            )
        return docs
