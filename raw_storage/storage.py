import json
import os

RAW_DIR = "raw_storage/data"
os.makedirs(RAW_DIR, exist_ok=True)

def save_raw_data(content: str, filename: str):
    with open(os.path.join(RAW_DIR, filename), "w", encoding="utf-8") as f:
        f.write(content)