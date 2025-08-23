import meilisearch
import pytest

from server.config import settings
from server.indexing.reddit_query_index import RedditQueryIndex

pytestmark = pytest.mark.integration


@pytest.mark.integration
def test_index_integration_smoke():
    # Use the same local HF embedding as production default (384 dims) to avoid dim mismatch
    rqi = RedditQueryIndex(collection_name="test_index_integration_smoke")
    # don't assert on results, just ensure it doesn't raise when creds are present
    try:
        rqi.index("reddit mcp", subreddit="mcp", limit=1)
    except ValueError:
        # Missing Reddit creds is acceptable in CI without secrets
        pass


@pytest.mark.integration
def test_meilisearch_indexing_live():
    # Skip if Meilisearch is not reachable
    try:
        client = meilisearch.Client(settings.meili_url, settings.meili_master_key)
        client.get_version()
    except Exception:
        pytest.skip("Meilisearch not reachable; skipping integration test")

    # Require Reddit credentials
    from server.connectors.reddit import os as _os

    if not (_os.getenv("REDDIT_CLIENT_ID") and _os.getenv("REDDIT_CLIENT_SECRET")):
        pytest.skip("Reddit credentials not configured; skipping integration test")

    index_name = "test_meilisearch_indexing_live"
    rqi = RedditQueryIndex(collection_name=index_name)
    results = rqi.index("reddit mcp", subreddit="mcp", limit=1)
    if not results:
        pytest.skip("No results from Reddit; skipping assertion")

    first_id = results[0].id
    idx = client.index(index_name)
    doc = idx.get_document(first_id)
    # Basic sanity: document exists and has a title
    title_val = None
    try:
        title_val = doc["title"]  # type: ignore[index]
    except Exception:
        if hasattr(doc, "title"):
            title_val = doc.title  # type: ignore[assignment]
        elif hasattr(doc, "get"):
            title_val = doc.get("title")  # type: ignore[attr-defined]
        elif hasattr(doc, "dict"):
            title_val = doc.dict().get("title")  # type: ignore[attr-defined]
    assert isinstance(title_val, str)
