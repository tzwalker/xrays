"""
coding: utf-8
Trumann
Mon Feb  7 16:53:50 2022

map step size: 200nm x 400nm
map area: 10um x 10um


# cmaps: 
    #RdYlGn 
    #inferno 
    #Greys_r
    #Blues_r
    #viridis
    #Oranges_r
    #YlOrBr_r

"""
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as mticker
from skimage.transform import rotate

import numpy as np

SAVE = 0
OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\NBL3 XRF maps'
FNAME = r'\TS58Ascan386_XBIC.eps'

img = Cu1b4c.maps[0][1,:,:]

data = img.copy()

draw_cbar = 1
cbar_txt_size = 11
top_cbar = 0
side_cbar=1

cbar_scale_control = 1; MIN = 0; MAX = 1.25e5
normalize = 0
standardized = 0
sci_notation = 1

unit = u'(cts/s)'; colormap = 'magma'; 

if normalize == 1:
    #data = data*1e8
    data_norm = data / data.max()
if standardized == 1:
    mean = np.mean(data)
    std = np.std(data)
    data_stand = (data - mean) / std


plt.figure()
fig, ax = plt.subplots(figsize=(2.5,2.5))

if cbar_scale_control == 1:
    im = ax.imshow(data, cmap=colormap, vmax=MAX, vmin=MIN, origin='lower')
if cbar_scale_control == 0:
    im = ax.imshow(data, cmap=colormap, origin='lower')
if normalize == 1:
    im = ax.imshow(data_norm, cmap=colormap, vmin=0.75, vmax=1, origin='lower')
if standardized == 1:
    im = ax.imshow(data_stand, cmap=colormap, origin='lower')

fmtr_x = lambda x, pos: f'{(x * 0.200):.0f}'
fmtr_y = lambda x, pos: f'{(x * 0.333):.0f}'
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmtr_x))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmtr_y))
ax.set_xlabel('X (μm)')
ax.set_ylabel('Y (μm)')

if draw_cbar == 1:
    divider = make_axes_locatable(ax)
    if side_cbar == 1:
        # create color bar
        cax = divider.append_axes('right', size='5%', pad=0.1)
        if sci_notation == 1:
            fmt = mticker.ScalarFormatter(useMathText=True)
            fmt.set_powerlimits((1, 0))
            cb = fig.colorbar(im, cax=cax, orientation='vertical',format=fmt)
        else:
            cb = fig.colorbar(im, cax=cax, orientation='vertical')#,format='.1f')
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
    if top_cbar == 1:
        cax = divider.new_vertical(size='5%', pad=0.1)
        fig.add_axes(cax)
        if sci_notation == 1:
            fmt = mticker.ScalarFormatter(useMathText=True)
            fmt.set_powerlimits((0, 0))
            cb = fig.colorbar(im, cax=cax, orientation='horizontal',format=fmt)
        else:
            cb = fig.colorbar(im, cax=cax, orientation='horizontal')
        # change cbar label font sizes
        cb.set_label(unit, fontsize=cbar_txt_size)
        cb.ax.tick_params(labelsize=cbar_txt_size)
        #move cbar ticks to top of cbar
        cax.xaxis.set_label_position('top')
        cax.xaxis.set_ticks_position('top')
        #change number of tick labels on cbar
        cbar = plt.gcf().axes[-1]
        cbar.locator_params(nbins=4)

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)