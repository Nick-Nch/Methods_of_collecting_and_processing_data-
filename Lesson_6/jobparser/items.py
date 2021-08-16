# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    name = scrapy.Field()
    salary = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    currency = scrapy.Field()
    vacancy_link = scrapy.Field()
    site = scrapy.Field()
    _id = scrapy.Field()




class SjruItem(scrapy.Item):
    name = scrapy.Field()
    salary = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    currency_sj = scrapy.Field()
    link = scrapy.Field()
    site_sj = scrapy.Field()
    _id = scrapy.Field()