import pandas as pd
import numpy as np
import scipy.stats as stats
import os

datalist = ['EA', 'EL', 'PI', 'PR', 'PG', 'TH', 'AX', 'AY', 'AZ', 'GX', 'GY', 'GZ', 'MX', 'MY', 'MZ', 'SA', 'SR', 'SF', 'HR', 'BI']
# No ER, T0, H0

cwd = os.getcwd()

for i in range (2, 8):
    name = cwd + '\\' + str(i).zfill(3) + '.csv'
    ddf = pd.read_csv(name)
    df = pd.DataFrame(data={})
    qrange = [0]
    qcolumn = list(ddf['Question'])
    questions = [qcolumn[0]]
    count = 0
    while count < len(qcolumn) - 1:
        while (count < len(qcolumn) - 1) and (qcolumn[count] == qcolumn[count+1]) :
            count+=1
        if count < len(qcolumn) - 1:
            count+=1
            qrange.append(count)
            questions.append(qcolumn[count])
    qrange.append(len(qcolumn))

    pairlist = []
    for l in range(0, len(questions)):
        for m in range(l + 1, len(questions)):
            if questions[l] != 0 and questions[m] != 0:
                pairlist.append(str(questions[l]) + '_' + str(questions[m]))

    df['QuestionsPair'] = pairlist

    for dataname in datalist:
        datacolumn = list(ddf[dataname])
        trimmeddata = []
        tresult = []

        for j in range(0, len(qrange) - 1):
            trimmedlist = np.array([])
            for k in range(qrange[j], qrange[j + 1]):
                if datacolumn[k] != 0:
                    trimmedlist = np.append(trimmedlist, datacolumn[k])
            trimmeddata.append(trimmedlist)
        
        for l in range(0, len(questions)):
            for m in range(l + 1, len(questions)):
                if questions[l] != 0 and questions[m] != 0:
                    tresult.append(stats.ttest_ind(a=trimmeddata[l], b=trimmeddata[m], equal_var=True))
        df[dataname] = tresult

    df.to_csv('ttest' + str(i).zfill(3) + '.csv', encoding='utf-8', index=False)