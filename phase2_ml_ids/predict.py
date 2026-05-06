import joblib
import pandas as pd
from phase2_ml_ids.preprocess import transform

model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")
encoders = joblib.load("encoders.pkl")


def predict_sample(sample):
    df = pd.DataFrame([sample])
    X = transform(df, scaler, encoders)
    return model.predict(X)[0]
