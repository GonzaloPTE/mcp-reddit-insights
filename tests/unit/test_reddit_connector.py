from __future__ import annotations

from types import SimpleNamespace

import pytest

from server.connectors.reddit import RedditConnector


def _fake_submission(**kwargs):
    defaults = dict(
        id="abc123",
        title="Sample Title",
        url="https://example.com",
        score=42,
        num_comments=5,
        created_utc=1720000000.0,
        subreddit="python",
        author=SimpleNamespace(name="someuser"),
    )
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


def test_init_requires_credentials(monkeypatch):
    monkeypatch.delenv("REDDIT_CLIENT_ID", raising=False)
    monkeypatch.delenv("REDDIT_CLIENT_SECRET", raising=False)
    with pytest.raises(ValueError):
        RedditConnector()


def test_search_with_subreddit(monkeypatch):
    # Provide credentials via env so constructor succeeds
    monkeypatch.setenv("REDDIT_CLIENT_ID", "cid")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "csecret")

    # Mock praw.Reddit and its chained calls
    class FakeSubreddit:
        def search(self, query: str, limit: int):
            assert query == "fastapi"
            assert limit == 3
            return [_fake_submission(id="1"), _fake_submission(id="2")]

    class FakeReddit:
        def subreddit(self, name: str):
            assert name == "learnpython"
            return FakeSubreddit()

    import server.connectors.reddit as reddit_mod

    monkeypatch.setattr(reddit_mod, "praw", SimpleNamespace(Reddit=lambda **_: FakeReddit()))

    conn = RedditConnector()
    results = conn.search("fastapi", subreddit="learnpython", limit=3)
    assert len(results) == 2
    assert results[0].id == "1"
    assert results[0].subreddit == "python"
    assert getattr(results[0].author, "name", None) == "someuser"


def test_search_all_subreddits(monkeypatch):
    monkeypatch.setenv("REDDIT_CLIENT_ID", "cid")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "csecret")

    class FakeAll:
        def search(self, query: str, limit: int):
            assert query == "pydantic"
            assert limit == 2
            return [_fake_submission(id="x")]

    class FakeReddit:
        def subreddit(self, name: str):
            assert name == "all"
            return FakeAll()

    import server.connectors.reddit as reddit_mod

    monkeypatch.setattr(reddit_mod, "praw", SimpleNamespace(Reddit=lambda **_: FakeReddit()))

    conn = RedditConnector()
    results = conn.search("pydantic", limit=2)
    assert len(results) == 1
    r = results[0]
    # now returns PRAW Submission objects
    assert hasattr(r, "id") and hasattr(r, "title")
    assert r.url.startswith("https://")


def test_search_empty_query_returns_empty(monkeypatch):
    monkeypatch.setenv("REDDIT_CLIENT_ID", "cid")
    monkeypatch.setenv("REDDIT_CLIENT_SECRET", "csecret")

    class FakeReddit:
        def subreddit(self, name: str):  # pragma: no cover - shouldn't be called
            raise AssertionError("subreddit should not be called for empty query")

    import server.connectors.reddit as reddit_mod

    monkeypatch.setattr(reddit_mod, "praw", SimpleNamespace(Reddit=lambda **_: FakeReddit()))

    conn = RedditConnector()
    assert conn.search("") == []
    assert conn.search("   ") == []
