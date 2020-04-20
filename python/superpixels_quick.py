# -*- coding: utf-8 -*-
"""
Trumann
Mon Feb  3 08:53:36 2020

first background subtract image
then apply superpixels

Note: origin='lower' in plots to compare to MAPS images,
#delete to compare to data in imageJ
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from background_subtraction import rollball_bkgnd_subtraction
from standardize_map import standardize_map
from skimage.segmentation import slic, mark_boundaries#, join_segmentations

# imitate image process in ImageJ #

# fitted data
img2 = NBL33.maps[6][3,:,:-2] #scan idx in scans
# standardize map
img2a = standardize_map(img2)
# background-subtracted, standardized data
img2b = rollball_bkgnd_subtraction(img2a, 25)
# apply gaussian filter
img2c = gaussian_filter(img2b, sigma=1)
# background subtract image with gaussian filter
img2d = rollball_bkgnd_subtraction(img2c, 25)


# get values below the average of the adjusted map (returns array)
mask_data = img2d[img2d<np.mean(img2d)]
# find these values in the most recent map (returns shaped boolean)
mask_img = np.isin(img2d, mask_data)
# apply masked data to the processed image
img2e = np.ma.masked_array(img2d,mask_img)
#%%
def mark_superpixels(img, edges):
    # initiate RGB image; color=(i,j,k) corresponds to bm[:,:,(i,j,k)] 
    bm = mark_boundaries(img, edges, color=(1,0,0)) #-> color is RGB
    # make boolean mask where color channel==1 above (e.g. 1,0,0 --> red)
    bm_mask = bm[:,:,0] == 1
    # make a copy of the image (to preserve original data)
    img_copy = img.copy()
    # in copy image, where bm_mask is True, convert to nan
    img_copy[bm_mask] = np.nan #--> could make function to convert to a color
    return img_copy
#img2 = NBL33.maps_[3][3,:,:-2] #scan idx in scans_for_correction

# prepare for SLIC segmentation; float32 to float64
img2a = np.float64(img2a)

# simple linear iterative clustering (SLIC)
labels = slic(img2a, n_segments=50, compactness=1,sigma=1)
plt.imshow(mark_superpixels(img2a, labels))

img_joint = np.stack((img1,img2), axis=2)


# =============================================================================
# """
# used to plot segmented Cu map in ImageJ colors  
# for SETO2020 poster
# """
# # define RBG colorspace:
# # [(R_strt,G_strt,B_strt),(R_mid,G_mid,B_mid),(R_end,G_end,B_end)]
# colors = [(0, 0, 0), (0.5, 0, 0), (1, 0, 0)]; cmap_name = 'imgj_reds'
# from matplotlib.colors import LinearSegmentedColormap
# # Create the colormap
# colormap = LinearSegmentedColormap.from_list(cmap_name, colors, N=255)
# # plot image with boundary data "missing"
# fig, ax = plt.subplots()
# ax.imshow(img_copy, cmap=colormap, vmin=0.5, vmax=3)
# plt.tick_params(
# axis='both',          # changes apply to the x-axis
# which='both',      # both major and minor ticks are affected
# bottom=False, labelbottom=False,
# left=False, labelleft=False)
# =============================================================================


# -*- coding: utf-8 -*-
"""
Trumann
Wed Jan 29 13:34:11 2020

originally made for XBIC maps of FS3
"""

from skimage.segmentation import slic, mark_boundaries
import numpy as np

img = r'C:\Users\Trumann\Desktop\FS_data\FS3_2019_06_2IDD_stage\output\combined_ASCII_2idd_0344.h5.csv'
df = pd.read_csv(img, skiprows = 1)
map_df = df.pivot(index = ' y pixel no', columns = 'x pixel no', values = ' us_ic')
map_np = map_df.to_numpy()
#plt.imshow(map_np, vmin=100000)


edges = slic(map_np, n_segments=100, compactness=5000, sigma=1)

# for some reason the boundaries from SLIC are not changing color
# initiate RGB channel to act as boundary mask
bm = mark_boundaries(map_np, edges, color=(1,0,0)) #-> color is RGB
# make boolean mask
bm_mask = bm[:,:,0] == 1
#everywhere where bm_edit is True, convert to nan
img_masked = map_np.copy(); img_masked[bm_mask] = np.nan
bm = mark_boundaries(map_np, edges, color=(1,0,0)) #-> color is RGB

# plot somehwat nicely
fig, ax1 = plt.subplots()
#ax0.imshow(map_np, cmap='magma', origin='lower', vmin=1E5)
im1 = ax1.imshow(map_np, cmap='magma', origin='lower', vmin=1E5) #bm[:,:,0]
plt.xlabel('X (\u03BCm/10)', fontsize=16)
plt.ylabel('Y (\u03BCm/10)', fontsize=16)
plt.colorbar(im1,fraction=0.046, pad=0.04)
cbar_ax = plt.gcf().axes[-1]                        #gets colorbar of current figure object, behaves as second y object
# colorbar label settings
cbar_ax.set_ylabel('cts/s', fontsize = 16, #\u03BCg/cm'+ r'$^{2}$
                   rotation = 90, labelpad = 10)   #label formatting
ax1.tick_params(labelsize = 14)