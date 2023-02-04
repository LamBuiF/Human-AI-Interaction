import pandas as pd
from sklearn.model_selection import train_test_split
import os
import numpy as np
# from sklearn import metrics
from sklearn.metrics import roc_auc_score

testdatalist = ['EA', 'EL', 'PI', 'PR', 'PG', 'TH', 'AX', 'AY', 'AZ', 'GX', 'GY', 'GZ', 'MX', 'MY', 'MZ', 'SA', 'SR', 'SF', 'HR', 'BI']
eyesdata = ['left eye 1', 'left eye 2', 'right eye 1', 'right eye 2']
AIresponse = ['Accuracy of AI response']

subjectslist = [1, 2, 3, 4, 5, 6, 7]
# subjectslist = [1]

cwd = os.getcwd()

for i in subjectslist:
    name = cwd + '\\classificationdata3_' + str(i).zfill(3) + '.csv'
    df = pd.read_csv(name)

    X = df[testdatalist]
    y = df['response']

    X_train, X_test, y_train, y_test = train_test_split(X, y , test_size = 0.2, random_state = 0)

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

    accuracy, precision, recall, auc_scores = {}, {}, {}, {}

    for key in models.keys():
        
        # Fit the classifier
        models[key].fit(X_train, y_train)
        
        # Make predictions
        predictions = models[key].predict(X_test)
        
        # Calculate metrics
        accuracy[key] = accuracy_score(predictions, y_test)
        precision[key] = precision_score(predictions, y_test, average='micro')
        recall[key] = recall_score(predictions, y_test, average='micro')

        y = np.array(y_test)
        pred = np.array(predictions)
        auc_scores[key] = roc_auc_score(y, pred)

    df_model = pd.DataFrame(index = models.keys(), columns = ['Accuracy', 'Precision', 'Recall'])
    df_model['Accuracy'] = accuracy.values()
    df_model['Precision'] = precision.values()
    df_model['Recall'] = recall.values()
    df_model['AUC'] = auc_scores.values()

    df_model.to_csv('classification4.4_' + str(i).zfill(3) + '.csv', encoding='utf-8', index=False)