"""
Functions used for generating numeric columns
"""
import pandas as pd
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import re
import datetime
import numpy as np
from sklearn.preprocessing import OneHotEncoder


def actors_countvectorize(df):
    """
    Use bag of words model to convert categorical variables to numeric vector
    :param df: the whole dataset
    :return: a dataset with a new column, instance of CountVectorizer()
    """
    df_actors = df['stars']
    vectorizer = CountVectorizer(token_pattern='[^,]+')
    result = vectorizer.fit_transform(df_actors)
    print(result.shape)
    print(vectorizer.vocabulary_)
    print(vectorizer.get_feature_names())
    result = pd.DataFrame(result.toarray(), columns=["actors_" + x for x in vectorizer.get_feature_names()])
    df = pd.concat([df, result], axis=1)
    df.drop('stars', axis=1, inplace=True)
    return df, vectorizer


def actors_featurehashing(df):
    """
    Use feature hashing to convert categorical variables to numeric vector with a fixed dimension
    :param df: the whole dataset
    :return:a dataset with a new column, instance of HashingVectorizer()
    """
    df_actors = df['stars']
    vectorizer = HashingVectorizer(n_features=2**9, alternate_sign=False, norm=None)
    result = vectorizer.fit_transform(df_actors)
    print(result.shape)
    columns = ["actors_hash_val_{}".format(i) for i in range(result.shape[1])]
    result = pd.DataFrame(result.toarray(), columns=columns)
    df = pd.concat([df, result], axis=1)
    df.drop('stars', axis=1, inplace=True)
    return df, vectorizer


def calculate_stars_value(df, star_list):
    """
    Calculate the actors' total gross of each movie
    :param df: testing dataset
    :param star_list: the total gross of each actor
    :return: a dataframe(testing set) with a new column containing the sum of actors' gross
    """
    df_temp = df.explode('stars')
    df_temp.loc[:, 'stars_value'] = df_temp['stars'].map(star_list)
    result = df_temp.groupby('movie')['stars_value'].sum()
    df.drop('stars', axis=1, inplace=True)
    return df.merge(result, on='movie', how='outer')


def actors_mean_sum_encoding(df, method='mean', benchmark='gross'):
    """
    Use mean/sum encoding to convert actor column to numeric variable.
    Use the mean/sum of actor's gross box office to replace the original content
    :param df: training dataset
    :param method: how to calculate the value
    :param benchmark: the column used for calculation
    :return: a dataframe(training set) with a new column containing the sum of actors' gross,
            a encoding map that records the total box office of each actor
    """
    df_temp = df.explode('stars')
    if method == 'mean':
        encode_map = df_temp.groupby('stars')[benchmark].mean()
    if method == 'sum':
        encode_map = df_temp.groupby('stars')[benchmark].sum()
    encode_map.drop('', axis=0, inplace=True)
    print(encode_map)
    return calculate_stars_value(df, encode_map), encode_map


def select_top_k_actors(df, benchmark='gross', k=30):
    df_temp = df.explode('stars')
    encode_map = df_temp.groupby('stars')[benchmark].sum().sort_values(ascending=False)
    encode_map = encode_map.iloc[:k]
    encode_list = encode_map.index.tolist()
    print(encode_map)
    for i in range(k):
        df.loc[:, 'stars_' + str(i)] = df['stars'].map(lambda x: 1 if encode_list[i] in x else 0)
    df.loc[:, 'stars'] = df['stars'].map(lambda x: len(set(x).intersection(set(encode_list))))
    return df, encode_list


def select_top_k(df, column_name, benchmark='gross', existed=False, k=30):
    encode_map = df.groupby(column_name)[benchmark].sum().sort_values(ascending=False)
    encode_map = encode_map.iloc[:k]
    encode_list = encode_map.index.tolist()
    if existed:
        df.loc[:, column_name] = df[column_name].map(lambda x: 1 if x in encode_list else 0)
    else:
        for i in range(k):
            df.loc[:, column_name + '_' + str(i)] = df[column_name].map(lambda x: 1 if encode_list[i] in x else 0)
            df.drop(column_name, inplace=True, axis=1)
    return df, encode_list


