import requests
import json
from time import sleep


TOKEN = "YOUR TOKEN HERE"


def scrape(token, track_ids):
    track_writers = {}

    try:
        for track_id in track_ids:
            request_url = f"https://spclient.wg.spotify.com/track-credits-view/" \
                          f"v0/experimental/{track_id}/credits"

            response = requests.get(request_url, headers={
                'authorization': token,
            })
            data = response.json()

            track_writers[track_id] = {
                'labels': data['sourceNames'],
                'credits': data['roleCredits'],
                'extended_credits': data['extendedCredits']
            }
            print("Scrapped writers for", len(track_writers), "out of", len(track_ids), 'tracks.')
            sleep(1)

    finally:
        return track_writers


if __name__ == '__main__':
    with open('../data/raw/tracks.json', 'r') as input_file:
        tracks = json.load(input_file)

    track_ids = set()
    for artist_tracks in tracks.values():
        for track_id in artist_tracks.keys():
            track_ids.add(track_id)

    writers = scrape(TOKEN, track_ids)

    with open('../data/raw/writers.json', 'w') as output_file:
        json.dump(writers, output_file, indent=2)
