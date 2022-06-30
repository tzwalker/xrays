# -*- coding: utf-8 -*-
"""

Trumann
Wed Jun 29 16:11:06 2022

this program plots the TRPL data from PVSe33.3_2 and PVSe33.4_3

"""

import matplotlib.pyplot as plt
import matplotlib.offsetbox as offbox
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
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

#f = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts\20220317_TRPL_0hr_example_0423bPL2Axis.txt.tif"
f = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts\20220410_TRPL_500hr_example_0423ePL2Axis.txt.tif"
import_data = tifffile.imread(f)

total_cts1 = np.sum(import_data,axis=0)
SAVE = 0
OUT_PATH = r''
FNAME = r''

data = total_cts1.copy()

scalebar_color = 'white'
px = 10; dist = u"2.4\u03bcm"

cbar_txt_size = 11

unit = u'Intensity (cts/s)'

fig, ax = plt.subplots()

im = ax.imshow(data, cmap='Greens_r', vmin=2000, vmax=14000)

ax.axis('off')

ob = AnchoredHScaleBar(size=px, label=dist, loc=4, frameon=False,
                       pad=0.25, borderpad=0.25, sep=4, 
                       linekw=dict(color=scalebar_color))
ax.add_artist(ob)

# format colorbar
cax1 = fig.add_axes([ax.get_position().x1+0.025,ax.get_position().y0,0.025,ax.get_position().height])
fmt = ticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))

cbar = fig.colorbar(im, cax=cax1, orientation='vertical',format=fmt)
cbar.ax.set_ylabel(unit, rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
#cbar.locator_params(nbins=4)
cbar.ax.tick_params(labelsize=cbar_txt_size)
cbar.ax.yaxis.get_offset_text().set(size=cbar_txt_size)
cbar.ax.yaxis.set_offset_position('left')

# read these coordinates from drawn box in IMageJ: [28,36,28,36],[28,28,36,36]
    # then Image -> Stacks -> Plot Z-axis profile
    # saved the TRPL spectra within these pixels
    #"Dropbox (ASU)\1_PVSe33 ex-situ\DATA\TRPL\20220317_datacube_txts\0423bPL2Axis_spectrumROI_longDecay1.csv"
#ax.add_patch(Rectangle((28, 28), 8, 8, linestyle = 'solid', facecolor="none", ec='w', lw=2))

# read these coordinates from drawn box in IMageJ: [28,36,28,36],[28,28,36,36]
    # then Image -> Stacks -> Plot Z-axis profile
    # saved the TRPL spectra within these pixels
#ax.add_patch(Rectangle((26, 37), 8, 8, linestyle = 'dashed', facecolor="none", ec='w', lw=2))

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)