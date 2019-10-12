# -*- coding: utf-8 -*-
"""
Trumann
Fri Oct 11 17:05:06 2019
"""

XBIC = [422,423,424, 550, 264,265,266, 475, 385,386,387, 439, 341,342,343, 519]
XBIV = [419,420,421, 551, 261,262,263, 472, 382,383,384, 440, 338,339,340, 517]

path = r'C:\Users\Trumann\Desktop\NBL3_data\output'

import h5py
XBIC_csvs = [(path + r'\combined_ASCII_2idd_0' + str(scan) + '.h5.csv') for scan in XBIC]
XBIV_csvs = [(path + r'\combined_ASCII_2idd_0' + str(scan) + '.h5.csv') for scan in XBIV]

import pandas as pd

imported_csvs = [pd.read_csv(csv_name, skiprows=1) for csv_name in XBIC_csvs]
    
    