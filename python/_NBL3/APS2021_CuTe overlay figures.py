"""
coding: utf-8

tzwalker
Wed Mar 17 09:34:01 2021
"""


'''adds scalebar to matplotlib images'''

        
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
        txt = offbox.TextArea(label, minimumdescent=False, 
                              textprops=dict(color="white",size=14))
        self.vpac = offbox.VPacker(children=[size_bar,txt],  
                                 align="center", pad=ppad, sep=sep) 
        offbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, 
                 borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,
                 **kwargs)
    
Cu = TS58A.scan386[1,:,:-2]
Te = TS58A.scan386[3,:,:-2]

# process image
#Cu_bs = bs.background_subtraction(Cu, 10)
#Cu_gauss = gaussian_filter(Cu_bs, 1)

# threshold image copy (need to copy to avoid overwriting original image)
plt_Gauss = 0
if plt_Gauss == 0:
    Cu1 = Cu.copy()
    Cu1[Cu1<0.5]=np.nan
    cmin = 0; cmax = 2
if plt_Gauss == 1:
    Cu_gauss1 = Cu_gauss.copy()
    Cu_gauss1[Cu_gauss1<0.63]=np.nan
    cmin = 0; cmax = 3

Te1 = Te.copy()
#Te1[Te1<10]=np.nan

fig, ax = plt.subplots(figsize=(2.5, 2.5))

pltTe = ax.imshow(Te1, cmap='Blues_r',
                   vmin=0,vmax=30,
                   alpha=1)
if plt_Gauss == 0:
    pltCu = ax.imshow(Cu1, cmap='Oranges_r',
                       vmin=cmin,vmax=cmax,
                       alpha=0.75)
if plt_Gauss == 1:
    pltCu = ax.imshow(Cu_gauss1, cmap='Oranges_r',
                       vmin=cmin,vmax=cmax,
                       alpha=0.5)
ax.axis('off')

ob = AnchoredHScaleBar(size=20, label="", loc=2, frameon=False,
                       pad=0.5, borderpad=0.25, sep=4, 
                       linekw=dict(color="white",linewidth=3))
#ob.patch.set_facecolor('k')
#ax.add_artist(ob)

divider = make_axes_locatable(ax)

cax = divider.append_axes('right', size='5%', pad=0.55)
fig.add_axes(cax)
cbarTe = fig.colorbar(pltTe, cax=cax, orientation='vertical')
cbarTe.set_label('Te ($\mu$g/cm$^2$)', fontsize=8)
cbarTe.ax.tick_params(labelsize=8)
cax.yaxis.set_label_position('left')
cax.yaxis.set_ticks_position('left')


cax1 = divider.append_axes('right', size='5%', pad=0)
fig.add_axes(cax1)
cbarCu = fig.colorbar(pltCu, cax=cax1, orientation='vertical')
cbarCu.set_label('Cu ($\mu$g/cm$^2$)', fontsize=8)
cbarCu.ax.tick_params(labelsize=8)


#%%
import numpy as np
import matplotlib.pyplot as plt


Cu = NBL33.scan264[1,:,:-2]
Te = NBL33.scan264[3,:,:-2]

# process image
Cu_bs = bs.background_subtraction(Cu, 10)
Cu_gauss = gaussian_filter(Cu_bs, 1)

# threshold image copy (need to copy to avoid overwriting original image)
plt_Gauss = 0
if plt_Gauss == 0:
    Cu1 = Cu.copy()
    Cu1[Cu1<2.92]=np.nan
    cmin = 0; cmax = 5
if plt_Gauss == 1:
    Cu_gauss1 = Cu_gauss.copy()
    Cu_gauss1[Cu_gauss1<0.63]=np.nan
    cmin = 0; cmax = 3

Te1 = Te.copy()
#Te1[Te1<10]=np.nan

fig, ax = plt.subplots(figsize=(2.5, 2.5))

pltTe = ax.imshow(Te1, cmap='Blues_r',
                   vmin=10,vmax=50,
                   alpha=1)
if plt_Gauss == 0:
    pltCu = ax.imshow(Cu1, cmap='Oranges_r',
                       vmin=cmin,vmax=cmax,
                       alpha=0.75)
if plt_Gauss == 1:
    pltCu = ax.imshow(Cu_gauss1, cmap='Oranges_r',
                       vmin=cmin,vmax=cmax,
                       alpha=0.5)
ax.axis('off')

ob = AnchoredHScaleBar(length=20, label="", loc=2, frameon=False,
                       pad=0.5, borderpad=0.25, sep=4, 
                       linekw=dict(color="white",linewidth=3))
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
