from selenium import webdriver
import pandas as pd
import pickle as pkl
from selenium.webdriver.common.keys import Keys # 스크롤을 내리기 위해 Import


# 가상 브라우저 사용
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--diable-dev-shm-usage")
options.add_argument("user-agent={Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36}")

driver = webdriver.Chrome('/Users/eesun/Downloads/chromedriver', options = options)
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

# 자유게시판 메뉴로 이동
driver.find_element_by_xpath('//*[@id="submenu"]/div/div[2]/ul/li[1]/a').click()

## ActionChains 생성
action = webdriver.ActionChains(driver)

# 검색창에서 '학식' 입력
## 1. 검색창까지 scroll 내리기
# driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
## 2. keyword 입력할 element 찾고 변수에 저장
search_btn = driver.find_element_by_xpath('//*[@id="searchArticleForm"]/input')
## 3. '학식'값을 전송
search_btn.send_keys('학정')
driver.implicitly_wait(3)
## 4. Enter
search_btn.send_keys(Keys.ENTER)
driver.implicitly_wait(3)


# question을 저장할 List
question_list =[]
# question counter
question_counter = 2
# 가져올 페이지 수
num_question = 10
# page counter
page_counter = 1

# question counter xpath base string
def updateQuestionCssSelector(cur_question_counter):
    return '#container > div.wrap.articles > article:nth-child('+ str(cur_question_counter) +') > a > h2'


while page_counter <= num_question:


    question_list.append([driver.find_element_by_css_selector(updateQuestionCssSelector(question_counter)).text])
    driver.implicitly_wait(3)
    question_counter += 1


    # 다음 장으로 넘김
    if question_counter == 21:
        question_counter = 2
        if page_counter == 1:
            driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[2]/a').click()
        elif page_counter == 2:
            driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[2]/a[2]').click()
        else:
            driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[2]/a[3]').click()
        page_counter += 1

    driver.implicitly_wait(3)



question = pd.DataFrame(question_list)
question.columns = ["question_name"]
question.to_csv("question_hakjeong2.csv", index=False, header=True)

print(question)

driver.close()