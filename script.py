# script.py
import json
import datetime
import uuid
import os
from yt_dlp import YoutubeDL

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

# Bypass YouTube bot-check
os.environ['YT_DLP_BYPASS'] = '1'

ydl = YoutubeDL({
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'socket_timeout': 30,
    'retries': 3,
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    },
    'age_limit': 99,
    'skip_download': True,
})

# Read links
try:
    with open('links.txt') as f:
        urls = [line.strip() for line in f if line.strip().startswith('http')]
except FileNotFoundError:
    print("links.txt not found!")
    urls = []

entries = []

for url in urls:
    try:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            info = info['entries'][0]

        direct_url = info['url'].split('?')[0]

        entry = {
            "changeuuid": str(uuid.uuid4()),
            "stationuuid": str(uuid.uuid5(uuid.NAMESPACE_URL, url)),
            "serveruuid": str(uuid.uuid5(uuid.NAMESPACE_URL, url + "_srv")),
            "name": info.get('title', 'Unknown'),
            "url": url,
            "url_resolved": direct_url,
            "homepage": info.get('uploader_url', 'https://youtube.com'),
            "favicon": info.get('thumbnail', ''),
            "tags": "",
            "country": "User Defined (YouTube)",
            "countrycode": "YT",
            "iso_3166_2": None,
            "state": "",
            "language": "",
            "languagecodes": "",
            "votes": 0,
            "lastchangetime": now()[:-1],
            "lastchangetime_iso8601": now(),
            "codec": "MP3",
            "bitrate": info.get('abr', 128),
            "file_name_from_url": (info.get('title', 'song')[:50].replace(' ', '_') + ".mp3"),
            "hls": 0,
            "lastcheckok": 1,
            "lastchecktime": now()[:-1],
            "lastchecktime_iso8601": now(),
            "lastcheckoktime": now()[:-1],
            "lastcheckoktime_iso8601": now(),
            "lastlocalchecktime": now()[:-1],
            "lastlocalchecktime_iso8601": now(),
            "clicktimestamp": now()[:-1],
            "clicktimestamp_iso8601": now(),
            "clickcount": 0,
            "clicktrend": 0,
            "ssl_error": 0,
            "geo_lat": None,
            "geo_long": None,
            "geo_distance": None,
            "has_extended_info": False
        }
        entries.append(entry)
        print(f"Success: {info['title']}")
    except Exception as e:
        print(f"Failed: {url} → {e}")

# Save
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(entries, f, indent=2, ensure_ascii=False)

print(f"\n{len(entries)} stations saved to output.json")
