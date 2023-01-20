import os
import pandas as pd
import matplotlib.pyplot as plt

datalist = ['EA', 'EL', 'PI', 'PR', 'PG', 'TH', 'AX', 'AY', 'AZ', 'GX', 'GY', 'GZ', 'MX', 'MY', 'MZ', 'SA', 'SR', 'SF', 'HR', 'BI']
# No ER, T0, H0

subjectslist = [2, 3, 4, 5, 6, 7, 9]
# subjectslist = [2, 4, 9]

cwd = os.getcwd()

def addlabels(y, x):
    for i in range(len(y)):
        plt.text(i, x[i], x[i], ha = 'center')

for i in subjectslist:
    name = cwd + '\\mean' + str(i).zfill(3) + '.csv'
    data = pd.read_csv(name)
    df = pd.DataFrame(data)

    y = df['Question'].map(str)
    

    for j in range(0, len(y)):
        while y[0:j].eq(y[j]).any():
            y[j] = y[j] + '*'

    for dataname in datalist:
        x = df[dataname]
        fig = plt.figure(figsize =(10, 10))

        plt.bar(y, x)
        addlabels(y, x)
        plt.xlabel('Types of Questions')
        plt.ylabel(dataname)
        plt.title(dataname + ' measurements of each type of questions of subject ' + str(i).zfill(3))

        plt.savefig(os.path.join(cwd + '\IMG', str(i).zfill(3) + dataname + ".jpg"))

        plt.close()