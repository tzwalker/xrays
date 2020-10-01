"""
coding: utf-8

tzwalker
Mon Sep 21 16:21:52 2020


First Solar cross sections FS2_1, FS2_2 measured 2019_03_2IDD
degradation and bias measurements

the program has two cells: one for FS2_1 and one for FS2_2

this program calculates the average and standard deviation over
5 rows of a scan, and saves the reduced output

it also reduces the rows in the timescan data; MAPS saves timescan
data with repeat rows. there are 3, identical rows for each
data point. these are reduced to one row, and saved as reduced output

all of these measurements were a type of line scan
    for statistics, flyscan repeated 5 times in the same position
    the average and std. dev. of 5 rows needs to be calculated and saved
the electrical settings are not saved in a separate csv file
    the conversion from cts to ampere will be done in Origin
only the before and after line scans are dealt with here
    the timeseries scans have rows that are copies of one another;
    these will be reduced in Origin
"""

import pandas as pd
import numpy as np

### FS2_2

# reduce linescan data (create statistical data points)
ASCII_PATH =  r'C:\Users\triton\decay_data\FS2_2_2019_03_2IDD\degradation\output' 
OUT_PATH = r'C:\Users\triton\decay_data\FS2_2_2019_03_2IDD\degradation\ASCII_reduced'

# reduce linescan data (create statistical data points)
# degradation before and after line scans
SCANS = [662,664,665,667,669,671,674,676]

for scan in SCANS:
    scan_str = str(scan)
    file_string = r'\combined_ASCII_2idd_0{s}.h5.csv'.format(s=scan_str)
    file = ASCII_PATH + file_string
    # import ascii as dataframe
    data = pd.read_csv(file, skiprows=1)
    
    # average over every 5th row
    # https://stackoverflow.com/questions/36810595/calculate-average-of-every-x-rows-in-a-table-and-create-new-table
    avgs = data.groupby(np.arange(len(data))//5).mean()
    # standard deviation over every 5th row
    stds = data.groupby(np.arange(len(data))//5).std()
    
    # combine row-by-row averages and standard deviation...
    master= pd.DataFrame()
    for col1,col2 in zip(avgs,stds):
        # get column from the avgs df and std. dev. df
        c1 = avgs[col1]
        c2 = stds[col2]
        # concatenate the columns
        result = pd.concat([c1,c2], axis=1)
        #re-assign standard deviation column to prevent identical df keys
        std_key = col2+" std"
        result.columns = [*result.columns[:-1], std_key]
        # append corresponding columns to master df
        master[col1] = result[col1]
        master[std_key] = result[std_key]
    
    # save master df as csv
    out_file = OUT_PATH+file_string
    master.to_csv(out_file, sep=',')
    
# reduce timescan data (remove redundant rows)
SCANS_time = [663,666,670,675]
for scan in SCANS_time:
    scan_str = str(scan)
    file_string = r'\combined_ASCII_2idd_0{s}.h5.csv'.format(s=scan_str)
    file = ASCII_PATH + file_string
    # import ascii as dataframe
    data = pd.read_csv(file, skiprows=1)
    # select every 3rd row from dataframe
    data_red = data[data.index % 3 == 0]
    out_file = OUT_PATH+file_string
    data_red.to_csv(out_file, sep=',')


#%%
import pandas as pd
import numpy as np

### FS2_1

ASCII_PATH =  r'C:\Users\triton\decay_data\FS2_1_2019_03_2IDD\degradation\output' 
OUT_PATH = r'C:\Users\triton\decay_data\FS2_1_2019_03_2IDD\degradation\ASCII_reduced'

# reduce linescan data (create statistical data points)
# degradation before and after line scans
SCANS = [625, 627, 628, 630, 631, 633, 634, 636]

for scan in SCANS:
    scan_str = str(scan)
    file_string = r'\combined_ASCII_2idd_0{s}.h5.csv'.format(s=scan_str)
    file = ASCII_PATH + file_string
    # import ascii as dataframe
    data = pd.read_csv(file, skiprows=1)
    
    # average over every 5th row
    # https://stackoverflow.com/questions/36810595/calculate-average-of-every-x-rows-in-a-table-and-create-new-table
    avgs = data.groupby(np.arange(len(data))//5).mean()
    # standard deviation over every 5th row
    stds = data.groupby(np.arange(len(data))//5).std()
    
    # combine row-by-row averages and standard deviation...
    master= pd.DataFrame()
    for col1,col2 in zip(avgs,stds):
        # get column from the avgs df and std. dev. df
        c1 = avgs[col1]
        c2 = stds[col2]
        # concatenate the columns
        result = pd.concat([c1,c2], axis=1)
        #re-assign standard deviation column to prevent identical df keys
        std_key = col2+" std"
        result.columns = [*result.columns[:-1], std_key]
        # append corresponding columns to master df
        master[col1] = result[col1]
        master[std_key] = result[std_key]
    
    # save master df as csv
    out_file = OUT_PATH+file_string
    master.to_csv(out_file, sep=',')

# reduce timescan data (remove redundant rows)
SCANS_time = [626,629,632,635]
for scan in SCANS_time:
    scan_str = str(scan)
    file_string = r'\combined_ASCII_2idd_0{s}.h5.csv'.format(s=scan_str)
    file = ASCII_PATH + file_string
    # import ascii as dataframe
    data = pd.read_csv(file, skiprows=1)
    # select every 3rd row from dataframe
    data_red = data[data.index % 3 == 0]
    out_file = OUT_PATH+file_string
    data_red.to_csv(out_file, sep=',')
