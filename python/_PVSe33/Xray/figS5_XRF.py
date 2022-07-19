# -*- coding: utf-8 -*-
"""

Trumann
Tue May 31 14:51:17 2022

this program plots the masked XRF maps on top of their integrated profiles
it is meant to show the layers are aligned and in focu sin cross section

supplementary info fig 5 file

plots the maps and interfaces

"""
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
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

def norm(data):
    return (data)/(max(data)-min(data))

''' 0hr plotting '''
SAVE = 1
OUT = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_xsect\0hr_alignment.pdf'

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

# scan 119 - integrate line profiles
df_sums = []
for df in df_maps:
    df_arr = np.array(df)
    df_sum = df_arr.sum(axis=0)
    df_sums.append(df_sum)
    
df_sums_arr = np.array(df_sums).T

colors = ["Greens_r", "Blues_r", "Greys_r", "Oranges_r"]

sn = df_maps[5]
sn = sn.to_numpy()
sn = sn[:,:-2]
msn = np.ma.masked_where(sn<1e3,sn,copy=True)

se = df_maps[2]
se = se.to_numpy()
se = se[:,:-2]
mse = np.ma.masked_where(se<1.75e4,se,copy=True)

te = df_maps[3]
te = te.to_numpy()
te = te[:,:-2]
mte = np.ma.masked_where(te<1.75e3,te,copy=True)

au = df_maps[4]
au = au.to_numpy()
au = au[:,:-2]
mau = np.ma.masked_where(au<8e3,au,copy=True)

masks = [msn,mse,mte,mau]

# plot overlaid images
fig, (ax1,ax2) = plt.subplots(2,1, sharex='all')
ax1.xaxis.set_ticks(np.arange(0,101,11)) # calibrate

for i,m in enumerate(masks):
    im = ax1.imshow(m,cmap=colors[i],origin='lower',alpha=0.65,aspect=9)
    #fig.colorbar(im, format=fmt)
    #color bar labels
    #cbar = plt.gcf().axes[-1]
    #cbar.set_ylabel(unit[i], rotation=90, va="bottom", labelpad=30)
    #change color bar scale label position 
    #cbar.yaxis.set_offset_position('left')

fmtr_y = lambda x, pos: f'{(x * 1.000):.0f}'
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax1.set_ylabel('$Y$ (μm)')

# plot line plot underneath image
ax2.xaxis.set_ticks(np.arange(0,101,11)) # calibrate

ax2.plot(norm(df_sums_arr[:,5]),color='g') # Sn
ax2.plot(norm(df_sums_arr[:,2]),color='b') # Se
ax2.plot(norm(df_sums_arr[:,3]),color='k') # Te
ax2.plot(norm(df_sums_arr[:,4]),color='orange') # Au


fmtr_x = lambda x, pos: f'{(x * 0.100):.0f}'
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax2.set_xlabel('$X$ (μm)')
ax2.set_ylabel('XRF (arb. unit)')

asp = np.diff(ax2.get_xlim())[0] / np.diff(ax2.get_ylim())[0]
ax2.set_aspect(asp)

if SAVE == 1:
    plt.savefig(OUT, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)

#%%
''' 500hr plotting '''

SAVE = 1
OUT = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_xsect\500hr_alignment.pdf'

# directory information for data file
PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\XRF_XANES - cross section\2021_07_2IDD_SeXRF\output'
FILENAME = r'\combined_ASCII_2idd_0151.h5.csv' # 0hr infinite cross section
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

# scan 119 - integrate line profiles
df_sums = []
for df in df_maps:
    df_arr = np.array(df)
    df_sum = df_arr.sum(axis=0)
    df_sums.append(df_sum)
    
df_sums_arr = np.array(df_sums).T

sn = df_maps[5]
sn = sn.to_numpy()
sn = sn[:-13,13:-2]
msn = np.ma.masked_where(sn<1e3,sn,copy=True)

se = df_maps[2]
se = se.to_numpy()
se = se[:-13,13:-2]
mse = np.ma.masked_where(se<1.75e4,se,copy=True)

te = df_maps[3]
te = te.to_numpy()
te = te[:-13,13:-2]
mte = np.ma.masked_where(te<1.75e3,te,copy=True)

au = df_maps[4]
au = au.to_numpy()
au = au[:-13,13:-2]
mau = np.ma.masked_where(au<8e3,au,copy=True)

masks = [msn,mse,mte,mau]

# plot overlaid images
fig, (ax1,ax2) = plt.subplots(2,1, sharex='all')
ax1.xaxis.set_ticks(np.arange(0,76,12)) # calibrate

for i,m in enumerate(masks):
    im = ax1.imshow(m,cmap=colors[i],origin='lower',alpha=0.65)
    #fig.colorbar(im, format=fmt)
    #color bar labels
    #cbar = plt.gcf().axes[-1]
    #cbar.set_ylabel(unit[i], rotation=90, va="bottom", labelpad=30)
    #change color bar scale label position 
    #cbar.yaxis.set_offset_position('left')



fmtr_y = lambda x, pos: f'{(x * 0.160):.0f}'
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax1.set_ylabel('$Y$ (μm)')

# plot line plot underneath image
ax2.xaxis.set_ticks(np.arange(0,76,12)) # calibrate

ax2.plot(norm(df_sums_arr[13:,5]),color='g') # Sn
ax2.plot(norm(df_sums_arr[13:,2]),color='b') # Se
ax2.plot(norm(df_sums_arr[13:,3]),color='k') # Te
ax2.plot(norm(df_sums_arr[13:,4]),color='orange') # Au


