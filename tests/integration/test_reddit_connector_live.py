import os

import pytest

from server.connectors.reddit import RedditConnector

pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    not (os.getenv("REDDIT_CLIENT_ID") and os.getenv("REDDIT_CLIENT_SECRET")),
    reason="Reddit credentials not set",
)
def test_reddit_connector_live_search_all():
    conn = RedditConnector()
    results = conn.search("fastapi", limit=1)
    assert isinstance(results, list)
    assert 0 < len(results) <= 3
    assert results[0].title
    assert results[0].url


@pytest.mark.skipif(
    not (os.getenv("REDDIT_CLIENT_ID") and os.getenv("REDDIT_CLIENT_SECRET")),
    reason="Reddit credentials not set",
)
def test_reddit_connector_live_search_subreddit():
    conn = RedditConnector()
    results = conn.search("pydantic", subreddit="learnpython", limit=1)
    assert isinstance(results, list)
    assert 0 < len(results) <= 3
    assert all(r.subreddit for r in results)
