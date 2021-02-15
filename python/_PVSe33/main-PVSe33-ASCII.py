# -*- coding: utf-8 -*-
"""
Trumann
Thu Oct 29 12:16:48 2020

this is a hard-code program meant to extract and shape 
the data arrays in a combined_ASCII file generated by the MAPS software

once the array is isolated in "Map",
it is converted from a pandas object to a numpy object
    this makes computation more convenient

to plot a pretty map
insert the variable name "Map_arr" in "plot_master.py" 

2020_10_26IDC
scan0011 --> PVSe33.3_4 (not stressed)
scan0148 --> PVSe33.4_3 (stressed)
"""

import pandas as pd

PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\nanoXRF_XBIC\fit1_ASCII'
FILE = r'\combined_ASCII_26idbSOFT_0148.h5.csv'

DATA = PATH+FILE

data = pd.read_csv(DATA, skiprows=1)

def remove_column_header_spaces(df):
    old_colnames = df.columns.values
    new_colnames = []
    for name in old_colnames:
        new_colnames.append(name.strip())
    col_names = {i:j for i,j in zip(old_colnames,new_colnames)}
    df.rename(columns = col_names, inplace=True)
    return df

data = remove_column_header_spaces(data)

Map = data.pivot(index='y pixel no', columns='x pixel no', values = "ds_ic")

#%%
Map_arr = Map.to_numpy()

# these are stanford settings
scan011_stanford = 500 #nA/V # PVSe33.3_4
scan148_standford = 10 #nA/V # PVSe33.4_3
V2F_sector26 = 1E5 #cts/V

xbic_nA = Map_arr * scan148_standford / V2F_sector26
