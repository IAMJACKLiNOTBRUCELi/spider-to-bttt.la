from downloader import Downloader
from infoconfiger import configs
from siteparser import Parser
from validater import Vaildater
import time


class Crawler(object):
    def __init__(self):
        self.down_load = Downloader()
        self.site_parse = Parser()
        self.vail_data = Vaildater()

    def crawl(self):
        for config in configs:
            urls = config['urls']
            parse_config = config
            offset = 0
            for url in urls:
                offset += 1
                print(f"抓取{config['site']}的第{offset}页...")
                proxy_list = self.site_parse.who_parse(self.down_load.download(url), parse_config)
                for proxy in proxy_list:
                    self.vail_data.valid(proxy, 'crawl')

        print("抓取完成...")


def want_to_sleep():
    while True:
        print("开始抓取数据...")
        Crawler().crawl()
        time.sleep(30 * 60)


if __name__ == '__main__':
    # c = Crawler()
    # c.crawl()
    pass
