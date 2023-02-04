import pandas as pd
import os
import statistics

subjectslist = [1, 2, 3, 4, 5, 6, 7]

cwd = os.getcwd()

fdf = pd.DataFrame(data={})

mean1 = []
mean2 = []
mean3 = []
mean4 = []

aucmean1 = []
aucmean2 = []
aucmean3 = []
aucmean4 = []

for i in subjectslist:
    name = cwd + '\\classfication4.1_' + str(i).zfill(3) + '.csv'
    df = pd.read_csv(name)

    aname = cwd + '\\classficationAllbut_' + str(i).zfill(3) + '.csv'
    adf = pd.read_csv(aname)

    rname = cwd + '\\classfication4.3_' + str(i).zfill(3) + '.csv'
    rdf = pd.read_csv(rname)

    hname = cwd + '\\classification4.4_' + str(i).zfill(3) + '.csv'
    hdf = pd.read_csv(hname)
    
    tdf = pd.DataFrame(data={})

    accuracy = [df.iloc[0, 0], adf.iloc[0, 0], rdf.iloc[0, 0], hdf.iloc[0, 0]]
    auc = [df.iloc[0, 3], adf.iloc[0, 3], rdf.iloc[0, 3], hdf.iloc[0, 3]]

    mean1.append(df.iloc[0, 0])
    mean2.append(adf.iloc[0, 0])
    mean3.append(rdf.iloc[0, 0])
    mean4.append(hdf.iloc[0, 0])
    aucmean1.append(df.iloc[0, 3])
    aucmean2.append(adf.iloc[0, 3])
    aucmean3.append(rdf.iloc[0, 3])
    aucmean4.append(hdf.iloc[0, 3])

    tdf['File'] = ['subject' + str(i).zfill(3), 'Every subject but subject' + str(i).zfill(3), 'subject' + str(i).zfill(3) + '(all measurements)', 'subject' + str(i).zfill(3) + '(all measurements high Conf)']
    tdf['Accuracy'] = accuracy
    tdf['AUC'] = auc

    fdf = pd.concat([fdf, tdf])

mdf = pd.DataFrame(data={})
mdf['File'] = ['Mean all subjects', 'Mean every subject but 1 subject', 'Mean all subjects (all measurements)', 'Mean all subjects (all measurements high Conf)']

accuracy2 = [sum(mean1)/len(mean1), sum(mean2)/len(mean2), sum(mean3)/len(mean3), sum(mean4)/len(mean4)]
auc2 = [sum(aucmean1)/len(aucmean1), sum(aucmean2)/len(aucmean2), sum(aucmean3)/len(aucmean3), sum(aucmean4)/len(aucmean4)]

mdf['Accuracy'] = accuracy2
mdf['AUC'] = auc2

fdf = pd.concat([fdf, mdf])

ddf = pd.DataFrame(data={})
ddf['File'] = ['Standard deviation all subjects', 'Standard Deviation every subject but 1 subject', 'Standard Deviation all subjects (all measurements)', 'Standard Deviation all subjects (all measurements high Conf)']

accuracy3 = [statistics.pstdev(mean1), statistics.pstdev(mean2), statistics.pstdev(mean3), statistics.pstdev(mean4)]
auc3 = [statistics.pstdev(aucmean1), statistics.pstdev(aucmean2), statistics.pstdev(aucmean3), statistics.pstdev(aucmean4)]

ddf['Accuracy'] = accuracy3
ddf['AUC'] = auc3

fdf = pd.concat([fdf, ddf])

fdf.to_csv('result(LogRes&AUC).csv', encoding='utf-8', index=False)