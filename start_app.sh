#!/bin/bash

# Email Extractor - Streamlit App Launcher
# This script activates the virtual environment and starts the Streamlit app

echo "🚀 Starting Email Extractor Web Interface..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found in virtual environment!"
    echo "Please run: pip install -r requirements.txt"
    exit 1
fi

# Kill any existing streamlit processes
pkill -f "streamlit run app.py" 2>/dev/null || true

echo "✅ Virtual environment activated"
echo "✅ Starting Streamlit server..."
echo ""
echo "📧 Email Extractor will open in your browser"
echo "🌐 URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start streamlit
streamlit run app.py --server.port 8501
