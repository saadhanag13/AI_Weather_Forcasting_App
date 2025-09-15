#!/bin/bash

# Build and run AI Weather Forecast Application
echo "🌤️  Building AI Weather Forecast Application..."

# Stop any existing containers
echo "Stopping existing containers..."
docker-compose down

# Build the images
echo "Building Docker images..."
docker-compose build --no-cache

# Start the services
echo "Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Check if services are running
echo "Checking service status..."
docker-compose ps

echo ""
echo "✅ Application is ready!"
echo "🔗 Frontend (Streamlit): http://localhost:8501"
echo "🔗 Backend (FastAPI): http://localhost:8000"
echo "📖 API Documentation: http://localhost:8000/docs"
echo ""
echo "To stop the application, run: docker-compose down"