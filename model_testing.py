"""
Model testing
"""

from sklearn.externals import joblib
import pandas as pd
from sklearn.metrics import r2_score
import xgboost as xgb
import matplotlib.pyplot as plt

model = joblib.load('model.pkl')
testset = pd.read_csv('data/testset.csv', index_col=0)
print(testset.head(5))

header = list(testset)
y_test = testset['gross']

header.remove('gross')
header.remove('metascore')
header.remove('imdb')
header.remove('vote')

X_test = testset.loc[:, header[1:]]

prediction = model.predict(X_test)
result = pd.DataFrame({'movie': testset['movie'], 'label': y_test, 'prediction': [max(0, x) for x in prediction]})
r2 = r2_score(y_test, prediction)
result.to_csv('data/prediction.csv', encoding='utf-8-sig')

print('r2_score: {}'.format(r2))

xgb.plot_importance(model, max_num_features=15)
plt.show()
