"""
coding: utf-8

tzwalker
Thu Nov 18 20:49:20 2021

this program is for normalizing the XBIC channel to the us_ic
at 20C and 80C

it was run after creating csvs in "XBIC-translate-and-deltas.py"

XBIC
20C: scan0323
80C: scan0339

"""
import numpy as np

# specificy path to csvs
PATH_IN = r'C:\Users\triton\Dropbox (ASU)\2_FS_operando\XBIC aligned image csvs\stage paper'
scans = [323,339]
scans1 = [str(s) for s in scans]

# import aligned XBIC maps
XBIC = []
for S in scans1:
    FNAME = r'\FS3_scan{SCN}_XBIC.csv'.format(SCN=S)
    IMG = np.genfromtxt(PATH_IN+FNAME, delimiter=',')
    XBIC.append(IMG)

US_IC = []
for S in scans1:
    FNAME = r'\FS3_scan{SCN}_us_ic.csv'.format(SCN=S)
    IMG = np.genfromtxt(PATH_IN+FNAME, delimiter=',')
    US_IC.append(IMG)

norm_20 = XBIC[0] / US_IC[0]
norm_80 = XBIC[1] / US_IC[1]

#%%

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.offsetbox as offbox
from matplotlib.lines import Line2D
from matplotlib import ticker

'''adds scalebar to matplotlib images'''
class AnchoredHScaleBar(offbox.AnchoredOffsetbox):
    """ size: length of bar in pixels
        extent : height of bar ends in axes units """
    def __init__(self, length=1, extent = 0.03, label="", loc=2, ax=None,
                 pad=0.4, borderpad=0.5, ppad = 0, sep=2, prop=None, 
                 frameon=True, linekw={}, **kwargs):
        if not ax:
            ax = plt.gca()
        trans = ax.get_xaxis_transform()
        size_bar = offbox.AuxTransformBox(trans)
        line = Line2D([0,length],[0,0], **linekw)
        #vline1 = Line2D([0,0],[-extent/2.,extent/2.], **linekw)
        #vline2 = Line2D([size,size],[-extent/2.,extent/2.], **linekw)
        size_bar.add_artist(line)
        #size_bar.add_artist(vline1)
        #size_bar.add_artist(vline2)
        txt = offbox.TextArea(label, minimumdescent=False, 
                              textprops=dict(color="black",size=8))
        self.vpac = offbox.VPacker(children=[size_bar,txt],  
                                 align="center", pad=ppad, sep=sep) 
        offbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, 
                 borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,
                 **kwargs)
SAVE = 1

img = norm_80

fig, ax = plt.subplots(figsize=(1.8,3.6))

pltTe = ax.imshow(img, cmap='afmhot', vmin=1.6,vmax=2.1)
ax.axis('off')


ob = AnchoredHScaleBar(length=67, label="", loc=2, frameon=False,
                       pad=0.1, borderpad=0.25, sep=-1, 
                       linekw=dict(color="black",linewidth=3))

ax.add_artist(ob)

divider = make_axes_locatable(ax)

cax = divider.new_vertical(size='5%', pad=0.1)
fig.add_axes(cax)

cbarTe = fig.colorbar(pltTe, cax=cax, orientation='horizontal')
#cbarTe.set_label('XBIC (arb. unit)', fontsize=8)
cbarTe.ax.tick_params(labelsize=8)
cbarTe.ax.locator_params(nbins=5)
cax.xaxis.set_label_position('top')
cax.xaxis.set_ticks_position('top')


OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\0_stage design\20211114 figures_v2\figure5 materials'
FNAME = r'\FS3_scan339_XBICnormToUSIC.eps'

if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)
