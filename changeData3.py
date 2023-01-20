import pandas as pd
import os
import math
import scipy.stats as stats

measureddatalist = ['EA', 'EL', 'PI', 'PR', 'PG', 'TH', 'AX', 'AY', 'AZ', 'GX', 'GY', 'GZ', 'MX', 'MY', 'MZ', 'SA', 'SR', 'SF', 'HR', 'BI']
eyedata = ['left eye 1', 'left eye 2', 'right eye 1', 'right eye 2']
accuracydata = ['Accuracy of AI response', 'Image authentic?']

subjectslist = [1, 2, 3, 4, 5, 6, 7]
# subjectslist = [7, 9]

cwd = os.getcwd()

for i in subjectslist:
    print(str(i).zfill(3))
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
    # df = df.apply(stats.zscore)
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
    # df['response'] = response
    df2['response'] = binary
    # print(df)
    print(df2)
    # df.to_csv('lineardata4_' + str(i).zfill(3) + '.csv', encoding='utf-8', index=False)
    df2.to_csv('classificationdata4_' + str(i).zfill(3) + '.csv', encoding='utf-8', index=False)
    
