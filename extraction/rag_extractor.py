# extraction/rag_extractor.py — RAG с Gemini 1.5 Flash (рекомендую!)
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def extract_with_rag(description: str) -> dict:
    prompt = f"""
Ты — эксперт по государственным закупкам Казахстана.
Извлеки из описания лота следующие параметры в формате JSON:

{{
  "item_name": "название товара/услуги",
  "quantity": число (или null),
  "unit": "единица измерения (шт, кг, литр, тонна и т.д.)",
  "requirements": "ключевые требования (ГОСТ, сертификаты, доставка и т.д.)",
  "region": "регион поставки (Алматы, Астана, Шымкент и т.д. или null)",
  "delivery_terms": "условия доставки (или null)"
}}

Описание лота:
{description}

Ответь ТОЛЬКО валидным JSON, без лишнего текста.
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Убираем возможные ```json и ```
        if text.startswith("```"):
            text = text.split("```", 2)[1].strip()
            if text.startswith("json"):
                text = text[4:].strip()
        
        import json
        result = json.loads(text)
        return result
    except Exception as e:
        print(f"Ошибка извлечения: {e}")
        return {
            "item_name": description[:50] + "...",
            "quantity": None,
            "unit": None,
            "requirements": "Не удалось извлечь",
            "region": None,
            "delivery_terms": None
        }