fmtr_x = lambda x, pos: f'{(x * 0.160):.0f}'
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax2.set_xlabel('$X$ (μm)')
ax2.set_ylabel('XRF (arb. unit)')

asp = np.diff(ax2.get_xlim())[0] / np.diff(ax2.get_ylim())[0]
ax2.set_aspect(asp)

if SAVE == 1:
    plt.savefig(OUT, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)

#%%
'''
plotting 0hr maps

this cell was the dirty way to mask and plot maps in a column
could be useful if i need to plot the maps in a single column quickly
'''
PERCENTILE = 80

sn = df_maps[5]
sn = sn.to_numpy()
sn = sn[:,:-2]
# threshold image copy (need to copy to avoid overwriting original image)
bound = np.percentile(sn, PERCENTILE)
print(bound)
#sn[sn<bound] = np.nan


se = df_maps[2]
se = se.to_numpy()
se = se[:,:-2]
# threshold image copy (need to copy to avoid overwriting original image)
bound = np.percentile(se, PERCENTILE)
print(bound)
#se[se<bound] = np.nan


te = df_maps[3]
te = te.to_numpy()
te = te[:,:-2]
# threshold image copy (need to copy to avoid overwriting original image)
bound = np.percentile(te, PERCENTILE)
print(bound)
#te[te<bound] = np.nan


au = df_maps[4]
au = au.to_numpy()
au = au[:,:-2]
# threshold image copy (need to copy to avoid overwriting original image)
bound = np.percentile(au, PERCENTILE)
print(bound)
#au[au<bound] = np.nan


fig, axs = plt.subplots(4,1,sharex='all')

maps = [sn,se,te,au]
colors = ['Greens_r','Blues_r','Greys_r','YlOrBr_r']
unit = ['Sn XRF \n (cts/s)','Se XRF \n (cts/s)','Te XRF \n (cts/s)','Au XRF \n (cts/s)']

for i,ax in enumerate(axs):
    im = ax.imshow(maps[i], cmap=colors[i], origin='lower')
    ax.set_aspect(9)
    ax.set_ylabel('$Y$ (μm)')
    # outline possible position of interfaces
    ax.axvline(20,color='r',linestyle='-', linewidth=0.5)
    ax.axvline(65,color='r',linestyle='-', linewidth=0.5)
    
    fmt = mticker.ScalarFormatter(useMathText=True)
    fmt.set_powerlimits((0, 0))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='2%',pad=-1.8) # for 072
    
    fig.colorbar(im, cax=cax, format=fmt)
    #color bar labels
    cbar = plt.gcf().axes[-1]
    cbar.set_ylabel(unit[i], rotation=90, va="bottom", labelpad=30)
    #change color bar scale label position 
    cbar.yaxis.set_offset_position('left')
    
    fmtr_y = lambda x, pos: f'{(x * 1.000):.0f}'
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
    
fmtr_x = lambda x, pos: f'{(x * 0.100):.0f}'
axs[3].xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
axs[3].set_xlabel('$X$ (μm)')
    
plt.tight_layout()

#%%
'''
plotting 500hr maps

this cell was the dirty way to mask and plot maps in a column
could be useful if i need to plot the maps in a single column quickly
'''
sn = df_maps[5]
sn = sn.to_numpy()
sn = sn[:-13,13:-2]
# threshold image copy (need to copy to avoid overwriting original image)
bound = np.percentile(sn, PERCENTILE)
print(bound)
#sn[sn<bound] = np.nan


se = df_maps[2]
se = se.to_numpy()
se = se[:-13,13:-2]
# threshold image copy (need to copy to avoid overwriting original image)
bound = np.percentile(se, PERCENTILE)
print(bound)
#se[se<bound] = np.nan


te = df_maps[3]
te = te.to_numpy()
te = te[:-13,13:-2]
# threshold image copy (need to copy to avoid overwriting original image)
bound = np.percentile(te, PERCENTILE)
print(bound)
#te[te<bound] = np.nan


au = df_maps[4]
au = au.to_numpy()
au = au[:-13,13:-2]
# threshold image copy (need to copy to avoid overwriting original image)
bound = np.percentile(au, PERCENTILE)
print(bound)
#au[au<bound] = np.nan


fig, axs = plt.subplots(4,1,sharex='all')

maps = [sn,se,te,au]
colors = ['Greens_r','Blues_r','Greys_r','YlOrBr_r']
unit = ['Sn XRF \n (cts/s)','Se XRF \n (cts/s)','Te XRF \n (cts/s)','Au XRF \n (cts/s)']

for i,ax in enumerate(axs):
    im = ax.imshow(maps[i], cmap=colors[i], origin='lower')
    ax.set_aspect(1)
    ax.set_ylabel('$Y$ (μm)')
    # outline possible position of interfaces
    ax.axvline(10,color='r',linestyle='-', linewidth=0.5)
    ax.axvline(55,color='r',linestyle='-', linewidth=0.5)
    
    fmt = mticker.ScalarFormatter(useMathText=True)
    fmt.set_powerlimits((0, 0))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='20%',pad=0.1) # for 072
    
    fig.colorbar(im, cax=cax, format=fmt)
    #color bar labels
    cbar = plt.gcf().axes[-1]
    cbar.set_ylabel(unit[i], rotation=90, va="bottom", labelpad=30)
    #change color bar scale label position 
    cbar.yaxis.set_offset_position('left')
    
    fmtr_y = lambda x, pos: f'{(x * 0.160):.0f}'
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
    
fmtr_x = lambda x, pos: f'{(x * 0.160):.0f}'
axs[3].xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
axs[3].set_xlabel('$X$ (μm)')

plt.tight_layout()