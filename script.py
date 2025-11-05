# script.py
import json, datetime, uuid, os
from yt_dlp import YoutubeDL

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00','Z')

ydl = YoutubeDL({
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'socket_timeout': 15,
    'retries': 2,
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    },
    'age_limit': 99,
    'skip_download': True,
    'extractor_args': {'youtube': {'player_client': ['web']}},
})

# READ LINKS
try:
    urls = [l.strip() for l in open('links.txt') if l.strip().startswith('http')]
except:
    urls = []

entries = []
for url in urls:
    try:
        info = ydl.extract_info(url, download=False)
        if 'entries' in info:
            info = info['entries'][0]

        direct = info['url'].split('?')[0]
        title = info.get('title','Live')[:60]

        entries.append({
            "changeuuid": str(uuid.uuid4()),
            "stationuuid": str(uuid.uuid5(uuid.NAMESPACE_URL, url)),
            "serveruuid": str(uuid.uuid5(uuid.NAMESPACE_URL, url+"_srv")),
            "name": title,
            "url": url,
            "url_resolved": direct,
            "homepage": info.get('uploader_url','https://youtube.com'),
            "favicon": info.get('thumbnail',''),
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
            "bitrate": info.get('abr',128),
            "file_name_from_url": title.replace(' ','_') + ".mp3",
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
        })
        print(f"Success: {title}")
    except Exception as e:
        print(f"Failed: {url} → {e}")

json.dump(entries, open('output.json','w'), indent=2)
print(f"\n{len(entries)} WORKING stations → output.json")
