# -*- coding: utf-8 -*-
"""

Trumann
Mon Apr 18 15:05:57 2022

run main-TS118_1A-ASCII.py before this program
    use class def 'import_planmaps()'

this program was used to get the larger map in figure 1 of paper
2022 04 19
this program is meant to draw horizonatl lines and vertical lines 
on plan-view overview scan 197
    it saves the data from the hlines
    the vline data was just copied from the variable

it is meant as an alternative to the xy spatial extent figure

"""

import matplotlib.pyplot as plt
import matplotlib.offsetbox as offbox
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.lines import Line2D
from matplotlib import ticker
from matplotlib.patches import Rectangle

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

        txt = offbox.TextArea(label, textprops=dict(color=scalebar_color,weight='bold',size=cbar_txt_size))
        self.vpac = offbox.VPacker(children=[size_bar,txt], align="center", pad=ppad, sep=sep)
        
        offbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, 
                 borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,
                 **kwargs)

import numpy as np

SAVE = 0
OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\1_XBIC_decay\figures v1\figure1 materials'
FNAME = r'\TS118_1A_scan197_XBIC_v2.eps'

# horizontal line indices
drawline1_idx = 30
drawline2_idx = 70

# vertical line index
drawline3_idx = 30

scalebar_color = 'black'
# SET SCALE BAR
px = 20; dist = u'10\u00B5m'

cbar_txt_size = 11

unit = 'XBIC (nA)'; colormap='inferno'

img = TS1181A.scan197[0,:,:]
data = img.copy()
data = data * 1e9


plt.figure()
fig, ax = plt.subplots(figsize=(3.4,5.65))

im = ax.imshow(data, cmap=colormap)


ax.axis('off')
ob = AnchoredHScaleBar(size=px, label=dist, loc=4, frameon=False,
                       pad=0.1, borderpad=0.5, sep=4, 
                       linekw=dict(color=scalebar_color))
ax.add_artist(ob)

# =============================================================================
# # plot 'meta' data - lines and indices
# # scan 197 indices for spots in zoom in maps
# plt.scatter([27,28,35], [69,76,70], marker='+', s=50, color='white')
# plt.scatter([33,22,25], [28,22,32], marker='x', s=50, color='white')
# =============================================================================

# plot horizontla lines
plt.axhline(drawline1_idx, color='w',linestyle=':',linewidth=1)
plt.axhline(drawline2_idx, color='w',linestyle=':',linewidth=1)
# plot vertical line lines
plt.axvline(drawline3_idx, color='w',linestyle=':',linewidth=1)

# plot smaller area outlines
# these indices were taken from Sheet2 in
# C:\Users\Trumann\Dropbox (ASU)\1_XBIC_decay\positions in small plan view and large plan view maps.xlsx
ax.add_patch(Rectangle((20, 20), 20, 20, linestyle = 'dashed', facecolor="none", ec='w', lw=1))
ax.add_patch(Rectangle((20, 60), 20, 20, linestyle = 'dashed', facecolor="none", ec='w', lw=1))

# create color bar
divider = make_axes_locatable(ax)

cax = divider.append_axes('right', size='5%', pad=0.1)
fmt = ticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))
cb = fig.colorbar(im, cax=cax, orientation='vertical',format=fmt)
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


if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)

drawline1_data = TS1181A.scan197[0,drawline1_idx,:].reshape(-1,1)
drawline2_data = TS1181A.scan197[0,drawline2_idx,:].reshape(-1,1)
drawline3_data = TS1181A.scan197[0,:,drawline3_idx].reshape(-1,1)

merge = np.concatenate((drawline1_data,drawline2_data),axis=1)
FNAME = r"C:\Users\Trumann\Dropbox (ASU)\1_XBIC_decay\DATA\scan197_hlines.csv"
#np.savetxt(FNAME, merge, delimiter=',')