"""
Crawl the detail of each movie
"""

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import datetime
import os
from .proxy.proxy_pool import Proxy

current_year = int(datetime.datetime.now().year)
headers = {'User-agent': 'Mozilla/5.0'}
proxy_inst = Proxy('proxy/proxy.txt')


def get_details(url):
    result = {}
    res = requests.get(url, headers=headers, timeout=10)

    html_soup = BeautifulSoup(res.text, 'html.parser')
    details_container = html_soup.find('div', attrs={'id': 'titleDetails'})
    details = details_container.find_all('div', class_="txt-block")
    for detail in details:
        if detail.h4 is None:
            continue
        if "Country:" in detail.h4.text:
            result['country'] = detail.a.text
            continue
        if "Budget:" in detail.h4.text:
            result['budget'] = detail.h4.next_element.next_element.strip()
            continue
        if "Cumulative Worldwide Gross:" in detail.h4.text:
            result['worldwide_gross'] = detail.h4.next_element.next_element.strip()
            continue
        if "Production Co:" in detail.h4.text:
            result['company'] = detail.a.text.strip()
            break
    return result


input_year = int(input("Please enter start year (eg. 2016): "))
end_year = int(input("Please enter end year (eg. 2020): "))
if input_year > current_year or end_year > current_year:
    print("No movie is recorded in year %i yet!!" % (max(input_year, end_year)))
else:
    starts = range(1, 10000, 50)
    for year in tqdm(range(input_year, end_year + 1)):
        for start in tqdm(starts):
            names = []
            countries = []
            budgets = []
            companies = []
            worldwide_grosses = []

            url = "http://www.imdb.com/search/title?release_date=" + str(year) + "," + str(
                year) + "&sort=num_votes,desc&start=" + str(start)
            proxies = {"https": proxy_inst.get_proxy()}
            response = requests.get(url, headers=headers, timeout=10)

            html_soup = BeautifulSoup(response.text, 'html.parser')
            movie_containers = html_soup.find_all('div', class_='lister-item mode-advanced')

            # Extract data from individual movie page
            for container in movie_containers:
                # The gross
                if len(container.find_all('span', attrs={'name': 'nv'})) <= 1:
                    continue

                # The name
                name = container.h3.a.text
                names.append(name)

                # Details
                page_url = "http://www.imdb.com" + container.h3.a['href'].strip()
                detail = get_details(page_url)
                if detail.__contains__("country"):
                    countries.append(detail['country'])
                else:
                    countries.append("None")
                if detail.__contains__("budget"):
                    budgets.append(detail['budget'])
                else:
                    budgets.append("None")
                if detail.__contains__("worldwide_gross"):
                    worldwide_grosses.append(detail['worldwide_gross'])
                else:
                    worldwide_grosses.append("None")
                if detail.__contains__("company"):
                    companies.append(detail['company'])
                else:
                    companies.append("None")
            df = pd.DataFrame({'movie': names,
                               'country': countries,
                               'budget': budgets,
                               'worldwide_gross': worldwide_grosses,
                               'production_company': companies
                               })
            if not os.path.exists('IMDB_movie_detail_{}.csv'.format(year)):
                df.to_csv('IMDB_movie_detail_{}.csv'.format(year), header=True, mode='a', index=None, encoding='utf_8_sig')
            else:
                df.to_csv('IMDB_movie_detail_{}.csv'.format(year), header=None, mode='a', index=None, encoding='utf_8_sig')
