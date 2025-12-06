#!/bin/bash

# Start FastAPI Backend for Semantic Image Search
# This script runs the uvicorn server with the API

echo "🚀 Starting Semantic Image Search API..."
echo "================================================"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "✓ Activating virtual environment..."
    source .venv/bin/activate
fi

# Check if required packages are installed
echo "✓ Checking dependencies..."
python -c "import fastapi, uvicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installing required packages..."
    pip install fastapi uvicorn python-multipart
fi

# Set environment variables
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Start the server
echo "✓ Starting uvicorn server..."
echo "================================================"
echo "API Documentation: http://localhost:8000/docs"
echo "ReDoc: http://localhost:8000/redoc"
echo "Health Check: http://localhost:8000/health"
echo "================================================"

uvicorn semantic_image_search.backend.api_main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --log-level info
