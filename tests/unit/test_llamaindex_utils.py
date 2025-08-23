from server.connectors.reddit import RedditSearchResult
from server.indexing.llamaindex_utils import LlamaIndexUtils


def test_map_reddit_results_to_text_nodes_basic():
    results = [
        RedditSearchResult(
            id="abc123",
            title="Hello World",
            url="https://reddit.com/r/test/abc123",
            score=42,
            num_comments=3,
            created_utc=1700000000.0,
            subreddit="test",
            author="user1",
        )
    ]

    nodes = LlamaIndexUtils.map_reddit_results_to_text_nodes(results, query="hello")
    assert len(nodes) == 1
    n = nodes[0]
    assert n.text == "Hello World"
    assert n.metadata["url"].endswith("abc123")
    assert n.metadata["query"] == "hello"
    assert n.metadata["source"] == "reddit"


def test_map_reddit_results_to_text_nodes_empty_title():
    results = [
        RedditSearchResult(
            id="x1",
            title="",
            url="https://reddit.com/x1",
            score=0,
            num_comments=0,
            created_utc=0.0,
            subreddit="test",
            author=None,
        )
    ]

    nodes = LlamaIndexUtils.map_reddit_results_to_text_nodes(results, query="q")
    assert len(nodes) == 1
    assert isinstance(nodes[0].text, str)
    assert nodes[0].text == ""
