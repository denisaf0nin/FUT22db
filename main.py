# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


URL = "https://www.futbin.com/22/players"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, "html.parser")


# Get number of pages
page_link = [p.text for p in soup.find_all(class_="page-link")]
page_link = [int(p) for p in page_link if p.isdigit()]
number_of_pages = max(page_link)

data = pd.DataFrame( columns= ['Name', 'Rating', 'Position', 'Nation', 'League', 'Club', 'Card Type', 'Rare'])

def players_list(url):
    page = requests.get(url)
    time.sleep(5)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find_all('tr')
    players = [row.get_attribute_list('data-url')[0] for row in table if row.has_attr('data-url')]
    players = ["https://www.futbin.com" + player for player in players]
    return players


def player(url):
    player_page = requests.get(url)
    player_soup = BeautifulSoup(player_page.content, "html.parser")
    name = player_soup.find('div', {"class": "pcdisplay-name"}).text
    rating = player_soup.find('div', {"class": "pcdisplay-rat"}).text
    position = player_soup.find('div', {"class": "pcdisplay-pos"}).text

    tab = player_soup.find_all('tr', {"class": ""})
    tab = [x for x in tab if x.find('th') != None]

    nation = [x.find("td", {'class': 'table-row-text'}).text for x in tab if x.find('th').text == "Nation"][0]
    league = [x.find("td", {'class': 'table-row-text'}).text for x in tab if x.find('th').text == "League"][0]
    club = [x.find("td", {'class': 'table-row-text'}).text for x in tab if x.find('th').text == "Club"][0]
    card_type = player_soup.find("div", id="Player-card").get_attribute_list("data-level")[0]
    rare = player_soup.find("div", id="Player-card").get_attribute_list("data-rare-type")[0]
    player_data = {'Name': name, 'Rating': rating, 'Position': position, 'Nation': nation, 'League': league,
         'Club': club, 'Card Type': card_type, 'Rare': rare}
    return player_data

for page_number in range(1,number_of_pages+1):
    print(page_number)
    url = "https://www.futbin.com/22/players?page=" + str(page_number)
    players = players_list(url)
    for p in players:
        player_data = player(p)
        data = data.append(player_data, ignore_index=True)
        print(player_data['Name'])
    data.to_excel('fut22.xlsx')

