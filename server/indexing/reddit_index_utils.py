"""Reddit indexing mappers.

This module contains helpers to map PRAW models (Submission/Comment) to
LlamaIndex TextNodes (Qdrant) and Meilisearch documents.
"""

from __future__ import annotations

from typing import Any, List

from llama_index.core.schema import TextNode


class RedditIndexUtils:
    """Namespace for reusable indexing utilities.

    Consolidates transformations from PRAW models to:
    - LlamaIndex ``TextNode`` objects (Qdrant vector store)
    - Meilisearch documents (BM25/lexical search)
    """

    @staticmethod
    def map_submissions_to_text_nodes(results: List[Any], query: str) -> List[TextNode]:
        nodes: List[TextNode] = []
        for r in results:
            text = getattr(r, "selftext", "") or ""
            node = TextNode(
                text=text,
                id_=getattr(r, "id", None),
                metadata={
                    "title": getattr(r, "title", None),
                    "url": getattr(r, "url", None),
                    "permalink": getattr(r, "permalink", None),
                    "score": getattr(r, "score", None),
                    "num_comments": getattr(r, "num_comments", None),
                    "created_utc": getattr(r, "created_utc", None),
                    "created": getattr(r, "created", None),
                    "edited_ts": getattr(r, "edited_ts", None),
                    "subreddit": (
                        str(getattr(r, "subreddit", "")) if getattr(r, "subreddit", None) else None
                    ),
                    "subreddit_id": getattr(r, "subreddit_id", None),
                    "author": getattr(getattr(r, "author", None), "name", None),
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
            comments = getattr(r, "comments", None)
            if comments:
                flat_comments = comments
                # If it's a CommentForest, flatten to include all replies
                if hasattr(comments, "list"):
                    try:
                        flat_comments = comments.list()
                    except Exception:
                        flat_comments = list(comments)
                nodes.extend(RedditIndexUtils.map_comments_to_text_nodes(flat_comments, query))
        return nodes

    @staticmethod
    def map_submissions_to_meili_documents(results: List[Any], query: str) -> List[dict]:
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
                    "subreddit": (
                        str(getattr(r, "subreddit", "")) if getattr(r, "subreddit", None) else None
                    ),
                    "subreddit_id": getattr(r, "subreddit_id", None),
                    "author": getattr(getattr(r, "author", None), "name", None),
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
            comments = getattr(r, "comments", None)
            if comments:
                flat_comments = comments
                if hasattr(comments, "list"):
                    try:
                        flat_comments = comments.list()
                    except Exception:
                        flat_comments = list(comments)
                docs.extend(RedditIndexUtils.map_comments_to_meili_documents(flat_comments, query))
        return docs

    @staticmethod
    def map_comments_to_text_nodes(comments: List[Any], query: str) -> List[TextNode]:
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
                    "author": getattr(getattr(c, "author", None), "name", None),
                    "score": getattr(c, "score", None),
                    "created_utc": getattr(c, "created_utc", None),
                    "is_submitter": getattr(c, "is_submitter", None),
                    "depth": getattr(c, "depth", None),
                    "controversiality": getattr(c, "controversiality", None),
                    "stickied": getattr(c, "stickied", None),
                    "locked": getattr(c, "locked", None),
                    "distinguished": getattr(c, "distinguished", None),
                    "subreddit": (
                        str(getattr(c, "subreddit", "")) if getattr(c, "subreddit", None) else None
                    ),
                    "subreddit_id": getattr(c, "subreddit_id", None),
                    "query": query,
                    "source": "reddit",
                },
            )
            nodes.append(node)
        return nodes

    @staticmethod
    def map_comments_to_meili_documents(comments: List[Any], query: str) -> List[dict]:
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
                    "author": getattr(getattr(c, "author", None), "name", None),
                    "score": getattr(c, "score", None),
                    "created_utc": getattr(c, "created_utc", None),
                    "is_submitter": getattr(c, "is_submitter", None),
                    "depth": getattr(c, "depth", None),
                    "controversiality": getattr(c, "controversiality", None),
                    "stickied": getattr(c, "stickied", None),
                    "locked": getattr(c, "locked", None),
                    "distinguished": getattr(c, "distinguished", None),
                    "subreddit": (
                        str(getattr(c, "subreddit", "")) if getattr(c, "subreddit", None) else None
                    ),
                    "subreddit_id": getattr(c, "subreddit_id", None),
                    "query": query,
                    "source": "reddit",
                }
            )
        return docs
