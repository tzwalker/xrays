"""
coding: utf-8
Trumann
Thu Feb  3 16:48:02 2022

plotting nicer XBIC that matches what's in the presentation
"""

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.offsetbox as offbox
from matplotlib.lines import Line2D

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
        txt = offbox.TextArea(label, 
                              textprops=dict(color="white",size=cbar_txt_size))
        self.vpac = offbox.VPacker(children=[size_bar,txt],  
                                 align="center", pad=ppad, sep=sep) 
        offbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, 
                 borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,
                 **kwargs)
    
XBIC = NBL32.scan422[0,:,:-2]

PERCENTILE = 80
cbar_txt_size = 16

# threshold image copy (need to copy to avoid overwriting original image)
XBIC_norm = XBIC.copy()

XBIC_norm = XBIC_norm/ XBIC_norm.max()
fig, ax = plt.subplots(figsize=(4, 4))

pltTe = ax.imshow(XBIC_norm, cmap='magma',
                   alpha=1, vmin=0.75, vmax=1)



ax.axis('off')

ob = AnchoredHScaleBar(length=20, label="3um", loc=4, frameon=False,
                       pad=0.5, borderpad=0.25, sep=4, 
                       linekw=dict(color="white",linewidth=3))

ax.add_artist(ob)

divider = make_axes_locatable(ax)

cax = divider.append_axes('right', size='5%', pad=0.1)
fig.add_axes(cax)
cbarTe = fig.colorbar(pltTe, cax=cax, orientation='vertical')
cbarTe.set_label('XBIC (arb. unit)', fontsize=cbar_txt_size)
cbarTe.ax.tick_params(labelsize=cbar_txt_size)
cax.yaxis.set_label_position('right')
cax.yaxis.set_ticks_position('right')


#%%
XBIC = TS58A.scan386[0,:,:-2]

PERCENTILE = 80
cbar_txt_size = 14

# threshold image copy (need to copy to avoid overwriting original image)
XBIC_norm = XBIC.copy()

XBIC_norm = XBIC_norm/ XBIC_norm.max()
fig, ax = plt.subplots(figsize=(4, 4))

pltTe = ax.imshow(XBIC_norm, cmap='magma',
                   alpha=1, vmin=0.75, vmax=1)



ax.axis('off')

ob = AnchoredHScaleBar(length=20, label="3um", loc=4, frameon=False,
                       pad=0.5, borderpad=0.25, sep=4, 
                       linekw=dict(color="white",linewidth=3))

ax.add_artist(ob)

divider = make_axes_locatable(ax)

cax = divider.append_axes('right', size='5%', pad=0.1)
fig.add_axes(cax)
cbarTe = fig.colorbar(pltTe, cax=cax, orientation='vertical')
cbarTe.set_label('XBIC (arb. unit)', fontsize=cbar_txt_size)
cbarTe.ax.tick_params(labelsize=cbar_txt_size)
cax.yaxis.set_label_position('right')
cax.yaxis.set_ticks_position('right')