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

# 검색창에서 '수강편람' 입력
## 1. 검색창까지 scroll 내리기
# driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
## 2. keyword 입력할 element 찾고 변수에 저장
search_btn = driver.find_element_by_xpath('//*[@id="searchArticleForm"]/input')
## 3. '수강편람'값을 전송
search_btn.send_keys('졸업요건')
driver.implicitly_wait(3)
## 4. Enter
search_btn.send_keys(Keys.ENTER)


# question을 저장할 List
question_list =[]
# question counter
question_counter = 1
# 가져올 페이지 수
num_question = 10

page_counter = 1
# question counter xpath base string
def updateLectureXpath(cur_question_counter):
    return '//*[@id="container"]/div[2]/article['+ str(cur_question_counter) +']/a/h2'


while page_counter <= num_question:

    driver.find_element_by_xpath(updateLectureXpath(question_counter)).click()
    driver.implicitly_wait(3)


    question_list.append([driver.find_element_by_css_selector('#container > div.wrap.articles > article > a > p').text, driver.current_url[29:]])
    driver.back()
    driver.implicitly_wait(3)

    question_counter += 1

    if question_counter == 20:
        question_counter = 1
        if page_counter == 1:
            driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[2]/a').click() # 다음 장으로 넘김
        elif page_counter == 2:
            driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[2]/a[2]').click() # 다음 장으로 넘김
        else:
            driver.find_element_by_xpath('//*[@id="container"]/div[2]/div[2]/a[3]').click() # 다음 장으로 넘김
        page_counter += 1

    driver.implicitly_wait(3)



question = pd.DataFrame(question_list)
question.columns = ["question_name", "url_id"]
question.to_csv("question_graduate.csv", index=False, header=True)

print(question)

driver.close()