# -*- coding: utf-8 -*-
import scrapy

from scrapy.http import Request, FormRequest
from scrapy.selector import Selector
from scrapy_splash.request import SplashRequest, SplashFormRequest

from power_market.linkmysql import Element
from power_market.linkmysql import GetListFromMySQL

from power_market.items import CurrentItem
from power_market.items import PicItem

lua_script = """
	function main(splash, args)
		splash:go(args.url)
		splash:wait(args.wait)
		splash:runjs("document.getElementByClassName('mod_trun_page clearfix mt20')[0].scrollIntoView(true)")
		splash:wait(args.wait)
		return splash:html()
	end
	"""

class SplashSpider(scrapy.Spider):
    name = 'splash'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    # Content - 数据内容，类型取决于Type
    Url = ''
    elements = []

    def parse(self, response):
        # 打开数据库，并读取数据，生成Elements数组
        self.elements = GetListFromMySQL()
        for element in self.elements:
            if element.ID == 0:
                self.Url = element.Xpath
                #self.allowed_domains.append(element.Xpath)# 添加允许域名，不然scrapy会过滤掉
                self.elements.remove(element)

        yield SplashRequest(self.Url,callback=self.parse_detail,endpoint='execute',args={'lua_source':lua_script, 'images':0, 'wait':5},dont_filter=True)
        pass
    def parse_detail(self,response):
        for element in self.elements:
            if element.Type == 'text':
                yield SplashSpider.GetText(self,response,element)
            elif element.Type == 'link':
                yield SplashSpider.GetLink(self,response,element)
            elif element.Type == 'table':
                yield SplashSpider.GetTable(self,response,element)
            elif element.Type == 'picture':
                yield SplashSpider.GetPicture(self,response,element)
            elif element.Type == 'video':
                yield SplashSpider.GetVideo(self,response,element)
            else:
                item = CurrentItem(id=element.ID,content='Type input error.')
                yield item

    # 针对用户选取数据类型，选用爬取方法
    def GetText(self,response,element):
        if element.Single == 'true':
            text = response.xpath(element.Xpath+'/text()').get()
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
    
    def GetVideo(self,response,element):
        pass