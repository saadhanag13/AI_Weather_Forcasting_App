# AI Weather Forecasting Application

A sophisticated weather forecasting system that combines machine learning predictions with real-time data to provide personalized weather insights and decision support.

## Architecture Overview

This application follows a microservices architecture with containerized deployment:

- **Backend**: FastAPI-based REST API with LSTM neural network for weather prediction
- **Frontend**: Streamlit-based dashboard with role-based weather insights
- **Model**: TensorFlow/Keras LSTM model trained on historical weather data
- **Deployment**: Docker Compose orchestration with health monitoring

## Features

### Core Functionality
- **AI-Powered Predictions**: LSTM neural network for accurate temperature forecasting
- **Real-Time Data**: Integration with OpenMeteo API for current weather conditions
- **Personalized Insights**: Role-based recommendations for Commuters, Event Planners, Outdoor Workers, and Tourists
- **Hourly Forecasts**: 12-hour detailed weather projections with trend analysis
- **Smart Alerts**: Automated warnings for extreme weather conditions
- **Interactive Dashboard**: Mobile-responsive interface with dynamic visualizations

### Timezone Awareness
- Forecasts are generated in the **city’s local timezone** (ensures realistic weather patterns).  
- All times shown in the dashboard are converted to the **user’s selected timezone** for convenience.  
- This prevents mismatches (e.g., viewing London weather while in Asia/Kolkata).  

### Technical Features
- **RESTful API**: Comprehensive endpoints for weather prediction and health monitoring
- **Data Processing**: Automated feature engineering and sequence generation
- **Model Serving**: Production-ready model deployment with error handling
- **Health Monitoring**: Container health checks and service status monitoring
- **Scalable Architecture**: Docker-based deployment with service orchestration

## Main Project Structure

```bash
Weather_Forecasting_App/
├── backend/
│   ├── models/
│   │   ├── global_weather_saved_model.keras
│   │   └── scaler_global.pkl
│   ├── main.py
│   ├── model_loader.py
│   ├── data_fetcher.py
│   ├── model_utils.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── frontend/
│   ├── utils/
│   │   └── timezone_utils.py
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
├── scripts/
│   ├── setup.sh
│   ├── build.sh
│   ├── deploy.sh
│   └── check_str.sh
├── logs/
├── docker-compose.yml
└── README.md
```

## Prerequisites

### System Requirements
- Docker Desktop 4.0+
- Docker Compose 2.0+
- 4GB RAM minimum
- 2GB free disk space

### Development Requirements
- Python 3.9+
- TensorFlow 2.16+
- FastAPI 0.104+
- Streamlit 1.28+

## Installation

### Quick Start (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/saadhanag13/Weather_Forecasting_App.git
cd Weather_Forecasting_App
```

2. **Run setup script**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

3. **Build and start services**
```bash
./scripts/build.sh
```

4. **Access the application**
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Manual Installation

1. **Environment Setup**
```bash
# Create directory structure
mkdir -p backend/models frontend/pages scripts logs

# Copy your trained model files
cp your_model.keras backend/models/global_weather_saved_model.keras
cp your_scaler.pkl backend/models/scaler_global.pkl
```

2. **Configure Environment**

Backend configuration (`backend/.env`):
```env
ENVIRONMENT=production
API_HOST=0.0.0.0
API_PORT=8000
MODEL_PATH=/app/models/global_weather_saved_model.keras
OPENMETEO_BASE_URL=https://api.open-meteo.com/v1
LOG_LEVEL=INFO
```

Frontend configuration (`frontend/.env`):
```env
BACKEND_URL=http://backend:8000
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

3. **Deploy with Docker**
```bash
docker-compose build --no-cache
docker-compose up -d
```

## API Documentation

### Core Endpoints

#### Health Check
```http
GET /health
```

#### Weather Prediction
```http
POST /predict
Content-Type: application/json

{
"city": "London"
}
```

