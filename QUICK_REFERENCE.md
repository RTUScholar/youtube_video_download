# ⚡ Quick Reference Card

## 🚀 Start Application

**macOS/Linux:**
```bash
./start.sh
```

**Windows:**
```cmd
start.bat
```

**Then open:** `http://localhost:5000`

---

## 📥 Download Process

1. **Paste** YouTube URL
2. **Select** quality
3. **Click** Download
4. **Wait** for completion
5. **Save** video

---

## 🎯 Quality Options

| Option | Resolution | Use Case |
|--------|-----------|----------|
| Best | Auto | Recommended |
| 4K | 2160p | TVs, Large Screens |
| 2K | 1440p | High-end Monitors |
| 1080p | Full HD | Computers |
| 720p | HD | General Use |
| 480p | SD | Mobile |

---

## ⚙️ Features

✅ **High Quality** - Up to 4K  
✅ **Fast Downloads** - Optimized speed  
✅ **Simple UI** - One-click process  
✅ **Safe** - No ads, no malware  
✅ **Free** - Open-source  
✅ **Progress Tracking** - Real-time updates  

---

## 🔧 Quick Fixes

**Won't start?**
- Install Python 3.7+
- Run start script

**Download fails?**
- Check URL is valid
- Try different quality
- Check internet connection

**Slow downloads?**
- Lower quality setting
- Close other programs
- Try off-peak hours

---

## 📞 Commands

### Stop Server
Press `Ctrl+C` in terminal

### Update Dependencies
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install --upgrade yt-dlp
```

### Manual Start
```bash
source venv/bin/activate
python app.py
```

---

## 📂 File Structure

```
youtube_video_download/
├── app.py           # Main server
├── start.sh         # macOS/Linux starter
├── start.bat        # Windows starter
├── templates/
│   └── index.html   # Web interface
└── downloads/       # Temp storage
```

---

## ⚠️ Important Notes

- Downloads delete after 1 hour
- Save videos immediately
- Only download videos you have rights to
- Respect copyright laws
- Support content creators

---

## 📊 Expected Performance

**1080p video (10 min):**
- Fast (100+ Mbps): 1-2 min
- Medium (50 Mbps): 3-4 min
- Slow (25 Mbps): 5-8 min

---

## 🌐 Supported URLs

✅ `youtube.com/watch?v=...`  
✅ `youtu.be/...`  
✅ `youtube.com/shorts/...`  
❌ Other websites (not supported)

---

## 🔒 Privacy

✅ No data collection  
✅ No tracking  
✅ No ads  
✅ Local processing  
✅ Open-source  

---

## 📚 More Help

- **README.md** - Technical details
- **USAGE_GUIDE.md** - Complete guide
- **Error messages** - Read them carefully

---

**Made with ❤️ for simple YouTube downloads**

*Version 1.0 | January 2026*
