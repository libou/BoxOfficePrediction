"""
Crawl movie score from DouBan
"""

from bs4 import BeautifulSoup
from requests import get
from .proxy import proxy_pool


def getInfo(movie_url, proxy):
    # req = Request(movie_url, headers={'User-Agent': 'Mozilla/5.0'})
    # response = urlopen(req).read()
    response = get(movie_url, headers={'User-Agent': 'Mozilla/5.0'}, proxies={"https": proxy})
    html_soup = BeautifulSoup(response.text, "html.parser")
    content = html_soup.find('div', class_="subjectwrap clearfix")

    result = []

    # Get movie's name
    name = html_soup.h1.span.text
    result.append(name)

    # Get alias
    info = content.find('div', attrs={'id': 'info'}).find_all('span', class_='pl')
    for element in info:
        if "又名:" in element.text:
            result.append(element.next_sibling)
            break

    # Get release date
    allDate = content.find_all('span', attrs={'property': 'v:initialReleaseDate'})
    date = [date.text for date in allDate]
    date = ";".join(date)
    result.append(date)

    # Get score
    score = content.find('strong', class_="ll rating_num")
    result.append(score.text)

    return result


# url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start={}&limit=100"
# for i in range(1):
#     list = []
#
#     # Select proxy
#     inst = WebScraping.proxyPool.Proxy("proxy.txt")
#     proxy = inst.get_proxy()
#
#     # req = Request(url.format(80 * 100), headers={'User-Agent': 'Mozilla/5.0'},)
#     # response = urlopen(req).read()
#     # response = urlopen(req)
#     response = get(url.format(i * 100), headers={'User-Agent': 'Mozilla/5.0'}, proxies={"https": proxy}, timeout=10)
#     data = json.loads(response.text)['data']
#     for d in data:
#         proxy = inst.get_proxy()
#         movie_info = getInfo(d['url'], proxy)
#         # time.sleep(randint(1, 5))
#         list.append(movie_info)
#     result = pd.DataFrame(list, columns=['title', 'alias', 'date', 'rate'])
#     result.to_csv('douban.csv', mode='a', header=True, index=None)
#     time.sleep(randint(1, 10))

# inst = WebScraping.proxyPool.Proxy('proxy.txt')
# proxy = inst.get_proxy()
# print(proxy)
# proxy = "https://182.138.182.133:8118"
# WebScraping.proxyPool.test_proxy(proxy)

WebScraping.proxy.proxy_pool.test_proxy_post()
