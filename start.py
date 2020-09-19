from scrapy import cmdline
print("输入运行的爬虫序号： ")
Number = int(input())
if Number == 7:
    cmdline.execute("scrapy crawl EVN".split())
elif Number == 6:
    cmdline.execute("scrapy crawl EGAT".split())
elif Number == 0:
    cmdline.execute("scrapy crawl manualSpider".split())