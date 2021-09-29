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
    player_data = {"URL": url}
    player_page = requests.get(url)
    player_soup = BeautifulSoup(player_page.content, "html.parser")

    player_data["Name"] = player_soup.find('div', {"class": "pcdisplay-name"}).text

    age = player_soup.find_all('tr', {"class": 'info_tr_1'})
    player_data["Date of Birth"] = age[0].find('td').find('a')["title"].strip()

    player_data["Rating"] = player_soup.find('div', {"class": "pcdisplay-rat"}).text
    player_data["Position"] = player_soup.find('div', {"class": "pcdisplay-pos"}).text

    tab = player_soup.find_all('tr', {"class": ""})
    tab = [x for x in tab if x.find('th') != None]

    for i in ["Nation", "League", "Club", "Skills", "Weak Foot", "Foot", "Height", "Weight", "Att. WR", "Def. WR"]:
        player_data[i] = getInfo(i, tab)

    player_data["Card Type"] = player_soup.find("div", id="Player-card").get_attribute_list("data-level")[0]
    player_data["Rare"] = player_soup.find("div", id="Player-card").get_attribute_list("data-rare-type")[0]

    attr_groups = player_soup.find_all("div", {"class": "col-md-4 col-lg-4 col-6"})
    attrs = dict()
    for group in attr_groups:
        attr_names = [x.text for x in group.find_all('span', {"class": "ig-stat-name-tooltip"})]
        attr_vals = [x.text.strip() for x in group.find_all('div', {'class': "stat_val"})]
        attrs.update(dict(zip(attr_names, attr_vals)))

    player_data.update(attrs)
    return player_data

def getInfo(str, tab):
    info = [x.find("td", {'class': 'table-row-text'}).text for x in tab if x.find('th').text.strip() == str][0]
    return info


for page_number in range(1, 2):  #number_of_pages+1
    print(page_number)
    url = "https://www.futbin.com/22/players?page=" + str(page_number)
    players = players_list(url)
    for p in players:
        player_data = player(p)
        data = data.append(player_data, ignore_index=True)
        print(player_data['Name'])
    data.to_excel('fut22.xlsx')

# Stopped at 476

player_data
