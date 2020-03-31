import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import time
import datetime
import os
from WebScraping.proxy.proxy_pool import Proxy
import re

current_year = int(datetime.datetime.now().year)
headers = {'User-agent': 'Mozilla/5.0'}
proxy_inst = Proxy('proxy/proxy.txt')

input_year = int(input("Please enter start year (eg. 2016): "))
end_year = int(input("Please enter end year (eg. 2020): "))
if input_year > current_year or end_year > current_year:
    print("No movie is recorded in year %i yet!!" % (max(input_year, end_year)))
else:
    starts = range(1, 10000, 50)
    for year in tqdm(range(input_year, end_year + 1)):
        for start in tqdm(starts):
            names = []