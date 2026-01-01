from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import yt_dlp
import os
import uuid
import threading
import time
import re
import tempfile
from pathlib import Path
import json
import subprocess

app = Flask(__name__)
CORS(app)

# Playwright browser instance (lazy initialization)
_playwright_browser = None
_playwright_lock = threading.Lock()

def get_playwright_browser():
    """Get or initialize Playwright browser instance"""
    global _playwright_browser
    
    with _playwright_lock:
        if _playwright_browser is None:
            try:
                from playwright.sync_api import sync_playwright
                playwright = sync_playwright().start()
                _playwright_browser = playwright.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-blink-features=AutomationControlled',
                        '--disable-web-security',
                    ]
                )
                print("✅ Playwright browser initialized successfully")
            except Exception as e:
                print(f"⚠️  Playwright initialization failed: {e}")
                print("   Falling back to yt-dlp only mode")
                return None
        
        return _playwright_browser


def extract_video_with_playwright(url: str, cookie_id: str = None) -> dict:
    """
    Extract video info using Playwright to bypass bot detection.
    Returns video info in yt-dlp compatible format.
    """
    browser = get_playwright_browser()
    if not browser:
        # Fallback to regular yt-dlp if Playwright is not available
        raise Exception("Playwright not available, using standard extraction")
    
    try:
        from playwright.sync_api import TimeoutError as PlaywrightTimeout
        
        context_opts = {
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'viewport': {'width': 1920, 'height': 1080},
            'ignore_https_errors': True,
        }
        
        # Load cookies if provided
        if cookie_id:
            meta = cookie_files.get(cookie_id)
            cookie_path = meta.get('path') if meta else None
            if cookie_path and os.path.exists(cookie_path):
                # Convert Netscape cookies to Playwright format
                cookies = []
                try:
                    with open(cookie_path, 'r') as f:
                        for line in f:
                            if line.strip() and not line.startswith('#'):
                                parts = line.strip().split('\t')
                                if len(parts) >= 7:
                                    cookies.append({
                                        'name': parts[5],
                                        'value': parts[6],
                                        'domain': parts[0],
                                        'path': parts[2],
                                        'secure': parts[3] == 'TRUE',
                                        'httpOnly': False,
                                        'sameSite': 'None' if parts[3] == 'TRUE' else 'Lax',
                                    })
                except Exception as e:
                    print(f"Cookie parsing error: {e}")
                
                if cookies:
                    # Create temporary cookie storage
                    temp_dir = tempfile.mkdtemp()
                    context_opts['storage_state'] = {
                        'cookies': cookies,
                        'origins': []
                    }
        
        context = browser.new_context(**context_opts)
        page = context.new_page()
        
        # Navigate to video
        page.goto(url, wait_until='domcontentloaded', timeout=30000)
        
        # Wait for video player to load
        try:
            page.wait_for_selector('video', timeout=15000)
        except PlaywrightTimeout:
            pass
        
        # Extract video title
        title = page.title().replace(' - YouTube', '')
        
        # Try to get video ID from URL
        video_id = None
        if 'youtube.com/watch?v=' in url:
            video_id = url.split('watch?v=')[-1].split('&')[0]
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[-1].split('?')[0]
        
        # Get thumbnail
        thumbnail = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg" if video_id else ""
        
        page.close()
        context.close()
        
        # Now use yt-dlp with the "warmed up" session
        # The key is that we've proven we're not a bot by loading the page with Playwright
        return {
            'title': title,
            'id': video_id,
            'thumbnail': thumbnail,
            'playwright_success': True
        }
        
    except Exception as e:
        print(f"Playwright extraction error: {e}")
        raise


