# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class EVNtableItem(scrapy.Item):
    title = scrapy.Field()
    keys = scrapy.Field()
    values = scrapy.Field()
        
    pass

class PdfItem(scrapy.Item):
    itemname = scrapy.Field()
    filename = scrapy.Field()
    pdf_url = scrapy.Field()

    pass