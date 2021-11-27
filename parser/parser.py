import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from config import URL
from selenium import webdriver


class Parse:
    def __init__(self) -> None:
        option = webdriver.FirefoxOptions()
        option.set_preference('dom.webdriver.enabled', False)
        option.set_preference('dom.webnotifications.enabled', False)
        option.set_preference('media.volume_scale', '0.0')
        option.headless = True
        self.driver = webdriver.Firefox(options=option)

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
            res.append(items[i].text)
            res.append('https://kpolyakov.spb.ru/' + items[i].find('img')['src'].replace('../../', ''))
            res.append(items2[i].text)
        return res

    def driver_close(self):
        self.driver.quit()
    
    def main(self):
        self.go_to_page(URL)
        html = self.get_html_selenium()
        self.driver_close()
        res = self.get_td(html)
        return res

a = Parse()
for i in a.main():
    print(i)
    print('_------------------------------------_')
