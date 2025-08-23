from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable, List, Optional

import praw


@dataclass
class RedditSearchResult:
    id: str
    title: str
    url: str
    score: int
    num_comments: int
    created_utc: float
    subreddit: str
    author: Optional[str]


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
    ) -> List[RedditSearchResult]:
        if not query or not query.strip():
            return []

        submissions: Iterable[praw.models.Submission]
        if subreddit:
            sub = self._reddit.subreddit(subreddit)
            submissions = sub.search(query, limit=limit)
        else:
            submissions = self._reddit.subreddit("all").search(query, limit=limit)

        results: List[RedditSearchResult] = []
        for s in submissions:
            results.append(
                RedditSearchResult(
                    id=s.id,
                    title=s.title or "",
                    url=getattr(s, "url", ""),
                    score=int(getattr(s, "score", 0)),
                    num_comments=int(getattr(s, "num_comments", 0)),
                    created_utc=float(getattr(s, "created_utc", 0.0)),
                    subreddit=str(getattr(s, "subreddit", "")),
                    author=getattr(getattr(s, "author", None), "name", None),
                )
            )

        return results
