import requests
import traceback
import time
from pymongoer import Mongodber
from multiprocessing.pool import ThreadPool


class Vaildater(object):
    def __init__(self):
        self.test_url = "http://www.baidu.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        self.mongo_db = Mongodber()

    def valid_many(self, proxy_list, method):
        pool = ThreadPool(10)
        for proxy in proxy_list:
            pool.apply_async(self.valid, args=(proxy, method))
        pool.close()
        pool.join()

    def valid(self, proxy, method):
        try:
            proxies = {
                'http': 'http://' + proxy['proxy_ip'],
                'https': 'https://' + proxy['proxy_ip'],
            }

            start_time = time.time()
            resp = requests.get(self.test_url, proxies=proxies, headers=self.headers, timeout=10)
            end_time = time.time()
            delay = round(end_time - start_time, 1)

            if resp.status_code == 200:
                proxy['delay'] = delay
                # print(f"有效代理:{proxy}")
                if method == 'crawl':
                    self.mongo_db.insert_to_mongo(proxy)
                elif method == 'check':
                    self.mongo_db.update_to_mongo({'proxy_ip': proxy['proxy_ip']}, {'delay': delay})
            else:
                if method == 'check':
                    self.mongo_db.delete_to_mongo({'proxy_ip': proxy['proxy_ip']})

        except Exception:
            if method == 'check':
                self.mongo_db.delete_to_mongo({'proxy_ip': proxy['proxy_ip']})
            # traceback.print_exc()
            # pass


def check_validity():
    while True:
        print("开始检查数据有效性...")
        data_list = Vaildater().mongo_db.get_all_proxy()
        print(f"data_list:{data_list}")
        Vaildater().valid_many(data_list, 'check')
        print("检查完毕...")
        time.sleep(5 * 60)
