# entities/entity_resolver.py
from rapidfuzz import fuzz, process
import re

# Простая база известных компаний из синтетики (можно расширять)
KNOWN_COMPANIES = [
    "ТОО Строитель", "ТОО МедТорг", "ТОО АвтоЗапчасть", "ТОО Продукты Плюс",
    "ТОО ТехноСнаб", "ИП Иванов", "ТОО АлматыТопливо", "ТОО КазМясо",
    "ТОО АстанаМебель", "ТОО Школьник", "ТОО Фармация", "ТОО IT Solutions"
]

def normalize_company(raw_name: str) -> str:
    if not raw_name:
        return "Неизвестно"
    
    # Убираем юридическую форму
    cleaned = re.sub(r"\b(ТОО|ИП|АО|Филиал|РГП|ГУ)\b", "", raw_name, flags=re.IGNORECASE)
    cleaned = re.sub(r"[\"\.\,]", "", cleaned)
    cleaned = cleaned.strip().lower()
    
    if not cleaned:
        return raw_name.strip()
    
    # Ищем лучшее совпадение
    best_match, score, _ = process.extractOne(cleaned, [c.lower() for c in KNOWN_COMPANIES])
    
    if score > 85:
        return best_match.title()
    else:
        return raw_name.strip()  # оставляем как есть