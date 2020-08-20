# power_market
Spiders for power websites

1.采用scrapy架构进行爬虫
2.爬取新闻页和价格，产量等数据
3.运行方式为:
    cd power_market
    运行start.py

## 使用selenium+chromedriver模拟人上网行为，抓取任意的动态请求信息
以这种低效的方式实现可以让 即便不懂代码的管理员 也可以自定义配置的 爬虫程序
## 选择元素的方法
### driver.implicitly_wait(10) 设置等待时间，例如网络状况不佳时，可以不立刻返回错误，而是延时处理

### 1.通过id查找元素element = driver.find_element_by_id('id')
### 2.通过class查找所有元素element = driver.find_elements_by_class_name('classname') 返回一个element类的list，如果是elements去掉s则寻找第一个
###   循环提取 for element in elements：
###               print(element.text)
### 3.通过标签查找所有元素element = driver.find_elements_by_tag_name('tag') 返回一个Webelement类的list,Webelement对象可以继续调用find方法，来进行深一步搜索
### 键入element.send_keys('百度一下\n') 点击element.click()

### 4.获取元素属性element.get_attribute('属性键名')
### 5.获取整个元素对应的HTML element.get_attribute('outerHTML')和element.get_attribute('innerHTML')
### 6.获取整个元素对应的输入框里的文字element.get_attribute('value')
### 有些文本内容没有展示在界面上或没有完全展示，查找value就会有问题，可以尝试elt.get_attribute('innerTEXT')或element.get_attribute('textContent')

## css表达式,css查找方法事实上同样可以完成上述元素选择的功能
### 7.根据样式（class名）来查找元素driver.find_element_by_css_selector('.class名')
### 8.同时，这个方法里同同样可以接受dom元素的名字例如<span></span>
### 同理，你也可以通过填写id来查找元素，要求是元素名称前加"#",例如：find_element_by_css_selector('#id名称')
### 9.根据属性的名称来查找元素find_element_by_css_selector('[href="www.baidu.com"]')；此外，若只有href的就一个元素的话，就可以把'='及其后面的内容去掉，只留下"[href]"
### 此外，css属性可以使用包含语句，例如只填写"baidu"，也可以找到
### 还有的写法有：div元素名[class="name"]   .class名[name=""]

### 在css表达式中，选择子元素和后代元素语法，例如：查找元素2，元素2为元素1的直接子元素
### '元素1>元素2'；而后代元素是指元素1，2之间不是包含关系但不是直接下一层
### 至此说明，css的语法可以联合使用

### 使用','分割可以写多个查询语句，例如'[class="name1"],.class名[name="name2"]'，它们是分开查询的

### 10.按照次序查找父元素的第几个结点':nth-child(2)'，冒号前面接你想要指定的父节点，若没有指定就会查找所有元素下的第几节点。':nth-last-child'是按倒数查找
### 同理，我们还可以指定选择第几个某类型的元素（即在所有同类元素中按次序查找）例如'span:nth-of-type(1)'。'span:nth-last-of-type(1)'是按倒数查找
### 将括号内的数字改为'odd'或'even',如'.class名:nth-child(odd)'或'span:nth-of-type(even)'。为奇数或偶数查询
### 11.查询兄弟节点，使用'+'号，例如'h3+span'，若使用'~'，则为查找所有的兄弟节点，如 'h3~span'

### 验证CSS Selector，将上述语法在浏览器后台c+f查询中填写进去可以在浏览器上验证语法和想要查询的元素是否有误

## 抓取iframe或frame中的元素
### 使用语句：driver.switch_to('iframe_reference')  其中iframe_reference可以是iframe中任意的属性：name，id。
### 进一步讲，如果iframe没有上述的属性，可以使用css selector选择器来查找driver.switch_to(find_element_by_css_selector('[href="www.baidu.com"]'))
### 操作完成后，要跳出iframe，使用语句driver.switch_to.default_content()

## 切换浏览器窗口
### mainWindow = driver.current_window_handle # 记得保存主窗口
### for handle in driver.windows_handles:
###     if '' in handle.title:
###         driver.switch_to.window(handle)
### driver.switch_to.window(mainWindow) # 切换回来

