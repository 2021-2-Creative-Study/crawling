from selenium import webdriver
import random, time
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

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


lecture = pd.read_csv('lecture.csv')

#강의 -> 강의평가
lecture_review_list=[]
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
    review_list = soup.select("article")
    
    #강의리뷰 
    index = 0
    for review in review_list:
        if review.select_one('div.pay') == None: #강의평가가 아니라 중간,기말고사 족보
            rate = review.select_one('p.rate > span > span')["style"] #str사용해야 re사용가능
            rate = float(rate[-5:-2]) #숫자만 (리스트형태로 return되는데 [0]하면 오류뜸...)
            semester = review.select_one('p.info > span.semester').text
            semester = int(semester[0:2])
            text = review.select_one('p.text').text
            like = review.select_one("p.info > span.posvote")
            if like == None:
                like = 0
            else:
                like = int(like.text)
        
            lecture_review_list.append({
                "url_id"         : url_id,
                "index"          : index,
                "lecture_name"   : lecture_name,
                "professor_name" : professor_name,
                "rate"           : rate,
                "semester"       : semester,
                "like"           : like,
                 "text"          : text
               }
            )
            index+=1
    lecture_reviews = pd.DataFrame(lecture_review_list)
    lecture_reviews.to_csv(f'./review_data/{lecture_name}_{professor_name}.csv', index=False, header=True)
    lecture_review_list = []

driver.quit()