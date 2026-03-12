#!/bin/bash
# Quick start script to run both backend and frontend

set -e

echo "🚀 Customer Support Email Agent - Quick Start"
echo "=============================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run: python3 -m venv venv"
    exit 1
fi

# Activate venv
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -q -r requirements.txt
fi

# Check if data directory exists
if [ ! -d "data" ]; then
    echo "📁 Creating data directory..."
    mkdir -p data/knowledge data/faiss_index
fi

# Initialize database if needed
if [ ! -f "data/agent.db" ]; then
    echo "🗄️ Initializing database..."
    python -c "from src.db.database import Base, engine; Base.metadata.create_all(bind=engine)"
fi

echo ""
echo "✅ System is ready!"
echo ""
echo "To start the system:"
echo ""
echo "1. Start the backend server (run in terminal 1):"
echo "   source venv/bin/activate"
echo "   uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "2. Start the frontend (run in terminal 2):"
echo "   source venv/bin/activate"
echo "   streamlit run frontend/app.py"
echo ""
echo "Then open your browser to http://localhost:8501"
echo ""
