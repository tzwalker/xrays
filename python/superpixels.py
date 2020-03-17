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
# replacing with average #
# non-zero labels for regionprops
labels = labels + 1  
from skimage import color
# replace each segment with its average
label_rgb = color.label2rgb(labels, img2, kind='avg')
plt.imshow(label_rgb)

regions = regionprops(labels)



#%%
# access superpixel data

for edge in np.unique(edges):
   mask = np.zeros(img.shape, dtype='uint8') #make empty mask
   mask[edges == edge] = True #make binary mask according to selected superpixel
   superpixel = img[np.where(mask==1)] #get (1d) array of data within superpixel
   
   print()
   
# what to do once i can get to data in pixels...??? #
#import plot_defs as PLT
#PLT.plot_nice_superpixels_from_h5(NBL3_3, 0, img_copy, 'magma')
   
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

# =============================================================================
# """
# was used to plot background subtraction iterations (unsuccessfully)
# the for loop kept plotting the same background subtracted map in each subplot
# if you want to use it, this will have to be fixed
# """
# col_num = np.arange(5)
# fig, axs = plt.subplots(nrows=3,ncols=5)
# #plt.tight_layout()
# for ax in axs:
#     for col in ax:
#         img1 = rollball_bkgnd_subtraction(img1, 25) # Cd map
#         col.imshow(img1)
# for i in list(range(15)):
#     img1 = rollball_bkgnd_subtraction(img1, 25) # Cd map
#     print(np.median(img1))
# =============================================================================