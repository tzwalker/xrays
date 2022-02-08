"""
coding: utf-8
Trumann
Thu Feb  3 16:48:02 2022

plotting Cu on Te XRF for comprehensive; i wanted the scalebar on the side...
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
                              textprops=dict(color="white",size=14))
        self.vpac = offbox.VPacker(children=[size_bar,txt],  
                                 align="center", pad=ppad, sep=sep) 
        offbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, 
                 borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,
                 **kwargs)
    
Cu = NBL32.scan422[1,:,:-2]
Te = NBL32.scan422[3,:,:-2]

PERCENTILE = 80
cbar_txt_size = 11

# threshold image copy (need to copy to avoid overwriting original image)
Cu1 = Cu.copy()
bound = np.percentile(Cu1, PERCENTILE)
Cu1[Cu1<bound]=np.nan
#Cu1[Cu1<2.9]=np.nan

Te1 = Te.copy()
#Te1[Te1<10]=np.nan

fig, ax = plt.subplots(figsize=(4, 4))

pltTe = ax.imshow(Te1, cmap='bone',
                   alpha=1, vmin=0, vmax=1500)

pltCu = ax.imshow(Cu1, cmap='Oranges_r',
                   alpha=0.75, vmin=0, vmax=2000, interpolation='none')

ax.axis('off')

ob = AnchoredHScaleBar(length=20, label="3um", loc=4, frameon=False,
                       pad=0.5, borderpad=0.25, sep=4, 
                       linekw=dict(color="white",linewidth=3))

ax.add_artist(ob)

divider = make_axes_locatable(ax)

cax = divider.append_axes('right', size='5%', pad=0.75)
fig.add_axes(cax)
cbarTe = fig.colorbar(pltTe, cax=cax, orientation='vertical')
cbarTe.set_label('Te (cts/s)', fontsize=cbar_txt_size)
cbarTe.ax.tick_params(labelsize=cbar_txt_size)
cax.yaxis.set_label_position('left')
cax.yaxis.set_ticks_position('left')


cax1 = divider.append_axes('right', size='5%', pad=0)
fig.add_axes(cax1)
cbarCu = fig.colorbar(pltCu, cax=cax1, orientation='vertical')
cbarCu.set_label('Cu (cts/s)', fontsize=cbar_txt_size)
cbarCu.ax.tick_params(labelsize=cbar_txt_size)


#%%
Cu = TS58A.scan386[1,:,:-2]
Te = TS58A.scan386[3,:,:-2]

PERCENTILE = 80
cbar_txt_size = 11

# threshold image copy (need to copy to avoid overwriting original image)
Cu1 = Cu.copy()
bound = np.percentile(Cu1, PERCENTILE)
Cu1[Cu1<bound]=np.nan
#Cu1[Cu1<2.9]=np.nan

Te1 = Te.copy()
#Te1[Te1<10]=np.nan

fig, ax = plt.subplots(figsize=(4, 4))

pltTe = ax.imshow(Te1, cmap='bone',
                   alpha=1, vmin=0, vmax=1500)

pltCu = ax.imshow(Cu1, cmap='Oranges_r',
                   alpha=0.75, vmin=0, vmax=2000, interpolation='none')

ax.axis('off')

ob = AnchoredHScaleBar(length=20, label="3um", loc=4, frameon=False,
                       pad=0.5, borderpad=0.25, sep=4, 
                       linekw=dict(color="white",linewidth=3))

ax.add_artist(ob)

divider = make_axes_locatable(ax)

cax = divider.append_axes('right', size='5%', pad=0.75)
fig.add_axes(cax)
cbarTe = fig.colorbar(pltTe, cax=cax, orientation='vertical')
cbarTe.set_label('Te (cts/s)', fontsize=cbar_txt_size)
cbarTe.ax.tick_params(labelsize=cbar_txt_size)
cax.yaxis.set_label_position('left')
cax.yaxis.set_ticks_position('left')


cax1 = divider.append_axes('right', size='5%', pad=0)
fig.add_axes(cax1)
cbarCu = fig.colorbar(pltCu, cax=cax1, orientation='vertical')
cbarCu.set_label('Cu (cts/s)', fontsize=cbar_txt_size)
cbarCu.ax.tick_params(labelsize=cbar_txt_size)
