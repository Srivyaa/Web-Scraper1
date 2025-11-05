# script.py
import json, datetime, uuid, os
from yt_dlp import YoutubeDL

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')

# MAGIC LINE → bypasses 99 % of “Sign in” blocks
os.environ['YT_DLP_BYPASS'] = '1'

ydl = YoutubeDL({
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'extract_flat': False,
    'retries': 3,
    'fragment_retries': 5,
    'socket_timeout': 30,
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    },
    # ↓↓↓ THE 3 LINES THAT KILL AGE-GATE
    'age_limit': 99,
    'skip_download': True,
    'extractor_args': {'youtube': {'skip': ['dash', 'hls']}},
})

with open('links.txt') as f:
    urls = [u.strip() for u in f if u.strip().startswith('http')]

entries = []
for url in urls:
    try:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            info = info['entries'][0]

        direct = info['url'].split('?')[0]  # clean URL
        entries.append({
            "changeuuid": str(uuid.uuid4()),
            "stationuuid": str(uuid.uuid5(uuid.NAMESPACE_URL, url)),
            "serveruuid": str(uuid.uuid5(uuid.NAMESPACE_URL
