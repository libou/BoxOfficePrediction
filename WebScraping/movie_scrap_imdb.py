import time
from random import randint
from requests import get
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import sys
import datetime
import os
from WebScraping.proxy.proxy_pool import Proxy
import re

# Lists to store the scraped data in
# names = []
# release_dates = []
# years = []
# content_ratings = []
# runtimes = []
# genres = []
# intros = []
# directors = []
# stars = []
# imdb_ratings = []
# grosses = []
# metascores = []
# votes = []

dataset_location = os.path.realpath(os.path.join(os.path.dirname(__file__), "DataSets"))
current_year = int(datetime.datetime.now().year)
headers = {'User-agent': 'Mozilla/5.0'}
proxy_inst = Proxy('proxy/proxy.txt')

# Monitoring the loop as it’s still going
start_time = time.time()
m_requests = 0


def release_date_scraping(url, proxies):
    response = requests.get(url, headers=headers, timeout=100)
    if response.status_code != 200:
        return

    try:
        html_soup = BeautifulSoup(response.text, 'html.parser')
        # release_date_container = html_soup.find('table', class_ = 'ipl-zebra-list ipl-zebra-list--fixed-first release-dates-table-test-only')
        release_date_containers = html_soup.table.find_all('tr', class_="ipl-zebra-list__item release-date-item")
        for container in release_date_containers:
            if container.find('td', class_="release-date-item__country-name").a.text.strip() == "USA":
                if container.find('td', class_="release-date-item__attributes--empty") is None:
                    continue
                else:
                    return container.find('td', class_="release-date-item__date").text.strip()
    except Exception:
        return


input_year = int(input("Please enter start year (eg. 2016): "))
if input_year > current_year:
    print("No movie is recorded in year %i yet!!" % (input_year))
else:
    starts = range(1, 10000, 50)
    for year in tqdm(range(input_year, current_year + 1)):
        for start in tqdm(starts):
            names = []
            release_dates = []
            years = []
            content_ratings = []
            runtimes = []
            genres = []
            intros = []
            directors = []
            stars = []
            imdb_ratings = []
            grosses = []
            metascores = []
            votes = []

            url = "http://www.imdb.com/search/title?release_date=" + str(year) + "," + str(
                year) + "&sort=num_votes,desc&start=" + str(start)
            proxies = {"https": proxy_inst.get_proxy()}
            response = requests.get(url, headers=headers, timeout=10)

            html_soup = BeautifulSoup(response.text, 'html.parser')
            movie_containers = html_soup.find_all('div', class_='lister-item mode-advanced')

            # Extract data from individual movie container
            for container in movie_containers:
                # The name
                name = container.h3.a.text
                names.append(name)

                # The release date
                movie_id = container.h3.a['href'].strip('/').split('/')[1]
                release_date_url = "http://www.imdb.com/title/{}/releaseinfo?ref_=tt_dt_dt".format(movie_id)
                release_date = release_date_scraping(release_date_url, proxies)
                release_dates.append(release_date)

                # The year
                movie_year = container.h3.find('span', class_='lister-item-year').text
                if len(re.findall("\d+", movie_year)) > 0:
                    movie_year = re.findall("\d+", movie_year)[-1]
                years.append(movie_year)

                # The content rating
                if container.find('span', class_='certificate') == None:
                    content_rating = "None"
                else:
                    content_rating = container.find('span', class_='certificate').text
                content_ratings.append(content_rating)

                # The runtime
                if container.find('span', class_='runtime') == None:
                    runtime = "None"
                else:
                    runtime = container.find('span', class_='runtime').text
                runtimes.append(runtime)

                # The genre
                if container.find('span', class_='genre') == None:
                    genre = "None"
                else:
                    genre = container.find('span', class_='genre').text.strip()
                genres.append(genre)

                # The intro
                intro = container.find_all('p', class_='text-muted')[1].text.strip()
                intros.append(intro)

                # The director & stars
                sub_container = container.find('p', class_='')
                crew_list = sub_container.find_all('a')
                if len(crew_list) > 1:
                    director = crew_list[0].text
                    star_list = []
                    for i in range(1, len(crew_list)):
                        star_list.append(crew_list[i].text)
                else:
                    director = "None"
                    star_list = "None"
                directors.append(director)
                stars.append(star_list)

                # The IMDB rating
                if container.strong == None:
                    imdb = "None"
                else:
                    imdb = float(container.strong.text)
                imdb_ratings.append(imdb)

                # The gross
                if len(container.find_all('span', attrs={'name': 'nv'})) > 1:
                    gross = container.find_all('span', attrs={'name': 'nv'})[1]['data-value']
                    grosses.append(gross)
                else:
                    grosses.append('None')

                # The Metascore
                if container.find('span', class_='metascore') == None:
                    m_score = "None"
                else:
                    m_score = container.find('span', class_='metascore').text.strip()
                metascores.append(m_score)

                # The number of votes
                if container.find('span', attrs={'name': 'nv'}) == None:
                    vote = "None"
                else:
                    vote = container.find('span', attrs={'name': 'nv'})['data-value']
                votes.append(vote)
            # print(url)
            # print(year)
            # print(start)
            # print(len(names))
            df = pd.DataFrame({'movie': names,
                                'year': years,
                                'release_date': release_dates,
                                'content_rating': content_ratings,
                                'runtime': runtimes,
                                'genre': genres,
                                'intro': intros,
                                'director': directors,
                                'stars': stars,
                                'imdb': imdb_ratings,
                                'gross': grosses,
                                'metascore': metascores,
                                'vote': votes
                                })
            if not os.path.exists('IMDB_Top10000.csv'):
                df.to_csv('IMDB_Top10000.csv', header=True, mode='a', index=None, encoding='utf_8_sig')
            else:
                df.to_csv('IMDB_Top10000.csv', header=None, mode='a', index=None, encoding='utf_8_sig')

    # test_df = pd.DataFrame({'movie': names,
    #                         'year': years,
    #                         'release_date': release_dates,
    #                         'content_rating': content_ratings,
    #                         'runtime': runtimes,
    #                         'genre': genres,
    #                         'intro': intros,
    #                         'director': directors,
    #                         'stars': stars,
    #                         'imdb': imdb_ratings,
    #                         'gross': grosses,
    #                         'metascore': metascores,
    #                         'vote': votes
    #                         })
    # test_df.to_csv('IMDB_Top10000.csv', header=True)
