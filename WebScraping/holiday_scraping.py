import pandas as pd
from .proxy.proxy_pool import Proxy
from bs4 import BeautifulSoup
from requests import get

inst_proxy = Proxy("proxy/proxy.txt")

url = "https://www.timeanddate.com/holidays/us/2011?hol=25"
headers = {'User-agent': 'Mozilla/5.0'}

years = range(2008, 2020)

res = get(url, headers=headers, )