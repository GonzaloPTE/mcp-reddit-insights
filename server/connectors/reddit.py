from __future__ import annotations

import os
from typing import Iterable, List, Optional

import praw

"""Reddit connector returning PRAW models directly."""


class RedditConnector:
    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> None:
        # Resolve credentials strictly from provided args or current environment.
        client_id = client_id or os.getenv("REDDIT_CLIENT_ID")
        client_secret = client_secret or os.getenv("REDDIT_CLIENT_SECRET")
        user_agent = user_agent or os.getenv(
            "REDDIT_USER_AGENT",
            "reddit-mcp/0.1",
        )

        if not client_id or not client_secret:
            raise ValueError(
                "Reddit credentials are required: set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET"
            )

        self._reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )

    def search(
        self,
        query: str,
        subreddit: Optional[str] = None,
        limit: int = 10,
        *,
        include_comments: bool = True,
        comments_limit: Optional[int] = 50,
        comment_sort: Optional[str] = None,
        replace_more_limit: Optional[int] = None,
    ) -> List[praw.models.Submission]:
        if not query or not query.strip():
            return []

        submissions: Iterable[praw.models.Submission]
        if subreddit:
            sub = self._reddit.subreddit(subreddit)
            submissions = sub.search(query, limit=limit)
        else:
            submissions = self._reddit.subreddit("all").search(query, limit=limit)

        results: List[praw.models.Submission] = []
        for s in submissions:
            if include_comments and hasattr(s, "comments"):
                try:
                    if comment_sort:
                        s.comment_sort = comment_sort
                    # Expand MoreComments according to requested strategy
                    s.comments.replace_more(limit=replace_more_limit)
                    # Force full flatten to ensure replies are present in consumers
                    _ = s.comments.list()
                except Exception:
                    pass

            results.append(s)

        return results
