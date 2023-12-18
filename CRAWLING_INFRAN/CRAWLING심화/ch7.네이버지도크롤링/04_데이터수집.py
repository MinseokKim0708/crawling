from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

chrome_options.add_experimental_option('excludeSwitches', ["enable-logging"])

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.implicitly_wait(10)
driver.maximize_window()

driver.get("https://map.naver.com/p")

search = driver.find_element(By.CSS_SELECTOR, "input.input_search")
search.click()
time.sleep(1)
search.send_keys("강남역 맛집")
time.sleep(1)
search.send_keys(Keys.ENTER)
time.sleep(2)

# iframe 안으로 들어가기
driver.switch_to.frame("searchIframe")

# driver.switch_to_default_content() iframe 밖으로 나오기

# iframe 안쪽을 한번 클릭
driver.find_element(By.CSS_SELECTOR, "#_pcmap_list_scroll_container").click()

# 로딩된 데이터 개수 확인
lis = driver.find_elements(By.CSS_SELECTOR, "li.UEzoS")
before_len = len(lis)

while True:
    # 맨 아래로 스크롤 내린다
    driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END) # 아무 태그나 선택하기 위해 body를 선택하는 것

    # 스크롤 사이 페이지 로딩 시간
    time.sleep(1.5)

    # 스크롤 후 로딩된 데이터 개수 확인
    lis = driver.find_elements(By.CSS_SELECTOR, "li.UEzoS")
    after_len = len(lis)

    # 로딩된 데이터 개수가 같다면 반복 멈춤
    if before_len == after_len:
        break
    before_len = after_len

# 데이터 기다리는 시간을 0으로 만들어줌 (데이터가 없어도 빠르게 넘어감)
driver.implicitly_wait(0)

for li in lis:
    # 별점이 있는 것만 크롤링
    if len(li.find_elements(By.CSS_SELECTOR, "span.h69bs.orXYY")) > 0:
        # 가게명
        name = li.find_element( By.CSS_SELECTOR, "span.TYaxT").text
        
        # 별점
        star = li.find_element(By.CSS_SELECTOR, ".h69bs.orXYY").text.split('\n')[1]

        # # 새롭게 오픈한 가게이면
        # if len(li.find_elements(By.CSS_SELECTOR, "span.h69bs.DjPAB")) > 0:
        #     try:
        #         # 방문자 리뷰수
        #         visit_review = li.find_element(By.CSS_SELECTOR,"span.h69bs:nth-child(3)").text
        #     except:
        #         visit_review = "0"
            
        # # 새로 오픈한 가게가 아니면
        # else:
        #     try:
        #         visit_review = li.find_element(By.CSS_SELECTOR,"span.h69bs:nth-child(2)").text
        #     except:
        #         visit_review = "0"
        
        print(name, star)