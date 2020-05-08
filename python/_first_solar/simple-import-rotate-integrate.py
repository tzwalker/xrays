"""
coding: utf-8

tzwalker
Thu May  7 16:06:51 2020

this program is meant to analyze First Solar cross-section data
Set 1 (July 2018)
Set 2 (November 2018)

imports ASCII from MAPS
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
PATH = r'C:\Users\triton\FS_xsect_revised'

# change depending on sector
FILENAME = r'\combined_ASCII_2idd_0083.h5.csv'
DATA = PATH+FILENAME

# import the data as a pandas dataframe ('df'); skip first row header
df = pd.read_csv(DATA, skiprows=1)

# remove column header spaces (for convenient reference to column headers)
    # this step is necessary because MAPS outputs ASCIIs with extra spaces
df_clean = remove_column_header_spaces(df)

# shape data of a given column into 2D map
x_pix = 'x pixel no'
y_pix = 'y pixel no'
# specify XRF or XBIC (usually under 'ds_ic' column header)
channel = 'Te_L'
df_map = df_clean.pivot(index = y_pix, columns = x_pix, values = channel)

# rotate dataframe, second argument is rotation in degrees
df_rot = rotate(df_map, 0)

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

