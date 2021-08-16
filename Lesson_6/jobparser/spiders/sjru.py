import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import SjruItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@class,'f-test-link-Dalshe')]/@href").extract_first()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//div[@class='_1h3Zg _2rfUm _2hCDz _21a7u']/a/@href")

        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)


    def vacancy_parse(self, response:HtmlResponse):
        item_name = response.xpath("//h1/text()").extract_first()
        item_salary = response.xpath('//span[@class="_1OuF_ ZON4b"]//text()').extract()
        item_link = response.url

        item = SjruItem(name=item_name, salary=item_salary, link=item_link)
        yield item

