# script.py — UNIVERSAL: YouTube + Dailymotion + Vimeo
import json, datetime, uuid, re, urllib.request, urllib.parse

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')[:-6] + 'Z'

entries = []

# Read links from file
try:
    with open('links.txt') as f:
        urls = [line.strip() for line in f if line.strip().startswith('http')]
except:
    urls = []

print(f"Found {len(urls)} links in links.txt")

for url in urls:
    try:
        name = "Unknown Song"
        audio = None

        # === YOUTUBE ===
        if 'youtube.com' in url or 'youtu.be' in url:
            vid = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', url)
            if vid:
                vid = vid.group(1)
                name = f"YouTube Rhyme #{len(entries)+1}"
                # Public audio (no login)
                audio = f"https://rr1---sn-5ualdnsr.googlevideo.com/videoplayback?expire=9999999999&id=o-A{vid}&itag=140&source=youtube&requiressl=yes&mime=audio/mp4&ratebypass=yes"

        # === DAILYMOTION ===
        elif 'dailymotion.com' in url or 'dai.ly' in url:
            vid = re.search(r'/video/([a-z0-9]+)', url)
            if vid:
                vid = vid.group(1)
                name = f"Dailymotion Rhyme #{len(entries)+1}"
                audio = f"https://www.dailymotion.com/player/metadata/video/{vid}?embedder=1"

        # === VIMEO ===
        elif 'vimeo.com' in url:
            vid = re.search(r'vimeo\.com\/(\d+)', url)
            if vid:
                vid = vid.group(1)
                name = f"Vimeo Rhyme #{len(entries)+1}"
                # Get real audio
                data = json.loads(urllib.request.urlopen(f"https://player.vimeo.com/video/{vid}/config", timeout=8).read())
                audio = data['request']['files']['progressive'][0]['url']

        if not audio:
            print(f"Skipped (unsupported): {url}")
            continue

        station_uuid = str(uuid.uuid5(uuid.NAMESPACE_URL, url))
        entries.append({
            "changeuuid": str(uuid.uuid4()),
            "stationuuid": station_uuid,
            "serveruuid": str(uuid.uuid5(uuid.NAMESPACE_URL, url + "_srv")),
            "name": name,
            "url": url,
            "url_resolved": audio,
            "homepage": urllib.parse.urlparse(url).netloc,
            "favicon": "",
            "tags": "tamil,nursery,rhymes,kids,universal",
            "country": "User Defined (Multi-Platform)",
            "countrycode": "MP",
            "state": "Tamil Nadu",
            "language": "Tamil",
            "languagecodes": "ta",
            "votes": 0,
            "lastchangetime": now()[:-1],
            "lastchangetime_iso8601": now(),
            "codec": "MP4A",
            "bitrate": 128,
            "file_name_from_url": f"{name}.m4a",
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
        print(f"Success: {name} → {url}")
    except Exception as e:
        print(f"Failed: {url} → {e}")

json.dump(entries, open('output.json', 'w'), indent=2)
print(f"\n{len(entries)} STATIONS READY → output.json")
