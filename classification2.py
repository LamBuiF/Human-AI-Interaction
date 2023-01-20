import pandas as pd
from sklearn.linear_model import LogisticRegression
import os

testdatalist = ['EA', 'EL', 'PI', 'PR', 'PG', 'TH', 'AX', 'AY', 'AZ', 'GX', 'GY', 'GZ', 'MX', 'MY', 'MZ', 'SA', 'SR', 'SF', 'HR', 'BI', 'left eye 1', 'left eye 2', 'right eye 1', 'right eye 2']

subjectslist = [1, 2, 3, 4, 5, 6]
test = 7

cwd = os.getcwd()

df = pd.DataFrame(data={})

for i in subjectslist:
    name = cwd + '\\classificationdata' + str(i).zfill(3) + '.csv'
    ddf = pd.read_csv(name)
    df = pd.concat([df, ddf])

X_train = df[testdatalist]
y_train = df['response']

testname = cwd + '\\classificationdata' + str(test).zfill(3) + '.csv'
tdf = pd.read_csv(testname)

X_test = tdf[testdatalist]
y_test = tdf['response']

# print(X_train)
# print(X_test)
# print(y_train)
# print(y_test)

from sklearn.preprocessing import StandardScaler

ss_train = StandardScaler()
X_train = ss_train.fit_transform(X_train)

ss_test = StandardScaler()
X_test = ss_test.fit_transform(X_test)

models = {}

# Logistic Regression
from sklearn.linear_model import LogisticRegression
models['Logistic Regression'] = LogisticRegression()

# Support Vector Machines
from sklearn.svm import LinearSVC
models['Support Vector Machines'] = LinearSVC()

# Decision Trees
from sklearn.tree import DecisionTreeClassifier
models['Decision Trees'] = DecisionTreeClassifier()

# Random Forest
from sklearn.ensemble import RandomForestClassifier
models['Random Forest'] = RandomForestClassifier()

# Naive Bayes
from sklearn.naive_bayes import GaussianNB
models['Naive Bayes'] = GaussianNB()

# K-Nearest Neighbors
from sklearn.neighbors import KNeighborsClassifier
models['K-Nearest Neighbor'] = KNeighborsClassifier()

from sklearn.metrics import accuracy_score, precision_score, recall_score

accuracy, precision, recall = {}, {}, {}

for key in models.keys():
    
    # Fit the classifier
    models[key].fit(X_train, y_train)
    
    # Make predictions
    predictions = models[key].predict(X_test)
    
    # Calculate metrics
    accuracy[key] = accuracy_score(predictions, y_test)
    precision[key] = precision_score(predictions, y_test, average='micro')
    recall[key] = recall_score(predictions, y_test, average='micro')

df_model = pd.DataFrame(index = models.keys(), columns = ['Accuracy', 'Precision', 'Recall'])
df_model['Accuracy'] = accuracy.values()
df_model['Precision'] = precision.values()
df_model['Recall'] = recall.values()

df_model.to_csv('classfication3.csv', encoding='utf-8', index=False)