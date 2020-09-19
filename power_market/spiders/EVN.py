# -*- coding: utf-8 -*-
import scrapy
from power_market.items import CurrentItem
from power_market.items import PdfItem


class EvnSpider(scrapy.Spider):
    name = 'EVN'
    allowed_domains = ['en.evn.com.vn']
    start_urls = ['https://en.evn.com.vn/c3/gioi-thieu-l/Annual-Report-6-13.aspx']
    base_url = "https://en.evn.com.vn"
    table_url = "https://en.evn.com.vn/c3/gioi-thieu-f/Projects-6-14.aspx"
    count = 1

    def parse(self, response):
        yield scrapy.Request(self.table_url,callback=self.table_grab) # 先抓取网页表格

        urls = response.xpath('//div[@class="blog-page page_list"]//@href').getall()
        urls = list(map(lambda x: response.urljoin(x),urls))
        
        for url in urls:
            if "Annual" in url:
                yield scrapy.Request(url,callback=self.pdf_grab) # 筛选含有pdf的链接并执行下载回调

    def pdf_grab(self,response):
        urls = response.xpath('//div[@id="ContentPlaceHolder1_ctl00_159_content_news"]//@href').getall()
        urls = list(map(lambda x: response.urljoin(x),urls))
        for pdf_url in urls:
            if ".pdf" in pdf_url: # 筛选还有.pdf的链接
                filename = str(pdf_url[-10:])
                item = PdfItem(filename=filename,pdf_url=pdf_url)
                self.count = self.count+1 # 下载计数+1
                yield item

    def table_grab(self,response):
        title = response.xpath('//span[@id="ContentPlaceHolder1_ctl00_1391_ltlTitle"]/text()').get() # 标题
        filename = "".join(title) + ".json"
        tables = response.xpath('//div[@class="blog margin-bottom-40 content-detail"]//tbody/tr') # 表格
        #keys = [] # 放到一个list序列中
        values = ''
        for table in tables:
            tds = table.xpath('td')
            for td in tds:
                values = values + "".join(td.xpath('p/text()').get()) + ','
            values = values + ';'
            #keys.append(tds[0].xpath('p/text()').get()) # 列键
            #values.append(tds[1].xpath('p/text()').get()) #列值
        item = CurrentItem(rename=filename,content=values)
        yield item