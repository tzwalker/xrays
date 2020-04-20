# -*- coding: utf-8 -*-
"""
Trumann
Wed Jan 29 13:34:11 2020

originally made for XBIC maps of FS3
"""

# standardize map
# segment
# average segements
# apply Otsu threshold
# stats on pixels below the threshold
# stats on pixels above the threshold
HOME_PATH = r'C:\Users\triton\xrays\python'
import sys
sys.path.append(HOME_PATH)
from background_subtraction import background_subtraction as bksb
from standardize_map import standardize_map as stmap
#import numpy as np
from skimage.segmentation import slic, mark_boundaries

img = FS3.scan323[0,:,:-2]
img1 = stmap(img)
img2 = bksb(img1,15)

edges = slic(img2, n_segments=100, compactness=5000, sigma=1)

# for some reason the boundaries from SLIC are not changing color
# initiate RGB channel to act as boundary mask
bm = mark_boundaries(map_np, edges, color=(1,0,0)) #-> color is RGB
# make boolean mask
bm_mask = bm[:,:,0] == 1
#everywhere where bm_edit is True, convert to nan
img_masked = map_np.copy(); img_masked[bm_mask] = np.nan
bm = mark_boundaries(map_np, edges, color=(1,0,0)) #-> color is RGB

# replacing with average #
# non-zero labels for regionprops
labels = labels + 1  
from skimage import color
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
   
# what to do once i can get to data in pixels...??? #
#import plot_defs as PLT
#PLT.plot_nice_superpixels_from_h5(NBL3_3, 0, img_copy, 'magma')

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
