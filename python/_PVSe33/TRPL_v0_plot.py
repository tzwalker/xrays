# -*- coding: utf-8 -*-
"""

Trumann
Fri Apr 29 13:27:05 2022

run TRPL_v0.py before this program

this program plots the TRPL data from PVSe33.3_2 and PVSe33.4_3

for the DoE report 20220530

"""

import matplotlib.pyplot as plt
import matplotlib.offsetbox as offbox
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import ticker
import numpy as np
import tifffile

'''adds scalebar to matplotlib images'''
class AnchoredHScaleBar(offbox.AnchoredOffsetbox):
    """ size: length of bar in pixels
        extent : height of bar ends in axes units """
    def __init__(self, size=1, extent = 0.03, label="", loc=2, ax=None,
                 pad=0.4, borderpad=0.5, ppad = 0, sep=2, prop=None, 
                 frameon=True, linekw={}, **kwargs):
        if not ax:
            ax = plt.gca()
        trans = ax.get_xaxis_transform()
        size_bar = offbox.AuxTransformBox(trans)
        line = Line2D([0,size],[0,0], **linekw)
        size_bar.add_artist(line)
        txt = offbox.TextArea(label, textprops=dict(color=scalebar_color, size=cbar_txt_size))
        self.vpac = offbox.VPacker(children=[size_bar,txt], align="center", pad=ppad, sep=sep) 
        offbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,**kwargs)

f = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts\20220317_TRPL_0hr_example_0423bPL2Axis.txt.tif"

import_data = tifffile.imread(f)

total_cts1 = np.sum(import_data,axis=0)
SAVE = 0
OUT_PATH = r''
FNAME = r''

data = total_cts1.copy()

scalebar = 1
scalebar_color = 'white'
px = 10; dist = u"5\u03bcm"

draw_cbar = 1
cbar_txt_size = 16
top_cbar = 0
side_cbar=1

cbar_scale_control = 1; MIN = 0; MAX = 14000
normalize = 0
standardized = 0
sci_notation = 1

unit = u'Intensity (cts/s)'; colormap = 'hot'; 

if normalize == 1:
    #data = data*1e8
    data_norm = (data - data.min()) / (data.max() - data.min())
if standardized == 1:
    mean = np.mean(data)
    std = np.std(data)
    data_stand = (data - mean) / std


plt.figure()
fig, ax = plt.subplots()

if cbar_scale_control == 1:
    im = ax.imshow(data, cmap=colormap, vmax=MAX, vmin=MIN)
if cbar_scale_control == 0: 
    im = ax.imshow(data, cmap=colormap)
if normalize == 1:
    im = ax.imshow(data_norm, cmap=colormap)
if standardized == 1:
    im = ax.imshow(data_stand, cmap=colormap)

ax.axis('off')

# read these coordinates from drawn box in IMageJ: [28,36,28,36],[28,28,36,36]
    # then Image -> Stacks -> Plot Z-axis profile
    # saved the TRPL spectra within these pixels
    #"Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts\0423bPL2Axis_spectrumROI_longDecay1.csv"
ax.add_patch(Rectangle((28, 28), 8, 8, linestyle = 'solid', facecolor="none", ec='w', lw=2))

# read these coordinates from drawn box in IMageJ: [28,36,28,36],[28,28,36,36]
    # then Image -> Stacks -> Plot Z-axis profile
    # saved the TRPL spectra within these pixels
ax.add_patch(Rectangle((26, 37), 8, 8, linestyle = 'dashed', facecolor="none", ec='w', lw=2))

if scalebar == 1:
    ob = AnchoredHScaleBar(size=px, label=dist, loc=4, frameon=False,
                           pad=0.25, borderpad=0.25, sep=4, 
                           linekw=dict(color=scalebar_color))
    ax.add_artist(ob)

if draw_cbar == 1:
    divider = make_axes_locatable(ax)
    if side_cbar == 1:
        # create color bar
        cax = divider.append_axes('right', size='5%', pad=0.1)
        if sci_notation == 1:
            fmt = ticker.ScalarFormatter(useMathText=True)
            fmt.set_powerlimits((1, 0))
            cb = fig.colorbar(im, cax=cax, orientation='vertical',format=fmt)
        else:
            cb = fig.colorbar(im, cax=cax, orientation='vertical')#,format='.1f')
            #get color bar object
        cbar = plt.gcf().axes[-1]
            #format colorbar
        cbar.set_ylabel(unit, rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
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
            fmt = ticker.ScalarFormatter(useMathText=True)
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