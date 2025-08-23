from types import SimpleNamespace

from server.indexing.reddit_index_utils import RedditIndexUtils


def test_map_submissions_to_text_nodes_basic():
    results = [
        SimpleNamespace(
            id="abc123",
            title="Hello World",
            url="https://reddit.com/r/test/abc123",
            score=42,
            num_comments=3,
            created_utc=1700000000.0,
            subreddit="test",
            author="user1",
            permalink="/r/test/comments/abc123/hello_world/",
            is_self=True,
            selftext="Body text",
        )
    ]

    nodes = RedditIndexUtils.map_submissions_to_text_nodes(results, query="hello")
    assert len(nodes) == 1
    n = nodes[0]
    assert n.text == "Body text"
    assert n.metadata["url"].endswith("abc123")
    assert n.metadata["query"] == "hello"
    assert n.metadata["source"] == "reddit"
    assert n.metadata["title"] == "Hello World"
    assert n.metadata["permalink"].startswith("/r/test/")
    assert n.metadata["is_self"] is True
    assert "selftext" not in n.metadata


def test_map_submissions_to_text_nodes_empty_title():
    results = [
        SimpleNamespace(
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

    nodes = RedditIndexUtils.map_submissions_to_text_nodes(results, query="q")
    assert len(nodes) == 1
    assert isinstance(nodes[0].text, str)
    assert nodes[0].text == ""
