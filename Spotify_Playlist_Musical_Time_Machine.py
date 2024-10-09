from dotenv import load_dotenv
import os
import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

invalid_date = False
date = ""
track_uri_list = []


def request_date():
    return input("which year do you want to travel to? Type the date in this format: YYYY-MM-DD: ")


# Billboard 100
while not invalid_date:
    date = request_date()
    if len(date) >= 10 and date[4] == "-" and date[7] == "-":
        invalid_date = True
        
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
  }

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}/", headers=header)
hot_100 = response.text
soup = BeautifulSoup(hot_100, "html.parser")

song_list = [songs.getText().strip() for songs in soup.select(selector="li h3", class_="c-title")]
del song_list[100:111]

load_dotenv(dotenv_path='.env')

# Spotify
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
username= os.getenv('USER_NAME')
redirect_uri = "http://localhost:8888/callback"
scope = "playlist-modify-private"

# Authorization
# Had to authenticate how the guide did it, documentation sucks
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:8888/callback",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username= os.getenv('USERNAME'),
    )
)
user_id = sp.current_user()["id"]


# Adding tracks to the playlist
def get_track_id(song_name):
    result = sp.search(q=song_name, type='track', limit=1)
    if result['tracks']['items']:
        track = result['tracks']['items'][0]  # Get the first result
        return track['uri']  # Return track ID, name, and artist
    return None


# Iterate through our songs list to get the uri and add them all to a list
for song in song_list:
    track_uri = get_track_id(song)
    #
    if track_uri:
        track_uri_list.append(track_uri)
    else:
        print(f"Track not found for song name: {song}")


# Playlist creation
new_playlist = sp.user_playlist_create(user=user_id, name=date, public=False, collaborative=False, description="")
playlist_id = new_playlist['id']


# add songs to the playlist using the uri's gathered
sp.playlist_add_items(playlist_id=playlist_id, items=track_uri_list, position=None)