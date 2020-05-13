"""
coding: utf-8

tzwalker
Wed May 13 15:31:19 2020
"""

'''adds scalebar to matplotlib images'''
from mpl_toolkits.axes_grid1 import make_axes_locatable
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
                              textprops=dict(color="white"))
        self.vpac = offbox.VPacker(children=[size_bar,txt],  
                                 align="center", pad=ppad, sep=sep) 
        offbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, 
                 borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,
                 **kwargs)

data = XRF_or_XBIC_2d_array_map
data1 = data.copy()
plt.figure()

fig, ax = plt.subplots()
im = ax.imshow(data1, cmap='inferno', vmax=0.007906, vmin=0.001245)
ax.axis('off')

ob = AnchoredHScaleBar(size=100, label="10 um", loc=4, frameon=False,
                       pad=0.6,sep=4, 
                       linekw=dict(color="white"))
ax.add_artist(ob)

#divider = make_axes_locatable(ax)
#cax = divider.append_axes('right', size='5%', pad=0.1)
#fig.colorbar(im, cax=cax, orientation='vertical')