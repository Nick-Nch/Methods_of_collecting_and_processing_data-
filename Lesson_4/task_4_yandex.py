import requests
from lxml import html
from pymongo import MongoClient
import time


DB_CLIENT = MongoClient('localhost', 27017)
DB = DB_CLIENT['news_data']


try:
    COLLECTION = DB.create_collection('news_yandex')
except BaseException:
    COLLECTION = DB.news


HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.203'}
URL = 'https://yandex.ru/news/'


def get_news_yandex(url, headers, collection):
    response = requests.get(url, headers=headers)
    target = html.fromstring(response.text)
    news_block = target.xpath('//article')[:5]
    for i in news_block:
        news = {
            'title': i.xpath('..//h2/text()')[0].replace(
                '\xa0',
                ' '),
            'link': i.xpath('..//a/@href')[0],
            'date': i.xpath('..//span[@class="mg-card-source__time"]/text()')[0],
            'source': i.xpath('..//a/text()')[0]}
        try:
            collection.insert_one(news)
        except BaseException:
            continue


start_time = time.time()
get_news_yandex(URL, HEADERS, COLLECTION)

print("--- %s seconds ---" % round(( time.time() - start_time), 3))
print('---------EOF---------')