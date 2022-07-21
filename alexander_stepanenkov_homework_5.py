# Задача 1. Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и
# складывает данные в БД. Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары

from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pprint
from pymongo import MongoClient
from pymongo import errors

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
mongo_mvideo = db.mvdieo_trend_goods

s = Service('./chromedriver')

options = Options()
options.add_argument('start-maximized')

driver = webdriver.Chrome(service = s, options = options)
driver.implicitly_wait(10)

driver.get('https://www.mvideo.ru')
# driver.refresh()

driver.execute_script("window.scrollTo(0, 1500)")

trend_button = driver.find_element(By.XPATH, "//*[contains(text(),'В тренде')]/parent::*/parent::*")
trend_button.click()

goods = driver.find_elements(By.XPATH, "//mvid-carousel[@class = 'carusel ng-star-inserted']/div[@class = 'mvid-carousel-outer mv-hide-scrollbar']/div[@class = 'mvid-carousel-inner']/mvid-product-cards-group")
time.sleep(4)
for good in goods:
    titles = good.find_elements(By.XPATH, ".//div[@class = 'product-mini-card__name ng-star-inserted']")

    titles_list = []
    links_list = []
    prices_list = []
    ids_list = []

    for title in titles:
        title_new = title.find_element(By.XPATH, "./div/a/div").text
        titles_list.append(title_new)

    links = good.find_elements(By.XPATH, ".//div[@class = 'product-mini-card__name ng-star-inserted']")
    for link in links:
        link_new = link.find_element(By.XPATH, "./div/a").get_attribute('href')
        links_list.append(link_new)

        regex_id = r'(\d{6,12})'
        object_id = re.findall(regex_id, link_new)
        _id = int(''.join(object_id))
        ids_list.append(_id)

    prices_new = good.find_elements(By.XPATH, ".//div[@class = 'product-mini-card__price ng-star-inserted']")
    for price in prices_new:
        price_new = price.find_element(By.XPATH, "./mvid-price/div/span[@class = 'price__main-value']").text
        prices_list.append(price_new)

list_len = len(titles_list)
i = 0
while i < list_len:
    dict_temp = {}
    dict_temp['_id'] = ids_list[i]
    dict_temp['title'] = titles_list[i]
    dict_temp['price'] = prices_list[i]
    dict_temp['link'] = links_list[i]
    i += 1

    try:
        mongo_mvideo.insert_one(dict_temp)
    except errors.DuplicateKeyError:
        print(f"Document with id = {mongo_mvideo['_id']} is already exists")

for item in mongo_mvideo.find():
    print(item)
