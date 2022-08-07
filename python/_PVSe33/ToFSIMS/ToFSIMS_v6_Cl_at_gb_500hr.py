# -*- coding: utf-8 -*-
"""

Trumann
Thu Jul 21 09:52:55 2022

this program processes the quantified Cl map and generates a GB mask from it

this v6 version integrated the quaantified Cl map over a different depth than
the v5 program
    this was done since the 500hr cell has a different thickness than the 0hr cell
    the grains near the Au interface would be larger in the 500hr cell than the 0hr cell

the depth step for 500hr cell was 0.135um
this implies 8 indices are about 1.080um of the layer, comparable to the depth
    probed in the 0hr chlroine-at-grain-boundary analysis v5

pretty much only ran first cell to get image with same colorscale as in dissertation
    this file is mostly meant to generate supplmentary images
    
"""

import cv2
from skimage import io
import matplotlib.pyplot as plt
import numpy as np

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

PATH_TOF = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Cl_maps_quantified.tif"

# import ToF-SIMS image
TOF = io.imread(PATH_TOF)

# added indices to probe different depths of the CdSeTe
#TOF_slice = TOF[1+32:9+32,:,:].sum(axis=0)

# comparable distance from TCO - notes.ppt
TOF_slice = TOF[44-15-8:44-15,:,:].sum(axis=0)

# alter image to match EBSD in EBSD_v1.py
img = np.rot90(TOF_slice, k=1)   # rotate image
img = np.flipud(img)                # flip along horizontal axis
#img = rotate_image(img, -3)         # rotate altered image

# crop image to about same dimension as EBSD
#img = img[75:425,100:450]
plt.figure(figsize=(10,10))
plt.imshow(img,vmin=1e18,vmax=4.5e19)
plt.axis("off")
#%%
# manually mask FIB marks
img2 = img.copy()
# for cropped image
# =============================================================================
# img2[10:50,10:50] = np.nan      # top-left
# img2[10:50,300:340] = np.nan    # top-right
# img2[290:330,10:50] = np.nan    # bottom-left
# img2[290:330,300:340] = np.nan  # bottom-right
# =============================================================================

# for full image
img2[100:140,135:175] = np.nan      # top-left
img2[110:150,415:455] = np.nan    # top-right
img2[380:420,130:170] = np.nan    # bottom-left
img2[385:425,415:455] = np.nan  # bottom-right

plt.figure(figsize=(10,10))
plt.imshow(img2,vmin=1e18,vmax=4.5e19)
#plt.axis("off")
#%%
# threshold
img3 = img2.copy()

# normalize so thresholding is easier
#img3[np.where(img3<3.5e19)] = 0
#img3[np.where(img3>2)] = 0

plt.figure(figsize=(10,10))
plt.imshow(img3)#,vmin=1e18,vmax=8.5e19)

#%%
# gaussian blur 5 times
img4 = img3.copy()
img4 = cv2.GaussianBlur(img4,(5,5),cv2.BORDER_DEFAULT)
img4 = cv2.GaussianBlur(img4,(5,5),cv2.BORDER_DEFAULT)
img4 = cv2.GaussianBlur(img4,(5,5),cv2.BORDER_DEFAULT)
img4 = cv2.GaussianBlur(img4,(5,5),cv2.BORDER_DEFAULT)
img4 = cv2.GaussianBlur(img4,(5,5),cv2.BORDER_DEFAULT)

plt.figure(figsize=(10,10))
plt.imshow(img4)

#%%
# create mask from blurred image
img_msk = img4.copy()

high = np.nanmax(img_msk)
low = np.nanmax(img_msk)/6
(thresh, img_msk) = cv2.threshold(img_msk, low, 255, cv2.THRESH_BINARY)

plt.figure(figsize=(10,10))
plt.imshow(img_msk)

#%%
# skeletonize
img5 = img_msk.copy().astype('uint8')

from skimage import morphology

