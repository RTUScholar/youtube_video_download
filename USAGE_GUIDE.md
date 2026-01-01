# 📖 Complete Usage Guide

## Getting Started

### First Time Setup

1. **Download the project** to your computer
2. **Open Terminal** (macOS/Linux) or **Command Prompt** (Windows)
3. **Navigate to the project folder**:
   ```bash
   cd path/to/youtube_video_download
   ```
4. **Run the start script**:
   - macOS/Linux: `./start.sh`
   - Windows: `start.bat`

That's it! The application will automatically open in your browser.

## How to Download Videos

### Step-by-Step Process

1. **Copy YouTube URL**
   - Go to YouTube
   - Find the video you want to download
   - Copy the URL from the address bar
   - Example: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

2. **Paste URL**
   - Return to the YouTube Downloader
   - Paste the URL in the input box
   - The app will automatically load video information

3. **Choose Quality**
   - Select your preferred quality from the dropdown
   - Options: Best Quality (default), 4K, 2K, 1080p, 720p, 480p
   - Higher quality = larger file size

4. **Click Download**
   - Click the "📥 Download Video" button
   - Watch the progress bar
   - Wait for the download to complete

5. **Save Video**
   - Once complete, the video will automatically download
   - Choose where to save it on your computer
   - Done! 🎉

## Understanding Quality Options

### Quality Guide

| Quality | Resolution | Best For | File Size |
|---------|-----------|----------|-----------|
| **4K** | 2160p | Large displays, TVs | Very Large |
| **2K** | 1440p | High-end monitors | Large |
| **1080p** | Full HD | Most computers, laptops | Medium-Large |
| **720p** | HD | Standard viewing | Medium |
| **480p** | SD | Mobile devices, slow internet | Small |
| **Best** | Highest available | Auto-selects best quality | Varies |

### Recommendations

- **For watching on TV/large monitor**: Use 4K or 2K
- **For laptop/computer**: Use 1080p
- **For mobile devices**: Use 720p
- **For saving space**: Use 480p
- **When unsure**: Use "Best Quality"

## Speed Optimization

### Tips for Faster Downloads

1. **Close unnecessary programs** - Free up bandwidth
2. **Use wired connection** - Ethernet is faster than WiFi
3. **Download during off-peak hours** - Less internet congestion
4. **Choose appropriate quality** - Lower quality = faster download
5. **Disable VPN temporarily** - VPNs can slow downloads

### Download Speed Factors

The download speed depends on:
- Your internet connection speed
- YouTube's server speed
- Video quality and length
- Current server load
- Time of day

Typical speeds:
- **Fast connection (100+ Mbps)**: 5-15 MB/s
- **Average connection (25-100 Mbps)**: 2-8 MB/s
- **Slow connection (<25 Mbps)**: 0.5-3 MB/s

## Advanced Features

### Real-Time Progress Tracking

Watch your download progress with:
- **Percentage**: How much has been downloaded
- **Speed**: Current download speed (MB/s)
- **ETA**: Estimated time remaining

### Video Preview

Before downloading, you can see:
- Video thumbnail
- Video title
- Duration
- Available quality options

### Automatic Features

The app automatically:
- Merges video and audio for best quality
- Converts to MP4 format
- Retries failed downloads
- Cleans up temporary files
- Optimizes download speed

## Troubleshooting

### Common Issues and Solutions

#### "Failed to start download"
**Possible causes:**
- Invalid YouTube URL
- Private or age-restricted video
- Removed or deleted video

**Solutions:**
- Check the URL is correct
- Make sure video is public
- Try a different video

#### "Download is very slow"
**Possible causes:**
- Slow internet connection
- High server load
- Large video file

**Solutions:**
- Check your internet speed
- Try again later
- Choose lower quality

#### "Video won't play after download"
**Possible causes:**
- Incomplete download
- Corrupted file
- Unsupported format

**Solutions:**
- Download again
- Update your video player
- Try VLC Media Player (plays everything)

#### "Server won't start"
**Possible causes:**
- Python not installed
- Port 5000 already in use
- Missing dependencies

**Solutions:**
- Install Python 3.7+
- Close other programs using port 5000
- Run the start script again

### Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "URL is required" | Empty input field | Paste a YouTube URL |
| "Invalid YouTube URL" | Wrong URL format | Use proper YouTube link |
| "File not found" | Download failed | Try downloading again |
| "Module not found" | Missing package | Run start script |

