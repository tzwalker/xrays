# -*- coding: utf-8 -*-
"""
Trumann
Fri Apr 10 16:21:17 2020

*note this could be problematic if the same
scaler channel was used to store certain data
    e.g. the XBIC data could be stored under the 'us_ic' key in
    one csv, and the upstream ion chamber data could be stored 
    under the same 'us_ic kay in a different csv;
in my case, the XBIC data were stored under 'us_ic'
    and the us_ic data were stored under 'US_IC';
    these are different strings, and therefore the data for both
    kept in the merged csv; however one may want to remove this
    duplicate operation in the future if one isn't so lucky
	

only the 20C and 80C XBIC data were preserved for XRF maps since these had
the better XRF response

"""

# 2021 11 13
# this directory was created to save ug/cm2 ASCIIs
# C:/Users/triton/FS3_2019_06_operando\BL_fit_202002\output\ug_per_cm2_XRF


import pandas as pd

#SYS_PATH = r'C:\Users\Trumann\Desktop\FS_data\FS3_2019_06_2IDD'
SYS_PATH = r'C:\Users\triton\FS3_2019_06_operando'
XRF_ASCII = SYS_PATH + r'\BL_fit_202002\output'
XBICV_ASCII = SYS_PATH + r'\TW_fit_201907\output'

FS3_scans = [323,339]

for SCANNUM in FS3_scans:
    fname = r'\combined_ASCII_2idd_0{s}.h5.csv'.format(s=SCANNUM)
    # import the scan data from the two locations
    df_eh = pd.read_csv(XBICV_ASCII+fname, skiprows=1)
    df_xrf = pd.read_csv(XRF_ASCII+fname, skiprows=1)
    
    # *remove duplicate column keys to make keys unique, e.g. 'y pixel no'
    df_both = pd.concat([df_eh, df_xrf], axis=1)
    same_columns = df_both.columns.duplicated()
    df_both_trim = df_both.loc[:,~same_columns]
    
    # remove white space from column headers 
    old_cols = df_both_trim.columns.values
    new_cols = [header.strip() for header in old_cols]
    df_both_trim.columns= new_cols
    
    OUT_PATH = r'C:\Users\triton\FS3_2019_06_operando\ASCIIS_TW_BL'
    fname1 = OUT_PATH + fname
    df_both_trim.to_csv(fname1)

