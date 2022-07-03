# -*- coding: utf-8 -*-
"""

Trumann
Sat Jul  2 17:10:28 2022

run main-PVSe33-ASCII-xsect.py with '0hr_inf' key before this program

this program plots the points for the Se XANES of the 0hr cell

"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

import pandas as pd

def remove_column_header_spaces(dataframe):
    old_colnames = dataframe.columns.values
    new_colnames = []
    for name in old_colnames:
        new_colnames.append(name.strip())
    header_dict = {i:j for i,j in zip(old_colnames,new_colnames)}
    dataframe.rename(columns = header_dict, inplace=True)
    return dataframe

# directory information for data file
PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\XRF_XANES - cross section\2021_07_2IDD_SeXRF\output'

FILENAME = r'\combined_ASCII_2idd_0119.h5.csv' # 0hr infinite cross section

DATA = PATH+FILENAME

channels = ['ds_ic', 'Cu', 'Se', 'Te_L', 'Au_L', 'Sn_L', 'Cl']

df_maps = []
for chan in channels:
    # import the data as a pandas dataframe ('df'); skip first row header
    df = pd.read_csv(DATA, skiprows=1)
    
    # remove column header spaces (for convenient reference to column headers)
        # this step is necessary because MAPS outputs ASCIIs with extra spaces
    df_clean = remove_column_header_spaces(df)
    
    # shape data of a given column into 2D map
    x_pix = 'x pixel no'
    y_pix = 'y pixel no'
    # specify XRF or XBIC (usually under 'ds_ic' column header)
    channel = chan
    df_map = df_clean.pivot(index = y_pix, columns = x_pix, values = channel)
    df_maps.append(df_map)

# convert XBIC
scaler_factor = (50E-6) / (2E5*1000) # ampere (A)
df_xbic = df_maps[0] * scaler_factor * 1E9 # from A to nA
df_maps[0] = df_xbic # replace imported df

#%%
'''this cell plots the data'''
# import indices for XANES spectra
FILE = r'C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\XRF_XANES - cross section\0hr_inf_SeXANES_indices.csv'
points = pd.read_csv(FILE,skiprows=1)
x = list(points['x pixel no'])
y = list(points['y pixel no'])

SAVE = 1
#OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\20210625 figures_v1\figure4 materials'
OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_XANESvP_Se'
FNAME = r'\0hr_SeXANESpoints.pdf'

# channel
idx = 2

img = df_maps[idx]
img = img.to_numpy()
img = img[:,:-2]

if idx ==0:
    unit = 'XBIC (nA)'; colormap='inferno'; low=0; high=70
if idx == 1:
    unit = 'Cu (cts/s)'; colormap = 'Oranges_r'; low = 1e2; high = 1e3
if idx == 2:
    unit = 'Se (cts/s)'; colormap = 'Blues_r'; low = 0; high = 5e4
if idx == 3:
    unit = 'Te (cts/s)'; colormap = 'Greys_r'; low = 0; high = 5e3
if idx == 4:
    unit = 'Au (cts/s)'; colormap = 'YlOrBr_r'; low = 0; high = 5e3
if idx == 5:
    unit = 'Sn (cts/s)'; colormap = 'Greens_r'; low = 0; high = 5e3
if idx == 6:
    unit = 'Cl (cts/s)'; colormap = 'viridis'; low = 0; high = 4e2
    
cbar_txt_size = 11

fig, ax = plt.subplots(figsize=(2.5,1.5))

ax.xaxis.set_ticks(np.arange(0,101,11))
ax.yaxis.set_ticks(np.arange(0,11,2))
#plt.locator_params(axis='x', nbins=6)
#plt.locator_params(axis='y', nbins=5)
fmtr_x = lambda x, pos: f'{(x * 0.100):.0f}'
fmtr_y = lambda x, pos: f'{(x * 1.000):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax.set_xlabel('$X$ (μm)')
ax.set_ylabel('$Y$ (μm)')

im = ax.imshow(img, cmap=colormap, origin='lower', vmin=low, vmax=high)
# outline possible position of interfaces
plt.axvline(20,color='r',linestyle='-', linewidth=0.5)
plt.axvline(65,color='r',linestyle='-', linewidth=0.5)

# scan 121 indices
plt.scatter(x, y, color='red', s=3)

# define colorbar format
fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))

#format and add colorbar
if idx == 0:
    fig.colorbar(im)
else:
    fig.colorbar(im, format=fmt)
#color bar labels
cbar = plt.gcf().axes[-1]
cbar.set_ylabel(unit, rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
    #change color bar scale label position 
cbar.yaxis.set_offset_position('left')

ax.set_aspect(9)

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)