# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from utils.mongo_DB import MongoDB



class GifspiderPipeline(object):
    def open_spider(self, spider):
        self.m = MongoDB('mongodb://sooko.ml:36565', 'yaohuo', need_auth=True, auth=('tk', 'Aa123456'))

    def process_item(self, item, spider):
        key = dict(item)['img_url'].split('/')[-1]
        if self.m.insert_one('img_backups', dict(item), key):
            print('does not exists before!')
            self.m.insert_one('img', dict(item), key)
        return item

    def close_spider(self, spider):
        pass