Response:
```json
{
"city": "London",
"predicted_temperature": 22.5,
"unit": "°C",
"confidence": 92.3,
"model_version": "1.0.0",
"timestamp": "2025-09-19T12:00:00",
"status": "success"
}
```

#### Supported Cities
```http
GET /cities
```

#### Model Information
```http
GET /model/info
```

## Configuration

### Backend Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Deployment environment | `production` |
| `API_HOST` | API server host | `0.0.0.0` |
| `API_PORT` | API server port | `8000` |
| `MODEL_PATH` | Path to model file | `/app/models/global_weather_saved_model.keras` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `OPENMETEO_BASE_URL` | Weather API endpoint | `https://api.open-meteo.com/v1` |

### Frontend Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `BACKEND_URL` | Backend API URL | `http://backend:8000` |
| `STREAMLIT_SERVER_PORT` | Frontend port | `8501` |
| `STREAMLIT_THEME_BASE` | UI theme | `dark` |

## Development

### Local Development Setup

1. **Backend Development**
```bash
cd backend
python -m venv musicgen
source musicgen/bin/activate  
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. **Frontend Development**
```bash
cd frontend
python -m venv musicgen
source musicgen/bin/activate
pip install -r requirements.txt
streamlit run app.py --server.port 8501
```

### Model Training

The application expects a trained LSTM model with the following specifications:
- Input shape: (6, n_features)
- Output: Single temperature prediction
- Format: Keras .keras file
- Scaler: Scikit-learn StandardScaler saved as .pkl

### Testing

```bash
# Test API endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"city":"London"}'

# Run health checks
./scripts/deploy.sh --env development

# Check service status
docker-compose ps
docker-compose logs -f
```

## Deployment

### Production Deployment

```bash
# Deploy with production configuration
./scripts/deploy.sh --env production

# With custom domain and SSL
./scripts/deploy.sh --env production --domain your-domain.com --email your@email.com
```

### Environment-Specific Deployment

```bash
# Development
docker-compose up --build

# Staging
docker-compose -f docker-compose.yml -f docker-compose.staging.yml up -d

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Health Monitoring

The application includes comprehensive health monitoring:
- Container health checks
- Model loading verification
- API endpoint availability
- Service dependency checks

## Monitoring and Logging

### Log Files
- Backend logs: `/app/logs/backend.log`
- Container logs: `docker-compose logs [service]`

### Monitoring Commands
```bash
# Service status
docker-compose ps

# Resource usage
docker stats

# Live logs
docker-compose logs -f backend frontend
```

## Troubleshooting

### Common Issues

1. **Model Loading Failures**
```bash
# Check model files exist
docker exec -it backend ls -la /app/models/

# Verify model compatibility
docker exec -it backend python -c "import tensorflow as tf; print(tf.__version__)"
```

2. **Container Communication Issues**
```bash
# Test network connectivity
docker exec -it frontend ping backend

# Check environment variables
docker exec -it frontend env | grep BACKEND_URL
```

3. **Port Conflicts**
```bash
# Check port usage
netstat -tulpn | grep :8000
netstat -tulpn | grep :8501
```

4. **Error connecting to WeatherAPI**
```bash
# Ensure backend is running
docker-compose ps

# Check backend logs
docker-compose logs backend

# Verify frontend BACKEND_URL
docker exec -it frontend env | grep BACKEND_URL
```

### Performance Optimization

1. **Model Optimization**
- Use TensorFlow Lite for faster inference
- Implement model caching
- Optimize batch processing

2. **API Optimization**
- Enable response compression
- Implement request caching
- Use connection pooling

3. **Frontend Optimization**
- Implement data caching
- Optimize component rendering
- Use lazy loading

## Security Considerations

- Change default secret keys in production
- Implement API rate limiting
- Use HTTPS in production
- Validate all input data
- Implement proper authentication for sensitive endpoints

## 🧑‍💻 Author
### Saadhana Ganesa Narasimhan
MSc Graduate | Aspiring AI/ML Engineer | Passionate about real-world deep learning applications

### 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://saadhanag13.github.io/MyResume/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/saadhana-ganesh-45a50a18b/)
