# -*- coding: utf-8 -*-
"""

Trumann
Thu Jun  2 16:53:10 2022

this cell is meant for Mariana's 2022 PCSV presentation

it is the same as 'plot_master.py' but rotates and plots XRF

"""


import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as mticker
from skimage.transform import rotate

import numpy as np

SAVE = 0
OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\NBL3 XRF maps'
FNAME = r'\.eps'

img = Cu1b4c.maps[0][2,:,:-2] # 0hr, 80C, 0V
#img = Cu1b4c.maps[-2][2,:,:-2] # 12hr, 80C, 0V
#img = Cu1b4c.maps[-1][2,:,:-2] # 24hr, 80C,+300mV

# for Mariana's 2022 PVSC presentation
img = rotate(img, -8)

data = img.copy()

draw_cbar = 1
cbar_txt_size = 11
top_cbar = 0
side_cbar=1

cbar_scale_control = 1; MIN = 0; MAX = 3e4
normalize = 0
standardized = 0
sci_notation = 0

unit = u'(cts/s)'; colormap = 'Oranges_r'

if normalize == 1:
    #data = data*1e8
    data_norm = data / data.max()
if standardized == 1:
    mean = np.mean(data)
    std = np.std(data)
    data_stand = (data - mean) / std


fig, ax = plt.subplots(figsize=(2.5,2.5))

if cbar_scale_control == 1:
    im = ax.imshow(data, cmap=colormap, vmax=MAX, vmin=MIN, origin='lower')
if cbar_scale_control == 0:
    im = ax.imshow(data, cmap=colormap, origin='lower')
if normalize == 1:
    im = ax.imshow(data_norm, cmap=colormap, vmin=0.75, vmax=1, origin='lower')
if standardized == 1:
    im = ax.imshow(data_stand, cmap=colormap, origin='lower')


# ONLY USE THESE LINES FOR FIRST SCAN238; ITS MAP HAD DIFFERENT ASPECT RATIO !!!
fmtr_x = lambda x, pos: f'{(x * 0.200):.0f}' # 0hr, 80C, 0V
fmtr_y = lambda x, pos: f'{(x * 0.333):.0f}' # 0hr, 80C, 0V
ax.xaxis.set_ticks(np.arange(0,41,19))
ax.yaxis.set_ticks(np.arange(0,31,30))
ax.set_aspect(0.6)

#fmtr_x = lambda x, pos: f'{(x * 0.200):.0f}' # 12hr, 80C, 0V
#fmtr_y = lambda x, pos: f'{(x * 0.500):.0f}' # 12hr, 80C, 0V
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax.set_xlabel('X (μm)')
ax.set_ylabel('Y (μm)')

# ONLY USE THIS LINE FOR FIRST SCAN238; ITS MAP HAD DIFFERENT ASPECT RATIO !!!
cax = fig.add_axes([ax.get_position().x1+0.03,ax.get_position().y0,0.04,ax.get_position().height])

fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))

cb = fig.colorbar(im, cax=cax, orientation='vertical',format=fmt)
    #get color bar object
cbar = plt.gcf().axes[-1]
    #format colorbar
cbar.set_ylabel(unit, rotation=90, va="bottom", size=cbar_txt_size, labelpad=12)
    # change number of tick labels on colorbar
#cbar.locator_params(nbins=4)
    #change colorbar tick label sizes
cbar.tick_params(labelsize=cbar_txt_size)
    #change color bar scale label size, e.g. 1e-8
cbar.yaxis.get_offset_text().set(size=cbar_txt_size)
    #change color bar scale label position   
cbar.yaxis.set_offset_position('left')
cbar.locator_params(nbins=5)
