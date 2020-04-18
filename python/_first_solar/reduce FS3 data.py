"""
coding: utf-8

tzwalker
Sat Apr 18 09:55:28 2020

this is reduce the ASCII of in TW_BL to the channels of interest
meanth to save degbugging time as the it takes
a while to load +10MB files into python (22 times)
"""


import pandas as pd
ASCII_PATH = r'C:\Users\triton\FS3_2019_06_operando\ASCIIS_TW_BL'
RED_ASCII_PATH = r'C:\Users\triton\FS3_2019_06_operando\ASCII_TW_BL_reduced'

scans = [321,322,323,324,325,326,327,328,329,330,331,332,333,
             337,338,339,340,341,342,343, 344, 345]

channels = ['x pixel no', 'y pixel no', 'x_coord', 'y_coord',
            'us_ic', 'Se', 'Cd_L', 'Te_L', 'Au_L', 'US_IC']

def reduce_maps(scans, path_ascii_in, channels, path_ascii_out):
    for scan in scans:
        scan_str = str(scan)
        fname = '/combined_ASCII_2idd_0'+scan_str+'.h5.csv'
        # define ascii of scan
        file = path_ascii_in + fname
        # import ascii as dataframe
        data = pd.read_csv(file, usecols=channels)
        file_out = path_ascii_out + fname
        data.to_csv(file_out)
    return

reduce_maps(scans, ASCII_PATH, channels, RED_ASCII_PATH)