def mean_sum_encoding(df, column_name, method='mean', benchmark='gross'):
    """
    Mean/Sum encoding
    :param df: the whole dataset
    :param column_name: the column that needs to be processed
    :param method: mean or sum
    :param benchmark: the column used as the benchmark
    :return: a dataset with a new column , encoding map
    """
    assert (method == 'mean' or method == 'sum')
    if method == 'mean':
        encode_map = df.groupby(column_name)[benchmark].mean()
    if method == 'sum':
        encode_map = df.groupby(column_name)[benchmark].sum()
    # encode_map.drop('', axis=0, inplace=True)
    print(encode_map)
    df.loc[:, column_name] = df[column_name].map(encode_map)
    return df, encode_map


def onehot_encoding(df, prefix, column_name):
    ohc = OneHotEncoder()
    result = ohc.fit_transform(df[column_name].values.reshape(-1, 1)).toarray()
    columns = [prefix + str(ohc.categories_[0][i]) for i in range(len(ohc.categories_[0]))]
    df_onehot = pd.DataFrame(result, columns=columns)
    df.drop(column_name, inplace=True, axis=1)
    return pd.concat([df, df_onehot], axis=1), ohc


def date_to_nth_day(date, format='%Y%m%d'):
    x = date.date()
    temp_x = str(x)
    date = temp_x.replace('-', '')
    date = pd.to_datetime(date, format=format)
    new_year_day = pd.Timestamp(year=date.year, month=1, day=1)
    return (date - new_year_day).days + 1


# Process release_date
def release_date_process(df):
    days = []
    months = []
    dayofyear = []
    weekdays = []
    date_pattern = re.compile(r"[0-9]+-[a-zA-Z]+-[0-9]+")
    date_pattern_2 = re.compile(r"[0-9]+-[a-zA-Z]+")
    for idx, row in df.iterrows():
        date_str = row['release_date']
        year = row['year']
        if date_pattern.match(date_str):
            date = datetime.datetime.strptime(date_str, '%d-%b-%y')
        elif date_pattern_2.match(date_str):
            date = datetime.datetime.strptime(date_str, '%d-%b')
            date = date.replace(year=int(year))
        else:
            date = datetime.datetime(int(year), 6, 30)
        dayofyear.append(date_to_nth_day(date))
        months.append(date.month)
        days.append(date.day)
        weekdays.append(date.weekday() + 1)
    df['month'] = months
    df['day'] = days
    df['dayofyear'] = dayofyear
    df['weekday'] = weekdays
    df.drop('release_date', inplace=True, axis=1)
    return df


# Process runtime
def runtime_process(df):
    df.loc[:, 'runtime'] = df['runtime'].apply(lambda x: int(re.findall(r'\d+', x)[0]) if x is not np.NaN else x)
    return df


# Genre countvectorize
def genre_countvectorize(df):
    df_genre = df['genre']
    vectorizer = CountVectorizer(token_pattern='[^,]+')
    result = vectorizer.fit_transform(df_genre)
    print(result.shape)
    result = pd.DataFrame(result.toarray(), columns=["genre_" + x for x in vectorizer.get_feature_names()])
    df.drop('genre', axis=1, inplace=True)
    return pd.concat([df, result], axis=1), vectorizer


# Frequency encoding
def frequency_encoding(df, column_name):
    fe = df.groupby(column_name).size() / len(df)
    df.loc[:, column_name] = df[column_name].map(fe)
    return df, fe


def budget_helper(x):
    if x is not np.NaN and '$' in x:
        return int(re.sub(r'[$,]', '', x))
    else:
        return np.NaN


def budget_processing(df):
    df['budget'] = df['budget'].apply(lambda x: budget_helper(x))
    df['budget'].fillna(0, inplace=True)
    return df
