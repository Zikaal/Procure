import pandas as pd
from raw_storage.storage import save_raw_data

def ingest_synthetic_data():
    ann = pd.read_csv("../synthetic_announcements.csv")
    lots = pd.read_csv("../synthetic_lots.csv")
    
    # Симулируем "сырые" данные
    for _, row in ann.iterrows():
        save_raw_data(row.to_json(), f"announcement_{row['announcement_id']}.json")
    for _, row in lots.iterrows():
        save_raw_data(row.to_json(), f"lot_{row['lot_id']}.json")
    
    print(f"Загружено {len(ann)} объявлений и {len(lots)} лотов")