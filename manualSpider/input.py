
class Baseinfo:
    def __init__(self):
        self.baseurl = ''           # 用户指定初始页面
        self.url = ''               # 一级页面解析，例如用户给的是新闻目录，需要点进去
        # rule
        self.multiPageParsing = False # 开启多页解析功能，需要指定上面的url

        self.catchRate = False      # 设定爬取频率，不点就不限制
        self.pageFlip = False       # 翻页规则开启，开启后需要指定翻页按钮
        self.scroll = False         # 开启自动下滚，针对某些网页下滚请求数据
        self.more = False           # 开启点击更多按钮，开启后需要指定更多按钮

class SearchInfo:
    def __init__(self):
        self.element_category = ''  # 通过id,class,标签，属性值（要唯一）查询单个元素,这边我们统一使用xpath吧
                                    # 增加一个判定，如果用户查找的元素是多个元素，则需要帮用户检查并循环输出
                                    # 问题在于用户想搜一个，还是想搜一组，或者直接加上一个选项，选取多个元素下的某系内容

        self.content_category = ''  # txt文本，图片，链接，dom源代码
        self.search_name = ''       # 查询元素的名称，要对应之前填写的元素种类
        self.count = 1              # 搜索个数，默认为1，-1或输入超出实际结果就全查
        self.rename = ''            # 用户自定义对爬取数据标注，方便后面存储进数据库
        self.content = ''           # 查询结果展示，如果有多个就只显示第一个
