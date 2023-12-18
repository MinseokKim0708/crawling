import requests
from bs4 import BeautifulSoup
import pyautogui

keyword = pyautogui.prompt("검색어를 입력하세요.")
lastpage = pyautogui.prompt("마지막 페이지번호를 입력해 주세요")
pageNum = 1
for i in range(1,int(lastpage)*10,10):
    print(f"{pageNum}페이지 입니다.===========================================")
    response = requests.get(f"https://search.naver.com/search.naver?where=news&sm=tab_jum&query={keyword}&start={i}") #fstring
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    links = soup.select(".news_tit") # 결과 리스트
    for link in links:
        title = link.text # 태그 안에 텍스트 요소를 가져옴
        url = link.attrs['href'] # href의 속성값을 가져옴
        print(title,url)
    pageNum += 1
    