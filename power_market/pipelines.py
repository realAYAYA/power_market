# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter #适合数据量多的时候
import json
import requests #used for download pdf

import pymysql
from twisted.enterprise import adbapi # 用于异步处理-连接池
from pymysql import cursors

from .items import CurrentItem
from .items import PdfItem

class PowerMarketPipeline:
    def __init__(self):
        pass

    def open_spider(self,spiders):
        print("------ TablePipeline start ------")

    def process_item(self, item, spider):
        if isinstance(item,CurrentItem):
            self.fp = open(item['rename'],'wb')
            self.exporters = JsonLinesItemExporter(self.fp,ensure_ascii=False,encoding='utf-8')
            self.exporters.export_item(item)
            self.fp.close()
        else:
            Type = str(type(item))
            print('------ '+'Warnning, PowerMarketPipeline: ItemType('+ Type +') matched failed, so skip it. ------')
        return item

    def close_spider(self,spider):
        print("------ TablePipeline end ------")

class Pdf_Download_Pipeline:
    def __init__(self):
        pass

    def open_spider(self,spiders):
        print("------ PDF downloader running ------")

    def process_item(self, item, spider):
        if isinstance(item,PdfItem):
            self.fp = open(item['rename'],'wb')
            pdf = requests.get(item['pdf_url'])
            self.fp.write(pdf.content)
            self.fp.close()
        else:
            Type = str(type(item))
            print('------ '+'Warnning, Pdf_Downloader_Pipeline: ItemType('+ Type +') matched failed, so skip it. ------')
        return item
    
    def close_spider(self,spider):
        print("------ PDF downloader end ------")




# 异步管线
class MySQLPipeline(object):
    def __init__(self):
        dbparams = { #
            'host': '127.0.0.1',
            'port':3306,
            'user':'root',
            'password':'123456',
            'database':'powermarket',
            'charset':'utf8',
            #'oursorclass':cursors.DictCursor
        }
        self.dppool = adbapi.ConnectionPool('pymysql',**dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            UPDATE news_cache SET content=%s WHERE id=%s
            """
        return self._sql
    
    def open_spider(self,spiders):
        print("------ MySQLPipeline start ------")

    # 异步存储数据到MYSQL
    def process_item(self,item,spider):
        defer = self.dppool.runInteraction(self.insert_item,item)
        defer.addErrback(self.handle_error,item,spider)

    def close_spider(self,spider):
        print("------ MySQLPipeline end ------")

    def insert_item(self,cursor,item):
        if isinstance(item,CurrentItem):
            cursor.execute(self.sql,(item['content'],item['id']))
        return item

    def handle_error(self,cursor,item,spider):
        print(cursor)
        pass