# -*- coding: utf-8 -*-
"""

Trumann
Tue Aug  9 18:47:45 2022

this program plots an integration from the Au side,
and integration from the TCO side
and the mask associated with the TCO-side integration

the intent is to compare the integrations from different sides
of CdTe layers that have different thicknesses

in this case the unaged cell has a thinner layer than the aged cell

only quantified Cl density maps are used

for TCO-side integration, the indices were identified and recorded in notes.pptx

"""

from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import LogNorm
from matplotlib.gridspec import GridSpec
import matplotlib.offsetbox as offbox
from matplotlib.lines import Line2D

def match_EBSD_orientation(array):
    transformed = np.rot90(array, k=1)   # rotate image
    transformed = np.flipud(transformed)                # flip along horizontal axis
    return transformed
    
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
        txt = offbox.TextArea(label, 
                              textprops=dict(color=scalebar_color,size=cbar_txt_size))
        self.vpac = offbox.VPacker(children=[size_bar,txt],  
                                 align="center", pad=ppad, sep=sep) 
        offbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, 
                 borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,
                 **kwargs)



SAVE = 0
file1 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Cl_maps_quantified.tif"
file2 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Cl_maps_quantified.tif"

cbar_txt_size = 11
lower = 1e18 ; upper = 4.5e19
scalebar_color = 'white'

# import ToF-SIMS images
imgs1 = io.imread(file1)
imgs2 = io.imread(file2)

# integrate near Au side, exclude index 0 since it has artifacts
img1 = imgs1[1:10,:,:].sum(axis=0)
img1 = match_EBSD_orientation(img1)
img2 = imgs2[1:10,:,:].sum(axis=0)
img2 = match_EBSD_orientation(img2)

# integrate near TCO side, taken from v6_Cl_at_gb
img3 = imgs1[39-18-9:39-18,:,:].sum(axis=0)
img3 = match_EBSD_orientation(img3)
img4 = imgs2[44-15-8:44-15,:,:].sum(axis=0)
img4 = match_EBSD_orientation(img4)

# get masks from TCO-side integration
    # run "v6_0hr" and "v6_500hr" to process masks
    # these should have the orientation of the EBSD already
mask0 = masked_data0.copy()
mask500 = masked_data500.copy()
#%%
fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6)) = plt.subplots(figsize=((8,8)), nrows=3,ncols=2, sharex=True,sharey=True)

# add data to figure
im1 = ax1.imshow(img1, vmin=lower, vmax=upper,interpolation='none')
im2 = ax2.imshow(img2, vmin=lower, vmax=upper,interpolation='none')
im3 = ax3.imshow(img3, vmin=lower, vmax=upper,interpolation='none')
im4 = ax4.imshow(img4, vmin=lower, vmax=upper,interpolation='none')
im5 = ax5.imshow(img3, vmin=lower, vmax=upper,interpolation='none')
ax5.imshow(mask0, cmap='Greys_r', vmin=0.5, interpolation='none')
im6 = ax6.imshow(img4, vmin=lower, vmax=upper,interpolation='none')
ax6.imshow(mask500, cmap='Greys_r', vmin=0.5, interpolation='none')

# disable axis ticklabels
for ax in fig.axes:
    ax.axis('off')

# add scale bar to first axis
ob = AnchoredHScaleBar(length=172, label=u"25\u03BCm", loc=3, frameon=False,
                       pad=0.5, borderpad=0.25, sep=4, 
                       linekw=dict(color=scalebar_color,linewidth=1.5))
ax1.add_artist(ob)

# add colorbar to plots in right column

# define colorbar format
fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))

# add color bar to plots in right column
cax2 = fig.add_axes([ax2.get_position().x1-0.06,ax2.get_position().y0,0.015,ax2.get_position().height])
cbar2 = fig.colorbar(im2,cax=cax2,format=fmt)
cbar2.ax.set_ylabel('Cl (atom/cm$^3$)', rotation=90, va="bottom", size=cbar_txt_size, labelpad=25)
cbar2.ax.tick_params(labelsize=cbar_txt_size)
cbar2.ax.yaxis.set_offset_position('left')
cbar2.ax.yaxis.offsetText.set(size=cbar_txt_size)

# add color bar to plots in right column
cax4 = fig.add_axes([ax4.get_position().x1-0.06,ax4.get_position().y0,0.015,ax4.get_position().height])
cbar4 = fig.colorbar(im4,cax=cax4,format=fmt)
cbar4.ax.set_ylabel('Cl (atom/cm$^3$)', rotation=90, va="bottom", size=cbar_txt_size, labelpad=25)
cbar4.ax.tick_params(labelsize=cbar_txt_size)
cbar4.ax.yaxis.set_offset_position('left')
cbar4.ax.yaxis.offsetText.set(size=cbar_txt_size)

# add color bar to plots in right column
cax6 = fig.add_axes([ax6.get_position().x1-0.06,ax6.get_position().y0,0.015,ax6.get_position().height])
cbar2 = fig.colorbar(im6,cax=cax6,format=fmt)
cbar2.ax.set_ylabel('Cl (atom/cm$^3$)', rotation=90, va="bottom", size=cbar_txt_size, labelpad=25)
cbar2.ax.tick_params(labelsize=cbar_txt_size)
cbar2.ax.yaxis.set_offset_position('left')
cbar2.ax.yaxis.offsetText.set(size=cbar_txt_size)

#plt.tight_layout()
plt.subplots_adjust(wspace=-0.5, hspace=0.1)

if SAVE == 1:
    OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_tof_sims'
    FNAME = r'\PVSe33_ToF_Cl_bothSides2.png'
    plt.savefig(OUT_PATH+FNAME, format='png', dpi=300, bbox_inches='tight', pad_inches = 0)
