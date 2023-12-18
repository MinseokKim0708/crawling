import requests
from bs4 import BeautifulSoup
import time

url = 'https://search.naver.com/search.naver?where=news&sm=tab_jum&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90'
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
        title = soup.select_one('#title_area').text
        content = soup.select_one('#newsct_article').text.strip()
        print("==========링크==========\n", article_url)
        print("==========제목==========\n", title)
        print("==========본문==========\n", content)
        time.sleep(0.3)


        

