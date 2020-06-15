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

from background_subtraction import background_subtraction
from standardize_map import standardize_map
from skimage.segmentation import slic,mark_boundaries,find_boundaries
from skimage.measure import regionprops
from skimage import color

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

# fitted data
img = NBL33.scan264[2,:,:-2]
#img_joint = np.stack((img1,img2), axis=2)

# standardize map
img_stnd = standardize_map(img)
# subtract background
img_cln = background_subtraction(img_stnd, 20)


# prepare for SLIC segmentation; float32 to float64
img_cln = img_cln.astype('float64')

# simple linear iterative clustering (SLIC) segmentation
labels = slic(img_cln, n_segments=50, compactness=1,sigma=1)
plt.imshow(mark_superpixels(img_cln, labels))


# view segmentation on other image
img_test = NBL33.scan264[0,:,:-2].copy()
# standardize map
img_test_stnd = standardize_map(img_test)
# subtract background
img_test_cln = background_subtraction(img_test_stnd, 20)

# get boolean array where boundaries are True
mask = find_boundaries(labels)
mask = mask.astype('int')

# replacing with average #
# non-zero labels for regionprops
labels = labels + 1  
# replace each segment with its average
label_rgb = color.label2rgb(labels, img2, kind='avg')
plt.imshow(label_rgb)
regions = regionprops(labels)

# access superpixel data
for edge in np.unique(edges):
   mask = np.zeros(img.shape, dtype='uint8') #make empty mask
   mask[edges == edge] = True #make binary mask according to selected superpixel
   superpixel = img[np.where(mask==1)] #get (1d) array of data within superpixel
   print()


# =============================================================================
# """
# plotting segmented DoE SETO session maps
# """
# 
# from skimage.segmentation import slic, mark_boundaries
# import numpy as np
# 
# img = r'C:\Users\Trumann\Desktop\FS_data\FS3_2019_06_2IDD_stage\output\combined_ASCII_2idd_0344.h5.csv'
# df = pd.read_csv(img, skiprows = 1)
# map_df = df.pivot(index = ' y pixel no', columns = 'x pixel no', values = ' us_ic')
# map_np = map_df.to_numpy()
# 
# edges = slic(map_np, n_segments=100, compactness=5000, sigma=1)
# # for some reason the boundaries from SLIC are not changing color
# # initiate RGB channel to act as boundary mask
# bm = mark_boundaries(map_np, edges, color=(1,0,0)) #-> color is RGB
# # make boolean mask
# bm_mask = bm[:,:,0] == 1
# #everywhere where bm_edit is True, convert to nan
# img_masked = map_np.copy(); img_masked[bm_mask] = np.nan
# bm = mark_boundaries(map_np, edges, color=(1,0,0)) #-> color is RGB
# 
# # plot somehwat nicely
# fig, ax1 = plt.subplots()
# #ax0.imshow(map_np, cmap='magma', origin='lower', vmin=1E5)
# im1 = ax1.imshow(map_np, cmap='magma', origin='lower', vmin=1E5) #bm[:,:,0]
# plt.xlabel('X (\u03BCm/10)', fontsize=16)
# plt.ylabel('Y (\u03BCm/10)', fontsize=16)
# plt.colorbar(im1,fraction=0.046, pad=0.04)
# #gets colorbar of current figure object, behaves as second y object
# cbar_ax = plt.gcf().axes[-1]                        
# # colorbar label settings
# cbar_ax.set_ylabel('cts/s', fontsize = 16, #\u03BCg/cm'+ r'$^{2}$
#                    rotation = 90, labelpad = 10)   #label formatting
# ax1.tick_params(labelsize = 14)
# =============================================================================

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