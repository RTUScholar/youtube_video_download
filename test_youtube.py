#!/usr/bin/env python3
"""Test YouTube download with bot bypass"""

import yt_dlp

# Test URL
url = "https://www.youtube.com/watch?v=I6ps_05Wsf0"

# Configuration with bot bypass
ydl_opts = {
    'quiet': False,
    'no_warnings': False,
    'extractor_args': {
        'youtube': {
            'player_client': ['android', 'ios', 'mweb'],
            'player_skip': ['webpage', 'configs'],
            'skip': ['dash', 'hls'],
        }
    },
    'http_headers': {
        'User-Agent': 'com.google.android.youtube/19.29.37 (Linux; U; Android 14) gzip',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9',
    },
}

print("Testing YouTube download with bot bypass...")
print(f"URL: {url}\n")

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print("Extracting video info...")
        info = ydl.extract_info(url, download=False)
        
        print(f"\n✅ SUCCESS!")
        print(f"Title: {info.get('title', 'Unknown')}")
        print(f"Duration: {info.get('duration', 0)} seconds")
        print(f"View count: {info.get('view_count', 0):,}")
        print(f"\nAvailable formats: {len(info.get('formats', []))}")
        
        # Show some quality options
        qualities = set()
        for f in info.get('formats', []):
            if f.get('height'):
                qualities.add(f"{f.get('height')}p")
        
        print(f"Qualities available: {sorted(qualities, key=lambda x: int(x.replace('p', '')), reverse=True)}")
        
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
