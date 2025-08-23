import os
from unittest.mock import patch

from server.indexing.reddit_query_index import RedditQueryIndex


@patch("server.indexing.reddit_query_index.RedditConnector")
def test_index_empty_query(mock_reddit):
    rqi = RedditQueryIndex(collection_name="test_index_empty_query")
    assert rqi.index("") == []


@patch("server.indexing.reddit_query_index.RedditConnector")
def test_index_with_results(mock_reddit):
    os.environ["IS_TESTING"] = "1"

    class DummyResult:
        def __init__(self):
            self.id = "abc"
            self.title = "T"
            self.url = "u"
            self.score = 1
            self.num_comments = 0
            self.created_utc = 0.0
            self.subreddit = "s"
            self.author = "a"

    instance = mock_reddit.return_value
    instance.search.return_value = [DummyResult()]

    rqi = RedditQueryIndex(collection_name="test_index_with_results", embed_model="default")

    out = rqi.index("q", subreddit="s", limit=1)
    assert len(out) == 1
    assert out[0].id == "abc"
