from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import urllib.request
import pyautogui
# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

keyword = pyautogui.prompt("검색어를 입력하세요.")

if not os.path.exists(f'CRAWLING심화\ch4.구글이미지크롤링\{keyword}') == True:
    os.mkdir(f'CRAWLING심화\ch4.구글이미지크롤링\{keyword}')

# 브라우저 꺼짐 방지 코드
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메세지 차단
chrome_options.add_experimental_option('excludeSwitches', ["enable-logging"])

# 최신 버전의 ChromeDriver 경로를 자동으로 다운로드하거나 검색
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# url 검색
url = f"https://www.google.com/search?q={keyword}&sca_esv=581612012&tbm=isch&sxsrf=AM9HkKnRu6DCGGz23e29xT4BSB7Hq95zgA:1699754235522&source=lnms&sa=X&ved=2ahUKEwiboaf7rb2CAxWJfd4KHWkWA9MQ_AUoAXoECAQQAw&biw=1552&bih=737&dpr=1.65"

# 웹 페이지가 로딩될때까지 10초 기다림
driver.implicitly_wait(10)

# 화면 최대화
driver.maximize_window()

driver.get(url)

# 스크롤 전 높이
before_h = driver.execute_script("return window.scrollY")

# 무한 스크롤
while True:

    # 맨 아래로 스크롤 내린다.
    driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)

    # 스크롤 사이 페이지 로딩 시간
    time.sleep(1)

    # 스크롤 후 높이
    after_h = driver.execute_script("return window.scrollY")
    if after_h == before_h:
        break
    before_h = after_h

# 썸네일 이미지 태크 추출
imgs = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")


for i, img in enumerate (imgs, 1):
    # 이미지를 클릭해서 큰 사이즈 찾기
    # 클릭하다보면 element click intercepted 에러가 등장
    # javascript로 클릭을 직접 하도록 만들어주면 된다
    driver.execute_script("arguments[0].click();", img)
    time.sleep(1)

    # 큰 이미지 주소 추출
    target = driver.find_element(By.CSS_SELECTOR, 'img.sFlh5c.pT0Scc.iPVvYb')
    img_src = target.get_attribute('src')

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozila/5.0')]
    urllib.request.install_opener(opener)

    # 이미지 다운로드

    urllib.request.urlretrieve(img_src, f'CRAWLING심화\ch4.구글이미지크롤링\{keyword}\{keyword}{i}.jpg')

    print(f'img {i}개 : {target}')