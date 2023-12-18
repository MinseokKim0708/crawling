from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager # 크롬 드라이버 자동 업데이트
from bs4 import BeautifulSoup
import pyautogui
import openpyxl

def text_to_num(text):
    text = text.replace("조회수", "").replace("회", "").strip()
    if "억" in text:
        num = float(text.replace("만", "")) * 100000000
    elif "만" in text:
        num = float(text.replace("만", "")) * 10000
    elif "천" in text:
        num = float(text.replace("천", "")) * 1000
    elif "없음" == text:
        num = 0
    else:
        num = int(text) 
    return num

# 검색어 입력하기
keyword = pyautogui.prompt("검색어를 입력하세요")

# 엑셀 생성
wb = openpyxl.Workbook()
ws = wb.create_sheet(keyword)
ws.append(['번호', '제목', '조회수', '날짜'])

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option('excludeSwitches', ["enable-logging"])
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = f'https://www.youtube.com/results?search_query={keyword}'

driver.implicitly_wait(10)
driver.maximize_window()
driver.get(url)

# 7번 스크롤 하기
scroll_count = 3

i = 1
while True:
    # 맨 아래로 스크롤 내린다
    driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)

    # 스크롤 사이에 페이지 로딩 시간
    time.sleep(2)

    if i == scroll_count:
        break
    i += 1

# Selenium - Beautifulsoup 연동방법
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

infos = soup.select("div.text-wrapper")
for i, info in enumerate(infos, 1):
    # 원하는 정보 가져오기
    # 제목
    title = info.select_one("a#video-title").text

    try:
        # 조회수
        views = info.select_one("div#metadata-line > span:nth-of-type(1)").text

        # 날짜
        date = info.select_one("div#metadata-line > span:nth-of-type(2)").text
    except:
        views = "조회수 0회"
        date = "날짜 없음"

    views = text_to_num(views)
    print(title, views, date)
    ws.append([i ,title, views, date])

wb.save(f'CRAWLING심화\ch5.유튜브크롤링\{keyword}.xlsx')