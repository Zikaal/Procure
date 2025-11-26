import pandas as pd

def normalize_dates(df: pd.DataFrame, cols):
    for col in cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def normalize_numbers(df: pd.DataFrame, cols):
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df