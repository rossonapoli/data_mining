# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность) с
# сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
#   Наименование вакансии.
#   Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
#   Ссылку на саму вакансию.
#   Сайт, откуда собрана вакансия. (можно прописать статично hh.ru или superjob.ru)
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv

import requests, re
from bs4 import BeautifulSoup
from pprint import pprint
from collections import OrderedDict

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15'}

url = 'https://hh.ru/search/vacancy?area=1%customDomain=1'
params = {'text': 'разработчик',
          'page': 1}

session = requests.Session()
response = session.get(url, headers = headers, params = params)

dom = BeautifulSoup(response.text, 'html.parser')

vacancies = dom.find_all('div', {'class': 'vacancy-serp-item__layout'})

num_of_pages = int(input())

vacancies_list = []

for i in range (1, int(num_of_pages) + 1):
    print(i)
    params['page'] = i
    response = session.get(url, headers = headers, params = params)
    dom = BeautifulSoup(response.text, 'html.parser')
    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item__layout'})
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

        # if salary is None:
        #     break
        # else:
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

        vacancy_data['1_title'] = title
        # vacancy_data['salary_all'] = salary
        vacancy_data['2_salary_min'] = temp[0]
        vacancy_data['3_salary_max'] = temp[1]
        vacancy_data['4_salary_cur'] = temp[2]
        vacancy_data['5_href'] = href

        for i in vacancy_data:
            try:
                vacancy_data[i] = int(vacancy_data[i])
            except:
                continue

        for i in vacancy_data:
            if vacancy_data[i] == 0:
                vacancy_data[i] = None

        vacancy_data = OrderedDict(sorted(vacancy_data.items()))

        vacancies_list.append((vacancy_data))

pprint(vacancies_list)

