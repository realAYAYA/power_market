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

    def parse(self,response):
        # 打开数据库，并读取数据，生成Elements数组
        self.elements = GetListFromMySQL()
        for element in self.elements:
            if element.ID == 0:
                self.Url = element.Xpath
                #self.allowed_domains.append(element.Xpath)# 添加允许域名，不然scrapy会过滤掉
                self.elements.remove(element)

        yield scrapy.Request(self.Url,callback=self.parse_detail,dont_filter=True)

    def parse_detail(self,response):
        for element in self.elements:
            if element.Type == 'text':
                yield ManualspiderSpider.GetText(self,response,element)
            elif element.Type == 'link':
                yield ManualspiderSpider.GetLink(self,response,element)
            elif element.Type == 'table':
                yield ManualspiderSpider.GetTable(self,response,element)
            elif element.Type == 'picture':
                yield ManualspiderSpider.GetPicture(self,response,element)
            elif element.Type == 'video':
                yield ManualspiderSpider.GetVideo(self,response,element)
            else:
                item = CurrentItem(id=element.ID,content='Type input error.')
                yield item

    # 针对用户选取数据类型，选用爬取方法
    def GetText(self,response,element):
        if element.Single == 'true':
            text = response.xpath(element.Xpath+'/text()').get()
            count = 0 #若xpath爬取失败，此计数器则将用来倒计时次数，尝试修改xpath
            while (not text and count < 3):# 如果返回为空，则说明网页开发者工具下复制的xpath路径和网页源码不一样，里面还有动态加载的标签，尝试去掉
                element.Xpath = element.Xpath.replace('/div','',1)
                text = response.xpath(element.Xpath+'/text()').get()
                count = count+1
            item = CurrentItem(id=element.ID,content=text)
            return item
        else:
            texts = response.xpath(element.Xpath+'//text()').getall()
            texts = "".join(texts).strip()
            item = CurrentItem(id=element.ID,content=texts)
            return item

    def GetLink(self,response,element):
        if element.Single == 'true':
            link = response.xpath(element.Xpath+'/@href').get()
            count = 0 #若xpath爬取失败，此计数器则将用来倒计时次数，尝试修改xpath
            while (not link and count < 3):# 如果返回为空，则说明网页开发者工具下复制的xpath路径和网页源码不一样，里面还有动态加载的标签，尝试去掉
                element.Xpath = element.Xpath.replace('/div','',1)
                link = response.xpath(element.Xpath+'/@href').get()
                count = count+1
            link = response.urljoin(link)
            item = CurrentItem(id=element.ID,content=link)
            return item
        else:
            links = response.xpath(element.Xpath+'//@href').getall()
            links = list(map(lambda x: response.urljoin(x),links))
            content = ''
            for link in links:
                content = content + "".join(link) + ';'
            item = CurrentItem(id=element.ID,content=content)
            return item
        
    def GetTable(self,response,element):
        trs = response.xpath(element.Xpath+'//tbody/tr')
        content = ''
        for tr in trs:
            tds = tr.xpath('td')
            for td in tds:
                v = td.xpath('p/text()').get()
                if v==None:
                    v = td.xpath('text').get() #不同的页面td标签里可以能夹杂其他标签也可能没有
                content = content + v + ','
            content = content + ';'
        item = CurrentItem(id=element.ID,content=content)
        return item

    def GetPicture(self,response,element):
        if element.Single == 'true':
            link = response.xpath(element.Xpath+'/@src').get()
            content = "".join(link)
            item = PicItem(id=element.ID,content=content)
            return item
        else:
            links = response.xpath(element.Xpath+'//img/@src').getall()
            links = list(map(lambda x: response.urljoin(x),links))
            content = ''
            for link in links:
                content = content + "".join(link) + ';'
            item = CurrentItem(id=element.ID,content=content)
            return item
    
    def GetPDF(self,response,element):
        pass

    def GetVideo(self,response,element):
        pass