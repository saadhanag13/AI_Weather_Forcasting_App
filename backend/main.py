# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from model_loader import model, scaler
from data_fetcher import fetch_city_data, FEATURES
from model_utils import create_sequences

app = FastAPI()

class ForecastRequest(BaseModel):
    city: str

@app.post("/predict")
def predict_weather(request: ForecastRequest):
    try:
        df = fetch_city_data(request.city)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    last_6 = df[FEATURES].tail(6).values
    scaled = scaler.transform(last_6)
    X = create_sequences(scaled)
    X = X.reshape(1, 6, len(FEATURES))  # Single sample for prediction

    pred_scaled = model.predict(X)[0][0]
    # Pad other features with 0s for inverse scaling
    pred_full = np.hstack([pred_scaled] + [0]*(len(FEATURES)-1))
    pred_actual = scaler.inverse_transform([pred_full])[0][0]

    return {
        "city": request.city,
        "predicted_temperature": round(pred_actual, 2),
        "unit": "°C"
    }
