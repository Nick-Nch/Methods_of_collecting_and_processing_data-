#Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность) с  Hh.ru
#Получившийся список должен содержать в себе минимум:

    #Наименование вакансии.
    #Предлагаемую зарплату (отдельно минимальную и максимальную).
    #Ссылку на саму вакансию.
    #Сайт, откуда собрана вакансия.
#Nick-Nch

import csv
import re
import requests
from bs4 import BeautifulSoup as bs
import time

TARGET = input('Please input vacantion: ')


def hh_parser(target):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.203'}
    domain = 'https://hh.ru'
    url = '/search/vacancy'
    vacancy_output = []
    params = {
        'text': target,
        'search_field': 'name',
        'items_on_page': '50',
        'page': 0
    }

    for page in range(0, 1000):
        params['page'] = page
        response = requests.get(domain + url, params=params, headers=headers)
        target_page = bs(response.text, 'html.parser')
        vacancy_list = target_page.find_all('div', {'class': 'vacancy-serp-item'})
        try:
            target_page.find('a', {'data-qa': 'pager-next'}).find('span')
            for vacancy in vacancy_list:
                vacancy_output.append(get_info_hh(vacancy))
        except:
            break

    with open('result.csv', 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, vacancy_output[0].keys())
        writer.writeheader()
        writer.writerows(vacancy_output)

    return vacancy_output


def get_info_hh(element):
    vacancy_base = {}
    vacancy_name = element.find(
        'a', {
            'data-qa': 'vacancy-serp__vacancy-title'}).getText().replace(u'\xa0', u' ')
    vacancy_base['vacancy_name'] = vacancy_name
    employer_name = element.find(
        'a', {
            'data-qa': 'vacancy-serp__vacancy-employer'}).getText().replace(
        u'\xa0', u' ').split(', ')[0]
    vacancy_base['employer_name'] = employer_name
    city = element.find(
        'span', {
            'data-qa': 'vacancy-serp__vacancy-address'}).getText().split(', ')[0]
    vacancy_base['city'] = city
    station_name = element.find('span', {'class': 'metro-station'})
    if not station_name:
        station_name = None
    else:
        station_name = station_name.getText()
    vacancy_base['station_name'] = station_name
    salary = element.find(
        'span', {
            'data-qa': 'vacancy-serp__vacancy-compensation'})
    salary_currency = None
    if not salary:
        salary_min = None
        salary_max = None
        salary_currency = None
    else:
        salary = salary.getText().replace(u'\u202f', u'')
        salary = re.split(r'\s|-', salary)
        if salary[0] == 'до':
            salary_min = None
            salary_max = int(salary[1])
            salary_currency = str(salary[2])
        elif salary[0] == 'от':
            salary_min = int(salary[1])
            salary_max = None
        else:
            salary_min = int(salary[0])
            salary_max = int(salary[2])
            salary_currency = str(salary[3])
    vacancy_base['salary_min'] = salary_min
    vacancy_base['salary_max'] = salary_max
    vacancy_base['salary_currency'] = salary_currency
    vacancy_link = element.find(
        'a', {'data-qa': 'vacancy-serp__vacancy-title'}).get('href').split('?')[0]
    vacancy_base['vacancy_link'] = vacancy_link
    vacancy_base['site_address'] = 'https://hh.ru'
    return vacancy_base

start_time = time.time()

hh_parser(TARGET)
print("--- %s seconds ---" % round(( time.time() - start_time), 3))
print('----------EOF----------')