#!/bin/bash

# Initial setup script for AI Weather Forecast Application
echo "🌤️  Setting up AI Weather Forecast Application..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop first."
    echo "Visit: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    exit 1
fi

echo "✅ Docker is installed and running"

# Create necessary directories if they don't exist
echo "📁 Creating project structure..."

mkdir -p backend/models
mkdir -p backend/api
mkdir -p backend/utils
mkdir -p backend/config
mkdir -p frontend/pages
mkdir -p frontend/components
mkdir -p frontend/utils
mkdir -p logs

echo "✅ Directory structure created"

# Create environment files
echo "📝 Creating environment configuration..."

# Backend environment file
cat > backend/.env << EOF
# Backend Configuration
ENVIRONMENT=development
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# OpenMeteo API Configuration
OPENMETEO_BASE_URL=https://api.open-meteo.com/v1

# Model Configuration
MODEL_PATH=/app/backend/models/global_weather_saved_model.keras
MODEL_VERSION=1.0.0

# Database (if you add one later)
# DATABASE_URL=sqlite:///./weather.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/backend.log
EOF

# Frontend environment file
cat > frontend/.env << EOF
# Frontend Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Backend API URL
BACKEND_URL=http://backend:8000

# UI Configuration
STREAMLIT_THEME_BASE=dark
STREAMLIT_THEME_PRIMARY_COLOR=#00AA00
STREAMLIT_THEME_BACKGROUND_COLOR=#0E1117
STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR=#262730
EOF

echo "✅ Environment files created"

# Make scripts executable
echo "🔧 Setting up permissions..."
chmod +x scripts/*.sh

# Check if model file exists
if [ ! -f "backend/models/global_weather_saved_model.keras" ]; then
    echo "⚠️  Warning: global_weather_saved_model.keras not found in backend/models/"
    echo "   Please copy your trained model to backend/models/global_weather_saved_model.keras"
fi

# Check for main application files
if [ ! -f "backend/main.py" ]; then
    echo "⚠️  Warning: backend/main.py not found"
    echo "   Please ensure your FastAPI application is in backend/main.py"
fi

if [ ! -f "frontend/app.py" ]; then
    echo "⚠️  Warning: frontend/app.py not found"
    echo "   Please ensure your Streamlit application is in frontend/app.py"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy your trained model to: backend/models/global_weather_saved_model.keras"
echo "2. Move your FastAPI code to: backend/main.py"
echo "3. Move your Streamlit code to: frontend/app.py"
echo "4. Split your requirements.txt into backend and frontend versions"
echo "5. Run: ./scripts/build.sh to build and start the application"
echo ""
echo "For deployment: ./scripts/deploy.sh"