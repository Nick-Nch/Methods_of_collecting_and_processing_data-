# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['vacancies_hh_sj']


    def process_item(self, item, spider):

        if spider.name == 'hhru':
            salary_list = []
            for i in item['salary']:
                s = i.replace(" ", "").replace("\xa0", "")
                salary_list.append(s)
            item['salary'] = salary_list
            if item['salary'][0] == 'от':
                item['min_salary'] = item['salary'][1]

                if item['salary'][2] == 'до':
                    item['max_salary'] = item['salary'][3]
                    item['currency'] = item['salary'][5]
                else:
                    item['max_salary'] = None
                    item['currency'] = item['salary'][3]
                if item['salary'][0] != 'от':
                    item['min_salary'] = item['salary'][0]
                    item['currency'] = item['salary'][3]

            elif item['salary'][0] == 'до':
                item['min_salary'] = 'NA'
                item['max_salary'] = int(item['salary'][1])
                item['currency'] = item['salary'][3]
            elif item['salary'][0] == 'з/пнеуказана':
                item['min_salary'] = 'NA'
                item['max_salary'] = 'NA'
            else:
                item['min_salary'] = 'wrong'
                item['max_salary'] = 'wrong'
            del item['salary']
            item['site'] = 'https://hh.ru'

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        if spider.name == 'sjru':
            salary_sj_list = []
            for i in item['salary']:
                sj = i.replace(" ", "").replace("\xa0", "").replace("-", "").replace("/", "")
                salary_sj_list.append(sj)
                item['salary'] = salary_sj_list
                if item['salary'][0] == "Подоговорённости" or item['salary'][0] == "По договорённости":
                    item['salary'][0] == "По договорённости"
                    item['salary_min'] = 'NA'
                    item['salary_max'] = 'NA'

                elif item['salary'][0] != "от" or item['salary'][0] != "От":
                    item['salary_min'] = ['salary'][0]
                    item['salary_max'] = 'NA'
                    for y in item['salary_min']:
                        item['currency_sj'] = "".join(" " if el.isdigit() else el for el in y).split()
                        item['salary_min'] = "".join(el if el.isdigit() else " " for el in y).split()
                if item['salary'][0] == "от":
                    for x in item['salary']:
                        item['currency_sj'] = "".join(" " if el.isdigit() else el for el in x).split()
                        item['salary_min'] = "".join(el if el.isdigit() else " " for el in x).split()
                elif item['salary'][0] == 'от':
                    pos = item['salary'][2].find('руб.')
                    item['salary_min'] = item['salary'][2][:pos]
                    item['currency'] = item['salary'][2][pos:]
                if item['salary'][0] == '—':
                    item['salary_min'] = int(item['salary'][0])
                    item['salary_max'] = int(item['salary'][4])
                    item['currency'] = item['salary'][6]

                if item['salary'][0] == "до" or item['salary'][0] == "До":
                    item['salary_min'] = 'NA'
                    item['salary_max'] = item['salary'][4]
                    item['currency_sj'] = item['salary'][6]
                elif item['salary'][0] == 'до':
                    pos = item['salary'][2].find('руб.')
                    item['salary_max'] = item['salary'][2][:pos]
                    item['currency'] = item['salary'][2][pos:]
                else:
                    item['salary_min'] = 'wrong'
                    item['salary_max'] = 'wrong'
                del item['salary']
                item['site_sj'] = 'superjob.ru'

        collection = self.mongo_base[spider.name]
        collection.insert_one(item)


        return item
