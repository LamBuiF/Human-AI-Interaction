import pandas as pd
from sklearn import linear_model
import os

testdatalist = ['EA', 'EL', 'PI', 'PR', 'PG', 'TH', 'AX', 'AY', 'AZ', 'GX', 'GY', 'GZ', 'MX', 'MY', 'MZ', 'SA', 'SR', 'SF', 'HR', 'BI', 'left eye 1', 'left eye 2', 'right eye 1', 'right eye 2']

subjectslist = [1, 2, 3, 4, 5, 6, 7]
test = 7

cwd = os.getcwd()

df = pd.DataFrame(data={})

for i in subjectslist:
    name = cwd + '\\lineardata' + str(i).zfill(3) + '.csv'
    ddf = pd.read_csv(name)
    df = pd.concat([df, ddf])

X = df[testdatalist]
y = df['response']

regr = linear_model.LinearRegression()
regr.fit(X, y)

testname = cwd + '\\lineardata' + str(test).zfill(3) + '.csv'
tdf = pd.read_csv(testname)

odf = pd.DataFrame(data={})
odf['response'] = list(tdf['response'])

tdf.drop('response', inplace=True, axis=1)
tlist = tdf.values.tolist()
predictedresponse = regr.predict(tlist)

odf['predicted response'] = predictedresponse

odf.to_csv('linearRegression.csv', encoding='utf-8', index=False)