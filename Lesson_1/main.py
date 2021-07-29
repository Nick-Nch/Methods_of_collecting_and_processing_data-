#Посмотреть документацию к API GitHub;
#Разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json.

import json
import requests

"""Получить список репозиториев и записать их имена в JSON формате"""
def get_repo(url, user):
    response = requests.get(f'{url}/users/{user}/repos')
    repo_list = []
    """Вывести название репозиториев"""
    for i in response.json():
        repo_list.append(i['name'])
        print(i['name'])

    with open('repository_list.json', 'w') as file:
        json.dump(repo_list, file)

    with open('full_response.json', 'w') as file:
        json.dump(response.json(), file)

get_repo('https://api.github.com', 'Nick-Nch')












