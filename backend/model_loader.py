# backend/model_loader.py
import tensorflow as tf
import joblib
import os

# Load model and scaler from models folder
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "weather_model_global.h5")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "..", "scaler_global.pkl")

model = tf.keras.models.load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
