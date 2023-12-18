import requests
from bs4 import BeautifulSoup
import time


response = requests.get(f'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%97%90%EC%8A%A4%ED%8C%8C')
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
            title = soup.select_one(".end_tit")
            content = soup.select_one("#articeBody")
        else:
            title = soup.select_one("#title_area")
            content = soup.select_one('#newsct_article') #기사 본문 내용
        print("==========링크==========\n", url)
        print("==========제목==========\n", title.text.strip())
        print("==========본문==========\n", content.text.strip() )
        time.sleep(0.3)