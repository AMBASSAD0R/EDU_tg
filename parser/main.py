import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def generate_headers():
    ua = UserAgent()
    return {'User-Agent':ua.random}


def get_html(url):
    HEADERS = generate_headers()
    response = requests.get(url, headers=HEADERS)
    return response.content


def get_td(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.findAll('td', class_='topicview')
    items2 = soup.findAll('td', class_='answer')
    res = []
    for i in range(len(items)):
        res.append(items[i])
        res.append(items2[i])
    return res
