# backend/routers/ingest.py — ФИНАЛЬНАЯ ВЕРСИЯ ДЛЯ ТВОИХ ДАННЫХ
from fastapi import APIRouter, BackgroundTasks
from parser.csv_parser import load_announcements, load_lots
from vectorstore.chroma_client import add_lot
from risk.ml_anomaly import train_anomaly_model
import pandas as pd
import re

router = APIRouter()

# Простая функция — вытаскиваем город из адреса организатора
def extract_region_from_address(address: str) -> str:
    if pd.isna(address):
        return "Неизвестно"
    address = str(address).lower()
    cities = [
    'Алматы', 'Астана', 'Шымкент', 'Караганда', 'Актобе', 'Тараз', 'Павлодар',
    'Семей', 'Усть-Каменогорск', 'Костанай', 'Петропавловск', 'Кызылорда',
    'Атырау', 'Уральск', 'Туркестан', 'Талдыкорган', 'Кокшетау', 'Степногорск',
    'Жезказган', 'Темиртау', 'Каражал', 'Сатпаев', 'Балхаш', 'Аксай'
]
    for city in cities:
        if city in address:
            return city.title()
    return "Казахстан"

def index_all_lots():
    try:
        print("Загружаем данные...")
        ann_df = load_announcements()
        lots_df = load_lots()

        print(f"Лотов: {len(lots_df)}, Объявлений: {len(ann_df)}")

        # Добавляем регион из адреса организатора
        ann_df['region'] = ann_df['organizer_address'].apply(extract_region_from_address)

        # Объединяем только нужные поля
        df = lots_df.merge(
            ann_df[['announcement_id', 'organizer_name', 'region', 'publication_date']],
            on="announcement_id",
            how="left"
        )

        print(f"Объединено: {len(df)} лотов. Начинаем обучение ML-модели...")
        train_anomaly_model(df)

        print("Индексируем в Chroma...")
        for idx, row in df.iterrows():
            text_parts = [
                str(row.get('item_name', '') or ''),
                str(row.get('description', '') or ''),
                str(row.get('organizer_name', '') or ''),
                str(row.get('region', '') or '')
            ]
            text = " ".join(text_parts).strip()
            metadata = row.to_dict()
            metadata["id"] = str(row['lot_id'])

            add_lot(str(row['lot_id']), text, metadata)

            if (idx + 1) % 20000 == 0:
                print(f"Проиндексировано {idx + 1} лотов...")

        print(f"ГОТОВО! Успешно проиндексировано {len(df)} лотов в Chroma!")
        print("Теперь можно искать поставщиков!")

    except Exception as e:
        print(f"ОШИБКА: {e}")
        import traceback
        traceback.print_exc()

@router.post("/")
async def start_ingest(background_tasks: BackgroundTasks):
    background_tasks.add_task(index_all_lots)
    return {"status": "success", "message": "Индексация запущена! Жди 60–90 секунд"}