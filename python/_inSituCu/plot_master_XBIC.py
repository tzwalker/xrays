# -*- coding: utf-8 -*-
"""

Trumann
Thu Jul  7 10:06:46 2022

this program plot the same three XBIC images in Mariana's PVSC presentation
one at beginning of 80C
one at 12hr at 80C
one at 24hr 80C, 12hr 300mV

"""

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as mticker
from skimage.transform import rotate

import numpy as np

from class_ascii_Sample import Sample

ASCII_PATH =  r'C:\Users\Trumann\Dropbox (ASU)\2_insitu_Cu_cross_section\output' 
#PATH_LOCKIN = r'C:\Users\Trumann\FS3_2019_06_operando\ASCIIS_TW_BL\FS_plan_electrical.csv'

# create sample objects
Cu1b4c = Sample()

# define stack and scans of each sample, upstream layer first
Cu1b4c.stack = {'Au':   [19.3, 100E-7], 
                 'CdTe': [5.85, 5E-4],
                 'Se': [4.82, 100E-7],
                 'SnO2': [100E-7]}
#Cu1b4c.scans = [238,366]
Cu1b4c.scans = [238,366,524]

# channels to import from ASCII
channels = [' us_ic', ' ds_ic', ' Cu', ' Se_L', ' Cd_L', ' Te_L', ' Au_M']

# uncomment this line to import maps with XBIC converted to ampere
# this requires XBIC channel ('us_ic') to be in first position of 'channels' list
#Cu1b4c.import_maps(ASCII_PATH, PATH_LOCKIN, channels)

# uncomment this line to import maps without XBIC converted to ampere
Cu1b4c.import_maps_no_XBIC_conversion(ASCII_PATH, channels)

img1 = Cu1b4c.maps[0][1,:,:-2] # 0hr, 80C, 0V
img2 = Cu1b4c.maps[1][1,:,7:-5] # 12hr, 80C, 0V ; remove 2 nan columns, then 10 data columns to match first scan
img3 = Cu1b4c.maps[2][1,:,7:-5] # 24hr, 80C,+300mV ; ; remove 2 nan columns, then 10 data columns to match first scan

scaler_factor = (50000*1E-9) / (2e5*500)

XBIC_maps = [img1,img2,img3]

# convert to nA
XBIC_nA = []
for x in XBIC_maps:
    x = x*scaler_factor*1e9
    XBIC_nA.append(x)
#%%
SAVE = 1
out = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\insitu_maps\XBICmaps.pdf'

cbar_txt_size = 11

fig, axs = plt.subplots(nrows=3, ncols=1,sharex=True)

fmtrs_x = [lambda x, pos: f'{(x * 0.200):.0f}',lambda x, pos: f'{(x * 0.200):.0f}',lambda x, pos: f'{(x * 0.200):.0f}']
fmtrs_y = [lambda x, pos: f'{(x * 0.333):.0f}',lambda x, pos: f'{(x * 0.500):.0f}',lambda x, pos: f'{(x * 0.500):.0f}']

aspects = [0.67,1,1]

for ax,xm,fmtx,fmty,aspect in zip(axs, XBIC_nA ,fmtrs_x, fmtrs_y, aspects):
    im = ax.imshow(xm, cmap='magma', origin='lower', vmin = 0, vmax=50)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtx))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmty))
    
    ax.set_ylabel('Y (μm)')
    ax.set_aspect(aspect)
    
    # format colorbar
    cax = fig.add_axes([ax.get_position().x1+0.015,ax.get_position().y0,0.02,ax.get_position().height])

        #get color bar object
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        #format colorbar
    cbar.ax.set_ylabel('XBIC (nA)', rotation=90, va="bottom", size=cbar_txt_size, labelpad=12)
        # change number of tick labels on colorbar
    #cbar.locator_params(nbins=4)
        #change colorbar tick label sizes
    cbar.ax.tick_params(labelsize=cbar_txt_size)
        #change color bar scale label size, e.g. 1e-8
    cbar.ax.yaxis.get_offset_text().set(size=cbar_txt_size)
        #change color bar scale label position   
    cbar.ax.yaxis.set_offset_position('left')
    #cbar.locator_params(nbins=5)
    
ax.set_xlabel('X (μm)')

if SAVE == 1:
    plt.savefig(out, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)