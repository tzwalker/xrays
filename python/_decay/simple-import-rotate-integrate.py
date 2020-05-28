"""
coding: utf-8

tzwalker
Thu May 28 13:38:51 2020

this program is meant to analyze TS1181A data

imports custom csv (merge of h5 and mda)
shapes the data of a channel (e.g. Te_L XRF)
rotates the map (if desired)
sums along a given axis (e.g. the y-axis)
"""
import pandas as pd
from skimage.transform import rotate
import matplotlib.pyplot as plt

def remove_column_header_spaces(dataframe):
    old_colnames = dataframe.columns.values
    new_colnames = []
    for name in old_colnames:
        new_colnames.append(name.strip())
    header_dict = {i:j for i,j in zip(old_colnames,new_colnames)}
    dataframe.rename(columns = header_dict, inplace=True)
    return dataframe

# directory information for data file
PATH = r'C:\Users\triton\decay_data'

# change depending on sector
FILENAME = r'\combined_ASCII_26idbSOFT_0039.h5_mda.csv'
DATA = PATH+FILENAME

# import the data as a pandas dataframe ('df'); skip first row header
df = pd.read_csv(DATA)

# remove column header spaces (for convenient reference to column headers)
    # this step is necessary because MAPS outputs ASCIIs with extra spaces
df_clean = remove_column_header_spaces(df)

# shape data of a given column into 2D map
x_pix = 'x pixel no'
y_pix = 'y pixel no'
# specify XRF or XBIC (under '26idc:3820:scaler1_cts2.B' column header)
channel = 'Cu'
df_map = df_clean.pivot(index = y_pix, columns = x_pix, values = channel)

# rotate dataframe, second argument is rotation in degrees
df_rot = rotate(df_map, -2)

# integrate along y-axis
df_sum = df_rot.sum(axis = 0)

# check original map
plt.figure()
plt.imshow(df_map)
# check rotated map
plt.figure()
plt.imshow(df_rot)
# check integration (e.g. of rotated map)
plt.figure()
plt.plot(df_sum)

