# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BtttoneItem(scrapy.Item):
    # 电影名.
    title = scrapy.Field()
    # 年代.
    year = scrapy.Field()
    # 国家.
    country = scrapy.Field()
    # 语言.
    lan = scrapy.Field()
    # douban地址.
    douban_link = scrapy.Field()
    # 简介.
    introduce = scrapy.Field()
    # 导演.
    director = scrapy.Field()
    # 编剧.
    screenwriter = scrapy.Field()
    # 主演.
    main_actor = scrapy.Field()
    # 类型.
    types = scrapy.Field()
    # 片长.
    duration = scrapy.Field()
    # 海报地址.
    img_url = scrapy.Field()

    source = scrapy.Field()
    utc_time = scrapy.Field()

