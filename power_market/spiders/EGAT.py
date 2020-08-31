# -*- coding: utf-8 -*-
import scrapy
from power_market.items import PdfItem
from power_market.items import EVNtableItem


class EgatSpider(scrapy.Spider):
    name = 'EGAT'
    allowed_domains = ['egat.co.th']
    start_urls = ['https://www.egat.co.th/en/information/statistical-data']
    base_url = "https://www.egat.co.th"
    pdf_urls = 'https://www.egat.co.th/en/information/annual-report'
    count = 0

    def parse(self, response):
        urls = response.xpath('//*[@id="main-content"]/div[2]/div/table/tbody/tr//@href').getall()
        urls = list(map(lambda x: response.urljoin(x),urls))
        for url in urls:
            if "statistical" in url:
                yield scrapy.Request(url,callback=self.table_grab)
            
        yield scrapy.Request(self.pdf_urls,callback=self.pdf_grab) # 抓取pdf

    def pdf_grab(self,response):
        urls = response.xpath('///*[@id="main-content"]//@href').getall()
        urls = list(map(lambda x: response.urljoin(x),urls))
        for pdf_url in urls:
            if ".pdf" in pdf_url: # 筛选还有.pdf的链接
                filename = str(pdf_url[-11:])
                item = PdfItem(itemname="pdf",filename=filename,pdf_url=pdf_url)
                self.count = self.count+1 # 下载计数+1
                yield item

    def table_grab(self,response):
        title = response.xpath('//*[@id="main-content"]/div[2]/div/h1/text()').get() # 标题
        filename = "".join(title) + ".json"
        tables = response.xpath('//*[@id="main-content"]/div[2]/div/table/tbody/tr') # 表格
        keys = [] # 放到一个list序列中
        values = []
        for table in tables:
            tds = table.xpath('td')
            keys.append(tds[0].xpath('text()').get()) # 列键
            values.append(tds[1].xpath('text()').get()) #列值
            if(tds[2]):
                values.append(tds[2].xpath('text()').get()) #列值
        item = EVNtableItem(filename=filename,title=title,keys=keys,values=values)
        yield item