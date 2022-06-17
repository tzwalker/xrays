# -*- coding: utf-8 -*-
"""

Trumann
Wed Jun  8 15:27:48 2022

this program is meant to replicate the ImageJ procedure seen in
"Z\Trumann\Tutorial Videos\20220607_PVSe33_0hr_Cl_GBmask.mp4"

i don't need to rotate it since i will not use the images produced
in registration against the EBSD image (at least not yet)

20220608 this prgram is only meant for the 0hr images
    the FIB marks are manually masked and this mask position
    will be different for the 500hr images

"""

import cv2
from skimage import io,transform
import matplotlib.pyplot as plt
import numpy as np

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

PATH_TOF = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Cl_maps.tif"

# import ToF-SIMS image
TOF = io.imread(PATH_TOF)

# take average from top 3 depth slices, excluding first slice
# averaging give float array
# summing give integer array
# a float array is needed for image transforms
# the integer array can be 
TOF_slice = TOF[1:4,:,:].sum(axis=0)
#TOF_slice = TOF[0,:,:].astype('float64')


# alter image to match EBSD in EBSD_v1.py
img = np.rot90(TOF_slice, k=1)   # rotate image
img = np.flipud(img)                # flip along horizontal axis
#img = rotate_image(img, -3)         # rotate altered image

# crop image to about same dimension as EBSD
#img = img[75:425,100:450]
plt.imshow(img,vmax=2)
plt.axis("off")
#%%
# manually mask FIB marks
img2 = img.copy().astype('float64')\
# for cropped image
# =============================================================================
# img2[10:50,10:50] = np.nan      # top-left
# img2[10:50,300:340] = np.nan    # top-right
# img2[290:330,10:50] = np.nan    # bottom-left
# img2[290:330,300:340] = np.nan  # bottom-right
# =============================================================================

# for full image
img2[100:140,100:140] = np.nan      # top-left
img2[80:120,390:430] = np.nan    # top-right
img2[380:420,120:160] = np.nan    # bottom-left
img2[365:405,410:450] = np.nan  # bottom-right
plt.imshow(img2)

#%%
# threshold everything below 1 count
img3 = img2.copy()
img3[np.where(img3<2)] = 0
#img3[np.where(img3>2)] = 0

plt.imshow(img3)

#%%
# gaussian blur 5 times
img4 = img3.copy()
img4 = cv2.GaussianBlur(img4,(5,5),cv2.BORDER_DEFAULT)
img4 = cv2.GaussianBlur(img4,(5,5),cv2.BORDER_DEFAULT)
img4 = cv2.GaussianBlur(img4,(5,5),cv2.BORDER_DEFAULT)
img4 = cv2.GaussianBlur(img4,(5,5),cv2.BORDER_DEFAULT)
img4 = cv2.GaussianBlur(img4,(5,5),cv2.BORDER_DEFAULT)
plt.imshow(img4)

#%%
# create mask from blurred image
img_msk = img4.copy()

high = np.nanmax(img_msk)
low = np.nanmax(img_msk)/8
(thresh, img_msk) = cv2.threshold(img_msk, low, 255, cv2.THRESH_BINARY)

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
out = morphology.medial_axis(img5)
counts = np.array(counts)
rng = counts.max() - counts.min()

#%%
# get Cl count at grain boundaries and build histogram
Cl = img.copy()
gb = out.copy()

val = Cl*gb
#plt.imshow(val,vmax=0.5)

valarr = val.copy().astype('float64')
valarr[valarr==0] = np.nan
valarr = valarr.ravel()

#%%
# -*- coding: utf-8 -*-
"""

Trumann
Thu Jun 16 09:59:32 2022

run a "ToFSIMS_v2" files before this program

this program tries to overlay the mask constructed from Cl ToF-SIMS
on top of the original Cl ToF-SIMS map

note the rendered image can suffer from aliasing effects
since there is high frequency pixels beign displayed in a figure that is small
    see https://matplotlib.org/stable/gallery/images_contours_and_fields/image_antialiasing.html

can't save eps with no interpolation
    the non-mask image will be black
can save pdf with no interpolation
    color map needs to have white pixels for value of 1
    mask pixel widths are super tiny
can save png from the Spyder plot panel
    lower resolution...

okay for these overlaid images
    always import into Inkscape using Internal Import option
    after adding annotations, select all in Inkscape and Export as PNG
    this is the only way i found to preserve the mask-like features

"""

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as mticker
import numpy as np
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
        txt = offbox.TextArea(label, 
                              textprops=dict(color=scalebar_color,size=cbar_txt_size))
        self.vpac = offbox.VPacker(children=[size_bar,txt],  
                                 align="center", pad=ppad, sep=sep) 
        offbox.AnchoredOffsetbox.__init__(self, loc, pad=pad, 
                 borderpad=borderpad, child=self.vpac, prop=prop, frameon=frameon,
                 **kwargs)
SAVE = 1
show_mask = 0
unit = 'Cl (cts/s)'
cbar_txt_size = 11
scalebar_color = 'black'

out1 = out.astype('uint8')

masked_data = np.ma.masked_where(out1==0, out1)

# Overlay the two images
fig, ax = plt.subplots(figsize=(3.5,3.5))
im = ax.imshow(img, cmap='bone',vmin = 0, vmax=1.5,interpolation='none')

if show_mask == 1:
    ax.imshow(masked_data, cmap='Reds',vmin=0.5,interpolation='none')
ax.axis('off')

ob = AnchoredHScaleBar(length=172, label=u"25\u03BCm", loc=3, frameon=False,
                       pad=0.5, borderpad=0.25, sep=4, 
                       linekw=dict(color=scalebar_color,linewidth=1.5))
# change facecolor of frameon
#ob.patch.set_facecolor('k')
ax.add_artist(ob)

# define colorbar format
fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))
cax1 = fig.add_axes([ax.get_position().x1+0.025,ax.get_position().y0,0.025,ax.get_position().height])

#format and add colorbar
fig.colorbar(im, format=fmt,cax=cax1)
#color bar labels
cbar = plt.gcf().axes[-1]
cbar.set_ylabel(unit, rotation=90, va="bottom", size=cbar_txt_size, labelpad=20)
    #change color bar scale label position 
cbar.yaxis.set_offset_position('left')

if SAVE == 1:
    OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\PhD Documents\figures\Ch4eps\PVSe33_tof_sims'
    FNAME = r'\0hr_Cl_map_blues.pdf'
    plt.savefig(OUT_PATH+FNAME, format='pdf', dpi=300, bbox_inches='tight', pad_inches = 0)

