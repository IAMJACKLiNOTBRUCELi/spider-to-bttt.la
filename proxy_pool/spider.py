"""
    infoconfiger 配置文件.
    crawler 读取infoconfiger得到需要发送的请求等数据, 并获得结果.
    downloader 接收crawler传来的url并请求, 返回结果.
    siteparser 解析downloader返回的结果, 并返回解析后的数据.
    spider 自定义文件, 可用来调用以上py文件.

"""
from crawler import want_to_sleep
from validater import check_validity
from multiprocessing import Process


if __name__ == '__main__':
    crawl_process = Process(target=want_to_sleep)
    check_process = Process(target=check_validity)

    crawl_process.start()
    check_process.start()

    crawl_process.join()
    check_process.join()

