# -*- coding: utf-8 -*-
"""
Trumann
Tue Feb  4 11:26:59 2020

want to get at data taken at two different angles
2016_07_2IDD - miasole 'large grain' sample 5
Area 1 0  deg - scan130
Area 1 15 deg - scan122

Area 2 0  deg - scan127
Area 2 15 deg - scan119
"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plot_FS_defs as fsdef
sys.path.append(r'C:\Users\Trumann\xrays\python\2_FS_code')

SCAN = 119
path = r'C:\Users\Trumann\Desktop\angle_data\output'
file = r'\combined_ASCII_2idd_0{s}.h5.csv'.format(s=str(SCAN))
#import dats
csv = pd.read_csv(path+file, skiprows=1)

#remove white spaces in ascii headers
fsdef.noColNameSpaces(csv)

#convert ascii into 2d arrays
CHANNELS = ['ds_ic', 'Cu', 'In_L', 'Ga', 'Se', 'Zn', 'Ca']
maps_df = [csv.pivot(index='y pixel no', columns='x pixel no', values=chan) for chan in CHANNELS]
maps_arr = [np.array(df) for df in maps_df]
#stack 2d arrays into 3d structure
map_stack = np.array(maps_arr)

#plot map to check; origin='lower' to compare to MAPS image
plt.imshow(map_stack[5])




