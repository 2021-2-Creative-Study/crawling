from selenium import webdriver

# 가상브라우저 사용

options = webdriver.ChromeOptions() # 크롬 브라우저 사용 시 가능한 옵션 추가 가능
options.add_argument("--no-sandbox") # 크롬의 'sandox'라는 옵션을 사용하지 않음 -> "앗! 이런" 오류 해결
options.add_argument("--disable-dev-shm-usage") # 서버에서도 크롤링이 잘 되도록..?
# 크롤러 차단 방지 -> user-agent 설정하기
options.add_argument("user-agent={Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36}")

driver = webdriver.Chrome('../chromedriver/chromedriver.exe', options=options)
driver.implicitly_wait(1)
driver.maximize_window()

# log in 페이지 접속 & log in
driver.get('https://everytime.kr/login') # driver.get(urtl) -> 페이지 접근
driver.find_element_by_name('userid').send_keys('martinus99')
driver.find_element_by_name('password').send_keys('choi0415')
driver.find_element_by_xpath('//*[@class="submit"]/input').click()
driver.implicitly_wait(1)