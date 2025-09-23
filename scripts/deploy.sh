#!/bin/bash

# Production deployment script for AI Weather Forecast Application
echo "🚀 Deploying AI Weather Forecast Application..."

# Function to check if command succeeded
check_command() {
    if [ $? -ne 0 ]; then
        echo "❌ Error: $1 failed"
        exit 1
    fi
}

# Parse command line arguments
ENVIRONMENT="production"
DOMAIN=""
SSL_EMAIL=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        --domain)
            DOMAIN="$2"
            shift 2
            ;;
        --email)
            SSL_EMAIL="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --env ENVIRONMENT    Set environment (development/production) [default: production]"
            echo "  --domain DOMAIN      Domain name for SSL certificate"
            echo "  --email EMAIL        Email for SSL certificate"
            echo "  --help              Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option $1"
            exit 1
            ;;
    esac
done

echo "🔧 Deploying in $ENVIRONMENT mode..."

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose down --remove-orphans
check_command "Stopping containers"

# Clean up old images if in production
if [ "$ENVIRONMENT" = "production" ]; then
    echo "🧹 Cleaning up old images..."
    docker image prune -f
    docker container prune -f
    docker volume prune -f
fi

# Create production environment files
if [ "$ENVIRONMENT" = "production" ]; then
    echo "📝 Creating production environment..."
    
    # Update backend .env for production
    cat > backend/.env << EOF
# Production Backend Configuration
ENVIRONMENT=production
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# OpenMeteo API Configuration
OPENMETEO_BASE_URL=https://api.open-meteo.com/v1

# Model Configuration
MODEL_PATH=/app/backend/models/weather_model.keras
MODEL_VERSION=1.0.0

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/backend.log

# Security (generate secure keys in real deployment)
SECRET_KEY=your-super-secret-key-change-this-in-production
EOF

    # Update frontend .env for production
    cat > frontend/.env << EOF
# Production Frontend Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Backend API URL
BACKEND_URL=http://backend:8000

# UI Configuration
STREAMLIT_THEME_BASE=dark
STREAMLIT_THEME_PRIMARY_COLOR=#00AA00
EOF

    # Create production docker-compose override
    cat > docker-compose.prod.yml << EOF
version: '3.8'

services:
  backend:
    restart: always
    environment:
      - ENVIRONMENT=production
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 40s

  frontend:
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 40s

  # Nginx reverse proxy (optional)
  nginx:
    image: nginx:alpine
    container_name: weather_nginx
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    networks:
      - weather_network
EOF

fi

# Build and deploy
echo "🔨 Building Docker images..."
if [ "$ENVIRONMENT" = "production" ]; then
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml build --no-cache
    check_command "Building production images"
    
    echo "🚀 Starting production services..."
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
    check_command "Starting production services"
else
    docker-compose build --no-cache
    check_command "Building development images"
    
    echo "🚀 Starting development services..."
    docker-compose up -d
    check_command "Starting development services"
fi

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 15

# Health check
echo "🩺 Performing health checks..."

# Check backend
echo "Checking backend..."
for i in {1..10}; do
    if curl -f -s http://localhost:8000/docs > /dev/null; then
        echo "✅ Backend is healthy"
        break
    fi
    if [ $i -eq 10 ]; then
        echo "❌ Backend health check failed"
        docker-compose logs backend
        exit 1
    fi
    sleep 3
done

# Check frontend
echo "Checking frontend..."
for i in {1..10}; do
    if curl -f -s http://localhost:8501 > /dev/null; then
        echo "✅ Frontend is healthy"
        break
    fi
    if [ $i -eq 10 ]; then
        echo "❌ Frontend health check failed"
        docker-compose logs frontend
        exit 1
    fi
    sleep 3
done

# Show deployment info
echo ""
echo "🎉 Deployment successful!"
echo ""
echo "📊 Service Status:"
docker-compose ps
echo ""
echo "🔗 Access URLs:"
echo "   Frontend (Streamlit): http://localhost:8501"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"

if [ "$DOMAIN" != "" ]; then
    echo "   Production URL: https://$DOMAIN"
fi

echo ""
echo "📝 Useful commands:"
echo "   View logs: docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart: docker-compose restart"
echo "   Update: ./scripts/deploy.sh --env $ENVIRONMENT"
echo ""

# Optional: Setup SSL certificate if domain provided
if [ "$DOMAIN" != "" ] && [ "$SSL_EMAIL" != "" ]; then
    echo "🔒 Setting up SSL certificate..."
    echo "Note: SSL setup requires additional nginx configuration"
    echo "Consider using Let's Encrypt with certbot for production"
fi

echo "✅ Deployment complete!"