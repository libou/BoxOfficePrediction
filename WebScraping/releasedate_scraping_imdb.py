import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

headers = {'User-agent': 'Mozilla/5.0'}


def release_date_scraping(url):
    response = requests.get(url, headers=headers)
    assert response.status_code == 200

    try:
        html_soup = BeautifulSoup(response.text, 'html.parser')
        release_date_containers = html_soup.table.find_all('tr', class_="ipl-zebra-list__item release-date-item")
        for container in release_date_containers:
            if container.find('td', class_="release-date-item__country-name").a.text.strip() == "USA":
                return container.find('td', class_="release-date-item__date").text.strip()
        return release_date_containers[0].find('td', class_="release-date-item__date").text.strip()
    except Exception:
        return


years = range(2008, 2020)
for year in tqdm(years):
    df = pd.read_csv('../data/merged_data/merged_{}.csv'.format(year))
    date_df = df['release_date']
    isna_df = date_df.isna()
    for idx, row in tqdm(isna_df.iteritems()):
        if row is True:
            url = "http://www.imdb.com/title/{}/releaseinfo?ref_=tt_dt_dt".format(df['id'].iloc[idx])
            df['release_date'].iloc[idx] = release_date_scraping(url)
    df.iloc[:, 1:].to_csv('../data/merged_data/merged_{}.csv'.format(year), encoding='utf-8-sig', index=None, mode='w')
