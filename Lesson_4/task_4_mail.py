import requests
from lxml import html
from pymongo import MongoClient
import time


DB_CLIENT = MongoClient('localhost', 27017)
DB = DB_CLIENT['news_data']


try:
    COLLECTION = DB.create_collection('news_mail')
except BaseException:
    COLLECTION = DB.news


HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.203'}
URL = 'https://news.mail.ru'


def get_news_mail(url, headers, collection):
    response = requests.get(url, headers=headers)
    target = html.fromstring(response.text)
    news_block = target.xpath('//table[@class="daynews__inner"]//a/@href')
    for i in news_block:
        news = {}
        response_data = requests.get(i, headers=headers)
        target_date = html.fromstring(response_data.text)
        news['title'] = target_date.xpath('//h1/text()')[0]
        news['link'] = i
        news['source'] = target_date.xpath(
            '//span[contains(text(), "источник")]/following-sibling::node()/@href')[0]
        news['date'] = target_date.xpath('//span[@datetime]/@datetime')[0]
        try:
            collection.insert_one(news)
        except BaseException:
            continue


start_time = time.time()
get_news_mail(URL, HEADERS, COLLECTION)

print("--- %s seconds ---" % round(( time.time() - start_time), 3))
print('---------EOF---------')