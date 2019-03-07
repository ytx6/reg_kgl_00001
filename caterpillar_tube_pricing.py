"""
Beating the Benchmark 
Caterpillar @ Kaggle

__author__ : Abhishek

"""

import pandas as pd
import numpy as np
from sklearn import ensemble, preprocessing

# load training and test datasets
train = pd.read_csv('data/train_set.csv', parse_dates=[2,])
test = pd.read_csv('data/test_set.csv', parse_dates=[3,])

# create some new features
train['year'] = train.quote_date.dt.year
train['month'] = train.quote_date.dt.month
train['dayofyear'] = train.quote_date.dt.dayofyear
train['dayofweek'] = train.quote_date.dt.dayofweek
train['day'] = train.quote_date.dt.day

test['year'] = test.quote_date.dt.year
test['month'] = test.quote_date.dt.month
test['dayofyear'] = test.quote_date.dt.dayofyear
test['dayofweek'] = test.quote_date.dt.dayofweek
test['day'] = test.quote_date.dt.day


# drop useless columns and create labels
test = test.drop(['id', 'quote_date'], axis = 1)
labels = train.cost.values
train = train.drop(['quote_date', 'cost'], axis = 1)


# convert data to numpy array
train = np.array(train)
test = np.array(test)
print(train.shape, test.shape)

# label encode the categorical variables
for i in range(train.shape[1]):
    if i in [0,1,4]:
        lbl = preprocessing.LabelEncoder()
        lbl.fit(list(train[:,i]) + list(test[:,i]))
        train[:,i] = lbl.transform(train[:,i])
        test[:,i] = lbl.transform(test[:,i])


# object array to float
train = train.astype(float)
test = test.astype(float)

# i like to train on log(1+x) for RMSLE ;) 
# The choice is yours :)
label_log = np.log1p(labels)

# fit a random forest model
clf = ensemble.RandomForestRegressor(n_jobs=-1, n_estimators=1000, random_state=42)
clf.fit(train, label_log)

# get predictions from the model, convert them and dump them!
preds = np.expm1(clf.predict(test))
sample = pd.read_csv('data/sample_submission.csv')
sample['cost'] = preds
sample.to_csv('benchmark.csv', index=False)

# Swipe right on tinder ;)
