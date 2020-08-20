from selenium import webdriver

driver = webdriver.Chrome(executable_path=r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
driver.get('https://www.aemo.com.au/news')
driver.implicitly_wait(10)

elements = driver.find_elements_by_xpath("//h3[@class='field-title']")

print('*'*80)
for element in elements:
    print(element.text)
print('*'*80)

driver.quit()
