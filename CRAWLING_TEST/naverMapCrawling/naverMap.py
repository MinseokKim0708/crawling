from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager
import openpyxl
import pyautogui

keyword = pyautogui.prompt("검색어를 입력하세요")
wb = openpyxl.Workbook()
ws = wb.create_sheet(keyword)
ws.append(['NO', '이름', '별점' '영업 상태', '리뷰'])

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

chrome_options.add_experimental_option('excludeSwitches', ["enable-logging"])

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.implicitly_wait(10)
driver.maximize_window()

url = 'https://map.naver.com/p'

driver.get(url)

search = driver.find_element(By.CSS_SELECTOR, "input.input_search")
search.click()
time.sleep(1)
search.send_keys(keyword)
time.sleep(1) 
search.send_keys(Keys.ENTER)
time.sleep(1)

driver.switch_to.frame("searchIframe")

driver.find_element(By.CSS_SELECTOR, "#_pcmap_list_scroll_container").click()
lis = driver.find_elements(By.CSS_SELECTOR, "li.UEzoS")
before_len = len(lis)

while True:
    driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)

    time.sleep(1.5)

    lis = driver.find_elements(By.CSS_SELECTOR, "li.UEzoS")
    after_len = len(lis)

    if before_len == after_len:
        break
    before_len = after_len

driver.implicitly_wait(0)

rank = 1
for li in lis:
    if len(li.find_elements(By.CSS_SELECTOR, "svg.dPXjn")) == 0:
        if len(li.find_elements(By.CSS_SELECTOR, "span.h69bs.orXYY")) > 0:
            storeName = li.find_element(By.CSS_SELECTOR, "span.TYaxT").text
            stroeCategory = li.find_element(By.CSS_SELECTOR, "span.KCMnt").text
            storeStar = li.find_element(By.CSS_SELECTOR, ".h69bs.orXYY").text.split('\n')[1]

            if len(li.find_elements(By.CSS_SELECTOR, "span.h69bs.DjPAB")) > 0:
                openState = li.find_element(By.CSS_SELECTOR, "span.h69bs:nth-child(1)").text
                try:
                    review = li.find_element(By.CSS_SELECTOR, "span.h69bs:nth-child(3)").text
                except:
                    review = 0
            else:
                openState = li.find_element(By.CSS_SELECTOR, "span.h69bs:nth-child(1)").text
                try:
                    review = li.find_element(By.CSS_SELECTOR, "span.h69bs:nth-child(3)").text
                except:
                    review = 0

            review = review.replace("리뷰", "")
            
            print(rank, storeName, stroeCategory, storeStar, float(openState), review)
            ws.append([rank, storeName, stroeCategory, storeStar, float(openState), review])
            rank = rank + 1

wb.save(f'CRAWLING_TEST\\naverMapCrawling\\{keyword}.xlsx')