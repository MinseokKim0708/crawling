import requests
from bs4 import BeautifulSoup

mainUrl = 'https://www.coupang.com/np/search?component=&q=%ED%97%A4%EB%93%9C%EC%85%8B&channel=user'

header = {
    'Host': 'www.coupang.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
}

response = requests.get(mainUrl, headers=header)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

links = soup.select("a.search-product-link")
for link in links:
    if link.attrs.get('data-product-link'):
        subUrl = "https://www.coupang.com/" + link.attrs['data-product-link']
    
    else:
        subUrl = "https://www.coupang.com/" + link.attrs['data-link']
    
    response = requests.get(subUrl, headers=header) 
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    try:
        brandName = soup.select_one("a.prod-brand-name").text.strip()
    except:
        brandName = ""

    productName = soup.select_one("h2.prod-buy-header__title").text.strip()
    productPrice = soup.select_one("span.total-price > strong").text.strip()

    print(brandName, productName, productPrice)