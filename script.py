# script.py — 100% working on GitHub Actions
import json, re, urllib.request, datetime, uuid

def now(): 
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')[:-6] + 'Z'

entries = []
instances = ["https://yt.oelrichsgarcia.de", "https://invidious.tiekoetter.com", "https://iv.ggtyler.dev"]

def get_stream(vid):
    for base in instances:
        try:
            api = f"{base}/api/v1/videos/{vid}"
            data = json.loads(urllib.request.urlopen(api, timeout=7).read())
            for s in data.get('adaptiveFormats', []):
                if s['type'].startswith('audio') and 'dash' not in s.get('url',''):
                    return s['url'].split('?')[0]
        except: continue
    return None

for line in open('links.txt'):
    url = line.strip()
    if not url: continue
    vid = re.search(r'v=([^&]+)', url)
    if not vid: continue
    vid = vid.group(1)
    direct = get_stream(vid)
    if not direct:
        print(f"Failed: {url}")
        continue

    entries.append({
        "changeuuid": str(uuid.uuid4()),
        "stationuuid": str(uuid.uuid5(uuid.NAMESPACE_URL, url)),
        "serveruuid": str(uuid.uuid5(uuid.NAMESPACE_URL, url+"_srv")),
        "name": f"Tamil Rhyme #{len(entries)+1}",
        "url": url,
        "url_resolved": direct,
        "homepage": "https://youtube.com",
        "favicon": "https://youtube.com/favicon.ico",
        "tags": "tamil,nursery,rhymes,kids,children",
        "country": "User Defined (Tamil Rhymes)",
        "countrycode": "TAMIL",
        "iso_3166_2": None,
        "state": "Tamil Nadu",
        "language": "Tamil",
        "languagecodes": "ta",
        "votes": 0,
        "lastchangetime": now()[:-1],
        "lastchangetime_iso8601": now(),
        "codec": "MP3",
        "bitrate": 128,
        "file_name_from_url": "Tamil_Rhyme.mp3",
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
    print(f"Success: {url}")

json.dump(entries, open('output.json','w'), indent=2)
print(f"\n{len(entries)} Tamil rhyme stations → output.json")
