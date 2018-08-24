# Spider-to-bttt.la

## 前言

该项为 xfsearch 影视搜索的爬虫分支.

spider-to-bttt.la是由Python完成的一个针对bttt.la即BT电影天堂和豆瓣电影网站数据采集的爬虫.

现·爬取方式: 爬取bttt.la网站, 取其中的电影磁力和豆瓣link; 访问豆瓣link, 模拟登陆豆瓣账号登陆, 设置爬取速度和并发量来防止被封IP.

目前暂完成:

- 电影详情数据和磁力抓取, 插入数据库mysql, 数据去重.
- 简单代理池实现, 抓取对应代理IP网站的免费IP并存入mongodb.

其中电影相关爬虫位于: `spider-to-bttt.la\spider\bttt`

其中代理池爬虫位于: `spider-to-bttt.la\proxy_pool`

------

## btttOne

该爬虫作用于爬取指定网站的全站数据并插入数据库.

**运行环境**:

- ubantu 1804 or windows 10
- python3.6
- scrapy
- mysql

系统这里就不说, python3.6可以官网下载64位的安装使用.

[python3.6]: https://www.python.org/ftp/python/3.6.6/python-3.6.6-amd64.exe	"python3.6.6"

安装完成后可能需要设置环境变量.(自行百度靠谱)

**命令行(CMD)安装scrapy**: `pip3 install -i https://mirrors.aliyun.com/pypi/simple/ scrapy`

[mysql社区版]: https://dev.mysql.com/downloads/mysql/	"大家自行斟酌"

------

### btttOne下spider使用

#### **目录树**

--`btttOne`

	--`btttOne`

		--`__pychache__`

		--`spiders`

		--`__init__.py`

		--`items.py`

		--`middlewares.py`

		--`mysqldataset.py`

		--`mysqlface.py`

		--`pipelines.py`

		--`settings.py`

	--`scrapy.cfg`

其中**比较关键的**有:

- spiders: 该目录下有主爬虫文件和运行文件.
  - pabtOne.py: 主爬虫文件.
  - exec_crawl_spider.py: 执行文件, 运行该文件即开始爬取数据.
- items.py: 该文件用于定义爬取的项.
- middlewares.py: 该文件为scrapy的中间件, 可自定义编写功能, eg: 发起请求时使用代理IP.
- pipelines.py: 该文件为scrapy的管道, 用于获取主爬虫爬取的items中定义的项的返回值的处理方式.
- settings.py: 该文件为配置文件, 其中包含数据库配置信息, 并发量和速度配置, 豆瓣账号密码配置等.
- mysqlface.py: 该文件为根据项目需要自定义编写的文件, 目的是将pymysql模块的使用封装一个类来导入使用.
- mysqldataset.py: 该文件为根据项目需要自定义编写的文件, 目的是处理重复数据, 多余数据, 获取数据库数据等.

------

#### 运行主爬虫文件

在执行爬虫前需要配置相关信息, 具体的可在settings文件的末尾查看.

**linux运行**: 进入到spiders目录下, 执行 `scrapy runspider pabtOne.py`

**windows运行**: 运行exec_crawl_spider.py文件即可.

------

### proxypool

代理IP池.

**文件说明**:

- spider.py: 该文件为爬虫开始口, 可根据后续文件自定义编写.
- crawler.py: 该文件为抓取文件, 调用其他文件, 如downloader, siteparser等.
- downloader.py: 该文件用于下载文件, 接收其他crawler传来的请求并处理.
- siteparser.py: 该文件用于解析页面代码获取数据, 接收downloader返回的请求结果.
- validater.py: 该文件用于处理代理IP是否可用, 返回有效数据.
- pymongoer.py: 该文件为封装pymongo的类, 被其他文件调用使用来达到插入数据到mongo的目的.
- flaskerapi.py: 该文件使用flask框架, 建立联系mongodb的接口, 供其他程序使用.
- infoconfiger.py: 该文件为配置文件, 包含需抓取对象网站, xpath语句, 抓取页数设置等.

------

