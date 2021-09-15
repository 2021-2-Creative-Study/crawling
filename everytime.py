from selenium import webdriver

# driver 할당
driver = webdriver.Chrome('../chromedriver/chromedriver.exe')
driver.implicitly_wait(1)

# log in 페이지 접속 & log in
driver.get('https://everytime.kr/login') # driver.get(urtl) -> 페이지 접근
driver.find_element_by_name('userid').send_keys('martinus99')
driver.find_element_by_name('password').send_keys('choi0415')
driver.find_element_by_xpath('//*[@class="submit"]/input').click()
driver.implicitly_wait(1)

