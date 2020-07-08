# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AemoSpider(scrapy.Spider):
    name = 'aemo'
    allowed_domains = ['aemo.com.au']
    start_urls = ['https://www.aemo.com.au/news#e=0']

    rules = (
        Rule(LinkExtractor(allow=r'.+news#e=\d'), follow=True),
        Rule(LinkExtractor(allow=r'.+/news/.+'), callback='parse_item', follow=False),
    )

    def parse_detail(self, response):
        print("Begin test!"+" "+"*"*75)
        title = response.xpath("//h1[@class='field-title']/text()").get()
        pub_time = response.xpath("//div[@class='is-date field-published-date']/text()").get()
        article = response.xpath("//div[@class='component-content']//text()").getall()
        article_content = "".join(article).strip()
        print(title+" "+pub_time)
