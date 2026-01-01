@echo off
echo 🚀 Starting YouTube Video Downloader...
echo.

:: Navigate to the project directory
cd /d "%~dp0"

:: Check if virtual environment exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install/update dependencies
echo 📦 Installing dependencies...
pip install -q Flask Flask-CORS yt-dlp

:: Start the server
echo.
echo ============================================================
echo 🎬 YouTube Video Downloader is starting...
echo ============================================================
echo.
python app.py

pause
