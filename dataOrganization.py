from asyncio.windows_events import NULL
import pandas as pd
import glob
import os
from datetime import datetime
import time as tm

measureddatalist = ['EA', 'EL', 'PI', 'PR', 'PG', 'TH', 'AX', 'AY', 'AZ', 'GX', 'GY', 'GZ', 'MX', 'MY', 'MZ', 'SA', 'SR', 'SF', 'HR', 'BI']
# No ER, T0, H0

qtypes = ['feature', 'converstational', 'text', 'image']
qchoice = ['no', 'yes']

v4 = [0, 1, 2, 3, 2, 1, 0, 3]
v4c = [1, 1, 1, 1, 0, 0, 0, 0]
v3 = [2, 1, 0, 3, 0, 1, 2, 3]
v3c = [0, 0, 0, 0, 1, 1, 1, 1]
v2 = [0, 2, 1, 3, 2, 0, 3, 1]
v2c = [0, 0, 0, 0, 1, 1, 1, 1]
v1 = [1, 2, 3, 0, 1, 0, 3, 2]
v1c = [0, 0, 0, 0, 1, 1, 1, 1]

subjectsV = [1, 1, 2, 4, 4, 4, 3, 3, 3, 3]

subjectslist = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# subjectslist = [8]

cwd = os.getcwd()
    
for i in subjectslist:

    print('subject00' + str(i)  )

    swd = cwd + '\Data\subject' + str(i).zfill(3)

    df = pd.DataFrame(data={})

    for name in glob.glob(swd + '\\fNIRSdata\*\*.tri'):
        f = open(name, 'r')
        tridatatime = []
        tridataquestions = []
        tridatamark = []
        prevmark = 0
        for line in f:
            splitted = line.split(';')
            mark = int(splitted[1])
            if (abs(mark - prevmark) > 1):
                prevmark = mark
                dt = datetime.strptime(splitted[0], '%Y-%m-%dT%H:%M:%S.%f')
                unixtime = tm.mktime(dt.timetuple())
                tridatatime.append(unixtime)
                tridataquestions.append(int(splitted[2][0]))
                tridatamark.append(mark)

        tridataquestions.pop()

        if subjectsV[i - 1] == 1:
            v = v1
            vc = v1c
        elif subjectsV[i - 1] == 2:
            v = v2
            vc = v2c
        elif subjectsV[i - 1] == 3:
            v = v3
            vc = v3c
        else:
            v = v4
            vc = v4c

        tridataqtypes = []
        tridatachoices = []

        for num in tridataquestions:
            tridataqtypes.append(qtypes[v[num - 1]])
            tridatachoices.append(qchoice[vc[num - 1]])

        df['Question Number'] = tridataquestions
        df['Question Type'] = tridataqtypes
        df['Choice'] = tridatachoices

    eyename = swd + '\eyetrackerdata.xlsx'
    edf = pd.read_excel(eyename).replace([float('nan'), ' nan'], 0)

    eyetime = list(edf[edf.columns[4]])
    unixeyetime = []
    for t in eyetime:
        # et = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%f')
        eunixtime = tm.mktime(t.timetuple())
        unixeyetime.append(eunixtime)

    eyelist = list(edf)

    eyelist.pop()   

    for cname in eyelist:
        poslist = list(edf[cname])
        datacolumn = []
        dataindex = 0
        triindex = 0
        while dataindex < len(unixeyetime) and unixeyetime[dataindex] < tridatatime[triindex]:
            dataindex += 1
        
        while triindex < len(tridatatime) - 1:
            sum = 0
            count = 0
            while dataindex < len(unixeyetime) and unixeyetime[dataindex] < tridatatime[triindex + 1]:
                if (poslist[dataindex] != 0):
                    sum += poslist[dataindex]
                    count += 1
                dataindex += 1
            if count != 0:
                datacolumn.append(sum / count)
            else:
                datacolumn.append(NULL)
            triindex += 1
        df[cname] = datacolumn

    for dataname in measureddatalist:
        for name in glob.glob(swd + '\emotibitdata\*_' + dataname + '.csv'):
            # print(dataname)
            tdf = pd.read_csv(name)
            datalist = list(tdf[tdf.columns[-1]])
            datatime = list(tdf['LocalTimestamp'])
            datacolumn = []
            dataindex = 0
            triindex = 0
            while dataindex < len(datatime) and datatime[dataindex] < tridatatime[triindex]:
                dataindex += 1
            
            while triindex < len(tridatatime) - 1:
                sum = 0
                count = 0
                while dataindex < len(datatime) and datatime[dataindex] < tridatatime[triindex + 1]:
                    if (datalist[dataindex] != 0):
                        sum += datalist[dataindex]
                        count += 1
                    dataindex += 1
                if count != 0:
                    datacolumn.append(sum / count)
                else:
                    datacolumn.append(NULL)
                triindex += 1

            df[dataname] = datacolumn
    
    df.to_csv('qmeanCE' + str(i).zfill(3) + '.csv', encoding='utf-8', index=False)