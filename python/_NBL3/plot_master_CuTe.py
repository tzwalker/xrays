"""
coding: utf-8

tzwalker
Wed Jan  6 20:23:51 2021

this program is intended to make the base Cu XRF and Te XRF images
XBIC images will be handled separately

it overlays the Cu on the Te XRF, and plots the color bars above the image

the Cu response is quite noisy after masking and will be Gaussian filtered
before overlaying

the XBIC responses should be normalized (max-min stretch) to facilitate
comparison

# change font of labels
#plt.rcParams["font.family"] = "arial"

# experiment with color scales of NBL33 and TS58A

# apply gaussian filter to Cu images before overlaying

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
Cu = NBL31.scan341[1,:,:-2]
Te = NBL31.scan341[3,:,:-2]

# process image
Cu_bs = bs.background_subtraction(Cu, 10)
Cu_gauss = gaussian_filter(Cu_bs, 1)

# threshold image copy (need to copy to avoid overwriting original image)
#Cu1 = Cu.copy()
#Cu1[Cu1<0.16]=np.nan
Cu_gauss1 = Cu_gauss.copy()
Cu_gauss1[Cu_gauss1<0.023]=np.nan

Te1 = Te.copy()
#Te1[Te1<10]=np.nan

fig, ax = plt.subplots(figsize=(2.5, 2.5))

pltTe = ax.imshow(Te1, cmap='bone',
                   vmin=0,vmax=30,
                   alpha=1)

pltCu = ax.imshow(Cu_gauss1, cmap='Oranges_r',
                   vmin=0,vmax=0.1,
                   alpha=0.75)
ax.axis('off')

ob = AnchoredHScaleBar(length=20, label="", loc=2, frameon=False,
                       pad=0.5, borderpad=0.25, sep=4, 
                       linekw=dict(color="white",linewidth=3))
# change facecolor of frameon
#ob.patch.set_facecolor('k')
#ax.add_artist(ob)

divider = make_axes_locatable(ax)

cax = divider.new_vertical(size='5%', pad=0.55)
fig.add_axes(cax)
cbarTe = fig.colorbar(pltTe, cax=cax, orientation='horizontal')
cbarTe.set_label('Te ($\mu$g/cm$^2$)', fontsize=8)
cbarTe.ax.tick_params(labelsize=8)

cax1 = divider.new_vertical(size='5%', pad=0)
fig.add_axes(cax1)
cbarCu = fig.colorbar(pltCu, cax=cax1, orientation='horizontal')
cbarCu.set_label('Cu ($\mu$g/cm$^2$)', fontsize=8)
cbarCu.ax.tick_params(labelsize=8)
cax1.xaxis.set_label_position('top')
cax1.xaxis.set_ticks_position('top')


OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\20210106 figures_semifinals'
FNAME = r'\NBL31scan341_CuTe.eps'
if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)



#%%
Cu = NBL32.scan422[1,:,:-2]
Te = NBL32.scan422[3,:,:-2]

# process image
Cu_bs = bs.background_subtraction(Cu, 10)
Cu_gauss = gaussian_filter(Cu_bs, 1)

# threshold image copy (need to copy to avoid overwriting original image)
#Cu1 = Cu.copy()
#Cu1[Cu1<0.77]=np.nan
Cu_gauss1 = Cu_gauss.copy()
Cu_gauss1[Cu_gauss1<0.25]=np.nan

Te1 = Te.copy()
#Te1[Te1<10]=np.nan

fig, ax = plt.subplots(figsize=(2.5, 2.5))

pltTe = ax.imshow(Te1, cmap='bone',
                   vmin=0,vmax=30,
                   alpha=1)

pltCu = ax.imshow(Cu_gauss1, cmap='Oranges_r',
                   vmin=0,vmax=1,
                   alpha=0.75)
ax.axis('off')

ob = AnchoredHScaleBar(length=20, label="", loc=2, frameon=False,
                       pad=0.5, borderpad=0.25, sep=4, 
                       linekw=dict(color="white",linewidth=3))
#ob.patch.set_facecolor('k')
ax.add_artist(ob)

divider = make_axes_locatable(ax)

cax = divider.new_vertical(size='5%', pad=0.55)
fig.add_axes(cax)
cbarTe = fig.colorbar(pltTe, cax=cax, orientation='horizontal')
cbarTe.set_label('Te ($\mu$g/cm$^2$)', fontsize=8)
cbarTe.ax.tick_params(labelsize=8)


cax1 = divider.new_vertical(size='5%', pad=0)
fig.add_axes(cax1)
cbarCu = fig.colorbar(pltCu, cax=cax1, orientation='horizontal')
cbarCu.set_label('Cu ($\mu$g/cm$^2$)', fontsize=8)
cbarCu.ax.tick_params(labelsize=8)
cax1.xaxis.set_label_position('top')
cax1.xaxis.set_ticks_position('top')

OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\20210106 figures_semifinals'
FNAME = r'\NBL32scan422_CuTe.eps'
if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)
#%%
Cu = NBL33.scan264[1,:,:-2]
Te = NBL33.scan264[3,:,:-2]

# process image
Cu_bs = bs.background_subtraction(Cu, 10)
Cu_gauss = gaussian_filter(Cu_bs, 1)

# threshold image copy (need to copy to avoid overwriting original image)
#Cu1 = Cu.copy()
#Cu1[Cu1<2.9]=np.nan
Cu_gauss1 = Cu_gauss.copy()
Cu_gauss1[Cu_gauss1<0.65]=np.nan

Te1 = Te.copy()
#Te1[Te1<10]=np.nan

fig, ax = plt.subplots(figsize=(2.5, 2.5))

pltTe = ax.imshow(Te1, cmap='bone',
                   vmin=0,vmax=30,
                   alpha=1)

pltCu = ax.imshow(Cu_gauss1, cmap='Oranges_r',
                   vmin=0,vmax=3,
                   alpha=0.75)
ax.axis('off')

ob = AnchoredHScaleBar(length=20, label="", loc=2, frameon=False,
                       pad=0.5, borderpad=0.25, sep=4, 
                       linekw=dict(color="white",linewidth=3))
#ob.patch.set_facecolor('k')
ax.add_artist(ob)

divider = make_axes_locatable(ax)

cax = divider.new_vertical(size='5%', pad=0.55)
fig.add_axes(cax)
cbarTe = fig.colorbar(pltTe, cax=cax, orientation='horizontal')
cbarTe.set_label('Te ($\mu$g/cm$^2$)', fontsize=8)
cbarTe.ax.tick_params(labelsize=8)


cax1 = divider.new_vertical(size='5%', pad=0)
fig.add_axes(cax1)
cbarCu = fig.colorbar(pltCu, cax=cax1, orientation='horizontal')
cbarCu.set_label('Cu ($\mu$g/cm$^2$)', fontsize=8)
cbarCu.ax.tick_params(labelsize=8)
cax1.xaxis.set_label_position('top')
cax1.xaxis.set_ticks_position('top')


OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\20210106 figures_semifinals'
FNAME = r'\NBL33scan264_CuTe.eps'
if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)

#%%

Cu = TS58A.scan386[1,:,:-2]
Te = TS58A.scan386[3,:,:-2]

# process image
Cu_bs = bs.background_subtraction(Cu, 10)
Cu_gauss = gaussian_filter(Cu_bs, 1)

# threshold image copy (need to copy to avoid overwriting original image)
#Cu1 = Cu.copy()
#Cu1[Cu1<0.55]=np.nan
Cu_gauss1 = Cu_gauss.copy()
Cu_gauss1[Cu_gauss1<0.2]=np.nan

Te1 = Te.copy()
#Te1[Te1<10]=np.nan

fig, ax = plt.subplots(figsize=(2.5, 2.5))

pltTe = ax.imshow(Te1, cmap='bone',
                   vmin=0,vmax=30,
                   alpha=1)

pltCu = ax.imshow(Cu_gauss1, cmap='Oranges_r',
                   vmin=0,vmax=1,
                   alpha=0.75)
ax.axis('off')

ob = AnchoredHScaleBar(length=20, label="", loc=2, frameon=False,
                       pad=0.5, borderpad=0.25, sep=4, 
                       linekw=dict(color="white",linewidth=3))
#ob.patch.set_facecolor('k')
ax.add_artist(ob)

divider = make_axes_locatable(ax)

cax = divider.new_vertical(size='5%', pad=0.55)
fig.add_axes(cax)
cbarTe = fig.colorbar(pltTe, cax=cax, orientation='horizontal')
cbarTe.set_label('Te ($\mu$g/cm$^2$)', fontsize=8)
cbarTe.ax.tick_params(labelsize=8)


cax1 = divider.new_vertical(size='5%', pad=0)
fig.add_axes(cax1)
cbarCu = fig.colorbar(pltCu, cax=cax1, orientation='horizontal')
cbarCu.set_label('Cu ($\mu$g/cm$^2$)', fontsize=8)
cbarCu.ax.tick_params(labelsize=8)
cax1.xaxis.set_label_position('top')
cax1.xaxis.set_ticks_position('top')

OUT_PATH = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\20210106 figures_semifinals'
FNAME = r'\TS58Ascan386_CuTe.eps'
if SAVE == 1:
    plt.savefig(OUT_PATH+FNAME, format='eps', dpi=300, bbox_inches='tight', pad_inches = 0)