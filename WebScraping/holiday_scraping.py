import pandas as pd
from WebScraping.proxy.proxy_pool import Proxy
from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm

inst_proxy = Proxy("proxy/proxy.txt")

headers = {'User-agent': 'Mozilla/5.0'}

result = []
years = range(2008, 2020)
for year in tqdm(years):
    url = "https://www.calendarlabs.com/holidays/us/{}".format(year)
    proxy = inst_proxy.get_proxy()
    proxies = {"http": proxy}

    res = get(url, headers=headers, proxies=proxies)
    if res.status_code != 200:
        raise Exception

    html_soup = BeautifulSoup(res.text, 'html.parser')
    holiday_containers = html_soup.tbody
    holidays = holiday_containers.find_all('tr')

    for holiday in holidays:
        containers = holiday.find_all('td')
        date = containers[1].span.text
        weekday = containers[0].span.text
        name = containers[2].text
        result.append([date, weekday, name])

df = pd.DataFrame(result, columns=['date', 'weekday', 'name'])
df.to_csv('../data/holiday.csv', header=True, index=None)