check = 0
if check ==1:
    # check distirbution of pixels in the mask over 50 iterations
    counts = []
    check_idx = list(np.arange(0,51,1))
    for i in check_idx:
        out = morphology.medial_axis(img5)
        #plt.imshow(out,vmax=0.5)
        #plt.axis("off")
        counts.append(np.count_nonzero(out))
        #print(np.count_nonzero(out))
    counts = np.array(counts)
    rng = counts.max() - counts.min()

out1 = morphology.medial_axis(img5)

num = np.count_nonzero(out1)
print("number of pixels in the mask: {s}".format(s=str(num)))

plt.figure(figsize=(10,10))
plt.imshow(out1)

#%%
# get Cl count at grain boundaries and build histogram
Cl = img.copy()
gb = out.copy()

val = Cl*gb
#plt.imshow(val,vmax=0.5)

valarr1 = val.copy().astype('float64')
valarr1[valarr1==0] = np.nan
valarr1 = valarr1.ravel()

#%%
# -*- coding: utf-8 -*-
"""

this section plots the mask from the image processing above on top of 
the quantified Cl image 

"""

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as mticker
import numpy as np
import matplotlib.offsetbox as offbox
from matplotlib.lines import Line2D

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
show_mask = 1
unit = 'Cl (atom/cm3)'
cbar_txt_size = 11
scalebar_color = 'white'

from skimage import io

# convert mask
out1 = out1.astype('uint8')
# generate masked array for plotting purposes
masked_data = np.ma.masked_where(out1==0, out1)

# Overlay the two images
if SAVE == 1:
    fig, ax = plt.subplots(figsize=(2.5,2.5))
else:
    fig, ax = plt.subplots(figsize=(10,10))

# SET MASK CONDITION SO IT CAN DISPLAY EASILY
if show_mask == 0:
    im = ax.imshow(img, cmap='viridis',vmin=1e18,vmax=4.5e19,interpolation='none')

    ob = AnchoredHScaleBar(length=172, label=u"25\u03BCm", loc=3, frameon=False,
                           pad=0.5, borderpad=0.25, sep=4, 
                           linekw=dict(color=scalebar_color,linewidth=1.5))
    # change facecolor of frameon
    #ob.patch.set_facecolor('k')
    ax.add_artist(ob)
    
if show_mask == 1:
    im = ax.imshow(img, cmap='viridis',vmin=1e18,vmax=4.5e19,interpolation='none')
    ax.imshow(masked_data, cmap='Greys_r',vmin=0.5,interpolation='none')

ax.axis('off')

# define colorbar format
fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))
cax1 = fig.add_axes([ax.get_position().x1+0.025,ax.get_position().y0,0.025,ax.get_position().height])

cbar = fig.colorbar(im,cax=cax1,format=fmt)
cbar.ax.set_ylabel('Cl (atom/cm$^3$)', rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
cbar.ax.tick_params(labelsize=cbar_txt_size)
#cbar.yaxis.(labelsize=18)
cbar.ax.yaxis.set_offset_position('left')
cbar.ax.yaxis.offsetText.set(size=cbar_txt_size)

# =============================================================================
# #format and add colorbar
# fig.colorbar(im, format=fmt,cax=cax1)
# #color bar labels
# cbar = plt.gcf().axes[-1]
# cbar.set_ylabel(unit, rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
#     #change color bar scale label position 
# cbar.yaxis.set_offset_position('left')
# =============================================================================

if SAVE == 1:
    if show_mask == 0:
        OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_tof_sims'
        FNAME = r'\for_GB_fig_500hr_Cl_quantmap.pdf'
        plt.savefig(OUT_PATH+FNAME, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)
    if show_mask == 1:
        OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_tof_sims'
        FNAME = r'\for_GB_fig_500hr_Cl_quantmap_masked.png'
        plt.savefig(OUT_PATH+FNAME, format='png', dpi=300, bbox_inches='tight', pad_inches = 0)

