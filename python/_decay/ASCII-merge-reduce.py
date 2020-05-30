# -*- coding: utf-8 -*-
"""
Trumann
Fri Apr 10 16:21:17 2020

this program is meant to consolidate the ASCIIs relating
to the degradation study 2018_11_26IDC TS118_1A

the mda ASCIIs have the electrical data
    lockin XBIC and direct XBIC
the h5 ASCIIs have the XRF data and a copy of the lockin XBIC scaler

this program merges the lockin and direct XBIC data together with
the XRF data 

the csv headers containing XBIC data retain the scaler definitons 
seen in the mda file (e.g. "26idc:3820:scaler1_cts2.B")
lockin XBIC --> 26idc:3820:scaler1_cts2.B
direct XBIC --> 26idc:3820:scaler1_cts2.C
unsure what 26idc:3820:scaler1_cts2.D was, but it may be related to
the XBIC measurements, so this scaler was kept

note on filenames and different operations
combined_ASCII_26idbSOFT_00{s}.h5.csv used for double-digit scans
cross-section regular maps
    these were regular 2D maps of the cross-section
    insert index: i=5
    TS1181Ascans= [39,43,46,51]
combined_ASCII_26idbSOFT_0{s}.h5.csv used for triple-digit scans
plan view part 2
    timeseries and linescans from plan-view part 2
    different h5 ascii column headers, e.g. ' ds_ic' vs. 'ds_ic'
    insert index: i=5
    repeat rows for timeseries and linescan exports
    take every 3rd row
    TS1181Ascans= list(range(204,215)) + [218] + list(range(220,230))
cross-section degradation
    these h5 files do not have a ds_ic
    for this merge, 
        comment out drop columns for h5 ascii
        df_merged = 'df_h5' for df_merge
    TS1181Ascans = list(range(277,310))
note altered Sample class for TS118A_1A to be compatible with the output
from this program
"""


import pandas as pd

SYS_PATH = r'C:\Users\triton\decay_data\csv_separate'
OUT_PATH = r'C:\Users\triton\decay_data\csv_combined'
TS1181Ascans= [275,276]

for SCANNUM in TS1181Ascans:
    H5_fname = r'\combined_ASCII_26idbSOFT_0{s}.h5.csv'.format(s=SCANNUM)
    MDA_fname = r'\combined_ASCII_26idbSOFT_0{s}.mda.csv'.format(s=SCANNUM)
    # import the scan data from the two locations
    df_h5 = pd.read_csv(SYS_PATH + H5_fname, skiprows=1)
    df_mda = pd.read_csv(SYS_PATH + MDA_fname, skiprows=1)
    
    # delete repetitive data
    #drop_columns = ['ds_ic']
    #df_h51 = df_h5.drop(columns=drop_columns)
    
    drop_columns = ['x pixel no', ' y pixel no', ' x position', ' y position']
    df_mda1 = df_mda.drop(columns=drop_columns)
    
    # merge dataframes startring with 
    i = 5
    df_merged = pd.concat([df_h5.iloc[:, :i], df_mda1, df_h5.iloc[:, i:]], axis=1)
    
    # take every 3rd row; only use for linescans and timeseries!
    df_merged1 = df_merged[::3]
    
    OUT_PATH = r'C:\Users\triton\decay_data\csv_combined'
    MERGED_fname = r'\combined_ASCII_26idbSOFT_0{s}.h5.csv'.format(s=SCANNUM)
    fname1 = OUT_PATH + MERGED_fname
    df_merged1.to_csv(fname1)

