import requests

res = requests.get("https://www.naver.com")
html = res.text
print(html)