# backend/routers/extract.py
from fastapi import APIRouter
from pydantic import BaseModel
from extraction.rag_extractor import extract_with_rag

router = APIRouter()

class ExtractRequest(BaseModel):
    description: str

@router.post("/")
def extract(request: ExtractRequest):
    result = extract_with_rag(request.description)
    return {"extracted": result}