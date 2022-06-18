import json
from collections import OrderedDict
from time import sleep

import spotipy
from spotipy import SpotifyClientCredentials


CLIENT_ID = "YOUR CLIENT_ID HERE"
CLIENT_SECRET = "YOUR CLIENT_SECRET HERE"
START_ARTIST = "Lana Del Rey"
N_ARTIST_TO_SCRAPE = 10000


def add_artist(artist_store, artist):
    artist_store[artist['id']] = {
        'name': artist['name'],
        'popularity': artist['popularity'],
        'genres': artist['genres'],
        'n_followers': artist['followers']['total']
    }


def scrape(sp, artist_name, max_artists):

    results = sp.search(q='artist:' + artist_name, type='artist')
    items = results['artists']['items']
    artist = items[0]

    # Store artists information
    artist_store = {}
    # Store unique connections between artists
    connections_store = set()

    add_artist(artist_store, artist)

    # List of artists yet to process
    to_scrape = OrderedDict()
    to_scrape[artist['id']] = None
    # List of already processed artists.
    processed_artists = set()

    try:

        while to_scrape:
            source_artist_id, _ = to_scrape.popitem()
            processed_artists.add(source_artist_id)

            related_artists = None
            while related_artists is None:
                try:
                    related_artists = sp.artist_related_artists(source_artist_id)
                except:
                    print('Error for source_artist_id', source_artist_id, 'related artists.')
                    sleep(3)
                    pass

            for related_artist in related_artists['artists']:
                # Save connection information
                connections_store.add((source_artist_id, related_artist['id']))
                # Save artist information
                add_artist(artist_store, related_artist)

                if related_artist['id'] not in processed_artists:
                    if related_artist['id'] not in to_scrape:
                        to_scrape[related_artist['id']] = None

            print('Scrapped', len(artist_store), 'artists and found',
                  len(connections_store), 'connections.',
                  len(to_scrape), 'artists left to scrape.')

            if len(artist_store) > max_artists:
                break

            sleep(1)

    finally:
        return artist_store, connections_store


if __name__ == '__main__':
    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    artists, connections = scrape(sp, START_ARTIST, N_ARTIST_TO_SCRAPE)

    with open('../data/raw/artists.json', 'w') as output_file:
        json.dump(artists, output_file, indent=2)

    with open('../data/raw/connections.json', 'w') as output_file:
        json.dump(list(connections), output_file, indent=2)
