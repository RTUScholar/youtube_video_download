#!/usr/bin/env python3
"""Test YouTube download with bot bypass"""

import yt_dlp

# Test URL
url = "https://www.youtube.com/watch?v=I6ps_05Wsf0"

# Configuration with Android client only (most reliable)
ydl_opts = {
    'quiet': False,
    'no_warnings': False,
    'extractor_args': {
        'youtube': {
            'player_client': ['android'],
            'player_skip': ['webpage', 'configs'],
        }
    },
    'http_headers': {
        'User-Agent': 'com.google.android.youtube/19.29.37 (Linux; U; Android 14) gzip',
    },
}

print("Testing YouTube download with Android client...")
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
        
        # Check if format 18 is available (360p with audio, most reliable)
        format_18 = next((f for f in info.get('formats', []) if f.get('format_id') == '18'), None)
        if format_18:
            print(f"\n✅ Format 18 (360p combined) available: {format_18.get('ext')}")
        
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
