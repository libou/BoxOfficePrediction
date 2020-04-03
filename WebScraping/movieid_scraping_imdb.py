import time
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import datetime
import os

dataset_location = os.path.realpath(os.path.join(os.path.dirname(__file__), "DataSets"))
current_year = int(datetime.datetime.now().year)
headers = {'User-agent': 'Mozilla/5.0'}

# Monitoring the loop as it’s still going
start_time = time.time()
m_requests = 0

input_year = 2008
end_year = 2019
if input_year > current_year or end_year > current_year:
    print("No movie is recorded in year %i yet!!" % (max(input_year, end_year)))
else:
    starts = range(1, 10000, 50)
    for year in tqdm(range(input_year, end_year + 1)):
        for start in tqdm(starts):
            names = []
            ids = []

            url = "http://www.imdb.com/search/title?release_date=" + str(year) + "," + str(
                year) + "&sort=num_votes,desc&start=" + str(start)
            response = requests.get(url, headers=headers, timeout=10)

            html_soup = BeautifulSoup(response.text, 'html.parser')
            movie_containers = html_soup.find_all('div', class_='lister-item mode-advanced')

            # Extract data from individual movie container
            for container in movie_containers:
                # The gross
                if len(container.find_all('span', attrs={'name': 'nv'})) <= 1:
                    continue

                # The name
                name = container.h3.a.text
                names.append(name)

                # The release date
                movie_id = container.h3.a['href'].strip('/').split('/')[1]
                ids.append(movie_id)

            df = pd.DataFrame({'movie': names,
                               'id': ids
                               })
            if not os.path.exists('IMDB_ID_{}.csv'.format(year)):
                df.to_csv('IMDB_ID_{}.csv'.format(year), header=True, mode='a', index=None, encoding='utf_8_sig')
            else:
                df.to_csv('IMDB_ID_{}.csv'.format(year), header=None, mode='a', index=None, encoding='utf_8_sig')
