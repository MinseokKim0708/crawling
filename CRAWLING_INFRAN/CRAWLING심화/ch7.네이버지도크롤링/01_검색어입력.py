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