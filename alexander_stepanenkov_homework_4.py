# Задача 1 Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
        # название источника;
        # наименование новости;
        # ссылку на новость;
        # дата публикации.
# Задача 2 Сложить собранные новости в БД

from lxml import html
import requests, re, pymongo
from bs4 import BeautifulSoup
from pprint import pprint
from collections import OrderedDict
from pymongo import MongoClient
from pymongo import errors

client = MongoClient('127.0.0.1', 27017)
db = client['news']
mongo_news = db.news_coll

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15'}

url = 'https://lenta.ru'

session = requests.Session()
response = session.get(url, headers = headers)

dom = html.fromstring(response.text)

news = []
main_news= dom.xpath("//a[@class='card-mini _topnews'] | //a[@class='card-big _topnews _news']")

for item in main_news:
    news_element = {}

    title = item.xpath(".//span[@class = 'card-mini__title']//text() | .//h3[@class = 'card-big__title']//text()")
    title_str = ''.join(title
                        )
    link = item.xpath("./@href")
    link_str = ''.join(link)

    date = item.xpath(".//time[@class = 'card-big__date']/text() | .//time[@class = 'card-mini__date']/text()")
    date_str = ''.join(date)

    source = 'lenta'


    # В качестве ключа в mongo используется ссылка на новость, как единственный уникальный элемент в документе
    news_element['_id'] = url+link_str
    news_element['1_title'] = title_str
    news_element['3_date'] = date_str
    news_element['4_source'] = source

    news.append(news_element)

    try:
        mongo_news.insert_one(news_element)
    except errors.DuplicateKeyError:
        print(f"Document with id = {mongo_news['_id']} is already exists")

for item in mongo_news.find():
    pprint(item)
