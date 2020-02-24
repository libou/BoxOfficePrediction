"""
Crawl movie score from DouBan
"""

import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json
import time
from random import randint

def getInfo(movie_url):
    req = Request(movie_url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req).read()
    html_soup = BeautifulSoup(response, "html.parser")
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


url = "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=&start={}&limit=10"
for i in range(1):
    list = []
    req = Request(url.format(i * 100), headers={'User-Agent': 'Mozilla/5.0'})
    response = urlopen(req).read()
    data = json.loads(response.decode('utf-8'))['data']
    for d in data:
        movie_info = getInfo(d['url'])
        # time.sleep(randint(1, 5))
        list.append(movie_info)
    result = pd.DataFrame(list, columns=['title', 'alias', 'date', 'rate'])
    result.to_csv('douban.csv', mode='a', header=True, index=None)
    time.sleep(randint(1, 10))

