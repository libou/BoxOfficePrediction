"""
Generate training set and testing set containing different combination of features
"""

from feature_engineering import *
from sklearn.model_selection import train_test_split

df = pd.read_csv('data/boxoffice_dataset_part.csv', index_col=0)

# Fixed part
# Budget
df = budget_processing(df)

# Convert stars column from type str to type list
df['stars'] = df['stars'].apply(lambda x: eval(x))

# Fill nan value
df['release_date'].fillna('None', inplace=True)
df['avg_all'].fillna(0, inplace=True)
df['avg_30'].fillna(0, inplace=True)
df['max_30'].fillna(0, inplace=True)
df['country'].fillna('None', inplace=True)
df['imdb'].fillna(df['imdb'].mean(), inplace=True)
df['metascore'].fillna(df['metascore'].mean(), inplace=True)

# Release date
df = release_date_process(df)

# Runtime
df = runtime_process(df)
df['runtime'].fillna(df['runtime'].mean(), inplace=True)

# Content_rating
df, rating_onehoter = onehot_encoding(df, prefix='rating_', column_name='content_rating')
df.drop('rating_M', axis=1, inplace=True)

# Country
df, country_onehoter = onehot_encoding(df, prefix='country_', column_name='country')

# Genre
df, genre_vectorizer = genre_countvectorize(df)

# Drop worldwide_gross
df.drop(['worldwide_gross'], axis=1, inplace=True)

print(df)

Trainset, Testset, _, _ = train_test_split(df, df, test_size=0.3)

"""
Process Training set
"""
# Director
# Trainset, director_map = mean_sum_encoding(Trainset, 'director', method='mean', benchmark='gross')
Trainset, director_list = select_top_k(Trainset, 'director', existed=True)

# Actors
# Trainset, stars_map = actors_mean_sum_encoding(Trainset, method='sum', benchmark='gross')
Trainset, stars_list = select_top_k_actors(Trainset)

# Production company
# Trainset, company_map = mean_sum_encoding(Trainset, 'production_company', method='mean')
Trainset, company_list = select_top_k(Trainset, 'production_company', existed=True)

# Save training set
Trainset.fillna(0, inplace=True)
Trainset.to_csv("trainset.csv", encoding='utf-8-sig')

"""
Process testing set
"""
# Director
# Testset.loc[:, 'director'] = Testset['director'].map(director_map)
Testset.loc[:, 'director'] = Testset['director'].map(lambda x: 1 if x in director_list else 0)

# Production company
# Testset.loc[:, 'production_company'] = Testset['production_company'].map(company_map)
Testset.loc[:, 'production_company'] = Testset['production_company'].map(lambda x: 1 if x in company_list else 0)

# Actors
# Testset = calculate_stars_value(Testset, stars_map)
for i in range(30):
    Testset.loc[:, 'stars_' + str(i)] = Testset['stars'].map(lambda x: 1 if stars_list[i] in x else 0)
Testset.loc[:, 'stars'] = Testset['stars'].map(lambda x: len(set(x).intersection(set(stars_list))))

# Save testing set
Testset.fillna(0, inplace=True)
Testset.to_csv('testset.csv', encoding='utf-8-sig')
