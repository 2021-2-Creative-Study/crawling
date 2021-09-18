from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

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

## url_list
lecture_list = []

# 강의평가 메뉴로 이동
driver.find_element_by_xpath('//*[@id="menu"]/li[3]/a').click()

## ActionChains 생성
action = webdriver.ActionChains(driver)

## 스크롤 focus 조절 parameter
window = 20
## lecture review counter
review_counter = 1
## 가져올 강의 수
num_lecture = 100

## lecture reivew xpath base string
def updateLectureXpath(cur_review_counter):
    return '//*[@id="container"]/div[2]/div/a[' + str(cur_review_counter) + ']'

while review_counter <= num_lecture:

    if review_counter == window:
        body = driver.find_element_by_css_selector('body')

        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

        window += 20

    driver.find_element_by_xpath(updateLectureXpath(review_counter)).click()

    driver.implicitly_wait(3)

    lecture_list.append([driver.find_element_by_css_selector('#container > div.side.head > h2').text, driver.current_url[34:]])

    driver.back()

    review_counter += 1

lecture = pd.DataFrame(lecture_list)
lecture = lecture.drop_duplicates()
lecture.columns = ["lecture_name", "url_id"]
lecture.to_csv("lecture.csv", index=False, header=True)

driver.quit()