## 选择框
### radio框：driver.find_element_by_css_selector('#s_radio input[checked=checked]') # 选中当前元素
###          driver.find_element_by_css_selector('#s_radio input[value=小雷老师]').click() # 点选想要的元素
### checkbox框：driver.find_elements_by_css_selector('#s_checkbox input[checked=checked]') # 将所有已经选中的元素勾打掉
###             for element in elements:    element.click()
###             driver.find_element_by_css_selector('#s_checkbox input[value=小雷老师]').click() # 再把想选的点上
### select框：from selenium.webdriver.support.ui import Select # 导入select类
###           select = Select(driver.find_element_by_id('ss_single')) # 创建对象
###           select = select_by_visible_text("小雷老师") # 单选框下，直接按字符选中

###           select.deselect_all() # 多选下，清掉所有选中的
###           select = select_by_visible_text("小雷老师") # 再选想选的
###           select = select_by_visible_text("小雷老师")

## 其他元素处理：ActionChains类的使用
### from selenium.webdriver.common.action_chains import ActionChains # 导入类
### ac = ActionChains(driver) # 构建对象，该类接收一个Webdrvier对象
### ac.move_to_element(driver.find_element_by_css_selector('[name=dasda]')).perform() # 光标移动上去但并不点击，perform()必须调用不然不会执行

## 冻结元素
### SetTimeout(function(){debugger},5000) # 在浏览器控制台里使用，方便调试者观察网页时使用的技巧

## 弹出窗口 其中alert是个对象，可以单独获取，节省代码书写
### driver.switch_to.alert.accept() # 点击接受
### driver.switch_to.alert.dismiss() # 点击cancel
### driver.switch_to.alert.text() # 获取文本
### driver.switch_to.alert.send_keys('adsad') # 填空、
### 注意，有些弹框不是浏览器自带的弹框，而是html弹框，上述操作就无效，然而既然是是html里的就可以在元素里操作，方式如之前所学

## xpath语法 element = driver.find_element_by_xpath('/html/body/div') # 和学scrapy时的一样
### 根据id属性来xpath：element = driver.find_element_by_xpath("//*[@id='asdasd']")
### 根据属性值包含来选择：a[href*="asdasdad"]       开头：a[href^="asdasdad"]      结尾：a[href$="asdasdad"]
### 根据类名包含来选择："//*[contains(@style,'color')]"     包含并且以它为开头："//*[starts-with(@class,'sada')]"        包含并且以它为结尾："//*[ends-with(@class,'sada')]" 
### 注意，如果单纯以属性查询，//后会跟一个*号
### 选择第几个元素：p[2]        //div/*[2]      倒数：//div/*[last()-2]
### 选择一个范围的元素：//div/*[position()<=2]     选择后几个：//div/*[position()>last()-2]
### 组选择(加竖杠分开执行)：//div | //h4
### 选择父节点：//*[@id='asdasd']/..
### 选择后一个兄弟节点：//*[@class='single_choice']/following-sibling::*  选择前一个兄弟节点：//*[@class='single_choice']/preceding-sibling::h1   注：::后可以指定兄弟元素的类型，*为任意类型
### 注意，如果从基于对象上的内容来查询内容的话，一定要在搜索目录前加./      参考之前scrpay的学习
### 运行结束后关闭窗口driver.quit()


#### 附：
#### 创建Crawl爬虫：scrapy genspider -t crawl name basedomain.com
#### 创建 一般爬虫：scrapy genspider name basedomain.com
#### 打开scrapy shell：scrapy shell "url"


#### 更新pip：python -m pip install --upgrade pip
#### 输入运行后如果出现错误“no module named pip”，则运行以下指令：
#### python -m ensurepip
#### easy_install pip

#### 读取pdf文件的库：pip install camelot
import camelot

//从PDF文件中提取表格
tables = camelot.read_pdf('E://eg.pdf', pages='1', flavor='stream')

//表格信息
print(tables)
print(tables[0])
//表格数据
print(tables[0].data)