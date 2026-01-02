from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import yt_dlp
import os
import uuid
import threading
import time
import re
from pathlib import Path
from functools import wraps
import tempfile

app = Flask(__name__)
CORS(app)

# Setup Cookies from Env Var (Cloud-Native approach)
COOKIES_FILE = None
if os.environ.get('COOKIES_CONTENT'):
    try:
        # Create a temporary file for cookies
        tf = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        tf.write(os.environ.get('COOKIES_CONTENT'))
        tf.close()
        COOKIES_FILE = tf.name
        print(f"Loaded cookies from environment variable to {COOKIES_FILE}")
    except Exception as e:
        print(f"Failed to load cookies from env: {e}")
elif os.path.exists('cookies.txt'):
    COOKIES_FILE = 'cookies.txt'
    print("Loaded cookies from cookies.txt")

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

def _is_youtube_bot_error(message: str) -> bool:
    if not message:
        return False
    msg = message.lower()
    return (
        "sign in to confirm you're not a bot" in msg
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

# Start cleanup thread
threading.Thread(target=cleanup_old_files, daemon=True).start()

def progress_hook(d, download_id):
    """Hook to track download progress"""
    if d['status'] == 'downloading':
        try:
            percent_str = strip_ansi_codes(d.get('_percent_str', '0%')).strip()
            speed_str = strip_ansi_codes(d.get('_speed_str', 'N/A')).strip()
            eta_str = strip_ansi_codes(d.get('_eta_str', 'N/A')).strip()
            
            if percent_str and '%' in percent_str:
                percent_str = percent_str.replace('%', '').strip() + '%'
            
            try:
                percent_num = float(percent_str.replace('%', ''))
            except:
                percent_num = 0
            
            if download_id not in download_progress:
                download_progress[download_id] = {
                    'phase': 'video',
                    'last_percent': 0
                }
            
            current_data = download_progress[download_id]
            
            if current_data.get('last_percent', 0) > 90 and percent_num < 50:
                download_progress[download_id]['phase'] = 'audio'
            
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
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            # Android Client Emulation to bypass "Sign in" errors
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios'],
                    'player_skip': ['webpage', 'configs', 'js'],
                    'include_ssl_certificate': True
                }
            },
        }

        # Add Proxy if configured
        if os.environ.get('PROXY_URL'):
            ydl_opts['proxy'] = os.environ.get('PROXY_URL')

        # Add Cookies if configured
        if COOKIES_FILE:
            ydl_opts['cookiefile'] = COOKIES_FILE
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
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
            
            formats.sort(key=lambda x: int(x['quality'].replace('p', '')), reverse=True)
            
            return jsonify({
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
                'formats': formats[:10]
            })
    
    except Exception as e:
        raw_err = str(e)
        if _is_youtube_bot_error(raw_err):
            raw_err = (
                "YouTube blocked this request. The server's IP may be rate-limited. "
                "Try again in a few minutes or use a different video."
            )
        return jsonify({'error': raw_err}), 400

@app.route('/api/download', methods=['POST'])
def download_video():
    """Download video with selected quality"""
    try:
        data = request.json
        url = data.get('url')
        quality = data.get('quality', 'best')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        download_id = str(uuid.uuid4())
        download_progress[download_id] = {
            'status': 'starting',
            'percent': '0%',
            'speed': 'N/A',
            'eta': 'N/A'
        }
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(DOWNLOAD_DIR, f'{download_id}.%(ext)s'),
            'merge_output_format': 'mp4',
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [lambda d: progress_hook(d, download_id)],
            # Robust network options
            'socket_timeout': 30,
            'retries': 10,
            'fragment_retries': 10,
            'concurrent_fragment_downloads': 5,
            # Android Client Emulation to bypass "Sign in" errors
            'extractor_args': {
                'youtube': {
                    'player_client': ['android', 'ios'],
                    'player_skip': ['webpage', 'configs', 'js'],
                    'include_ssl_certificate': True
                }
            },
        }

        # Add Proxy if configured
        if os.environ.get('PROXY_URL'):
            ydl_opts['proxy'] = os.environ.get('PROXY_URL')

        # Add Cookies if configured
        if COOKIES_FILE:
            ydl_opts['cookiefile'] = COOKIES_FILE
        
        if quality != 'best':
            quality_num = quality.replace('p', '')
            ydl_opts['format'] = f'bestvideo[height<={quality_num}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality_num}][ext=mp4]/best'
        
        def download_thread():
            try:
                # Download with yt-dlp
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
                        "YouTube blocked this request from the server's IP address. "
                        "This is common on shared hosting. Try: 1) Wait a few minutes, "
                        "2) Use a different video, 3) Try during off-peak hours."
                    )
                download_progress[download_id] = {
                    'status': 'error',
                    'error': raw_err
                }
        
        thread = threading.Thread(target=download_thread)
        thread.start()
        
        return jsonify({
            'download_id': download_id,
            'message': 'Download started'
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
