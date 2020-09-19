import pymysql

# 这是新闻数据爬取配置的类
class Element(object):
    def __init__(self,Id,Type,single,xpath):
        self.ID = Id
        self.Type = Type
        self.Single = single
        self.Xpath = xpath
        self.Content=''
        pass

def GetListFromMySQL():
    config={
        'host': '127.0.0.1',
        'port':3306,
        'user':'root',
        'password':'123456',
        'database':'powermarket',
        'charset':'utf8',
    }
    db = pymysql.connect(**config)
    cursor = db.cursor() #生成游标

    sql = "select id,type,single,xpath from news_cache"# 获取表中所有数据
    cursor.execute(sql)

    Elements =[]
    result = cursor.fetchall()
    for i in range(len(result)):
        element = Element(result[i][0],result[i][1],result[i][2],result[i][3])
        Elements.append(element)

    cursor.close()
    db.close()
    return Elements
