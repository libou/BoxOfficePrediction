"""
Crawl the popularity of a specific movie on Twitter from www.trendsmap.com
"""
import json
import requests
import pandas as pd


def popularity_scrap(name, proxy):
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
        proxies = {"https": proxy}
        res = requests.post(https_url, headers=headers, timeout=10, proxies=proxies)
        content = res.content.decode("utf-8")

        data = json.loads(content)['data']
        result = []
        for d in data:
            result.append([name, d[0], d[1][0]])
        df = pd.DataFrame(result, columns=['name', 'date', 'count'])
        df.to_csv('popularity.csv', mode='a')

        if res.status_code == 200:
            return True
        return False
    except Exception as e:
        msg = str(e)
        print(msg)
        return False


df = pd.read_csv("IMDB_Top10000.csv", header=True)
for idx, row in df['name'].iterrows():
    print(row)