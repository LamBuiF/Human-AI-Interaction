import pandas as pd
import os
import math
import scipy.stats as stats

measureddatalist = ['EA', 'EL', 'PI', 'PR', 'PG', 'TH', 'AX', 'AY', 'AZ', 'GX', 'GY', 'GZ', 'MX', 'MY', 'MZ', 'SA', 'SR', 'SF', 'HR', 'BI']
eyedata = ['left eye 1', 'left eye 2', 'right eye 1', 'right eye 2']
accuracydata = ['Accuracy of AI response', 'Image authentic?']
qtype = ['Question Type']

subjectslist = [1, 2, 3, 4, 5, 6, 7]
# subjectslist = [7, 9]

cwd = os.getcwd()

fdf = pd.DataFrame(data={})
fdf2 = pd.DataFrame(data={})

for i in subjectslist:
    name = cwd + '\\New Data\\qmeanCE' + str(i).zfill(3) + '.csv'
    ddf = pd.read_csv(name)
    delrow = []
    qnum = list(ddf['Question Number'])
    acceptdeny = list(ddf['Accept_Deny_button.response'])
    confidence = list(ddf['Confidence_Slider.response'])
    accuracy = list(ddf['Accuracy of AI response'])
    for j in range(0, len(qnum)):
        if math.isnan(qnum[j]) or math.isnan(acceptdeny[j]) or math.isnan(accuracy[j]):
            delrow.append(j)
    ddf = ddf.drop(delrow)
    # print(ddf)
    df = ddf[measureddatalist].copy()
    df = df.apply(stats.zscore)
    for question in qtype:
        df[question] = ddf[question]
    for dataname in eyedata:
        df[dataname] = ddf[dataname]
    for dataname in accuracydata:
        df[dataname] = ddf[dataname]
    acceptdeny2 = list(ddf['Accept_Deny_button.response'])
    confidence2 = list(ddf['Confidence_Slider.response'])
    df2 = df.copy()
    response = []
    binary = []
    for j in range(0, len(acceptdeny2)):
        if acceptdeny2[j] == 1:
            response.append(confidence2[j])
            binary.append(1)
        else:
            response.append(confidence2[j] * -1)
            binary.append(0)
    df['response'] = response
    df2['response'] = binary
    # print(df)
    # print(df2)
    fdf = pd.concat([fdf, df])
    fdf2 = pd.concat([fdf2, df2])

fdf.to_csv('lineardataZ.csv', encoding='utf-8', index=False)
fdf2.to_csv('classificationdataZ.csv', encoding='utf-8', index=False)
    
