from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

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

# 웹 페이지 해당 주소 이동
driver.get("https://www.naver.com/")