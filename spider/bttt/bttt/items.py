# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BtttItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    country = scrapy.Field()
    lan = scrapy.Field()
    douban_link = scrapy.Field()
    introduce = scrapy.Field()
    main_actor = scrapy.Field()
    download_url = scrapy.Field()
    img_url = scrapy.Field()

    source = scrapy.Field()
    utc_time = scrapy.Field()
