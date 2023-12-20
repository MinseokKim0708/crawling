from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager
import os
import urllib.request
import pyautogui

keyword = pyautogui.prompt("어떤 이미지를 크롤링 할까요?")

if not os.path.exists(f"CRAWLING_TEST\\naverImgCrawling\\{keyword}") == True:
    os.mkdir(f"CRAWLING_TEST\\naverImgCrawling\\{keyword}")

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

chrome_options.add_experimental_option('excludeSwitches', ["enable-logging"])

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = f'https://search.naver.com/search.naver?where=image&sm=tab_jum&query={keyword}'

driver.implicitly_wait(10)
driver.maximize_window()
driver. get(url)

before_h = driver.execute_script("return window.scrollY")
while True:
    driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)
    time.sleep(1)
    after_h = driver.execute_script("return window.scrollY")
    if after_h == before_h:
        break
    before_h = after_h

imgs = driver.find_elements(By.CSS_SELECTOR, "._fe_image_tab_content_thumbnail_image")
for i, img in enumerate(imgs, 1) :
    imgSrc = img.get_attribute("src")
    print(i, imgSrc)
    urllib.request.urlretrieve(imgSrc, f'CRAWLING_TEST\\naverImgCrawling\\{keyword}\{i}.png')
