import pandas as pd
import os

datalist = ['EA', 'EL', 'PI', 'PR', 'PG', 'TH', 'AX', 'AY', 'AZ', 'GX', 'GY', 'GZ', 'MX', 'MY', 'MZ', 'SA', 'SR', 'SF', 'HR', 'BI']
# No ER, T0, H0

cwd = os.getcwd()

for i in range (9, 10):
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
    df['Question'] = questions

    for dataname in datalist:
        datacolumn = list(ddf[dataname])
        results = []
        for j in range(0, len(qrange) - 1):
            sum = 0
            count = 0
            for k in range(qrange[j], qrange[j + 1]):
                if datacolumn[k] != 0:
                    sum += datacolumn[k]
                    count += 1
            if count != 0:
                results.append(sum/count)
            else:
                results.append(0)
        df[dataname] = results
    
    df.to_csv('mean' + str(i).zfill(3) + '.csv', encoding='utf-8', index=False)


    