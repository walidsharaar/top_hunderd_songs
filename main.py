from bs4 import BeautifulSoup
import requests

URL = "https://www.billboard.com/charts/hot-100/"
user_date = input("What day in the past do you want to travel back? Type YYYY-MM-DD ")
response = requests.get(f"{URL}{user_date}")
billboard = response.text
soup = BeautifulSoup(billboard, "html.parser")
playlist_song = soup.find_all(name='span', class_='chart-element__information__song text--truncate color--primary')
playlist_song = [(item.getText()) for item in playlist_song]
playlist_author = soup.find_all(name='span', class_='chart-element__information__artist text--truncate color--secondary')
playlist_author = [(item.getText()) for item in playlist_author]

complete_list = [(item1+" - "+item2) for (item1, item2) in zip(playlist_author, playlist_song)]

with open(f"{user_date}_playlist.txt", mode="w") as file:
    for song in complete_list:
        file.write(f"{song}\n")