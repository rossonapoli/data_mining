# Задача 1
# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import requests, json, pprint

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15'}

url = 'https://api.github.com/users/octocat/repos'

path = '/Users/a.stepanenkov/Desktop/'

response = requests.get(url)
repos = response.json()

list_repos = []

for i in repos:
    list_repos.append(i['name'])

print(list_repos)

with open(path + 'repos.json', 'w') as f:
    json.dump(repos, f)

# Задача 2
# Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл. Если нет желания заморачиваться с поиском, возьмите
# API вконтакте (https://vk.com/dev/first_guide). Сделайте запрос, чтобы получить список всех сообществ на которые вы подписаны.

# Скрипт использует новостной API и выводит список новостных заголовков и ссылки на них для страны, указанной в params

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15'}
params = {
    'country' : 'us',
    'apiKey' : 'f23fc1bb0977426692953d5c2003028d'
}

url = 'https://newsapi.org/v2/top-headlines'

response = requests.get(url, headers = headers, params = params)

data = response.json()

print(f"Сегодняшние заголовки новостей в {params['country'].capitalize()}\n")
for i in data['articles']:
    print(f"Статья: {i['title']}\nИздание: {i['source']['name']}\nURL:{i['url']}\n")