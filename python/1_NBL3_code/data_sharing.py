# -*- coding: utf-8 -*-
"""
Trumann
Fri Oct 11 17:05:06 2019
"""

import pandas as pd
import scipy.io
import numpy as np

def make_matlab_dict(df):
    matlab_dict = {}
    df_data = np.array(df)
    for i,column_name in enumerate(df.columns.values):
        column_data = df_data[:,i]
        matlab_dict[column_name] = column_data
    return matlab_dict


XBIC = [422,423,424, 550, 264,265,266, 475, 385,386,387, 439, 341,342,343, 519]
XBIV = [419,420,421, 551, 261,262,263, 472, 382,383,384, 440, 338,339,340, 517]

import_path = r'C:\Users\triton\Dropbox (ASU)\Internal Reports\Data sharing with Math\Trumann' 
export_path = r'C:\Users\triton\NBL3_mat_files'
#r'C:\Users\Trumann\Desktop\NBL3_data\output'
def csv_to_matlab(scan_list, import_path, export_path):
    csv_names = [(import_path + r'\combined_ASCII_2idd_0' + str(scan) + '.h5.csv') for scan in scan_list]
    dfs_of_asciis = [pd.read_csv(csv_name, skiprows=1) for csv_name in csv_names]
    matdicts_of_asciis = [make_matlab_dict(df) for df in dfs_of_asciis]
    export_file_names = [(export_path + r'\scan_' + csv_name[-11:-7] + '.mat') for csv_name in csv_names]
    for mat_dict, fname in zip(matdicts_of_asciis, export_file_names):
        scipy.io.savemat(fname, mat_dict)
    return

csv_to_matlab(XBIV, import_path, export_path)

# =============================================================================
# XBIC_csv_names = [(path + r'\combined_ASCII_2idd_0' + str(scan) + '.h5.csv') for scan in XBIC]
# XBIV_csv_names = [(path + r'\combined_ASCII_2idd_0' + str(scan) + '.h5.csv') for scan in XBIV]
# 
# 
# dfs_of_asciis = [pd.read_csv(csv_name, skiprows=1) for csv_name in XBIC_csv_names]
# 
# matdicts_of_asciis = [make_matlab_dict(df) for df in dfs_of_asciis]
# 
# export_path = r'C:\Users\triton\NBL3_mat_files'
# export_file_names = [(export_path + r'\scan_' + csv_name[-11:-7] + '.mat') for csv_name in XBIC_csv_names]
# 
# for mat_dict, fname in zip(matdicts_of_asciis, export_file_names):
#     scipy.io.savemat(fname, mat_dict)
# =============================================================================
