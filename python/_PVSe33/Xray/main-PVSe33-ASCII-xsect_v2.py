# -*- coding: utf-8 -*-
"""

Trumann
Wed Aug 31 15:52:47 2022

Se XANES
this an updated program meant to analyze PVSe33 cross-section data
2021_07_2IDD
Dropbox (ASU)\1_PVSe33 ex-situ\DATA\XRF_XANES - cross section\2021_07_2IDD_SeXRF\output

this program includes a definition that makes it easier to manage
the maps from the few scans related to these samples

the scans had different reolutions and map parameters
this makes their plotting unorthodox:
    the length of scan 119 is 10um (11pts)
    the length of scan 151 is 12um (76pts)
        -both the physical distance and the resolution (no. of observations) 
        is different between the two scans
        -when integrating i want to compare same physical distance 
        and number of observations
        -this means i need to get rid of most of the y pts in scan151
        before integrating scan 151
        -from scan 151, keep 10 rows spread over a 10um length
        -keep row at every 1um step
        -1um step is about 6 rows at 0.16nm per row
        -keep pixel idxs: [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60]

lockin settings
scan72 (window): stanford 50uA/V, 1000 V/V
scan119 (inf): stanford 50uA/V, 1000 V/V 
scan144 (window): stanford 50uA/V, 1000 V/V
scan151 (inf): stanford 50uA/V, 1000 V/V

interface index estimates
"Dropbox (ASU)\1_PVSe33 ex-situ\DATA\CdTe layer thickness estimate - XRF_2021_07_2IDD.txt"
0hr
2.20/0.1 = 22
6.3/0.1 = 63

500hr (shifted by 13 pixels as done in plotted maps)
3.84/0.16 - 13 = 11 (1.76um)
11.04/0.16 - 13 = 56 (8.96um)

"""

import pandas as pd
import numpy as np

def remove_column_header_spaces(dataframe):
    old_colnames = dataframe.columns.values
    new_colnames = []
    for name in old_colnames:
        new_colnames.append(name.strip())
    header_dict = {i:j for i,j in zip(old_colnames,new_colnames)}
    dataframe.rename(columns = header_dict, inplace=True)
    return dataframe

def get_maps(filename, channels):
    df_maps = []
    for chan in channels:
        # import the data as a pandas dataframe ('df'); skip first row header
        df = pd.read_csv(filename, skiprows=1)
        
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
    df_maps_arr = [np.array(df) for df in df_maps]
    return df_maps_arr

def normalize(line):
    array = (line - line.min()) / (line.max() - line.min())
    return array

# directory information for data file
PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\XRF_XANES - cross section\2021_07_2IDD_SeXRF\output'

file0 = PATH + r'\combined_ASCII_2idd_0119.h5.csv'
file500 = PATH + r'\combined_ASCII_2idd_0151.h5.csv'

CHANNELS = ['ds_ic', 'Cu', 'Se', 'Te_L', 'Au_L', 'Sn_L', 'Cl']

# import cross-section maps for 0hr cell
data0 = get_maps(file0, CHANNELS)
# calculate line profiles for XBIC, Se, and Te maps
lines0 = [data0[m].sum(axis=0) for m in [0,2,3]]
# normalize Se and Te between 0 and 1
lines0norm = [normalize(lines0[l]) for l in [1,2]]

# import cross-section maps for 500hr cell
data500 = get_maps(file500, CHANNELS)
# calculate line profiles for XBIC, Se, and Te maps
keep_pixels = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60]
lines500 = [data500[m][keep_pixels,:].sum(axis=0) for m in [0,2,3]]
# normalize Se and Te between 0 and 1
lines500norm = [normalize(lines500[l]) for l in [1,2]]

