# -*- coding: utf-8 -*-
import scrapy
import re
from power_market.items import aemoItem

class Aemo2Spider(scrapy.Spider):   
    name = 'aemo2'
    allowed_domains = ['aemo.com.au']
    start_urls = ['https://www.aemo.com.au//sxa/search/results/?s={435046A2-7CA4-4692-8D08-31D8A873873E}|{C31F6A9A-41A9-46AC-8B43-07E1CE633F08}&itemid={9797562C-8792-4573-9F50-FE4803C9E714}&sig=&autoFireSearch=true&v=%7B9881B95B-FF45-4FED-BC25-1F7410493733%7D&p=10&e=0&o=Published%20date%2CDescending']
    base_url = "https://www.aemo.com.au"

    number = 0

    def parse(self, response):
        # 抓取新闻目录
        body = response.xpath("//body//text()").getall()
        body = "".join(body).strip() #转换为字符串。并把空白去掉，不然下面提取不出来
        news = re.findall('"Url":"(.*?)"',body) #提取出新闻页的url
        for new in news:
            new_url = self.base_url+new
            if new_url:
                yield scrapy.Request(new_url,callback=self.parse_detail) 

        #进入下一页
        if(self.number < 150):
            self.number = self.number + 10
        else:
            return
        page = str(self.number)
        print("*"*75)
        next_url = str(self.start_urls[0])
        next_url = next_url.replace('&e=0','&e='+page,2)
        print(page,next_url)
        if not next_url:
            return
        else:
            yield scrapy.Request(next_url,callback=self.parse)
        
    def parse_detail(self,response):
        title = response.xpath("//h1[@class='field-title']/text()").get()
        pub_time = response.xpath("//div[@class='is-date field-published-date']/text()").get()
        article = response.xpath("//div[@class='component-content']//text()").getall()
        article_content = "".join(article).strip()

        item = aemoItem(title=title,pub_time=pub_time,article_content=article_content)
        yield item
