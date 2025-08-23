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
    # Optional rich metadata
    permalink: Optional[str] = None
    selftext: Optional[str] = None
    is_self: Optional[bool] = None
    over_18: Optional[bool] = None
    stickied: Optional[bool] = None
    locked: Optional[bool] = None
    spoiler: Optional[bool] = None
    upvote_ratio: Optional[float] = None
    link_flair_text: Optional[str] = None
    link_flair_template_id: Optional[str] = None
    subreddit_id: Optional[str] = None
    author_fullname: Optional[str] = None
    created: Optional[float] = None
    edited_ts: Optional[float] = None
    num_crossposts: Optional[int] = None
    gilded: Optional[int] = None
    thumbnail: Optional[str] = None
    domain: Optional[str] = None
    fullname: Optional[str] = None
    # Embedded comments (optional, when requested)
    comments: Optional[List["RedditComment"]] = None


@dataclass
class RedditComment:
    id: str
    body: str
    author: Optional[str]
    score: int
    created_utc: float
    parent_id: Optional[str]
    link_id: Optional[str]
    is_submitter: Optional[bool]
    depth: Optional[int]
    controversiality: Optional[int]
    stickied: Optional[bool]
    locked: Optional[bool]
    distinguished: Optional[str]
    subreddit: Optional[str]
    subreddit_id: Optional[str]


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
        replace_more_limit: Optional[int] = 3,
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
            result = RedditSearchResult(
                    id=s.id,
                    title=s.title or "",
                    url=getattr(s, "url", ""),
                    score=int(getattr(s, "score", 0)),
                    num_comments=int(getattr(s, "num_comments", 0)),
                    created_utc=float(getattr(s, "created_utc", 0.0)),
                    subreddit=str(getattr(s, "subreddit", "")),
                    author=getattr(getattr(s, "author", None), "name", None),
                    permalink=getattr(s, "permalink", None),
                    selftext=getattr(s, "selftext", None),
                    is_self=bool(getattr(s, "is_self", False)),
                    over_18=bool(getattr(s, "over_18", False)),
                    stickied=bool(getattr(s, "stickied", False)),
                    locked=bool(getattr(s, "locked", False)),
                    spoiler=bool(getattr(s, "spoiler", False)),
                    upvote_ratio=(
                        float(getattr(s, "upvote_ratio", 0.0))
                        if getattr(s, "upvote_ratio", None) is not None
                        else None
                    ),
                    link_flair_text=getattr(s, "link_flair_text", None),
                    link_flair_template_id=getattr(s, "link_flair_template_id", None),
                    subreddit_id=getattr(s, "subreddit_id", None),
                    author_fullname=getattr(s, "author_fullname", None),
                    created=float(getattr(s, "created", 0.0)),
                    edited_ts=(
                        float(getattr(s, "edited", 0.0)) if getattr(s, "edited", False) else None
                    ),
                    num_crossposts=int(getattr(s, "num_crossposts", 0)),
                    gilded=int(getattr(s, "gilded", 0)),
                    thumbnail=getattr(s, "thumbnail", None),
                    domain=getattr(s, "domain", None),
                    fullname=f"t3_{s.id}" if getattr(s, "id", None) else None,
            )

            if include_comments and hasattr(s, "comments"):
                try:
                    if comment_sort:
                        setattr(s, "comment_sort", comment_sort)
                    # Expand MoreComments according to requested strategy
                    s.comments.replace_more(limit=replace_more_limit)
                    flat = s.comments.list()
                    if comments_limit is not None and comments_limit >= 0:
                        flat = flat[:comments_limit]
                    mapped: List[RedditComment] = []
                    for c in flat:
                        # Some entries could still be MoreComments if limit=0 and not expanded
                        # Guard by presence of 'body'
                        body = getattr(c, "body", None)
                        if body is None:
                            continue
                        mapped.append(
                            RedditComment(
                                id=str(getattr(c, "id", "")),
                                body=body or "",
                                author=getattr(getattr(c, "author", None), "name", None),
                                score=int(getattr(c, "score", 0)),
                                created_utc=float(getattr(c, "created_utc", 0.0)),
                                parent_id=getattr(c, "parent_id", None),
                                link_id=getattr(c, "link_id", None),
                                is_submitter=getattr(c, "is_submitter", None),
                                depth=getattr(c, "depth", None),
                                controversiality=getattr(c, "controversiality", None),
                                stickied=getattr(c, "stickied", None),
                                locked=getattr(c, "locked", None),
                                distinguished=getattr(c, "distinguished", None),
                                subreddit=str(getattr(c, "subreddit", "")) if getattr(c, "subreddit", None) else None,
                                subreddit_id=getattr(c, "subreddit_id", None),
                            )
                        )
                    result.comments = mapped
                except Exception:
                    # Non-fatal if comments cannot be fetched
                    result.comments = []

            results.append(result)

        return results
