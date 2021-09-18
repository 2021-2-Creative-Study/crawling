from selenium import webdriver

# 가상 브라우저 사용
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--diable-dev-shm-usage")
options.add_argument("user-agent={Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36}")

driver = webdriver.Chrome('../chromedriver/chromedriver.exe', options=options)
driver.implicitly_wait(1)
driver.maximize_window()

# Log in
driver.get("https://everytime.kr/login")
driver.find_element_by_name('userid').send_keys('martinus99')
driver.find_element_by_name('password').send_keys('choi0415')
driver.find_element_by_xpath('//*[@class="submit"]/input').click()
driver.implicitly_wait(1)

# make 'url_id_list'

## ActionChains 생성
action = webdriver.ActionChains(driver)
## 스크롤 focus 조절 parameter
focus = 20
## 스크롤 focus selector base string
scroll_base = '#container > div:nth-child(4) > div > a:nth-child(' + str(focus) + ')'

# 강의평가 메뉴로 이동
driver.find_element_by_xpath('//*[@id="menu"]/li[3]/a').click()

# 스크롤 focus를 맞출 review를 선택하고
review = driver.find_element_by_css_selector(scroll_base)
# 해당 review에 포커스 맞추기
action.move_to_element(review).perform()
# 특정 review 클릭(이후 현재 url 가져오기)
driver.find_element_by_xpath('//*[@id="container"]/div[2]/div/a[40]').click()