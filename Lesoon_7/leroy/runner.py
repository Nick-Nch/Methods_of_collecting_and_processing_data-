from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from leroy import settings
from leroy.spiders.leroymerlin import LeroyMerlinSpider

if __name__ == '__main__':

    searchInput = 'топор'
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroyMerlinSpider, searchInput=searchInput)
    process.start()