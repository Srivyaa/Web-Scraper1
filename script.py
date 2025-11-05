# script.py
import json, datetime, uuid, re, urllib.request, urllib.parse

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')[:-6]+'Z'

entries = []
instances = [
    "https://yewtu.be", "https://vid.puffyan.us", "https://invidious.fdn.fr",
    "https://invidious.snopyta.org", "https://inv.riverside.rocks"
]

def get_direct(url):
    vid = re.search(r'v=([^&]+)', url)
    if not vid: return None
    vid = vid.group(1)
    for base in instances:
        try:
            api = f"{base}/api/v1/videos/{vid}"
            data = json.loads(urllib.request.urlopen(api, timeout=8).read())
            for fmt in data['formatStreams']:
                if fmt['quality'].startswith('audio'):
                    return fmt['url']
        except: continue
    return None

for line in open('links.txt'):
    url = line.strip()
    if not url: continue
    direct = get_direct(url)
    if not direct:
        print(f"Failed: {url}")
        continue

    entries.append({
        "changeuuid": str(uuid.uuid4()),
        "stationuuid": str(uuid.uuid5(uuid.NAMESPACE_URL, url)),
        "serveruuid": str(uuid.uuid5(uuid.NAMESPACE_URL, url+"_srv")),
        "name": urllib.parse.unquote(url.split('v=')[1].split('&')[0])[:60],
        "url": url,
        "url_resolved": direct,
        "homepage": "https://youtube.com",
        "favicon": "https://youtube.com/favicon.ico",
        "tags": "Tamil,Nursery,Rhymes,Kids",
        "country": "User Defined (Tamil Rhymes)",
        "countrycode": "TAMIL",
        "iso_3166_2": None,
        "state": "",
        "language": "ta",
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
