import json
import spotipy
from scraper import scrape_tracks, scrape_artists, scrape_writers

CLIENT_ID = "YOUR CLIENT_ID HERE"
CLIENT_SECRET = "YOUR CLIENT_SERCRET HERE"
TOKEN = "YOUR TOKEN HERE"
START_ARTIST = "Lana Del Rey"
N_ARTIST_TO_SCRAPE = 10000

# Create authentication manager for Spotify.
auth_manager = spotipy.SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

print("[0/3] Starting to scrape.")

# Scrape artists starting from START_ARTIST and stop when you have scraped N_ARTISTS_TO_SCRAPE
# Get dictionary of artists and set of connections
artists, connections = scrape_artists.scrape(sp, START_ARTIST, N_ARTIST_TO_SCRAPE)

print("[1/3] Finished scrapping artists.")

# Save artists to JSON.
with open('data/raw/artists.json', 'w') as output_file:
    json.dump(artists, output_file, indent=2)

# Save connections to JSON.
with open('data/raw/connections.json', 'w') as output_file:
    json.dump(list(connections), output_file, indent=2)

# Get unique artist_ids.
artist_ids = set(artists.keys())

# Scrape artists top 10 tracks.
tracks = scrape_tracks.scrape(sp, artist_ids)

# Save tracks to JSON.
with open('data/raw/tracks.json', 'w') as output_file:
    json.dump(tracks, output_file, indent=2)

print("[2/3] Finished scrapping tracks.")

# Create a set of unique track_ids.
track_ids = set()
for artist_tracks in tracks.values():
    for track_id in artist_tracks.keys():
        track_ids.add(track_id)

# Scrape writers data from track_ids.
writers = scrape_writers.scrape(TOKEN, track_ids)

# Write writers to JSON.
with open('data/raw/writers.json', 'w') as output_file:
    json.dump(writers, output_file, indent=2)

print("[3/3] Finished scrapping writers.")
