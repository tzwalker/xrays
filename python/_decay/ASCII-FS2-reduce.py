"""
coding: utf-8

tzwalker
Mon Sep 21 16:21:52 2020


First Solar cross sections FS2_1, FS2_2 measured 2019_03_2IDD
degradation and bias measurements

this program is meant to reduce the csv for plotting and analysis in Origin

all of these measurements were a type of line scan
    for statistics, flyscan repeated 3-4 times in the same position
    the average of 3-4 rows needs to be calculated and saved
the electrical settings are not saved in a separate csv file
    the conversion from cts to ampere will be done in Origin
only the before and after line scans are dealt with here
    the timeseries scans have rows that are copies of one another;
    these will be reduced in Origin

the program wil have two cells: one for FS2_1 and one for FS2_2
"""
import pandas as pd
import numpy as np

### FS2_2

ASCII_PATH =  r'C:\Users\triton\decay_data\FS2_2_2019_03_2IDD\degradation\output' 
OUT_PATH = r'C:\Users\triton\decay_data\FS2_2_2019_03_2IDD\degradation\ASCII_reduced'
# degradation before and after line scans
SCANS = [662,664,665,667,669,671,674,676]

#for scan in SCANS:
scan_str = str(SCANS[0])
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
# zip iterate over columns in avgs and stds
    # concantenate each pair of columns
    # save as reduced csv

#out_file = OUT_PATH+file_string
#avgs.to_csv(out_file, sep=',')

