import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from config import URL
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Parse:
    def __init__(self) -> None:
        self.driver = webdriver.Firefox()

    def go_to_page(self, url):
        self.driver.get(url)

    def generate_headers(self):
        ua = UserAgent()
        return {'User-Agent': ua.random}

    def get_html_selenium(self):
        pageSource = self.driver.page_source
        return pageSource

    def get_html_requests(self, url):
        HEADERS = self.generate_headers()
        response = requests.get(url, headers=HEADERS)
        return response.content


    def get_td(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.findAll('td', class_='topicview')
        items2 = soup.findAll('td', class_='answer')
        res = []
        for i in range(len(items)):
            res.append(items[i])
            res.append(items2[i])
        return res
    
    def main(self):
        self.go_to_page(URL)
        html = self.get_html_selenium()
        print(html)

a = Parse()
a.main()
#print(get_td(get_html(URL)))
