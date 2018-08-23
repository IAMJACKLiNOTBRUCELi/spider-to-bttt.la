"""
    json数据格式: {'proxy_ip': 'ip:port', 'delay': 'time'}
"""

import pymongo
import traceback
from pymongo.errors import DuplicateKeyError


class Mongodber(object):
    def __init__(self):
        self.client = pymongo.MongoClient()     # ip, 27017
        self.db = self.client['proxydb']        # self.client.proxydb
        self.proxy_collect = self.db['proxypool']
        self.proxy_collect.ensure_index('proxy_ip', unique=True)    # 约束字段, 达到去重.

    def insert_to_mongo(self, proxy):
        try:
            self.proxy_collect.insert(proxy)
            print(f"成功插入{proxy}")

        except DuplicateKeyError:
            pass

    def update_to_mongo(self, conditions, value):
        self.proxy_collect.update(conditions, {'$set': value})      # 更新匹配到的第一个, 更新里面的value, 或者添加.
        print(f"{conditions}更新了{value}")

    def delete_to_mongo(self, conditions):
        self.proxy_collect.remove(conditions)
        print(f"删除: {conditions}")

    def get_proxy_ip(self, count):
        count = int(count)
        # 升序. 如果没有该字段, 则视为值最小.
        ascenting_list = list(self.proxy_collect.find({}, limit=count).sort('hha', pymongo.ASCENDING))
        return [info['proxy_ip'] for info in ascenting_list]

    def get_all_proxy(self):
        return list(self.proxy_collect.find({}))


if __name__ == '__main__':
    # d = Mongodber()
    # print(d.get_all_proxy())
    pass


