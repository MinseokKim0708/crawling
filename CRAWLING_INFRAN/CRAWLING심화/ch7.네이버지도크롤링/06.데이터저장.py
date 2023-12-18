from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
import openpyxl

keyword = pyautogui.prompt("검색어를 입력하세요")
wb = openpyxl.Workbook()
ws = wb.create_sheet(keyword)
ws.append(["순위", "이름", "구분", "별점"])


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
search.send_keys(keyword)
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

# 중복 제거
processed_items = set()

rank = 1
for li in lis:
    # 광고상품 아닌것만
    if len(li.find_elements(By.CSS_SELECTOR, "svg.dPXjn")) == 0:
        # 가게명   
        name = li.find_element( By.CSS_SELECTOR, "span.TYaxT").text

        if name not in processed_items:
            processed_items.add(name)

            # 별점이 있는 것만 크롤링
            if len(li.find_elements(By.CSS_SELECTOR, "span.h69bs.orXYY")) > 0:
                
                # 가게명
                # name = li.find_element( By.CSS_SELECTOR, "span.TYaxT").text

                # 가게 종류
                category_menu = li.find_element(By.CSS_SELECTOR, "span.KCMnt").text
                
                # 별점
                star = li.find_element(By.CSS_SELECTOR, ".h69bs.orXYY").text.split('\n')[1]

            print(rank, name, category_menu,  star)
            ws.append([rank, name, category_menu,  float(star)])
            rank = rank + 1
    

wb.save(f"CRAWLING심화\ch7.네이버지도크롤링\{keyword}.xlsx")