import json
from time import sleep

import spotipy
from spotipy import SpotifyClientCredentials

CLIENT_ID = "YOUR CLIENT_ID HERE"
CLIENT_SECRET = "YOUR CLIENT_SERCRET HERE"


def scrape(sp, artist_ids):
    artist_tracks = {}

    try:
        for artist_id in artist_ids:

            top_tracks = None
            while top_tracks is None:
                try:
                    top_tracks = sp.artist_top_tracks(artist_id)
                except:
                    print('Error for artist_id', artist_id)
                    sleep(3)
                    pass

            tracks = {}
            for track in top_tracks['tracks']:
                tracks[track['id']] = {'name': track['name'],
                                       'popularity': track['popularity']}

            track_features = None
            while track_features is None:
                try:
                    track_features = sp.audio_features(list(tracks.keys()))
                except:
                    print('Error for artist_id', artist_id, 'track features.')
                    sleep(3)
                    pass

            for track in track_features:
                if track is None:
                    continue

                track_id = track['id']

                # Remove properties we don't want.
                del track['id']
                del track['type']
                del track['uri']
                del track['track_href']
                del track['analysis_url']

                tracks[track_id].update(track)

            artist_tracks[artist_id] = tracks
            print("Scraped tracks for", len(artist_tracks), 'out of', len(artist_ids), 'artists.')
            sleep(2)

    finally:
        return artist_tracks


if __name__ == '__main__':
    with open('../data/raw/artists.json', 'r') as input_file:
        artists = json.load(input_file)

    artist_ids = set(artists.keys())

    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    tracks = scrape(sp, artist_ids)

    with open('../data/raw/tracks.json', 'w') as output_file:
        json.dump(tracks, output_file, indent=2)
