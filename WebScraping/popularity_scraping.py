"""
Crawl the popularity of a specific movie on Twitter from www.trendsmap.com
"""
import json
import requests
import pandas as pd
from WebScraping.proxy.proxy_pool import Proxy
import datetime
import re


def popularity_scrap(names, date, proxy):
    """
    Crawl the popularity of a movie discussed on Twitter
    :param name: a list of extracted keywords of the movie's title
    :param date: the timestamp of the release date
    :param proxy: the address of the proxy server
    :return: a tuple including the average popularity from 2014 to 2020, the average popularity within 30
    days around the release date, the max popularity within 30 days around the release date
    """

    avg_all = 0
    avg_30 = 0
    max_30 = 0
    for name in names:
        https_url = "https://www.trendsmap.com/api/keyword_volumes/%23{}".format(name)
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
            'path': "/api/keyword_volumes/%23{}".format(name),
            'referer': "https://www.trendsmap.com/historical?q={}".format(name), 'authority': "www.trendsmap.com",
            'accept': "application/json, text/javascript, */*; q=0.01", 'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.9", 'origin': "https://www.trendsmap.com", 'sec-fetch-mode': "cors",
            'sec-fetch-site': "same-origin", 'x-requested-with': "XMLHttpRequest"}
        try:
            # data = {}
            # data = json.dumps(data)
            proxies = {"http": proxy}
            res = requests.post(https_url, headers=headers, proxies=proxies)
            if res.status_code != 200:
                raise Exception

            content = res.content.decode("utf-8")
            data = json.loads(content)['data']
            result = []
            for d in data:
                # d[0]:timestamp  d[1][0]: value
                result.append([name, d[0], d[1][0]])
            df = pd.DataFrame(result, columns=['name', 'time', 'popularity'])
            if df['popularity'].mean() > avg_all:
                avg_all = df['popularity'].mean()

            left_date = datetime.datetime.fromtimestamp(date) - datetime.timedelta(days=15)
            right_date = datetime.datetime.fromtimestamp(date) + datetime.timedelta(days=15)
            df_30 = df.loc[(df['time'] >= left_date.timestamp()) & (df['time'] <= right_date.timestamp())]
            if df_30['popularity'].mean() > avg_30:
                avg_30 = df_30['popularity'].mean()
            if df_30['popularity'].max() > max_30:
                max_30 = df_30['popularity'].max()
        except Exception as e:
            msg = str(e)
            print(msg)

    return avg_all, avg_30, max_30


inst_proxy = Proxy('proxy/proxy.txt')
input_year = int(input("Please enter start year (eg. 2016): "))
current_year = int(datetime.datetime.now().year)
assert input_year <= current_year
df = pd.read_csv("../data/IMDB_movie_detail_{}.csv".format(input_year))
result = []
for idx, row in df.iterrows():
    movie = row['movie']
    name = row['extracted_name']
    date_str = row['release_date']
    date = datetime.datetime.strptime(date_str, '%d-%m-%y').timestamp()
    while True:
        proxy = inst_proxy.get_proxy()
        try:
            (avg_all, avg_30, max_30) = popularity_scrap(name, date, proxy=proxy)
            result.append([movie, avg_all, avg_30, max_30])
            break
        except Exception:
            print("Wrong proxy: {}".format(proxy))
            continue

new_df = pd.DataFrame(result, columns=['movie', 'avg_all', 'avg_30', 'max_30'])
new_df.to_csv('../data/movie_popularity_{}'.format(input_year), header=True, encoding='utf_8_sig')
