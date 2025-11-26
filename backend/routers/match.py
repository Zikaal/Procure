# backend/routers/match.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from matching.rag_matcher import find_suppliers

router = APIRouter()

class MatchRequest(BaseModel):
    query: str
    max_price: Optional[float] = None
    region: Optional[str] = None
    top_k: int = 10

@router.post("/")
def match(request: MatchRequest):
    suppliers = find_suppliers(
        query=request.query,
        max_price=request.max_price,
        region=request.region,
        top_k=request.top_k + 10  # берём с запасом
    )
    return {
        "query": request.query,
        "found": len(suppliers),
        "suppliers": suppliers[:request.top_k]
    }