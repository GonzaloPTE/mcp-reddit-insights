import os
import time

import meilisearch
import pytest
import redis
from qdrant_client import QdrantClient

pytestmark = pytest.mark.integration


def _wait_port(url: str, check_fn, timeout: float = 15.0, interval: float = 0.5):
    start = time.time()
    last_err = None
    while time.time() - start < timeout:
        try:
            check_fn()
            return
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(interval)
    raise AssertionError(f"Service at {url} not ready: {last_err}")


def test_redis_ping():
    url = os.environ.get("REDIS_URL", "redis://localhost:6379")
    client = redis.from_url(url)

    def _check():
        assert client.ping() is True

    _wait_port(url, _check)


def test_qdrant_collections():
    url = os.environ.get("QDRANT_URL", "http://localhost:6333")
    client = QdrantClient(url=url)

    def _check():
        cols = client.get_collections()
        assert hasattr(cols, "collections")

    _wait_port(url, _check)


def test_meilisearch_health():
    url = os.environ.get("MEILI_URL", "http://localhost:7700")
    client = meilisearch.Client(url)  # health endpoint doesn't require key

    def _check():
        h = client.health()
        assert h.get("status") == "available"

    _wait_port(url, _check)
