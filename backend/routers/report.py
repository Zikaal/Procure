# backend/routers/report.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from jinja2 import Environment, FileSystemLoader
from parser.csv_parser import load_lots
from matching.rag_matcher import find_suppliers

router = APIRouter()
env = Environment(loader=FileSystemLoader("templates"))

class ReportRequest(BaseModel):
    announcement_id: str

@router.post("/")
def generate_report(request: ReportRequest):
    lots = load_lots()
    ann_lots = lots[lots["announcement_id"] == request.announcement_id].to_dict("records")
    
    if not ann_lots:
        raise HTTPException(404, f"Тендер {request.announcement_id} не найден")

    for lot in ann_lots:
        lot["recommended_suppliers"] = find_suppliers(lot["description"], top_k=5)

    html = env.get_template("report.html").render(
        announcement_id=request.announcement_id,
        lots=ann_lots,
        total_lots=len(ann_lots)
    )
    return HTMLResponse(html)