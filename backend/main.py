# backend/main.py — ФИНАЛЬНАЯ РАБОЧАЯ ВЕРСИЯ
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json

class UTF8JSONResponse(JSONResponse):
    def render(self, content: any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,       
            allow_nan=False,
            indent=None,
            separators=(",", ":")
        ).encode("utf-8")

from backend.routers import ingest, extract, match, report

app = FastAPI(default_response_class=UTF8JSONResponse)

# ВАЖНО: именно с префиксами!
app.include_router(ingest.router, prefix="/ingest")
app.include_router(extract.router, prefix="/extract")
app.include_router(match.router, prefix="/match")
app.include_router(report.router, prefix="/report")   # сейчас HTML-отчёт

@app.get("/")
def root():
    import os
    return {
        "message": "AI-Procure RAG полностью готов!",
        "gemini_key_found": bool(os.getenv("GEMINI_API_KEY")),
        "endpoints": ["/ingest", "/extract", "/match", "/report"]
    }