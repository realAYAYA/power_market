# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# CurrentItem include Text,Link,Table
class CurrentItem(scrapy.Item):
    id = scrapy.Field()
    content = scrapy.Field()
    pass

class PdfItem(scrapy.Item):
    id = scrapy.Field()
    pdf_url = scrapy.Field()
    pass

class PicItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    pass