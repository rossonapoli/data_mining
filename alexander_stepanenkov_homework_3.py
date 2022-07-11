# Задача 1 Развернуть у себя на компьютере/виртуальной машине/хостинге
# MongoDB и реализовать функцию, которая будет добавлять только новые вакансии/продукты в вашу базу.

import requests, re, pymongo
from bs4 import BeautifulSoup
from pprint import pprint
from collections import OrderedDict
from pymongo import MongoClient
from pymongo import errors
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)

db = client['vacancies']
mongo_vac = db.vac_coll

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15'}

url = 'https://hh.ru/search/vacancy?area=1%customDomain=3'
params = {'text': 'разработчик',
          'page': 1,
          'items_on_page': 20}

session = requests.Session()
response = session.get(url, headers = headers, params = params)

dom = BeautifulSoup(response.text, 'html.parser')

vacancies = dom.find_all('div', {'class': 'vacancy-serp-item__layout'})

num_of_pages = int(input())

vacancies_list = []

for i in range (int(num_of_pages)):
    params['page'] = i
    response = session.get(url, headers = headers, params = params)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item__layout'})

    if response.ok and len(vacancies) != 0:
        for vacancy in vacancies:
            vacancy_data = {}

            title = vacancy.find('h3', {'class': 'bloko-header-section-3'})
            salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            href = vacancy.find('a', {'class': 'bloko-link', 'data-qa': 'vacancy-serp__vacancy-title'})

            title = title.text
            href = href.get('href')

            try:
                salary = salary.text
                salary = salary.replace('\u202f', ' ')
            except:
                salary = '0'

            salary = salary.replace(' ', '')

            if salary == '0':
                temp = ['0', '0', '0']
            else:
                if re.match('от', salary):
                    salary = salary.replace('от', '')
                    regex = r'(\d+\d+)|(\w+)'
                    matches = re.findall(regex, salary)
                    temp = [_ for tupl in matches for _ in tupl if _]
                    temp.insert(1, '0')

                elif re.match('до', salary):
                    salary = salary.replace('до', '')
                    regex = r'(\d+\d+)|(\w+)'
                    matches = re.findall(regex, salary)
                    temp = [_ for tupl in matches for _ in tupl if _]
                    temp.insert(0, '0')

                else:
                    regex = r'(\d+\d+)|(\d+\d+)|(\w+)'
                    matches = re.findall(regex, salary)
                    temp = [_ for tupl in matches for _ in tupl if _]

            regex_id = r'([0-9]{5,9})'

            object_id = re.findall(regex_id, href)
            _id = int(''.join(object_id))

            vacancy_data['_id'] = _id
            vacancy_data['1_title'] = title
            vacancy_data['2_salary_min'] = temp[0]
            vacancy_data['3_salary_max'] = temp[1]
            vacancy_data['4_salary_cur'] = temp[2]
            vacancy_data['5_href'] = href
            vacancy_data['6_source'] = 'HeadHunder'

            for i in vacancy_data:
                try:
                    vacancy_data[i] = int(vacancy_data[i])
                except:
                    continue

            for i in vacancy_data:
                if vacancy_data[i] == 0:
                    vacancy_data[i] = None

            vacancy_data = OrderedDict(sorted(vacancy_data.items()))

            vacancies_list.append(vacancy_data)

            try:
                mongo_vac.insert_one(vacancy_data)
            except errors.DuplicateKeyError:
                print(f"Document with id = {vacancy_data['_id']} is already exists")

for item in mongo_vac.find():
    pprint(item)

# Задача 2. Написать функцию, которая производит поиск и выводит на экран
# вакансии с заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты).
# То есть цифра вводится одна, а запрос проверяет оба поля

compensation = int(input('\n'+'Введите зарплату в рублях для поиска вакансий: '))

for item in mongo_vac.find({'$and':
                            [{'$or':
                                [{'2_salary_min': {'$gt': compensation}},
                                {'3_salary_max': {'$gt': compensation}}]},
                            {'4_salary_cur': 'руб'}]
                            }):

    pprint(item)

print()