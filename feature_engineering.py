import pandas as pd
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import re
import datetime
import numpy as np
from sklearn.model_selection import train_test_split


# Bag of words
def actors_countvectorize(df_actors):
    vectorizer = CountVectorizer(token_pattern='[^,]+')
    result = vectorizer.fit_transform(df_actors)
    print(result.shape)
    print(vectorizer.vocabulary_)
    print(vectorizer.get_feature_names())
    return pd.DataFrame(result.toarray(), columns=["actors_" + x for x in vectorizer.get_feature_names()])


# Feature hashing
def actors_featurehashing(df_actors):
    vectorizer = HashingVectorizer(n_features=2**9, alternate_sign=False, norm=None)
    result = vectorizer.transform(df_actors)
    print(result.shape)
    columns = ["actors_hash_val_{}".format(i) for i in range(result.shape[1])]
    return pd.DataFrame(result.toarray(), columns=columns)


# Mean Encoding for production_company
def production_company_mean_encoding(df, benchmark='gross'):
    mean_encode = df.groupby('production_company')[benchmark].mean()
    print(mean_encode)
    return df['production_company'].map(mean_encode), mean_encode


# One-hot for content_rating
def rating_onehot(df):
    return pd.get_dummies(df, prefix=['rating'], columns=['content_rating'])


# Process release_date
def release_date_process(df):
    days = []
    months = []
    date_pattern = re.compile(r"[0-9]+ [a-zA-Z]+ [0-9]+")
    for idx, row in df.iterrows():
        date_str = row['release_date']
    if date_pattern.match(date_str):
        date = datetime.datetime.strptime(date_str, '%d %B %Y')
    else:
        date = datetime.datetime(2020, 6, 30)
    months.append(date.month)
    days.append(date.day)
    df['month'] = months
    df['day'] = days
    return df


# Process runtime
def runtime_process(df_runtime):
    return df_runtime.apply(lambda x: re.findall(r'\d+', x))


# Genre countvectorize
def genre_countvectorize(df_genre):
    vectorizer = CountVectorizer(token_pattern='[^,]+')
    result = vectorizer.fit_transform(df_genre)
    print(result.shape)
    return pd.DataFrame(result.toarray(), columns=["genre_" + x for x in vectorizer.get_feature_names()])


# Director mean/sum encoding
def director_encoding(df, method='mean', benchmark='gross'):
    if method == 'mean':
        mean_encode = df.groupby('director')[benchmark].mean()
        print(mean_encode)
        return df['director'].map(mean_encode), mean_encode
    if method == 'sum':
        sum_encode = df.groupby('director')[benchmark].sum()
        print(sum_encode)
        return df['director'].map(sum_encode), sum_encode


# Mean/sum encoding
def mean_sum_encoding(df, column_name, method='mean', benchmark='gross'):
    if method == 'mean':
        mean_encode = df.groupby(column_name)[benchmark].mean()
        print(mean_encode)
        return df[column_name].map(mean_encode), mean_encode
    if method == 'sum':
        sum_encode = df.groupby(column_name)[benchmark].sum()
        print(sum_encode)
        return df[column_name].map(sum_encode), sum_encode


# Frequency encoding
def frequency_encoding(df, column_name):
    fe = df.groupby(column_name).size() / len(df)
    return df[column_name].map(fe), fe


# Actors mean/sum encoding
def actors_mean_sum_encoding(df, method='mean', benchmark='gross'):
    df_temp = df.explode('stars')
    if method == 'mean':
        mean_encode = df_temp.groupby('stars')[benchmark].mean()
        # the total box office of each actor
        print(mean_encode)
        df_temp.loc[:, 'stars_value'] = df_temp['stars'].map(mean_encode)
        # Return the total stars' value of each movie
        return df_temp.groupby('movie')['stars_value'].sum(), mean_encode


# Calculate the stars' value of each movie
def calculate_stars_value(df, star_list):
    df_temp = df.explode('stars')
    df_temp.loc[:, 'stars_value'] = df_temp['stars'].map(star_list)
    result = df_temp.groupby('movie')['stars_value'].sum()
    return df.merge(result, on='movie', how='outer')


df_origin = pd.read_csv('data/boxoffice_dataset.csv', index_col=0, keep_default_na=False)
features = list(df_origin)
features = features.remove('movie')
features = features.remove('intro')
features = features.remove('budget')
features = features.remove('id')
features = features.remove('worldwide_gross')
features = features.remove('extracted_name')
features = features.remove('gross')

X_train, X_test, y_train, y_test = train_test_split(df_origin)
