# webdriver 모듈을 selenium에서 가져옴
from selenium import webdriver

# selenium이 chrome을 제어하는데 사용하는 실행 파일인 ChromeDriver의 경로를 지정하는 데 필요한 Service 클래스를 가져옴
from selenium.webdriver.chrome.service import Service

# Chrome 브라우저의 동작을 맞춤설정하기 위해 Options 클래스를 가져옴
from selenium.webdriver.chrome.options import Options

# 크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메세지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 최신 버전의 ChromeDriver 경로를 자동으로 다운로드하거나 검색
service = Service(executable_path=ChromeDriverManager().install())

# 지정된 서비스 및 옵션을 사용하여 Chrome 웹 드라이버를 초기화
driver = webdriver.Chrome(service=service, options=chrome_options)

# 웹페이지 해당 주소 이동
driver.get("https://www.naver.com")