import os
import json
import math
import time
import spotipy
import webbrowser
from spotipy.oauth2 import SpotifyOAuth

'''

In Windows to declare necessary environment variables:

set SPOTIPY_CLIENT_ID=value
set SPOTIPY_CLIENT_SECRET=value
set SPOTIPY_REDIRECT_URI=path

To verify:

echo %SPOTIPY_CLIENT_ID%
echo %SPOTIPY_CLIENT_SECRET%
echo %SPOTIPY_REDIRECT_URI%

'''


# Declare necessary environment variables
def env_variables(client_id, client_secret, redirect_uri):
    os.environ['SPOTIPY_CLIENT_ID'] = client_id
    os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
    os.environ['SPOTIPY_REDIRECT_URI'] = redirect_uri


# Retrieve the list of playlists from the user
def display_user_playlists(sp):
    current_user_playlists = sp.current_user_playlists()
    current_user_playlists = current_user_playlists["items"]

    for i, playlist in enumerate(current_user_playlists):
        print(f"\n{i + 1}. {playlist['name']}")
        print(f"Total songs: {playlist['tracks']['total']}")

    return current_user_playlists


# Retrieve the song list from a playlist
def display_playlist(sp):
    current_user_playlists = display_user_playlists(sp)

    playlist_name = input("\nWhat playlist do you want to display?: ")

    playlist_tracks = []

    final_playlist_tracks = []

    for i, playlist in enumerate(current_user_playlists):
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
            laps = math.ceil(int(playlist['tracks']['total']) / 100)
            for lap in range(laps):
                result = sp.playlist_items(playlist_id=playlist_id, limit=100, offset=lap*100)
                time.sleep(1)
                playlist_tracks.extend(result['items'])
            break

    print(f"\n\n{playlist_name.upper()}")
    for i, track in enumerate(playlist_tracks):
        try:
            artists = []
            if track is not None:
                for artist in track['track']['artists']:
                    artists.append(artist['name'])
                print(f"\n{i + 1}. {track['track']['name']} - {', '.join(artists)}")
                final_playlist_tracks.append(f"{track['track']['name']} - {', '.join(artists)}")
        except TypeError as e:
            print(f"{e}")
            continue

    return final_playlist_tracks


# Main loop
while True:
    # Extract credentials from txt
    doc = open('./credentials.txt', 'r', encoding='utf-8')

    credentials = {}

    for line in doc:
        # Divide each line using "="
        key, value = line.strip().split('=')

        credentials[key] = value

    doc.close()

    env_variables(client_id=credentials['client_id'], client_secret=credentials['client_secret'],
                  redirect_uri=credentials['redirect_uri'])

    print("\n\nWelcome to PlaylistSync")
    print("1. Retrieve the song list from a playlist")
    print("2. Exit")
    choice = input("Choice: ")

    if choice == "1":
        scope = "user-library-read user-read-private playlist-read-private"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

        playlist_tracks = display_playlist(sp)

        doc = open("./playlist.txt", "w", encoding='utf-8')

        for track in playlist_tracks:
            doc.write(str(track) + "\n")

        doc.close()

    if choice == "2":
        break
