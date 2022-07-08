# -*- coding: utf-8 -*-
"""

Trumann
Wed Jul  6 13:57:13 2022

this prgram plots the Cu XRF map for my dissertation

these three scans had the same y center motor coordinate: 0.1862mm
but slightly different x center coordinates
img1 x center: 0.171500;
img2 x center: 0.172000;
img3 x center: 0.173000;

if i shift these with respect to img1, then they should be in same position

# scan238 img 1 has different resolution, 8.2  /41, 10.3 /31
# scan254 img 2 has different resolution, 8.2  /41, 10.5 /21
# scan524 img 3 has different resolution, 10.2 /51, 10.5 /21
just be careful when you apply ticklabels to these images

"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from skimage.transform import rotate
import numpy as np
import pandas as pd



# define ascii of scan
file = r"C:\Users\Trumann\Dropbox (ASU)\2_insitu_Cu_cross_section\output\combined_ASCII_2idd_0244.h5.csv"

# channels to import from ASCII
channels = [' us_ic', ' ds_ic', ' Cu', ' Cd_L', ' Sn_L', ' Au_M']

# scaler factor for XBIC map
scaler_factor = (50000*1E-9) / (2e5*500)

# import ascii as dataframe
data = pd.read_csv(file, skiprows=1)
# dataframe keys used for shaping into map
i = ' y pixel no'; j='x pixel no'
# extract maps of interest; shape according to pixel no
data_shape = [data.pivot(index=i, columns=j, values=c) for c in channels]
# convert dataframes to numpy arrays
data_arr = [df.to_numpy() for df in data_shape]

# convert electrical: cts to nanoampere
data_arr[1] = data_arr[1]*scaler_factor*1e9

# store maps as 3D cube - axis=0 equals index of channel in channels
maps = np.array(data_arr)

#%%
'''this cell plots a channel'''

SAVE = 0
OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\insitu_maps'
FNAME = r'\scan244_Cu.pdf'

idx = 2

img = maps[idx,:,:-2] # 0hr, 80C, 0V

# rotate so interfaces are vertical
#img = rotate(img, -8)

cbar_txt_size = 11
if idx == 1:
    unit = u'XBIC (nA)'; colormap = 'magma'; VMIN = 0; VMAX = 70 # XBIC
if idx == 2:
    unit = u'Cu (cts/s)'; colormap = 'Oranges_r'; VMIN = 0; VMAX = 3.5e4 # Cu
if idx == 3:
    unit = u'Cd (cts/s)'; colormap = 'Greys_r'; VMIN = 0; VMAX = 2.5e3 # Cd
if idx == 4:
    unit = u'Sn (cts/s)'; colormap = 'Greens_r'; VMIN = 0; VMAX = 2.5e3 # Cd


fig, ax = plt.subplots(figsize=(2.5,2.5)) # 

im = ax.imshow(img, cmap=colormap, origin='lower', vmin = VMIN, vmax= VMAX)

ax.scatter([33,37],[1,18], s=30, facecolors='none', edgecolors='r')

ax.set_aspect(2.25)

# ONLY USE THESE LINES FOR FIRST SCAN238; ITS MAP HAD DIFFERENT ASPECT RATIO !!!
#ax.xaxis.set_ticks(np.arange(0,41,11))
ax.yaxis.set_ticks(np.arange(0,21,10))
fmtr_x = lambda x, pos: f'{(x * 0.200):.0f}' # 0hr, 80C, 0V
fmtr_y = lambda x, pos: f'{(x * 0.500):.0f}' # 0hr, 80C, 0V
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax.set_xlabel('X (μm)')
ax.set_ylabel('Y (μm)')

# format colorbar
fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))
cax = fig.add_axes([ax.get_position().x1+0.03,ax.get_position().y0,0.04,ax.get_position().height])

if idx != 1:
    cbar = fig.colorbar(im, cax=cax, orientation='vertical',format=fmt)
else:
    cbar = fig.colorbar(im, cax=cax, orientation='vertical')
cbar.ax.set_ylabel(unit, rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
#cbar.locator_params(nbins=4)
cbar.ax.tick_params(labelsize=cbar_txt_size)
cbar.ax.yaxis.get_offset_text().set(size=cbar_txt_size)   
cbar.ax.yaxis.set_offset_position('left')

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)
    
#%%

'''this cell plots the images as subplots with the colorbars on top'''

SAVE = 1
OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\insitu_maps'
FNAME = r'\all_maps_with_markers.pdf'

# 0.23 hr, 80C, 0V, scan244
img1 = maps[1,:,:-2] # XBIC
img2 = maps[4,:,:-2] # Sn
img3 = maps[3,:,:-2] # Cd
img4 = maps[2,:,:-2] # Cu

# rotate so interfaces are vertical
#img = rotate(img, -8)

cbar_txt_size = 11

fig, (ax1,ax2,ax3,ax4) = plt.subplots(nrows=1,ncols=4,sharex=True,sharey=True) # figsize=(2.5,2.5)

im1 = ax1.imshow(img1, cmap='magma', origin='lower', vmin = 0, vmax= 70)
im2 = ax2.imshow(img2, cmap='Greens_r', origin='lower', vmin = 0, vmax= 2.5e3)
im3 = ax3.imshow(img3, cmap='Greys_r', origin='lower', vmin = 0, vmax= 2.5e3)
im4 = ax4.imshow(img4, cmap='Oranges_r', origin='lower', vmin = 0, vmax= 3.5e4)

ax1.scatter([33,37],[1,18], s=30, facecolors='none', edgecolors='r')
ax2.scatter([33,37],[1,18], s=30, facecolors='none', edgecolors='r')
ax3.scatter([33,37],[1,18], s=30, facecolors='none', edgecolors='r')
ax4.scatter([33,37],[1,18], s=30, facecolors='none', edgecolors='r')

ax1.set_aspect(2.25)
ax2.set_aspect(2.25)
ax3.set_aspect(2.25)
ax4.set_aspect(2.25)

# ONLY USE THESE LINES FOR FIRST SCAN238; ITS MAP HAD DIFFERENT ASPECT RATIO !!!
#ax.xaxis.set_ticks(np.arange(0,41,11))
ax1.yaxis.set_ticks(np.arange(0,21,10))
fmtr_x = lambda x, pos: f'{(x * 0.200):.0f}' # 0hr, 80C, 0V
fmtr_y = lambda x, pos: f'{(x * 0.500):.0f}' # 0hr, 80C, 0V
ax1.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax1.set_xlabel('X (μm)')
ax1.set_ylabel('Y (μm)')

ax2.set_xlabel('X (μm)')
ax3.set_xlabel('X (μm)')
ax4.set_xlabel('X (μm)')

# format colorbar
fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))

# XBIC colorbar
cax1 = fig.add_axes([ax1.get_position().x0,ax1.get_position().y1+0.03,ax1.get_position().width,0.02])
cbar1 = fig.colorbar(im1, cax=cax1, orientation='horizontal')
# change cbar label font sizes
cbar1.ax.set_xlabel('XBIC (nA)', fontsize=cbar_txt_size)
cbar1.ax.tick_params(labelsize=cbar_txt_size)
#move cbar ticks to top of cbar
cax1.xaxis.set_label_position('top')
cax1.xaxis.set_ticks_position('top')
#change number of tick labels on cbar
cbar1.ax.locator_params(nbins=4)

# Sn colorbar
cax2 = fig.add_axes([ax2.get_position().x0,ax2.get_position().y1+0.03,ax2.get_position().width,0.02])
cbar2 = fig.colorbar(im2, cax=cax2, orientation='horizontal', format=fmt)
# change cbar label font sizes
cbar2.ax.set_xlabel('Sn (cts/s)', fontsize=cbar_txt_size)
cbar2.ax.tick_params(labelsize=cbar_txt_size)
#move cbar ticks to top of cbar
cax2.xaxis.set_label_position('top')
cax2.xaxis.set_ticks_position('top')
#change number of tick labels on cbar
cbar2.ax.yaxis.set_offset_position('left')
cbar2.ax.locator_params(nbins=4)

# Cd colorbar
cax3 = fig.add_axes([ax3.get_position().x0,ax3.get_position().y1+0.03,ax3.get_position().width,0.02])
cbar3 = fig.colorbar(im3, cax=cax3, orientation='horizontal', format=fmt)
# change cbar label font sizes
cbar3.ax.set_xlabel('Cd (cts/s)', fontsize=cbar_txt_size)
cbar3.ax.tick_params(labelsize=cbar_txt_size)
#move cbar ticks to top of cbar
cax3.xaxis.set_label_position('top')
cax3.xaxis.set_ticks_position('top')
#change number of tick labels on cbar
cbar3.ax.yaxis.set_offset_position('left')
cbar3.ax.locator_params(nbins=4)

# Cu colorbar
cax4 = fig.add_axes([ax4.get_position().x0,ax4.get_position().y1+0.03,ax4.get_position().width,0.02])
cbar4 = fig.colorbar(im4, cax=cax4, orientation='horizontal', format=fmt)
# change cbar label font sizes
cbar4.ax.set_xlabel('Cu (cts/s)', fontsize=cbar_txt_size)
cbar4.ax.tick_params(labelsize=cbar_txt_size)
#move cbar ticks to top of cbar
cax4.xaxis.set_label_position('top')
cax4.xaxis.set_ticks_position('top')
#change number of tick labels on cbar
cbar4.ax.yaxis.set_offset_position('left')
cbar4.ax.locator_params(nbins=4)

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)