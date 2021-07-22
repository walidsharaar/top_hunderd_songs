import requests
from bs4 import BeautifulSoup

URL = "https://www.billboard.com/charts/hot-100"
#ask user input
user_date = input("Which year's song do you want to listen? Please enter the date in this format YYYY-MM-DD\n")

print(user_date)

# Scrape top 100 song from https://www.billboard.com/charts/hot-100

reponse = requests.get(URL)
print(reponse.text)
