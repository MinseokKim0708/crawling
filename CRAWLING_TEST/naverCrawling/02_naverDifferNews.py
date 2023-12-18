import requests
from bs4 import BeautifulSoup
import time

url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query=FC%EC%84%9C%EC%9A%B8'
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, "html.parser")

articles = soup.select('div.info_group')

for article in articles:
    links = article.select('a.info')
    if len(links) >= 2:
        article_url = links[1].attrs['href']
        response = requests.get(article_url, headers={'User-agent':'Mozila/5.0'})
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        if 'entertain' in response.url:
            title = soup.select_one('.end_tit')
            content = soup.select_one('#articeBody')

        elif 'sports' in response.url:
            title = soup.select_one('.title')
            content = soup.select_one('#newsEndContents')
            divs = content.select("div")
            for div in divs:
                div.decompose()
            ps = content.select("p")
            for p in ps:
                p.decompose()
       
        else:
            title = soup.select_one('#title_area')
            content = soup.select_one('#newsct_article')
            
        print("==========링크==========\n", article_url)
        print("==========제목==========\n", title.text.strip())
        print("==========본문==========\n", content.text.strip())    
        time.sleep(0.3)
