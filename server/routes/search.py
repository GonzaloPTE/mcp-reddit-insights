from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List


router = APIRouter(prefix="/search", tags=["search"])


class SearchRequest(BaseModel):
    query: str
    top_k: int = 10


class SearchItem(BaseModel):
    title: str
    url: str
    score: float


class SearchResponse(BaseModel):
    query: str
    results: List[SearchItem]


@router.post("", response_model=SearchResponse)
async def search(req: SearchRequest) -> SearchResponse:
    # Minimal stub: echo query and return stubbed results
    return SearchResponse(query=req.query, results=[
        SearchItem(title="Stubbed result 1", url="https://example.com/stubbed-result-1", score=0.95),
        SearchItem(title="Stubbed result 2", url="https://example.com/stubbed-result-2", score=0.92),
        SearchItem(title="Stubbed result 3", url="https://example.com/stubbed-result-3", score=0.88),
    ])
