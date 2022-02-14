import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from config import URL
from selenium import webdriver
import requests
from sql import SQL
import telebot
import time


class Parse:
    def __init__(self) -> None:
        option = webdriver.FirefoxOptions()
        option.set_preference('dom.webdriver.enabled', False)
        option.set_preference('dom.webnotifications.enabled', False)
        option.set_preference('media.volume_scale', '0.0')
        option.headless = True
        self.driver = webdriver.Firefox(options=option)
        self.db = SQL('C:/Users/zuiko/Desktop/EDU_tg/database.db')
        self.bot = telebot.TeleBot('2104313952:AAFb6dtxWE8d2vFdEi1k2ZYg81xwNCMz_gA')

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
            sp = []
            sp1 = self.work_text_task(items[i].text)
            sp.append(sp1[1])
            sp.append(sp1[0])
            try:
                url = 'https://kpolyakov.spb.ru/' + items[i].find('a')['href'].replace('../../', '')
                path = '../data/' + url.split('/')[-1]
                self.get_file(url, path)
                file_id = self.work_document('604900292', path)
                sp.append(file_id)
            except Exception as e:
                print(e)
            try:
                url = 'https://kpolyakov.spb.ru/' + items[i].find('img')['src'].replace('../../', '')
                path = '../data/' + url.split('/')[-1]
                self.get_file(url, path)
                file_id = self.work_photo('604900292', path)
                sp.append(file_id)
            except Exception as e:
                print(e)
            sp.append(self.work_text_answer(items2[i].text))
            res.append(sp)
        return res

    def driver_close(self):
        self.driver.quit()

    def get_file(self, url, path):
        p = requests.get(url)
        out = open(path, "wb")
        out.write(p.content)
        out.close()

    def get_index_space(self, text):
        ind = 0
        count_space = 0
        for j, i in enumerate(text):
            if i == ' ':
                ind = j
                count_space += 1
            if count_space == 1:
                return ind

    def work_text_task(self, text):
        ind = self.get_index_space(text)
        id = text[:ind]
        id1 = ''
        for i in id:
            if i in '0123456789':
                id1 += i
        text = text.replace('\n', '')
        text = text[ind:]
        return text, id1

    def work_text_answer(self, text):
        text = text.replace('\n', '')
        text = text.replace('Показать ответ', '')
        return text

    def work_photo(self, chat_id, path):
        try:
            photo = self.bot.send_photo(chat_id, open(f'{path}', 'rb'))
            file_id = photo.photo[0].file_id
            time.sleep(1)
            return file_id
        except Exception as e:
            print(e)

    def work_document(self, chat_id, path):
        try:
            msg = self.bot.send_document(chat_id, open(f'{path}', 'rb'))
            file_id = msg.document.file_id
            time.sleep(1)
            return file_id
        except Exception as e:
            print(e)

    def check_task_in_bd(self, id):
        return self.db.check_tasks(id)

    def update_db(self, num, sp):
        for i in sp:
            print(i)
            if len(i) == 5:
                self.db.create_task(int(i[0]), 'Информатика', num, i[1], i[-1], i[2], i[3])
            if len(i) == 4:
                self.db.create_task(int(i[0]), 'Информатика', num, i[1], i[-1], None, i[2])
            else:
                self.db.create_task(int(i[0]), 'Информатика', num, i[1], i[-1], None, None)

    def main(self):
        for i in URL:
            self.go_to_page(i[1])
            html = self.get_html_selenium()
            #self.driver_close()
            res = self.get_td(html)
            print(res)
            self.update_db(i[0], res)
        return res


a = Parse()
a.main()
