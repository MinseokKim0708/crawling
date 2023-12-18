import requests
from bs4 import BeautifulSoup
import time

path = f'https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90'
response = requests.get(path)
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
        content = soup.select_one('#newsct_article') #기사 본문 내용
        print(content.text)
        time.sleep(0.3)
        