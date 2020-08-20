# -*- coding: utf-8 -*-
import scrapy


class EgatSpider(scrapy.Spider):
    name = 'EGAT'
    allowed_domains = ['egat.co.th']
    start_urls = ['http://egat.co.th/']

    def parse(self, response):
        pass