## Keyboard Shortcuts

- **Enter**: Start download (when URL field is focused)
- **Ctrl+V / Cmd+V**: Paste URL
- **Ctrl+C / Cmd+C**: Stop server (in terminal)

## Supported Platforms

### Operating Systems
- ✅ macOS (10.14+)
- ✅ Windows (10/11)
- ✅ Linux (Ubuntu, Debian, Fedora, etc.)

### Browsers
- ✅ Chrome / Chromium
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Opera

## File Information

### Download Location
- Videos are temporarily stored in the `downloads/` folder
- Files are automatically deleted after 1 hour
- Make sure to save downloaded videos to a permanent location

### File Formats
- **Default format**: MP4
- **Video codec**: H.264/H.265
- **Audio codec**: AAC
- **Compatibility**: Works on all devices

## Privacy & Security

### What We Track
- **Nothing!** No data collection
- No analytics
- No cookies
- No user tracking

### Your Data
- All processing happens locally
- No data sent to third-party servers
- Downloads are not stored permanently
- URLs are not logged

### Safety
- No ads or pop-ups
- No malware or viruses
- Open-source code
- Trusted yt-dlp backend

## Legal & Ethical Use

### Allowed Uses
✅ Download your own videos
✅ Download videos with Creative Commons license
✅ Educational/research purposes (with permission)
✅ Personal backup of purchased content

### Not Allowed
❌ Downloading copyrighted content without permission
❌ Redistributing downloaded videos
❌ Commercial use of downloaded content
❌ Violating YouTube's Terms of Service

**Remember**: Only download videos you have the right to download!

## Performance Expectations

### Download Times (1080p, 10-minute video)

| Internet Speed | Expected Time |
|----------------|---------------|
| 100+ Mbps | 1-2 minutes |
| 50 Mbps | 3-4 minutes |
| 25 Mbps | 5-8 minutes |
| 10 Mbps | 10-15 minutes |

*Times vary based on video size and quality*

### System Requirements

**Minimum:**
- 2 GB RAM
- 500 MB free disk space
- 5 Mbps internet connection
- Python 3.7+

**Recommended:**
- 4+ GB RAM
- 2+ GB free disk space
- 25+ Mbps internet connection
- Python 3.10+

## Tips & Best Practices

### 1. Organize Your Downloads
- Create folders for different types of videos
- Use descriptive file names
- Keep backups of important videos

### 2. Optimize Storage
- Delete videos after watching
- Use appropriate quality for your needs
- Compress large files if needed

### 3. Respect Content Creators
- Consider watching videos on YouTube when possible
- Support creators through official channels
- Don't redistribute downloaded content

### 4. Maintain the App
- Update yt-dlp regularly for best compatibility
- Check for updates to the application
- Keep Python updated

## Getting Help

### Need More Help?

1. **Check this guide** - Most answers are here
2. **Read the README** - Technical details
3. **Check error messages** - They often explain the issue
4. **Try restarting** - Many issues are temporary

### Reporting Issues

If you find a bug or have a feature request:
1. Describe what happened
2. Include error messages
3. Mention your operating system
4. List steps to reproduce

## Frequently Asked Questions

**Q: Is this legal?**
A: The tool itself is legal. However, downloading copyrighted content without permission may violate laws and YouTube's ToS. Use responsibly.

**Q: Can I download playlists?**
A: Currently, you need to download videos one at a time.

**Q: What's the maximum quality?**
A: Up to 4K (2160p), depending on what YouTube provides for that video.

**Q: Can I download age-restricted videos?**
A: Not directly. You would need to add authentication support.

**Q: Does this work with other video sites?**
A: Currently only YouTube is supported.

**Q: Why is my video downloading in lower quality?**
A: Some videos aren't available in higher quality on YouTube.

**Q: Can I pause and resume downloads?**
A: Not currently. Downloads must complete in one session.

**Q: Is there a mobile app?**
A: Not yet, but you can access it from a mobile browser if running on your local network.

**Q: Can multiple people use this at once?**
A: Yes, if running on a server accessible to your network.

**Q: How do I update yt-dlp?**
A: Run: `pip install --upgrade yt-dlp`

---

**Need more help? Feel free to reach out or open an issue!** 💬
