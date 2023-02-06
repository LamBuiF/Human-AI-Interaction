import pandas as pd
import numpy as np
# import scipy.stats as stats
import os
import matplotlib.pyplot as plt

measureddatalist = ['EA', 'EL', 'PI', 'PR', 'PG', 'TH', 'AX', 'AY', 'AZ', 'GX', 'GY', 'GZ', 'MX', 'MY', 'MZ', 'SA', 'SR', 'SF', 'HR', 'BI', 'left eye 1', 'left eye 2', 'right eye 1', 'right eye 2']
# measureddatalist = ['left eye 1', 'left eye 2', 'right eye 1', 'right eye 2']
# measureddatalist = ['EA']
# No ER, T0, H0

subjectslist = [1, 2, 3, 4, 5, 6, 7]
# subjectslist = [3]

cwd = os.getcwd()

for i in subjectslist:
    name = cwd + '\\qmeanCE' + str(i).zfill(3) + '.csv'
    ddf = pd.read_csv(name)
    df = pd.DataFrame(data={})
    qrange = [0]
    qcolumn = list(ddf['Question Type'])
    count = 0
    qlistdupe = [qcolumn[0]]
    qlist = [qcolumn[0]]
    for q in qcolumn:
        if q not in qlist:
            qlist.append(q)
    while count < len(qcolumn) - 1:
        while (count < len(qcolumn) - 1) and (qcolumn[count] == qcolumn[count+1]) :
            count+=1
        if count < len(qcolumn) - 1:
            count+=1
            qrange.append(count)
            qlistdupe.append(qcolumn[count])
    qrange.append(len(qcolumn))

    for dataname in measureddatalist:

        datacolumn = list(ddf[dataname])
        trimmeddata = []
        tresult = []

        for j in range(0, len(qrange) - 1):
            if qlistdupe[j] not in qlistdupe[0:j]:
                trimmedlist = np.array([])
                for k in range(qrange[j], qrange[j + 1]):
                    if datacolumn[k] != 0:
                        trimmedlist = np.append(trimmedlist, datacolumn[k])
                trimmeddata.append(trimmedlist)
            else:
                pos = qlistdupe.index(qlistdupe[j], 0, j)
                trimmedlist = trimmeddata[pos]
                for k in range(qrange[j], qrange[j + 1]):
                    if datacolumn[k] != 0:
                        trimmedlist = np.append(trimmedlist, datacolumn[k])
                trimmeddata[pos] = trimmedlist
            
        fig = plt.figure(figsize = (10, 7))
        ax = fig.add_subplot(111)
        bp = ax.boxplot(trimmeddata, patch_artist = True, notch ='True', vert = 1)
        ax.set_xticklabels(qlist)
        ax.set_xlabel('Question Type')
        ax.set_ylabel(dataname)
        # plt.show()
        plt.title('Box plot for ' + dataname + ' measurements of each type of question of subject ' + str(i).zfill(3))

        plt.savefig(os.path.join(cwd + '\IMGFinal', 'boxplot' + str(i).zfill(3) + dataname.replace(' ', '_') + ".jpg"))
        plt.close()