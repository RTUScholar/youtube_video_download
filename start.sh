#!/bin/bash

echo "🚀 Starting YouTube Video Downloader..."
echo ""

# Navigate to the project directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -q Flask Flask-CORS yt-dlp

# Start the server
echo ""
echo "============================================================"
echo "🎬 YouTube Video Downloader is starting..."
echo "============================================================"
echo ""
python app.py
