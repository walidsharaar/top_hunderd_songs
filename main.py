from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


#website url
URL = "https://www.billboard.com/charts/hot-100/"
#Spotify Authentication
CLIENT_ID ="b6a721c6a21b46f9bc8a626e6ce1c5e7"
CLIENT_SECRET="6d46d4728d92451da5a284d339768563"
REDIRECT_URL="http://example.com"


#ask user the date
user_date = input("What day in the past do you want to travel back? Type YYYY-MM-DD \n")
response = requests.get(f"{URL}{user_date}")
billboard = response.text
soup = BeautifulSoup(billboard, "html.parser")
song_names_spans = soup.find_all("span", class_="chart-element__information__son")
#playlist_song = soup.find_all(name='span', class_='chart-element__information__song text--truncate color--primary')
#playlist_song = [(item.getText()) for item in playlist_song]
#playlist_author = soup.find_all(name='span', class_='chart-element__information__artist text--truncate color--secondary')
#playlist_author = [(item.getText()) for item in playlist_author]
#complete_list = [(item1+" - "+item2) for (item1, item2) in zip(playlist_author, playlist_song)]
song_names = [song.getText() for song in song_names_spans]

# Spotify Authentication

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URL,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.text"
    )
)

#get user id
user_id = sp.current_user()["id"]
print(user_id)

song_uris =[]
year= user_date.split("-")[0]

for song in song_names:
    result= sp.search(q=f"track :{song} year:{year}",type="track")
    print(result)
    try:
        uri= result["track"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped")

#create private playlist in spotify

playlist= sp.user_playlist_create(user=user_id, name=f"{user_date} Billboard 100",public=False)

#Adding found songs into the playlist

sp.playlist_add_items(playlist_id=playlist["id"],items=song_uris)


