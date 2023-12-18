import requests
from bs4 import BeautifulSoup
import time
import pyautogui
import pyperclip

keyword = pyautogui.prompt("검색어를 입력하세요.") #사용자 검색
lastpage = int(pyautogui.prompt("몇 페이지까지 크롤링 할까요?"))

total_content = "" #본문 전체 내용
article_num = 0 #기사 개수

page_num = 1
for i in range(1,lastpage*10, 10):
    print(f"{page_num}페이지 크롤링 중 입니다.==================")
    response = requests.get(f'https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query={keyword}&start={i}')
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.select('div.info_group') #뉴스 기사 10개 추출

    for article in articles:
        links = article.select('a.info')
        if len(links) >= 2: #링크가 2개 이상이면
            url = links[1].attrs['href'] #두번째 링크의 href를 추출
            response = requests.get(url, headers={'User-agent':'Mozila/5.0'})
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
        
            if "entertain" in response.url: #만약 연예 뉴스 라면
                content = soup.select_one("#articeBody") #연예 뉴스 본문 내용
            elif "sports" in response.url: #만약 스포츠 뉴스 라면
                content = soup.select_one("#newsEndContents") #스포츠 뉴스 본문 내용
                divs = content.select("div") #본문 내용안에 불필요한 내용 삭제
                for div in divs:
                    div.decompose()
                paragraphs = content.select("p")
                for p in paragraphs:
                    p.decompose()
            else:
                content = soup.select_one('#newsct_article') #기사 본문 내용
            print("==========본문==========\n", content.text.strip())

            total_content += content.text.strip() #본문에 대한 내용 누적 추가
            article_num = article_num + 1 #기사 개수 증가
            time.sleep(0.3)
    page_num += 1

print(f"{article_num}개 기사 크롤링 완료!!")
pyperclip.copy(total_content) #전체 본문 내용 클립보드에 복사
pyautogui.alert("클립보드에 복사되었습니다.") #클립보드에 복사 됐다는 팝업창 노출