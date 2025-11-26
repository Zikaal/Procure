# parser/csv_parser.py — РАБОЧАЯ ВЕРСИЯ
import pandas as pd
import os

# Абсолютный путь к файлам — работает из любой директории!
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANN_PATH = os.path.join(BASE_DIR, "synthetic_announcements.csv")
LOTS_PATH = os.path.join(BASE_DIR, "synthetic_lots.csv")

def load_announcements():
    if not os.path.exists(ANN_PATH):
        raise FileNotFoundError(f"Не найден файл: {ANN_PATH}\nЗапусти: python generate.py")
    return pd.read_csv(ANN_PATH)

def load_lots():
    if not os.path.exists(LOTS_PATH):
        raise FileNotFoundError(f"Не найден файл: {LOTS_PATH}\nЗапусти: python generate.py")
    return pd.read_csv(LOTS_PATH)