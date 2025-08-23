import os
from unittest.mock import MagicMock, patch

from server.indexing.reddit_query_index import RedditQueryIndex


@patch("server.indexing.reddit_query_index.RedditConnector")
def test_index_empty_query(mock_reddit):
    rqi = RedditQueryIndex(collection_name="test_index_empty_query")
    assert rqi.index("") == []


@patch("server.indexing.reddit_query_index.meilisearch")
@patch("server.indexing.reddit_query_index.RedditConnector")
def test_index_with_results(mock_reddit, mock_meili):
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

    # Mock Meilisearch client behavior
    mock_client = MagicMock()
    mock_index = MagicMock()
    mock_index.add_documents.return_value = {"taskUid": 123}
    mock_client.index.return_value = mock_index
    mock_meili.Client.return_value = mock_client

    rqi = RedditQueryIndex(collection_name="test_index_with_results", embed_model="default")

    out = rqi.index("q", subreddit="s", limit=1)
    assert len(out) == 1
    assert out[0].id == "abc"

    # Meilisearch client was used to index documents with primary key 'id'
    mock_meili.Client.assert_called()
    mock_client.index.assert_called()
    args, kwargs = mock_index.add_documents.call_args
    assert isinstance(args[0], list) and len(args[0]) == 1
    assert args[1] == "id"
    mock_client.wait_for_task.assert_called_with(123)
