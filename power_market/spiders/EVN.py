# -*- coding: utf-8 -*-
import scrapy
from power_market.items import EVNtableItem
from power_market.items import PdfItem


class EvnSpider(scrapy.Spider):
    name = 'EVN'
    allowed_domains = ['en.evn.com.vn']
    start_urls = ['https://en.evn.com.vn/c3/gioi-thieu-l/Annual-Report-6-13.aspx']
    base_url = "https://en.evn.com.vn"
    table_url = "https://en.evn.com.vn/c3/gioi-thieu-f/Projects-6-14.aspx"
    count = 1

    def parse(self, response):
        urls = response.xpath('//div[@class="blog-page page_list"]//@href').getall()
        urls = list(map(lambda x: response.urljoin(x),urls))

        yield scrapy.Request(self.table_url,callback=self.table_grab)
        
        for url in urls:
            if "Annual" in url:
                yield scrapy.Request(url,callback=self.pdf_grab)
                pass
        pass

    def pdf_grab(self,response):
        urls = response.xpath('//div[@id="ContentPlaceHolder1_ctl00_159_content_news"]//@href').getall()
        urls = list(map(lambda x: response.urljoin(x),urls))
        for pdf_url in urls:
            if ".pdf" in pdf_url:
                filename = str(self.count) + ".pdf"
                item = PdfItem(itemname="pdf",filename=filename,pdf_url=pdf_url)
                self.count = self.count+1
                yield item
        pass

    def table_grab(self,response): #代码爬取成功!
        title = response.xpath('//span[@id="ContentPlaceHolder1_ctl00_1391_ltlTitle"]/text()').get() # 标题
        tables = response.xpath('//div[@class="blog margin-bottom-40 content-detail"]//tbody/tr') # 表格
        keys = [] # 放到一个list序列中
        values = []
        for table in tables:
            tds = table.xpath('td')
            keys.append(tds[0].xpath('p/text()').get()) # 列键
            values.append(tds[1].xpath('p/text()').get()) #列值
        item = EVNtableItem(title=title,keys=keys,values=values)
        yield item