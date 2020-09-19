# -*- coding: utf-8 -*-
import scrapy


class EdlSpider(scrapy.Spider):
    name = 'EDL'
    allowed_domains = ['edlgen.com.la']
    start_urls = ['http://edlgen.com.la/']

    def parse(self, response):
        pass
