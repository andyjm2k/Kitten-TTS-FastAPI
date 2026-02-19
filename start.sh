#!/bin/bash

# Kitten TTS Startup Script

set -e

echo "🐱 Kitten TTS - Starting Server"
echo "================================"

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from example..."
    cp .env.example .env
    echo "✓ Created .env file. Please edit it to configure your settings."
fi

# Load environment variables
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Check for Docker
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo ""
    echo "🐳 Docker mode detected"
    echo ""
    
    # Check if API key is set
    if [ -n "$API_KEY" ]; then
        echo "🔒 API Key authentication: ENABLED"
        echo ""
        echo "Starting with docker-compose.api-key.yml..."
        docker-compose -f docker-compose.api-key.yml up -d
    else
        echo "🔓 API Key authentication: DISABLED"
        echo ""
        echo "Starting with docker-compose.yml..."
        docker-compose up -d
    fi
    
    echo ""
    echo "✓ Server started!"
    echo ""
    echo "📖 Access the WebUI at: http://localhost:8000"
    echo "🏥 Health check: http://localhost:8000/health"
    echo ""
    echo "📝 View logs: docker-compose logs -f"
    echo "🛑 Stop server: docker-compose down"
    echo ""
    
else
    echo ""
    echo "🐍 Python mode (Docker not available)"
    echo ""
    
    # Check if virtual environment exists
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
        echo "✓ Virtual environment created"
    fi
    
    # Activate virtual environment
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
    
    # Install KittenTTS if not already installed
    if ! python -c "import kittentts" 2>/dev/null; then
        echo "Installing KittenTTS..."
        pip install -q https://github.com/KittenML/KittenTTS/releases/download/0.8/kittentts-0.8.0-py3-none-any.whl
    fi
    
    echo ""
    echo "✓ Dependencies installed"
    echo ""
    
    if [ -n "$API_KEY" ]; then
        echo "🔒 API Key authentication: ENABLED"
    else
        echo "🔓 API Key authentication: DISABLED"
    fi
    
    echo ""
    echo "Starting server..."
    echo ""
    echo "📖 Access the WebUI at: http://localhost:${PORT:-8000}"
    echo "🏥 Health check: http://localhost:${PORT:-8000}/health"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    python app.py
fi
