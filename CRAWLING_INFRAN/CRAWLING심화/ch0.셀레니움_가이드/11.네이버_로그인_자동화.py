from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pyautogui
import pyperclip

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

# 브라우저 꺼짐 방지 코드
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메세지 차단
chrome_options.add_experimental_option('excludeSwitches', ["enable-logging"])

# 최신 버전의 ChromeDriver 경로를 자동으로 다운로드하거나 검색
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 웹 페이지가 로딩될때까지 5초 기다림
driver.implicitly_wait(5)

# 화면 최대화
driver.maximize_window()

# 웹 페이지 해당 주소 이동
driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")

# 아이디 입력창
id = driver.find_element(By.CSS_SELECTOR, "#id")
id.click()
pyperclip.copy("minsuk0708")
pyautogui.hotkey("ctrl", "v")
time.sleep(2)

# 비밀번호 입력창
pw = driver.find_element(By.CSS_SELECTOR, "#pw")
pw.click()
pyperclip.copy("Kms0708@!")
pyautogui.hotkey("ctrl", "v")
time.sleep(2)

# 로그인버튼 
login_btn = driver.find_element(By.CSS_SELECTOR, "#log\.login")
login_btn.click()