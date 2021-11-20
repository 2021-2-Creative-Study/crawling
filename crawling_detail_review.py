from selenium import webdriver
import random, time
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

# 가상 브라우저 사용
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--diable-dev-shm-usage")
options.add_argument("user-agent={Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36}")

driver = webdriver.Chrome('/Users/eesun/Downloads/chromedriver', options = options)
driver.implicitly_wait(1)
driver.maximize_window()

# log in 페이지 접속 & log in
driver.get('https://everytime.kr/login') # driver.get(urtl) -> 페이지 접근
driver.find_element_by_name('userid').send_keys('martinus99')
driver.find_element_by_name('password').send_keys('choi0415')
driver.find_element_by_xpath('//*[@class="submit"]/input').click()
driver.implicitly_wait(1)


lecture = pd.read_csv('lecture_list.csv')

#강의 -> 강의평가
lecture_review_list=[]
total_review_list = []
url_id_list = lecture.url_id.astype(str)

for url_id in tqdm(url_id_list):
    #강의 페이지로 넘어가기
    url = "https://everytime.kr/lecture/view/"+url_id
    rand_value = random.uniform(2,5)
    time.sleep(rand_value)
    driver.get(url)

    #하나의 강의 평가 페이지 bs로 데이터 수집
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser') #정적텍스트 분석을 사용하는 BS이 selenium보다 빠름 -> 페이지접근에는 동적 수집, 데이터 수집은 정적수집

    lecture_name = soup.select_one("#container > div.side.head > h2").text

    if ":" in lecture_name:
        lecture_name = lecture_name.replace(":","：")

    professor_name = soup.select_one("#container > div.side.head > p:nth-of-type(1) > span").text
    
    rate = soup.select_one('#container > div.side.article > div.rating > div.rate > span > span.value').text # 평점
    assignment = soup.select_one('#container > div.side.article > div.rating > div.details > p:nth-child(1) > span').get_text() # 과제
    team = soup.select_one('#container > div.side.article > div.rating > div.details > p:nth-child(2) > span').get_text() # 조모임
    grade = soup.select_one('#container > div.side.article > div.rating > div.details > p:nth-child(3) > span').get_text() # 학점비율
    Ucheck = soup.select_one('#container > div.side.article > div.rating > div.details > p:nth-child(4) > span').get_text() # 출결
    exam = soup.select_one('#container > div.side.article > div.rating > div.details > p:nth-child(5) > span').get_text() # 시험 횟수

    lecture_review_list.append({
        "url_id"         : url_id,
        "lecture_name"   : lecture_name,
        "professor_name" : professor_name,
        "rate"           : rate,
        "assignment"     : assignment,
        "team"           : team,
        "grade"          : grade,
        "Ucheck"         : Ucheck,
        "exam"           : exam
    })

    total_review_list.append({
        "url_id"         : url_id,
        "lecture_name"   : lecture_name,
        "professor_name" : professor_name,
        "rate"           : rate,
        "assignment"     : assignment,
        "team"           : team,
        "grade"          : grade,
        "Ucheck"         : Ucheck,
        "exam"           : exam
    })
    
    lecture_reviews = pd.DataFrame(lecture_review_list)
    lecture_reviews.to_csv(f'./review_data/{lecture_name}_{professor_name}.csv', index=False, header=True)
    lecture_review_list = []

total_review = pd.DataFrame(total_review_list)
total_review.to_csv(f'./review_data/total.csv', index=False, header=True)
driver.quit()