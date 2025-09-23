#backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import numpy as np
import logging
from datetime import datetime
from dotenv import load_dotenv
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your existing modules
try:
    from model_loader import model, scaler
    from data_fetcher import fetch_city_data, FEATURES
    from model_utils import create_sequences
    MODEL_LOADED = True
except ImportError as e:
    logging.error(f"Failed to import model modules: {e}")
    MODEL_LOADED = False
    model, scaler = None, None

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Weather Forecast API",
    description="Weather forecasting API using LSTM model with real-time data",
    version=os.getenv("MODEL_VERSION", "1.0.0"),
    debug=os.getenv("DEBUG", "False").lower() == "true"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ForecastRequest(BaseModel):
    city: str

class WeatherResponse(BaseModel):
    city: str
    predicted_temperature: float
    unit: str
    confidence: float
    model_version: str
    timestamp: str
    status: str

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    service: str
    model_loaded: bool
    checks: dict

@app.get("/")
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "🌦️ AI Weather Forecasting API is running!",
        "version": os.getenv("MODEL_VERSION", "1.0.0"),
        "model_loaded": MODEL_LOADED,
        "endpoints": {
            "predict": "/predict",
            "health": "/health",
            "cities": "/cities",
            "docs": "/docs"
        },
        "status": "running"
    }

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint for Docker, dev, and monitoring"""
    try:
        # Correct paths relative to backend/
        model_path = os.path.join(os.path.dirname(__file__), "models", "global_weather_saved_model.keras")
        scaler_path = os.path.join(os.path.dirname(__file__), "models", "scaler_global.pkl")

        # Run checks
        checks = {
            "model_loaded": MODEL_LOADED and model is not None,
            "model_file_exists": os.path.exists(model_path),
            "scaler_file_exists": os.path.exists(scaler_path),
            "scaler_available": scaler is not None,
            "data_fetcher_available": callable(globals().get("fetch_city_data")),
        }

        # Overall health
        is_healthy = all(checks.values())

        return HealthResponse(
            status="healthy" if is_healthy else "unhealthy",
            timestamp=datetime.now().isoformat(),
            version=os.getenv("MODEL_VERSION", "1.0.0"),
            service="weather-forecast-backend",
            model_loaded=MODEL_LOADED,
            checks=checks
        )

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")


@app.post("/predict", response_model=WeatherResponse)
def predict_weather(request: ForecastRequest):
    """Predict weather for a given city using LSTM model"""
    
    # Check if model is loaded
    if not MODEL_LOADED or model is None or scaler is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please check server configuration and model files."
        )
    
    try:
        logger.info(f"Weather prediction requested for {request.city}")
        
        # Fetch real-time data for the city
        df = fetch_city_data(request.city)
        
        # Prepare data for prediction
        last_6 = df[FEATURES].tail(6).values
        scaled = scaler.transform(last_6)
        X = create_sequences(scaled)
        X = X.reshape(1, 6, len(FEATURES))  # Single sample for prediction
        
        # Make prediction
        pred_scaled = model.predict(X)[0][0]
        
        # Inverse transform to get actual temperature
        pred_full = np.hstack([pred_scaled] + [0]*(len(FEATURES)-1))
        pred_actual = scaler.inverse_transform([pred_full])[0][0]
        
        # Calculate confidence based on model uncertainty (you can improve this)
        confidence = np.random.uniform(85, 95)  # Placeholder - implement proper confidence calculation
        
        logger.info(f"Prediction successful for {request.city}: {pred_actual:.2f}°C")
        
        return WeatherResponse(
            city=request.city,
            predicted_temperature=round(pred_actual, 2),
            unit="°C",
            confidence=round(confidence, 1),
            model_version=os.getenv("MODEL_VERSION", "1.0.0"),
            timestamp=datetime.now().isoformat(),
            status="success"
        )
        
    except ValueError as e:
        logger.error(f"City data fetch failed for {request.city}: {e}")
        raise HTTPException(status_code=404, detail=f"City not found or data unavailable: {str(e)}")
    
    except Exception as e:
        logger.error(f"Prediction failed for {request.city}: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/cities")
def get_supported_cities():

    cities = [
        "London", "New York", "Tokyo", "Sydney", "Delhi", "Paris",
        "Berlin", "Moscow", "Beijing", "Seoul", "Singapore", "Dubai",
        "Los Angeles", "San Francisco", "Toronto", "São Paulo",
        "Johannesburg", "Istanbul", "Bangkok", "Mexico City"
    ]
    return {
        "cities": cities,
        "total": len(cities),
        "model_version": os.getenv("MODEL_VERSION", "1.0.0")
    }

@app.get("/model/info")
def get_model_info():
    """Get model information and statistics"""
    if not MODEL_LOADED:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        model_info = {
            "model_loaded": MODEL_LOADED,
            "model_version": os.getenv("MODEL_VERSION", "1.0.0"),
            "features": FEATURES if 'FEATURES' in globals() else [],
            "model_summary": {
                "type": "LSTM",
                "input_shape": model.input_shape if model else None,
                "output_shape": model.output_shape if model else None,
            }
        }
        return model_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true"
    )