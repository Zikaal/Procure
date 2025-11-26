from sklearn.ensemble import IsolationForest
import pandas as pd

model = IsolationForest(contamination=0.1, random_state=42)

def train_anomaly_model(df: pd.DataFrame):
    features = ['planned_sum', 'quantity', 'unit_price']
    X = df[features].fillna(0)
    model.fit(X)

def predict_risk(row):
    X = [[row['planned_sum'], row['quantity'], row['unit_price']]]
    return model.predict(X)[0] == -1