# -*- coding: utf-8 -*-
import scrapy
import json

from power_market.linkmysql import Element
from power_market.linkmysql import GetListFromMySQL

from power_market.items import CurrentItem
from power_market.items import PicItem


class ManualspiderSpider(scrapy.Spider):
    name = 'manualSpider'
    allowed_domains = ['baidu.com']
    start_urls = ['https://baidu.com/']

    # Content - 数据内容，类型取决于Type
    Url = ''
    elements = []
    selector = 0

    def parse(self,response):
        # 打开数据库，并读取数据，生成Elements数组
        self.elements = GetListFromMySQL()
        for element in self.elements:
            if element.ID == 0:
                self.Url = element.Xpath
                #self.allowed_domains.append(element.Xpath)# 添加允许域名，不然scrapy会过滤掉
                self.elements.remove(element)

        scrapy.Request(self.Url,callback=self.parse_detail)

    def parse_detail(self,response):
        for element in self.elements:
            self.selector = element
            if element.Type == 'text':
                yield scrapy.Request(self.Url,self.GetText,dont_filter=True)
            elif element.Type == 'link':
                yield scrapy.Request(self.Url,self.GetLink,dont_filter=True)
            elif element.Type == 'table':
                yield scrapy.Request(self.Url,self.GetTable,dont_filter=True)
            elif element.Type == 'picture':
                yield scrapy.Request(self.Url,self.GetPicture,dont_filter=True)
            elif element.Type == 'video':
                yield scrapy.Request(self.Url,self.GetVideo,dont_filter=True)
            else:
                item = CurrentItem(id=self.selector.ID,content='Type input error.')
                yield item

    # 针对用户选取数据类型，选用爬取方法
    def GetLink(self,response,element):
        if self.selector.Single == 'true':
            link = response.xpath(self.selector.Xpath+'/@href').get()
            item = CurrentItem(id=self.selector.ID,content=link)
            yield item
        else:
            links = response.xpath(self.selector.Xpath+'//@href').getall()
            links = list(map(lambda x: response.urljoin(x),links))
            content = ''
            for link in links:
                content = content + "".join(link) + ';'
            item = CurrentItem(id=self.selector.ID,content=content)
            yield item
        
    def GetText(self,response):
        if self.selector.Single == 'true':
            text = response.xpath(self.selector.Xpath+'/text()').get()
            item = CurrentItem(id=self.selector.ID,content=text)
            yield item
        else:
            texts = response.xpath(self.selector.Xpath+'//text()').getall()
            texts = "".join(texts).strip()
            item = CurrentItem(id=self.selector.ID,content=texts)
            yield item
        
    def GetTable(self,response):
        trs = response.xpath(self.selector.Xpath+'//tr')
        values = ''
        for tr in trs:
            tds = tr.xpath('td')
            for td in tds:
                values = values + "".join(td.xpath('//text()').get()) + ','
            values = values + ';'
        item = CurrentItem(id=self.selector.ID,content=values)
        yield item

    def GetPicture(self,response):
        if self.selector.Single == 'true':
            link = response.xpath(self.selector.Xpath+'/@src').get()
            content = "".join(link)
            item = PicItem(id=self.selector.ID,content=content)
            yield item
        else:
            links = response.xpath(self.selector.Xpath+'//img/@src').getall()
            links = list(map(lambda x: response.urljoin(x),links))
            content = ''
            for link in links:
                content = content + "".join(link) + ';'
            item = CurrentItem(id=self.selector.ID,content=content)
            yield item
    
    def GetVideo(self,response):
        pass