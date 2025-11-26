# risk/heuristics.py
def detect_heuristics_risk(lot_data: dict) -> str:
    risks = []
    
    if lot_data.get("risk_affiliated"):
        risks.append("Аффилированность")
    if lot_data.get("risk_suspicious"):
        risks.append("Подозрительная сумма")
    if lot_data.get("risk_inconsistency"):
        risks.append("Несоответствие в описании")
    
    return ", ".join(risks) if risks else "Нет явных рисков"