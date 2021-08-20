# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import hashlib
import json
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import scrapy
from itemadapter import ItemAdapter


class LeroyPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['leroy_merlin']

    def process_item(self, item, spider):
        collection_name = 'leroy'
        try:
            collection = self.db.create_collection(f'{collection_name}')
        except BaseException:
            collection = self.db[collection_name]
        item_for_mongo = json.dumps(dict(item)).encode('utf-8')
        item_hash = hashlib.sha3_256(item_for_mongo)
        item_id = item_hash.hexdigest()
        item['_id'] = item_id
        try:
            collection.insert_one(item)
        except BaseException:
            pass

        return item

class ImagesLoader(ImagesPipeline):

    def get_media_requests(self, item, info):
        photo = item['photo']
        if photo:
            for img in photo:
                try:
                    yield scrapy.Request(img)

                except TypeError as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        directory = item['name'][0].replace('/', '_')
        split_url = request.url.split('/')
        file_name = split_url[len(split_url) - 1]
        return f'{directory}/{file_name}'

    def item_completed(self, results, item, info):
        if results:
            item['photo'] = [itm[1] for itm in results if itm[0]]
        return item