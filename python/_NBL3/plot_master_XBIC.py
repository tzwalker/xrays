"""
coding: utf-8

tzwalker
Sat Jan  9 18:18:56 2021

this program plots and saves nice figures of the XBIC images for the NBL3 set

these figures will go alongside the Cu XRF and Te XRF
"""

from scipy.ndimage import gaussian_filter
import background_subtraction as bs
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
                              textprops=dict(color="white",size=14))
        self.vpac = offbox.VPacker(children=[size_bar,txt],  
                                 align="center", pad=ppad, sep=sep) 
        offbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, 
                 borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,
                 **kwargs)
SAVE = 0;
# XBIC
img = NBL31.scan341[0,:,:-2]

#scale for proper colorbar
#img = img*1E8

# normalize data using "max-min stretch"
img_norm = (img - img.min()) / (img.max() - img.min())

fig, ax = plt.subplots(figsize=(1.825, 1.825))

pltTe = ax.imshow(img_norm, cmap='inferno')
                   #vmin=1.4,vmax=2)
ax.axis('off')

ob = AnchoredHScaleBar(length=20, label="", loc=2, frameon=False,
                       pad=0.5, borderpad=0.25, sep=4, 
                       linekw=dict(color="white",linewidth=3))
# change facecolor of frameon
#ob.patch.set_facecolor('k')
ax.add_artist(ob)

divider = make_axes_locatable(ax)

cax = divider.new_vertical(size='5%', pad=0.1, pack_start=True)
fig.add_axes(cax)
fmt = ticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))
cbarTe = fig.colorbar(pltTe, cax=cax, orientation='horizontal', format=fmt)
cbarTe.set_label('XBIC (au)', fontsize=8)
cbarTe.ax.tick_params(labelsize=8)
cax.xaxis.set_label_position('bottom')
cax.xaxis.set_ticks_position('bottom')


OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\20210106 figures_semifinals'
FNAME = r'\NBL31scan341_XBIC.eps'
if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)



#%%
img = NBL32.scan422[0,:,:-2]

#scale for nA colorbar
#img = img*1E8

# normalize data using "max-min stretch"
img_norm = (img - img.min()) / (img.max() - img.min())

fig, ax = plt.subplots(figsize=(1.825, 1.825))

pltTe = ax.imshow(img_norm, cmap='inferno')
                   #vmin=2.2,vmax=2.8)
ax.axis('off')

ob = AnchoredHScaleBar(length=20, label="", loc=2, frameon=False,
                       pad=0.5, borderpad=0.25, sep=4, 
                       linekw=dict(color="white",linewidth=3))
# change facecolor of frameon
#ob.patch.set_facecolor('k')
ax.add_artist(ob)

divider = make_axes_locatable(ax)

cax = divider.new_vertical(size='5%', pad=0.1, pack_start=True)
fig.add_axes(cax)
cbarTe = fig.colorbar(pltTe, cax=cax, orientation='horizontal')
cbarTe.set_label('XBIC (au)', fontsize=8)
cbarTe.ax.tick_params(labelsize=8)
cax.xaxis.set_label_position('bottom')
cax.xaxis.set_ticks_position('bottom')

SAVE =0
OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\20210106 figures_semifinals'
FNAME = r'\NBL32scan422_XBIC.eps'
if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)
    
#%%
img = NBL33.scan264[0,:,:-2]

#scale for proper colorbar
#img = img*1E8

# normalize data using "max-min stretch"
img_norm = (img - img.min()) / (img.max() - img.min())

fig, ax = plt.subplots(figsize=(1.825, 1.825))

pltTe = ax.imshow(img_norm, cmap='inferno')
                   #vmin=0.2,vmax=1)
ax.axis('off')

ob = AnchoredHScaleBar(length=20, label="", loc=2, frameon=False,
                       pad=0.5, borderpad=0.25, sep=4, 
                       linekw=dict(color="white",linewidth=3))
# change facecolor of frameon
#ob.patch.set_facecolor('k')
ax.add_artist(ob)

divider = make_axes_locatable(ax)

# =============================================================================
# cax = divider.new_vertical(size='5%', pad=0.1, pack_start=True)
# fig.add_axes(cax)
# cbarTe = fig.colorbar(pltTe, cax=cax, orientation='horizontal')
# cbarTe.set_label('XBIC (au)', fontsize=8)
# cbarTe.ax.tick_params(labelsize=8)
# cax.xaxis.set_label_position('bottom')
# cax.xaxis.set_ticks_position('bottom')
# =============================================================================

SAVE =0
OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\20210106 figures_semifinals'
FNAME = r'\NBL33scan264_XBIC.eps'
if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)

#%%
img = TS58A.scan386[0,:,:-2]

#scale for proper colorbar
#img = img*1E8

# normalize data using "max-min stretch"
img_norm = (img - img.min()) / (img.max() - img.min())

fig, ax = plt.subplots(figsize=(1.825, 1.825))

pltTe = ax.imshow(img_norm, cmap='inferno')
                   #vmin=0.07,vmax=0.1)
ax.axis('off')

ob = AnchoredHScaleBar(length=20, label="", loc=2, frameon=False,
                       pad=0.5, borderpad=0.25, sep=4, 
                       linekw=dict(color="white",linewidth=3))
# change facecolor of frameon
#ob.patch.set_facecolor('k')
ax.add_artist(ob)

divider = make_axes_locatable(ax)

# =============================================================================
# cax = divider.new_vertical(size='5%', pad=0.1, pack_start=True)
# fig.add_axes(cax)
# cbarTe = fig.colorbar(pltTe, cax=cax, orientation='horizontal')
# cbarTe.set_label('XBIC (au)', fontsize=8)
# cbarTe.ax.tick_params(labelsize=8)
# cax.xaxis.set_label_position('bottom')
# cax.xaxis.set_ticks_position('bottom')
# =============================================================================

SAVE =0
OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\20210106 figures_semifinals'
FNAME = r'\TS58Ascan386_XBIC.eps'
if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)