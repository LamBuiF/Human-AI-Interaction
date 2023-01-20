from asyncio.windows_events import NULL
import pandas as pd
import glob
import os
from datetime import datetime
import time as tm

# current working directory
cwd = os.getcwd()

# iterate through all the files, in this case 2 to 9 since 0 and 1 does not have the required files
for i in range (8, 9):

    # get path to each subject working directory
    swd = cwd + '\Data\subject' + str(i).zfill(3)

    # create main dataframe
    df = pd.DataFrame(data={})

    # create rows for main dataframe based on the file with the most row, which is AX (previously tested, written as such for less processing)
    for name in glob.glob(swd + '\emotibitdata\*_AX.csv'):
        tdf = pd.read_csv(name)
        # get the LocalTimestamp column as main column for the main dataframe
        df = tdf[['LocalTimestamp']].copy()
        df.astype('double').dtypes
    timelist = list(df['LocalTimestamp'])

    # get data in tri file, in this case there is only 1 tri file, but method runs for any number of tri file
    for name in glob.glob(swd + '\\fNIRSdata\*\*.tri'):
        f = open(name, 'r')
        # get the two lists of times and data of the tri file
        tridatatime = []
        tridataquestions = []
        for line in f:
            splitted = line.split(';')
            dt = datetime.strptime(splitted[0], '%Y-%m-%dT%H:%M:%S.%f')
            unixtime = tm.mktime(dt.timetuple())
            tridatatime.append(unixtime)
            tridataquestions.append(splitted[2][0])

        # create column to add to dataframe
        tridatacolumn = []

        # create pointer to iterate through the tri file's lists
        triindex = 0

        # go through the main LocalTimestamp time to add data in the tri file based on time using an index interating through the tri file's times and data lists
        for time in timelist:
            while triindex < len(tridatatime) and tridatatime[triindex] <= time:
                triindex += 1
            if triindex >= len(tridatatime):
                break
            tridatacolumn.append(tridataquestions[triindex])

        # fill the rest of the data column to match length
        curquestion = tridatacolumn[-1]
        while len(tridatacolumn) < len(timelist):
            tridatacolumn.append(curquestion)

        # add the newly created column to the main dataframe
        df['Question'] = tridatacolumn

    # iterate through all the data files end with _ and two letters before .csv
    for name in glob.glob(swd + '\emotibitdata\*_??.csv'):

        tdf = pd.read_csv(name)
        columnname = tdf.columns[-1]

        # get the two lists of times and data of the data file
        datalist = list(tdf[tdf.columns[-1]])
        
        datatime = list(tdf['LocalTimestamp'])

        # create column to add to dataframe
        datacolumn = []

        # create pointer to iterate through the data file's lists
        index = 0

        # go through the main LocalTimestamp time to add data in the data file based on time using an index interating through the data file's times and data lists
        for time in timelist:
            if index >= len(datatime):
                break
            if datatime[index] <= time:
                datacolumn.append(datalist[index])
                index += 1
            else:
                datacolumn.append(NULL)

        # fill the rest with NULL to match the length
        while len(datacolumn) < len(timelist):
            datacolumn.append(NULL)
        
        # add data column to main dataframe
        df[columnname] = datacolumn

    # write main dataframe to file
    # all the NULL value will be written as 0, so ignores any 0 value in the real file
    df.to_csv(str(i).zfill(3) + '.csv', encoding='utf-8', index=False)