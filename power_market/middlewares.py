# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
import time
from scrapy.http.response.html import HtmlResponse

class SeleniumDownloadMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

    def process_request(self,request,spider):
        self.driver.get(request.url)
        time.sleep(1)
        try:
            while True:
                showMore = self.driver.find_element_by_class_name('show-more') #查找元素，即使是动态请求的
                showMore.click() #模拟点击
                time.sleep(0.3)
                if not showMore:
                    break
        except:
            pass
        source = self.driver.page_source
        response = HtmlResponse(url=self.driver.current_url,body=source,request=request,encoding='utf-8')
        return response

class Selenium_ChromeMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application")

    def process_request(self,request,spider):
        self.driver.get(request.url)
        time.sleep(2)
        pass