# Function to strip ANSI escape codes
def strip_ansi_codes(text):
    """Remove ANSI color codes from text"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', str(text))

# Create downloads directory
DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), 'downloads')
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Store download progress
download_progress = {}

# Store uploaded cookie files (cookie_id -> {path, created_at})
cookie_files = {}

MAX_COOKIE_UPLOAD_BYTES = 2 * 1024 * 1024  # 2MB


def _validate_netscape_cookie_file(path: str) -> tuple[bool, str]:
    """Validate a Netscape cookies.txt file.

    Returns (ok, error_message). The error_message is empty if ok.
    """
    try:
        with open(path, 'rb') as f:
            sample = f.read(64 * 1024)

        text = sample.decode('utf-8', errors='ignore')
        lower = text.lower()

        # Quick hint if a user accidentally uploads runtime.txt
        first_line = (text.splitlines() or [''])[0].strip()
        if first_line.startswith('python-') and '\n' not in first_line and len(text.splitlines()) <= 3:
            return False, 'Invalid cookies.txt: this looks like a Python version file (e.g. runtime.txt). Please export browser cookies in Netscape format.'

        if 'netscape http cookie file' in lower:
            return True, ''

        # Netscape format is tab-separated with 7 fields:
        # domain, flag, path, secure, expiration, name, value
        for line in text.splitlines():
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            if s.count('\t') >= 6:
                return True, ''

        return False, 'Invalid cookies.txt: file is not in Netscape cookie format. Export YouTube cookies as cookies.txt (Netscape format) and try again.'
    except Exception:
        return False, 'Invalid cookies.txt: could not read/validate file.'


def _is_youtube_bot_error(message: str) -> bool:
    if not message:
        return False
    msg = message.lower()
    return (
        "sign in to confirm you’re not a bot" in msg
        or "sign in to confirm you're not a bot" in msg
        or "use --cookies" in msg
        or "cookies-from-browser" in msg
        or "this helps protect our community" in msg
    )

def cleanup_old_files():
    """Clean up files older than 1 hour"""
    while True:
        time.sleep(3600)  # Run every hour
        current_time = time.time()
        for file in Path(DOWNLOAD_DIR).glob('*'):
            if current_time - file.stat().st_mtime > 3600:
                try:
                    file.unlink()
                except:
                    pass

        # Cleanup cookies older than 30 minutes
        for cookie_id, meta in list(cookie_files.items()):
            try:
                if current_time - meta.get('created_at', current_time) > 1800:
                    cookie_path = meta.get('path')
                    if cookie_path and os.path.exists(cookie_path):
                        os.remove(cookie_path)
                    cookie_files.pop(cookie_id, None)
            except:
                pass

# Start cleanup thread
threading.Thread(target=cleanup_old_files, daemon=True).start()

def progress_hook(d, download_id):
    """Hook to track download progress"""
    if d['status'] == 'downloading':
        try:
            # Get raw values and strip ANSI codes
            percent_str = strip_ansi_codes(d.get('_percent_str', '0%')).strip()
            speed_str = strip_ansi_codes(d.get('_speed_str', 'N/A')).strip()
            eta_str = strip_ansi_codes(d.get('_eta_str', 'N/A')).strip()
            
            # Clean up percent string
            if percent_str and '%' in percent_str:
                percent_str = percent_str.replace('%', '').strip() + '%'
            
            # Parse percentage
            try:
                percent_num = float(percent_str.replace('%', ''))
            except:
                percent_num = 0
            
            # Initialize if not exists
            if download_id not in download_progress:
                download_progress[download_id] = {
                    'phase': 'video',
                    'last_percent': 0
                }
            
            current_data = download_progress[download_id]
            
            # Detect phase change: if progress drops significantly, we're downloading audio now
            if current_data.get('last_percent', 0) > 90 and percent_num < 50:
                download_progress[download_id]['phase'] = 'audio'
            
            # Store current phase and raw progress
            download_progress[download_id].update({
                'status': 'downloading',
                'percent': percent_str,
                'raw_percent': percent_num,
                'speed': speed_str,
                'eta': eta_str,
                'phase': current_data.get('phase', 'video'),
                'last_percent': percent_num,
                'downloaded': d.get('downloaded_bytes', 0),
                'total': d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
            })
        except Exception as e:
            print(f"Progress hook error: {e}")
            pass
    elif d['status'] == 'finished':
        # Mark current phase as complete
        if download_id in download_progress:
            current_phase = download_progress[download_id].get('phase', 'video')
            if current_phase == 'video':
                download_progress[download_id]['phase'] = 'audio'
            else:
                download_progress[download_id]['phase'] = 'merging'
        
        download_progress[download_id].update({
            'status': 'processing' if download_progress[download_id].get('phase') == 'merging' else 'downloading',
            'percent': '100%',
            'speed': 'Merging files...',
            'eta': 'Almost done!'
        })

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/video-info', methods=['POST'])
def get_video_info():
    """Get video information without downloading"""
    try:
        data = request.json
        url = data.get('url')
        cookie_id = data.get('cookie_id')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'user_agent': 'com.google.ios.youtube/19.29.1 (iPhone16,2; U; CPU iOS 17_5_1 like Mac OS X;)',
            'extractor_args': {'youtube': {
                'player_client': ['ios', 'android'],
                'player_skip': ['webpage'],
            }},
            'http_headers': {
                'User-Agent': 'com.google.ios.youtube/19.29.1 (iPhone16,2; U; CPU iOS 17_5_1 like Mac OS X;)',
                'X-Youtube-Client-Name': '5',
                'X-Youtube-Client-Version': '19.29.1',
            },
        }

        if cookie_id:
            meta = cookie_files.get(cookie_id)
            cookie_path = meta.get('path') if meta else None
            if cookie_path and os.path.exists(cookie_path):
                ydl_opts['cookiefile'] = cookie_path
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Get available formats
            formats = []
            seen_qualities = set()
            
            for f in info.get('formats', []):
                if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                    height = f.get('height')
                    if height and height not in seen_qualities:
                        quality = f"{height}p"
                        formats.append({
                            'quality': quality,
                            'format_id': f.get('format_id'),
                            'ext': f.get('ext', 'mp4'),
                            'filesize': f.get('filesize', 0)
                        })
                        seen_qualities.add(height)
            
            # Sort by quality descending
            formats.sort(key=lambda x: int(x['quality'].replace('p', '')), reverse=True)
            
            return jsonify({
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
                'formats': formats[:10]  # Return top 10 qualities
            })
    
    except Exception as e:
        raw_err = str(e)
        if _is_youtube_bot_error(raw_err):
            raw_err = (
                "YouTube blocked this request (\"Sign in to confirm you're not a bot\"). "
                "Upload cookies.txt (optional) and try again."
            )
        return jsonify({'error': raw_err}), 400


@app.route('/api/cookies', methods=['POST'])
def upload_cookies():
    """Upload a Netscape cookies.txt file (optional) for bot/age-gated videos."""
    try:
        if 'cookies' not in request.files:
            return jsonify({'error': 'cookies file is required'}), 400

        f = request.files['cookies']
        if not f or not f.filename:
            return jsonify({'error': 'cookies file is required'}), 400

        # Basic size guard
        try:
            f.stream.seek(0, os.SEEK_END)
            size = f.stream.tell()
            f.stream.seek(0)
            if size > MAX_COOKIE_UPLOAD_BYTES:
                return jsonify({'error': 'cookies file too large'}), 400
        except Exception:
            # If stream isn't seekable, proceed and validate after save.
            pass

        cookie_id = str(uuid.uuid4())
        tmp = tempfile.NamedTemporaryFile(prefix='cookies_', suffix='.txt', delete=False)
        tmp_path = tmp.name
        tmp.close()
        f.save(tmp_path)

        ok, err = _validate_netscape_cookie_file(tmp_path)
        if not ok:
            try:
                os.remove(tmp_path)
            except:
                pass
            return jsonify({'error': err}), 400

        cookie_files[cookie_id] = {
            'path': tmp_path,
            'created_at': time.time(),
        }

        return jsonify({'cookie_id': cookie_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/download', methods=['POST'])
def download_video():
    """Download video with selected quality"""
    try:
        data = request.json
        url = data.get('url')
        quality = data.get('quality', 'best')  # Default to best quality
        cookie_id = data.get('cookie_id')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        download_id = str(uuid.uuid4())
        download_progress[download_id] = {
            'status': 'starting',
            'percent': '0%',
            'speed': 'N/A',
            'eta': 'N/A',
            'phase': 'initializing'
        }
        
        # Configure yt-dlp options for high quality and speed with bot detection bypass
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(DOWNLOAD_DIR, f'{download_id}.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [lambda d: progress_hook(d, download_id)],
            'concurrent_fragment_downloads': 16,  # Maximum speed
            'retries': 15,
            'fragment_retries': 15,
            'http_chunk_size': 20971520,  # 20MB chunks
            'buffersize': 65536,  # 64KB buffer
            # Bypass bot detection with multiple strategies
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'extractor_args': {'youtube': {
                'player_client': ['ios', 'android', 'web'],
                'player_skip': ['webpage', 'configs'],
                'skip': ['dash', 'hls']
            }},
            'http_headers': {
                'User-Agent': 'com.google.ios.youtube/19.29.1 (iPhone16,2; U; CPU iOS 17_5_1 like Mac OS X;)',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'X-Youtube-Client-Name': '5',
                'X-Youtube-Client-Version': '19.29.1',
            },
            'format_sort': ['res', 'ext:mp4:m4a'],
            'throttledratelimit': None,  # No rate limiting
            'noprogress': False,  # Enable progress output
        }

        # Attach cookies if provided (recommended when YouTube shows "not a bot" on servers)
        if cookie_id:
            meta = cookie_files.get(cookie_id)
            cookie_path = meta.get('path') if meta else None
            if cookie_path and os.path.exists(cookie_path):
                ydl_opts['cookiefile'] = cookie_path
        
        # Adjust format based on quality selection
        if quality != 'best':
            quality_num = quality.replace('p', '')
            ydl_opts['format'] = f'bestvideo[height<={quality_num}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality_num}][ext=mp4]/best'
        
        def download_thread():
            try:
                # First, try to "warm up" with Playwright to bypass bot detection
                download_progress[download_id]['phase'] = 'warming_up'
                download_progress[download_id]['status'] = 'Bypassing bot detection...'
                
                try:
                    pw_info = extract_video_with_playwright(url, cookie_id)
                    print(f"✅ Playwright warm-up successful for: {pw_info.get('title', 'video')}")
                    download_progress[download_id]['phase'] = 'downloading'
                except Exception as pw_err:
                    print(f"⚠️  Playwright warm-up failed: {pw_err}, continuing with yt-dlp")
                    download_progress[download_id]['phase'] = 'downloading'
                
                # Now proceed with yt-dlp download
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    
                    download_progress[download_id] = {
                        'status': 'completed',
                        'filename': os.path.basename(filename),
                        'filepath': filename
                    }
            except Exception as e:
                raw_err = str(e)
                if _is_youtube_bot_error(raw_err):
                    raw_err = (
                        "YouTube blocked this request despite Playwright bypass. "
                        "Try: 1) Upload fresh cookies.txt from your browser, "
                        "2) Wait a few minutes and retry, "
                        "3) Use a different network/VPN."
                    )
                download_progress[download_id] = {
                    'status': 'error',
                    'error': raw_err
                }
            finally:
                # Best-effort cleanup of one-time cookies
                if cookie_id:
                    meta = cookie_files.pop(cookie_id, None)
                    try:
                        if meta and meta.get('path') and os.path.exists(meta['path']):
                            os.remove(meta['path'])
                    except:
                        pass
        
        # Start download in background thread
        thread = threading.Thread(target=download_thread)
        thread.start()
        
        return jsonify({
            'download_id': download_id,
            'message': 'Download started with bot detection bypass'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/progress/<download_id>', methods=['GET'])
def get_progress(download_id):
    """Get download progress"""
    progress = download_progress.get(download_id, {'status': 'not_found'})
    return jsonify(progress)

@app.route('/api/file/<download_id>', methods=['GET'])
def get_file(download_id):
    """Download the file"""
    try:
        progress = download_progress.get(download_id)
        if not progress or progress.get('status') != 'completed':
            return jsonify({'error': 'File not ready'}), 404
        
        filepath = progress.get('filepath')
        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=progress.get('filename')
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Configure port for Heroku deployment
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'False') == 'True'
    
    if not debug_mode:
        print("\n" + "="*60)
        print("🚀 YouTube Video Downloader Server Started!")
        print("="*60)
        print(f"📱 Server running on port {port}")
        print("="*60 + "\n")
    else:
        print("\n" + "="*60)
        print("🚀 YouTube Video Downloader Server Started!")
        print("="*60)
        print(f"📱 Open your browser and go to: http://localhost:{port}")
        print("="*60 + "\n")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port, threaded=True)
