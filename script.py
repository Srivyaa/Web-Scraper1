import json
import datetime
import uuid
from yt_dlp import YoutubeDL

def get_current_time_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')

def generate_entry(youtube_url):
    current_time = get_current_time_iso()
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
    
    # Assume single video; if playlist, take the first entry
    if 'entries' in info:
        info = info['entries'][0]
    
    direct_url = info['url']
    name = info['title']
    thumbnail = info.get('thumbnail', '')
    bitrate = info.get('abr', 0)
    codec = info.get('acodec', 'MP3').upper()  # Default to MP3 if unknown
    tags = ','.join(info.get('tags', []))
    language = info.get('language', '')
    file_name = f"{name.replace(' ', '_')}.mp3"  # Simplified file name
    
    # Generate consistent UUIDs based on URL
    namespace = uuid.NAMESPACE_URL
    stationuuid = str(uuid.uuid5(namespace, youtube_url))
    serveruuid = str(uuid.uuid5(namespace, youtube_url + '_server'))
    changeuuid = str(uuid.uuid4())  # New change UUID each time
    
    return {
        "changeuuid": changeuuid,
        "stationuuid": stationuuid,
        "serveruuid": serveruuid,
        "name": name,
        "url": youtube_url,
        "url_resolved": direct_url,
        "homepage": info.get('channel_url', 'https://www.youtube.com'),
        "favicon": thumbnail if thumbnail else "https://www.youtube.com/favicon.ico",
        "tags": tags,
        "country": "User Defined (YouTube)",
        "countrycode": "YT",
        "iso_3166_2": "",
        "state": "",
        "language": language,
        "languagecodes": language,
        "votes": 0,
        "lastchangetime": current_time[:-1],  # Without Z for this field as per example
        "lastchangetime_iso8601": current_time,
        "codec": codec,
        "bitrate": bitrate,
        "file_name_from_url": file_name,
        "hls": 0,
        "lastcheckok": 1,
        "lastchecktime": current_time[:-1],
        "lastchecktime_iso8601": current_time,
        "lastcheckoktime": current_time[:-1],
        "lastcheckoktime_iso8601": current_time,
        "lastlocalchecktime": current_time[:-1],
        "lastlocalchecktime_iso8601": current_time,
        "clicktimestamp": current_time[:-1],
        "clicktimestamp_iso8601": current_time,
        "clickcount": 0,
        "clicktrend": 0,
        "ssl_error": 0,
        "geo_lat": None,
        "geo_long": None,
        "geo_distance": None,
        "has_extended_info": False
    }

def main():
    with open('links.txt', 'r') as f:
        links = f.readlines()
    
    entries = []
    for link in links:
        link = link.strip()
        if link:
            try:
                entry = generate_entry(link)
                entries.append(entry)
            except Exception as e:
                print(f"Error processing {link}: {e}")
    
    with open('output.json', 'w') as f:
        json.dump(entries, f, indent=2)

if __name__ == "__main__":
    main()
