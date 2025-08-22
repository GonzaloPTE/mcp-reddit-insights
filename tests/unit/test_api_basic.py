import pytest
from httpx import ASGITransport, AsyncClient

from server.main import app


@pytest.mark.asyncio
async def test_healthz():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.get("/healthz")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_search_minimal():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        resp = await ac.post("/search", json={"query": "hello", "top_k": 3})
        assert resp.status_code == 200
        data = resp.json()
        assert data["query"] == "hello"
        assert isinstance(data["results"], list)
