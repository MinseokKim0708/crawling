import requests
from bs4 import BeautifulSoup
import pyautogui
import openpyxl

keyword = pyautogui.prompt("검색어를 입력하세요")

wb = openpyxl.Workbook('CRAWLING심화\ch3.쿠팡크롤링\coupang_result.xlsx')
ws = wb.create_sheet(keyword)
ws.append(['순위', '브랜드명', '상품명', '가격', '상세페이지링크'])

rank = 1
done = False

for page in range(1, 5):
    if done == True:
        break
    print(page, "번째 페이지 입니다.")
    main_url = f"https://www.coupang.com/np/search?component=&q={keyword}&channel=user"

    # 헤더에 User-Agent, Accept-Language 를 추가하지 않으면 멈춥니다
    header = {
        'Host': 'www.coupang.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
    }

    response = requests.get(main_url, headers=header)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    links = soup.select("a.search-product-link") # select의 결과는 리스트 자료형
    for link in links:
        if len(link.select("span.ad-badge-text")) > 0 :
            print("광고 상품 입니다")
        else:
            if link.attrs.get('data-product-link'):
                # 일반 상품 링크
                sub_url = "https://www.coupang.com/" + link.attrs['data-product-link']
            else:
                # 베스트셀러 상품 링크
                sub_url = "https://www.coupang.com/" + link.attrs['data-link']

            response = requests.get(sub_url, headers=header)
            html = response.text

            soup = BeautifulSoup(html, 'html.parser')

            # 브랜드명은 있을 수도 있고, 없을 수도 있어요
            # - 중고상품일 때는 태그가 달라져요
            # try - except로 예외처리를 해줍니다
            try:
                brand_name = soup.select_one("a.prod-brand-name").text.strip()
            except:
                brand_name = ""
            
            # 상품명
            product_name = soup.select_one("h2.prod-buy-header__title").text.strip()

            # 가격
            try:
                product_price = soup.select_one("span.total-price > strong").text
            except:
                product_price = 0

            print(rank, brand_name, product_name, product_price)
            ws.append([rank, brand_name, product_name, product_price, sub_url])
            rank = rank + 1
            if rank > 100:
                done = True
                break

wb.save('CRAWLING심화\ch3.쿠팡크롤링\coupang_result.xlsx')