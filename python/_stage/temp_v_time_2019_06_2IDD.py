"""
coding: utf-8

tzwalker
Fri Nov  5 08:40:04 2021

this program get the temperature vs time data from 2019_06_2IDD beamrun


"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read data file
DATAFILE = r"C:\Users\triton\Dropbox (ASU)\0_stage design\DATA\20219_06_2IDD_T1_edits.txt"
data = pd.read_csv(DATAFILE, delimiter='\t',header=None)
# take every 5th row
    # sampling rate about every 0.2sec; every 5th is about every second
data = data[::5]

# convert to numpy array for convenience
data_arr = np.array(data)

# define starting time index; change this to change plotting range
start_idx = 20000

#substract initial value of time array to get seconds
a = data_arr[start_idx:,1] - data_arr[start_idx,1]

# convert to hours
b = a/3600

# define plotting variables
time = b.copy()
temp = data_arr[start_idx:,2]

# mask outliers (caused by unplugging thermocouple)
mask = np.abs(temp) > 120
mask_temp = temp[~mask]
mask_time = time[~mask]

# plot data
fig, ax = plt.subplots()
ax.plot(mask_time,mask_temp)

plt.xlabel('Time (hr)')
plt.ylabel('Temperature (\u00B0C)')

OUT_PATH = r"C:\Users\triton\Dropbox (ASU)\0_stage design\supplementary"
FNAME = r"\2019_06_2IDD_temp_v_time.png"
plt.savefig(OUT_PATH+FNAME, format='png', dpi=300, bbox_inches='tight', pad_inches = 0)
