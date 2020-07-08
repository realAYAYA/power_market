# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class aemoItem(scrapy.Item):
    title = scrapy.Field()
    pub_time = scrapy.Field()
    article_content = scrapy.Field()
    pass

class nordpoolgroupItem(scrapy.Item):
    title = scrapy.Field()
    pub_time = scrapy.Field()
    article_content = scrapy.Field()
    pass