import requests
from bs4 import BeautifulSoup


def get_bestseller():
    base_url = 'http://book.interpark.com'
    url = '{base_url}/display/collectlist.do?_method=bestsellerHourNew&bookblockname=b_gnb&booklinkname=%BA%A3%BD%BA%C6%AE%C1%B8&bid1=w_bgnb&bid2=LiveRanking&bid3=main&bid4=001'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    lis = soup.select('.rankBestContentList > ol > li')
    data = []
    for li in lis:
        rank_data = li.select('.rankBtn_ctrl')
        if len(rank_data) == 1:
            rank = int(rank_data[0]['class'][1][-1])
        else:
            rank = int(rank_data[0]['class'][1][-1] + rank_data[1]['class'][1][-1])
        href = li.select_one('.coverImage > label > a')['href']
        src = li.select_one('.coverImage img')['src']
        title = li.select_one('.itemName').get_text().strip()
        author = li.select_one('.author').get_text().strip()
        company = li.select_one('.company').get_text().strip()
        price = li.select_one('.price > em').get_text().strip()
        price = int(price.replace(',', ''))
        data.append({'순위':rank, '제목':title, '저자':author, '출판사':company,
                     '가격':f'{price:7,d}', 'href':base_url+href, 'src':src})
        
    return data
        
    