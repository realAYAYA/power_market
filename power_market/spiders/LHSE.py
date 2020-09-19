# -*- coding: utf-8 -*-
import scrapy


class LhseSpider(scrapy.Spider):
    name = 'LHSE'
    allowed_domains = ['laoholding.com']
    start_urls = ['http://laoholding.com/']

    def parse(self, response):
        pass
