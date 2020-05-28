"""
coding: utf-8

tzwalker
Wed May 13 15:31:19 2020
"""

'''adds scalebar to matplotlib images'''
import matplotlib.pyplot as plt

import matplotlib.offsetbox as offbox
from matplotlib.lines import Line2D

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
        vline1 = Line2D([0,0],[-extent/2.,extent/2.], **linekw)
        vline2 = Line2D([size,size],[-extent/2.,extent/2.], **linekw)
        size_bar.add_artist(line)
        size_bar.add_artist(vline1)
        size_bar.add_artist(vline2)
        txt = offbox.TextArea(label, minimumdescent=False, 
                              textprops=dict(color="black"))
        self.vpac = offbox.VPacker(children=[size_bar,txt],  
                                 align="center", pad=ppad, sep=sep) 
        offbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, 
                 borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,
                 **kwargs)

data = TS1181A.scan197[0,:,:]
data1 = data.copy()
data1 = data1*1E12
plt.figure()

fig, ax = plt.subplots()
im = ax.imshow(data1, cmap='inferno')
ax.axis('off')

ob = AnchoredHScaleBar(size=20, label="10 um", loc=4, frameon=False,
                       pad=0.05,sep=4, 
                       linekw=dict(color="black"))
ax.add_artist(ob)

# create color bar
from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='5%', pad=0.1)
fig.colorbar(im, cax=cax, orientation='vertical')

# format colorbar
# get color bar object
cbar = plt.gcf().axes[-1]
# format colorbar
cbar.set_ylabel('pA', rotation=90, va="bottom", size=10, labelpad=15)
# change colorbar tick label sizes
#cbar.tick_params(labelsize=cbar_ticklbl_size)   
# change color bar scale label size, e.g. 1e-8
#cbar.yaxis.get_offset_text().set(size=14)
# change color bar scale label position   
#cbar.yaxis.set_offset_position('left')