#%%
'''
this cell plots cross-section maps with different xy scales

it is meant to plot all the maps and line plots in the same figure
thus avoiding the need to import the line plots to Origin
and arrange in Inkscape

run this program after 'main-PVSe33-ASCII-xsect_v2'
the cross-section maps are for PVSe33

#for PVS33 
    plan-view (2020_10_26IDC): 25px = 4um
    window cross-section(2021_07_2IDD): 
        0hr scan72:     x, 1px = 160nm - y, 1px = 160nm
        500hr scan114:  x, 1px = 160nm - y, 1px = 160nm
    infinite cross-section(2021_07_2IDD): 
        0hr scan119:    x, 1px = 100nm - y, 1px= = 1um
        500hr scan151:  x, 1px = 160nm - y, 1px = 160nm
    

# cmaps: 
    #RdYlGn 
    #inferno 
    #Greys_r
    #Blues_r
    #viridis
    #Oranges_r
    #YlOrBr_r
    
'''
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

SAVE = 0
OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\20210625 figures_v1\figure4 materials'
FNAME = r'\fig4_xsectXray2.eps'

txt_size = 10

fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6), (ax7,ax8)) = plt.subplots(figsize=((6,6)),nrows=4,ncols=2)

''' maps section '''
# plot map data for 0hr cross section
ax1.imshow(data0[0][:,:-2], cmap='inferno', origin = 'lower', vmin = 0, vmax = 70) # XBIC
ax3.imshow(data0[2][:,:-2], cmap='Blues_r', origin = 'lower', vmin = 0, vmax = 5e4) # Se 
ax5.imshow(data0[3][:,:-2], cmap='Greys_r', origin = 'lower', vmin = 0, vmax = 5e3) # Te

# plot map data for 500hr cross section
    # these need to be cropped by 13 pixels to match spatial extent of 0hr maps
    # these need to be assigned 'im' to apply color bar to these maps
im2 = ax2.imshow(data500[0][:-13,13:-2], cmap='inferno', origin = 'lower', vmin = 0, vmax = 70) # XBIC
im4 = ax4.imshow(data500[2][:-13,13:-2], cmap='Blues_r', origin = 'lower', vmin = 0, vmax = 5e4) # Se
im6 = ax6.imshow(data500[3][:-13,13:-2], cmap='Greys_r', origin = 'lower', vmin = 0, vmax = 5e3) # Te

#fig.subplots_adjust(wspace=0.75, hspace = -.2)

# apply axis calibration to 0hr maps
for ax in ax1,ax3,ax5:
    ax.xaxis.set_ticks(np.arange(0,101,20))
    ax.yaxis.set_ticks(np.arange(0,11,10))
    fmtr_x = lambda x, pos: f'{(x * 0.100):.0f}'
    fmtr_y = lambda x, pos: f'{(x * 1.000):.0f}'
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
    ax.set_ylabel('$Y$ (μm)', size = txt_size)
    ax.set_xticklabels([])
    # outline possible position of interfaces
    ax.axvline(22,color='r',linestyle='-', linewidth=1)
    ax.axvline(63,color='r',linestyle='-', linewidth=1)
    
    ax.set_aspect(9)

# apply axis calibration to 500hr maps
for ax in ax2,ax4,ax6:
    ax.xaxis.set_ticks(np.arange(0,76,12))
    ax.yaxis.set_ticks(np.arange(0,76,60))
    fmtr_x = lambda x, pos: f'{(x * 0.160):.0f}'
    fmtr_y = lambda x, pos: f'{(x * 0.160):.0f}'
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
    ax.set_xticklabels([])
    # outline possible position of interfaces
    ax.axvline(11,color='r',linestyle='-', linewidth=1)
    ax.axvline(56,color='r',linestyle='-', linewidth=1)
    ax.set_xlim(0,61)
    ax.set_ylim(0,63)
    ax.set_aspect(1)

''' line plot section '''
# plot line data for 0hr cross section
xdata0 = np.arange(0,9.9,0.1)
ax7.plot(xdata0,lines0[0][:-2], color = 'orange', linewidth = 1, linestyle = ':')
ax7.set_ylim(0,1000)
ax7.xaxis.set_ticks(np.arange(0,11,2))
ax7.yaxis.set_ticks(np.arange(0,1250,250))
ax7.set_xlim(0,10)
ax7.set_ylabel('XBIC (nA)', size = txt_size)
ax7.set_xlabel('Device Depth (μm)', size = txt_size)
ax7.xaxis.set_ticks_position('both')
ax7.tick_params(axis="x",direction="in")
ax7.tick_params(axis="y",direction="in")

