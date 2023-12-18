import requests
from bs4 import  BeautifulSoup

res=requests.get("https://www.naver.com/")
html = res.text
soup = BeautifulSoup(html, "html.parser")
word = soup.select_one("span.service_name")
print(word.text)