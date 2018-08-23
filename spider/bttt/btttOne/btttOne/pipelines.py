# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from datetime import datetime
from btttOne.mysqldataset import SqlDataReduction
from btttOne.mysqlface import SqlControl


class SourcePipeline(object):
    def process_item(self, item, spider):
        item['source'] = spider.name
        item['utc_time'] = str(datetime.utcnow())[0:19]
        return item


class BtttonePipeline(object):
    def __init__(self):
        super().__init__()
        self.mysqlTwo = SqlControl()
        self.front_str = "(title, year, country, lan, douban_link, introduce, main_actor, download_url," \
                    " img_url, length, director)"

    def open_spider(self):
        self.file = open('btttOne.json', 'w', encoding='utf-8')
        self.mysqlTwo.connect_mysql()
        # self.mysqlOne.get_set_column('t_movies')

    def process_item(self, item, spider):
        content = dict(item)

        ending_str = "(" + content['title'] + content['year'] + content['country'] + content['lan'] + \
                     content['douban_link'] + content['introduce'] + content['main_actor'] + \
                     content['download_url'] + content['img_url'] + content['duration'] + content['director'] + ")"
        print(ending_str)
        sql = "INSERT INTO t_movies" + self.front_str + 'VALUE' + ending_str
        print(sql)
        self.mysqlTwo.sql_to_mysql(sql)
        # self.file.write()
        return item

    def close_spider(self):
        self.mysqlTwo.close_mysql()
        self.file.close()
