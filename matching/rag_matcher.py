# matching/rag_matcher.py — ИСПРАВЛЕННАЯ ВЕРСИЯ
from vectorstore.chroma_client import search_similar
from entities.entity_resolver import normalize_company
from risk.heuristics import detect_heuristics_risk
from typing import List, Dict

def find_suppliers(
    query: str,
    max_price: float = None,
    region: str = None,
    top_k: int = 5
) -> List[Dict]:
    try:
        # Исправлено: top_k вместо k
        raw_results = search_similar(query, top_k=top_k * 3)  # берём больше, потом фильтруем
        
        suppliers = []
        seen = set()
        
        for res in raw_results:
            supplier = normalize_company(res.get("customer", "Неизвестно"))
            price = float(res.get("planned_sum", 0))
            lot_region = res.get("region", "")
            
            # Фильтры
            if max_price and price > max_price:
                continue
            if region and region.lower() not in lot_region.lower():
                continue
                
            key = (supplier, res.get("lot_id"))
            if key in seen:
                continue
            seen.add(key)
            
            risk_text = detect_heuristics_risk(res)
            
            suppliers.append({
                "supplier": supplier,
                "lot_id": res.get("lot_id"),
                "item_name": res.get("item_name"),
                "planned_sum": price,
                "region": lot_region,
                "relevance": round(res.get("distance", 0.0), 4),
                "risk_heuristics": risk_text,
                "risk_ml_anomaly": res.get("risk_anomaly", False)
            })
            
            if len(suppliers) >= top_k:
                break
                
        return suppliers[:top_k]
        
    except Exception as e:
        print(f"Ошибка в find_suppliers: {e}")
        return []