# plot XRF on second y axis
ax71 = ax7.twinx()
ax71.plot(xdata0,lines0norm[0][:-2], color = 'blue', linewidth = 1)
ax71.plot(xdata0,lines0norm[1][:-2], color = 'grey', linewidth = 1)
ax71.set_ylim(0,1.5)
ax71.tick_params(axis="y",direction="in")
ax71.yaxis.set_ticks(np.arange(0,1.75,0.5))
# add interface lines, in calibrated x-axis units
ax71.axvline(2.2,color='r',linestyle='-', linewidth=1)
ax71.axvline(6.3,color='r',linestyle='-', linewidth=1)

# change color of XBIC axis
ax71.spines['left'].set_color('orange')
ax7.tick_params(axis='y', colors='orange')
ax7.yaxis.label.set_color('orange')

# place and adjust line plot panel to match maps
box = ax5.get_position().translated(0,-.2)
ax7.set_position(box)

# plot line data for 500hr cross section
xdata500 = np.arange(0,9.7,0.160)
ax8.plot(xdata500,lines500[0][13:-2], color='orange', linewidth = 1 , linestyle = ':')
ax8.set_ylim(0,1000)
ax8.xaxis.set_ticks(np.arange(0,11,2))
ax8.yaxis.set_ticks(np.arange(0,1250,250))
ax8.set_xlim(0,10)
ax8.set_xlabel('Device Depth (μm)', size = txt_size)
ax8.xaxis.set_ticks_position('both')
ax8.tick_params(axis="x",direction="in")
ax8.tick_params(axis="y",direction="in")

# plot XRF on second y axis
ax81 = ax8.twinx()
ax81.plot(xdata500,lines500norm[0][13:-2], color = 'blue', linewidth = 1)
ax81.plot(xdata500,lines500norm[1][13:-2], color = 'grey', linewidth = 1)
ax81.set_ylim(0,1.5)
ax81.yaxis.set_ticks(np.arange(0,1.75,0.5))
ax81.set_ylabel('Normalized \n XRF (arb. unit)', size = txt_size)
ax81.tick_params(axis="y",direction="in")
# add interface lines, in calibrated x-axis units
ax81.axvline(1.76,color='r',linestyle='-', linewidth=1)
ax81.axvline(8.96,color='r',linestyle='-', linewidth=1)

# change color of XBIC axis
ax81.spines['left'].set_color('orange')
ax8.tick_params(axis='y', colors='orange')
ax8.yaxis.label.set_color('orange')

# place and adjust line plot panel to match maps
box = ax6.get_position().translated(0,-.2)
ax8.set_position(box)

''' color bar section '''
# XBIC maps color bar
cax2 = fig.add_axes([ax2.get_position().x1+0.02,ax2.get_position().y0,0.02,ax2.get_position().height])
cbar2 = fig.colorbar(im2, cax=cax2)
cbar2.ax.set_ylabel('XBIC (nA)', rotation=90, va="bottom", size=txt_size, labelpad=15)
cbar2.ax.yaxis.set_offset_position('left')

# Se maps color bar
fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))
cax4 = fig.add_axes([ax4.get_position().x1+0.02,ax4.get_position().y0,0.02,ax4.get_position().height])
cbar4 = fig.colorbar(im4, cax=cax4, format=fmt)
cbar4.ax.set_ylabel('(cts/s)', rotation=90, va="bottom", size=txt_size, labelpad=15)
cbar4.ax.yaxis.set_offset_position('left')

# Te maps color bar
fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))
cax6 = fig.add_axes([ax6.get_position().x1+0.02,ax6.get_position().y0,0.02,ax6.get_position().height])
cbar6 = fig.colorbar(im6, cax=cax6, format=fmt)
cbar6.ax.set_ylabel('(cts/s)', rotation=90, va="bottom", size=txt_size, labelpad=15)
cbar6.ax.yaxis.set_offset_position('left')

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)