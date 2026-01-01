# YouTube Video Downloader 🚀

A fast, modern, and secure YouTube video downloader built with Flask and yt-dlp. Download videos in high quality (up to 4K) with a simple one-click process.

## Features ✨

- 🎬 **High Quality Downloads** - Support for 4K, 2K, 1080p, and more
- ⚡ **Lightning Fast** - Optimized for maximum download speed
- 🎯 **One-Click Download** - Simple and intuitive process
- 🔒 **100% Safe** - No ads, no tracking, no malware
- 🎨 **Modern UI** - Beautiful and responsive design
- 📱 **Mobile Friendly** - Works perfectly on all devices

## Quick Start 🏃‍♂️

### Option 1: One-Click Start (Easiest)

**macOS/Linux:**
```bash
./start.sh
```

**Windows:**
```cmd
start.bat
```

The script will automatically:
- Create a virtual environment
- Install all dependencies
- Start the server
- Open in your browser at `http://localhost:5000`

### Option 2: Manual Setup

**1. Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**2. Install Dependencies**
```bash
pip install Flask Flask-CORS yt-dlp
```

**3. Run the Application**
```bash
python app.py
```

**4. Open in Browser**
Navigate to `http://localhost:5000` in your web browser.

## How to Use 📖

1. **Paste URL** - Copy and paste any YouTube video URL
2. **Select Quality** - Choose your preferred video quality (default: Best Quality)
3. **Click Download** - Hit the download button and wait
4. **Enjoy** - Your video will be downloaded automatically!

## Technology Stack 🛠️

- **Backend**: Flask (Python web framework)
- **Downloader**: yt-dlp (industry-standard YouTube downloader)
- **Frontend**: Pure HTML/CSS/JavaScript (no frameworks needed)

## Why yt-dlp? 🤔

yt-dlp is the gold standard for YouTube downloading because:

- ✅ Open-source and actively maintained
- ✅ Supports highest quality (4K, 8K, HDR)
- ✅ Zero ads, zero tracking
- ✅ Trusted by developers and archivists worldwide
- ✅ Fast and reliable
- ✅ Constantly updated to work with YouTube changes

## Features in Detail 📋

### High-Speed Downloads
- Concurrent fragment downloads (5 simultaneous chunks)
- 10MB chunk size for optimal performance
- Automatic retry on failure
- HTTP/2 support for faster connections

### Quality Options
- **Best Quality** - Automatically selects the highest available quality
- **4K (2160p)** - Ultra HD quality
- **2K (1440p)** - Quad HD quality
- **1080p** - Full HD quality
- **720p** - HD quality
- **480p** - Standard definition

### Smart Features
- Real-time download progress tracking
- Video preview with thumbnail
- Duration display
- Speed and ETA indicators
- Automatic file cleanup (files deleted after 1 hour)
- Error handling and notifications

## Project Structure 📁

```
youtube_video_download/
├── app.py                 # Flask backend server
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Frontend UI
└── downloads/            # Temporary download folder (auto-created)
```

## API Endpoints 🔌

### GET /
Serves the main application page

### POST /api/video-info
Get video information without downloading
- **Request**: `{ "url": "youtube_url" }`
- **Response**: Video title, duration, thumbnail, available formats

### POST /api/download
Start a video download
- **Request**: `{ "url": "youtube_url", "quality": "1080p" }`
- **Response**: Download ID for tracking

### GET /api/progress/{download_id}
Check download progress
- **Response**: Status, percentage, speed, ETA

### GET /api/file/{download_id}
Download the completed file

## System Requirements 💻

- Python 3.7 or higher
- 100MB free disk space (temporary)
- Internet connection
- Modern web browser

## Tips for Best Performance 🚀

1. **Use the default "Best Quality"** option for optimal results
2. **Stable internet connection** ensures faster downloads
3. **Close unnecessary tabs** to free up system resources
4. **For very long videos**, be patient - high quality takes time!

## Troubleshooting 🔧

### "Failed to download"
- Check if the URL is a valid YouTube video
- Make sure the video is not private or age-restricted
- Try a different quality setting

### Slow downloads
- Check your internet connection speed
- Try downloading during off-peak hours
- Lower the quality setting if needed

### "Module not found" errors
- Run `pip install -r requirements.txt` again
- Make sure you're using Python 3.7+

## Security & Privacy 🔐

- No data collection
- No user tracking
- No advertisements
- All processing happens locally
- Downloads are automatically cleaned up
- No connection to third-party services (except YouTube)

## Legal Notice ⚖️

This tool is for personal use only. Please respect YouTube's Terms of Service and copyright laws. Only download videos you have permission to download.

## Contributing 🤝

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License 📄

This project is open-source and available for personal use.

## Support 💬

If you encounter any issues or have questions, please open an issue on the repository.

---

**Made with ❤️ for simple, fast, and safe YouTube downloads**
