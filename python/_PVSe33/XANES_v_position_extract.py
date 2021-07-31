"""
coding: utf-8

tzwalker
Fri Jul 30 13:45:05 2021
"""

PATH = r'C:\Users\triton\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\XRF_XANES - cross section\output'
FILE = r'\combined_ASCII_2idd_0145.h5.csv'

F = PATH+FILE

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv(F, sep=',', skiprows=2)
data.columns = ["x_idx", "y_idx", "Energy", "position", "Se_XRF"]


data_dict = data.set_index(['y_idx', 'position']).agg(list, 1).groupby(level=(0)).agg(list).transform(np.array).to_dict()

for position in data_dict.values():
    # access energy and Se intensity
    energy = position[:,1]
    energy = energy * 1000 # units into keV
    xrf = position[:,2]
    # combine energy and XRF array
    # insert debug pause to copy/paste into Origin
    copy_array = np.vstack((energy, xrf)).T
    plt.plot(energy, xrf)