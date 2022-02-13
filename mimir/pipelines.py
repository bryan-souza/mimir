# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from pymongo import MongoClient

class TextPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('text'):
            text = adapter['text']
            text = text.replace('\n', '')
            text = text.strip()

            adapter['text'] = text
            return item

        raise DropItem(f"Missing quote text in {item}")

class AuthorPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('author'):
            author = adapter['author']
            author = author.replace('\n', '')
            author = author.replace(',', '')
            author = author.strip()

            adapter['author'] = author
            return item

        raise DropItem(f"Missing quote author in {item}")

class MongoPipeline:
    def open_spider(self, spider):
        db = json.load( open('config.json') )['db']
        self.client = MongoClient(
            host       = db['host'],
            port       = db['port'],
            username   = db['username'],
            password   = db['password'],
            authSource = db['database']
        )
        
        self.db = self.client[f"{ db['database'] }"]
        self.quotes = self.db[ db['collection'] ]

    def process_item(self, item, spider):
        quote = ItemAdapter(item)
        self.quotes.insert_one( quote.asdict() )
        return item

    def close_spider(self, spider):
        self.client.close()
