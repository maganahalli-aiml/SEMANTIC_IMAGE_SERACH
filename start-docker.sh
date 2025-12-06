#!/bin/bash

# Semantic Image Search - Docker Quick Start Script
# This script helps you quickly set up and run the entire application

set -e

echo "🚀 Semantic Image Search - Docker Setup"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    echo "Please install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed"
    echo "Please install Docker Compose from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "📝 Please edit .env file with your credentials:"
    echo "   - OPENAI_API_KEY"
    echo "   - QDRANT_URL"
    echo "   - QDRANT_API_KEY"
    echo ""
    echo "Run this script again after updating .env"
    exit 1
fi

echo "✅ .env file found"
echo ""

# Check if required environment variables are set
source .env
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
    echo "❌ Error: OPENAI_API_KEY is not set in .env file"
    exit 1
fi

if [ -z "$QDRANT_URL" ] || [ "$QDRANT_URL" = "https://your-cluster-url.aws.cloud.qdrant.io" ]; then
    echo "❌ Error: QDRANT_URL is not set in .env file"
    exit 1
fi

if [ -z "$QDRANT_API_KEY" ] || [ "$QDRANT_API_KEY" = "your_qdrant_api_key_here" ]; then
    echo "❌ Error: QDRANT_API_KEY is not set in .env file"
    exit 1
fi

echo "✅ Environment variables configured"
echo ""

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p temp_images saved_results data
echo "✅ Directories created"
echo ""

# Build and start services
echo "🔨 Building Docker images (this may take a few minutes)..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check backend health
echo "🏥 Checking backend health..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend is healthy!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Backend failed to start. Check logs with: docker-compose logs backend"
        exit 1
    fi
    echo "   Waiting... ($i/30)"
    sleep 2
done

echo ""
echo "✨ Application is ready!"
echo ""
echo "📍 Access URLs:"
echo "   Backend API:     http://localhost:8000"
echo "   API Docs:        http://localhost:8000/docs"
echo "   Frontend (Expo): http://localhost:19002"
echo "   Health Check:    http://localhost:8000/health"
echo ""
echo "📊 View logs:"
echo "   All services:    docker-compose logs -f"
echo "   Backend only:    docker-compose logs -f backend"
echo "   Frontend only:   docker-compose logs -f frontend"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
echo ""
echo "Happy searching! 🔍"
