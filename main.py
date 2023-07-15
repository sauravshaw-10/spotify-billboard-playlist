import requests
import spotify as spotify
from bs4 import BeautifulSoup


#-----------------------------Billboard------------------------#
date = input("Which year would you like to travel to? Type the date in this format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(URL)
billboard = response.text
soup = BeautifulSoup(billboard, "html.parser")

# print(soup.prettify())

billboard_hot_100 = [song.getText().strip() for song in soup.select("li ul li h3")]


#---------------------------SPOTIFY-------------------------#
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="34c3d2920c1d49aa8ad88ac71dfc1369",
                                               client_secret="efd180c0466b477abadcb1c90fb73e4e",
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt",
                                               username="3166k6ltwap3rg6vwpncyi42cowy"
                                              ))

user_id = sp.current_user()['id']


#--------------SONG INFO (URIs)-----------------#
from pprint import pprint

spy = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="34c3d2920c1d49aa8ad88ac71dfc1369",
                                                                        client_secret="efd180c0466b477abadcb1c90fb73e4e"))

track_uris = []
for item in billboard_hot_100:
    search_str = f"track: {item} year: {date[:4]}"
    try:
        result = spy.search(q=search_str, type="track")
    except IndexError:
        print("No songs found")
    else:
        track = result['tracks']['items'][0]['uri']
        track_uris.append(track)

#-----------Create Playlist and Add Items----------#

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
add_tracks = sp.playlist_add_items(playlist_id=playlist["id"], items=track_uris)
pprint(add_tracks)
























