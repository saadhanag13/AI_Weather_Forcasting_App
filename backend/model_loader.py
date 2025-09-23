# backend/model_loader.py
import tensorflow as tf
import joblib
import os

# Load model and scaler from models folder
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models" , "global_weather_saved_model.keras")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "models" , "scaler_global.pkl")

model = tf.keras.models.load_model(MODEL_PATH, compile=False)
scaler = joblib.load(SCALER_PATH)

print(f"Model file size: {os.path.getsize(MODEL_PATH)} bytes")
print(f"Scaler file size: {os.path.getsize(SCALER_PATH)} bytes")
print("✅ Model and scaler loaded successfully!")

