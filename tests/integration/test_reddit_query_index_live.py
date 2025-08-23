import pytest

from server.indexing.reddit_query_index import RedditQueryIndex

pytestmark = pytest.mark.integration


def test_index_integration_smoke():
    # Use the same local HF embedding as production default (384 dims) to avoid dim mismatch
    rqi = RedditQueryIndex(collection_name="test_index_integration_smoke")
    # don't assert on results, just ensure it doesn't raise when creds are present
    try:
        rqi.index("reddit mcp", subreddit="mcp", limit=1)
    except ValueError:
        # Missing Reddit creds is acceptable in CI without secrets
        pass
