import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests 
# --------------------------------------------------------------- #
date = input('Choose the year you want to travel to (format YYYY-MM-DD): ')
# ------------------ GETTING DATA FROM BILLBOARD ------------------ #
response = requests.get('https://www.billboard.com/charts/hot-100/' + date)
soup = BeautifulSoup(response.text, 'html.parser')
song_row = soup.find_all(name="div", class_='o-chart-results-list-row-container')
song_names = [song.ul.h3.getText().replace('\n', '').replace('\t', '') for song in song_row]
author_names = [song.find_all(name='span')[1].getText().replace('\n', '').replace('\t', '') for song in song_row]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://localhost:8888/callback",
        client_id="YOUR_CLIENT_ID",
        client_secret="YOUR_CLIENT_SERVER",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.me()['id']  

def get_uri(sn, date):
    song_uri = []
    year = date.split('-')[0]
    for song in sn:
        res = sp.search(q=f"track:{song} year:{year}", type="track")
        print(res)
        try:
            uri=res['tracks']['items'][0]['uri']
            song_uri.append(uri)
        except IndexError:
            print(f"{song} doesn't exist in spotify")
    return song_uri
#uri
song_uri = get_uri(sn=song_names, date=date)
playlist = sp.user_playlist_create(user_id, name=f'{date} Billboard100', public=False, collaborative=False, description=f'Billboard playlist of the {date}')
sp.playlist_add_items(playlist_id=playlist['id'], items=song_uri)