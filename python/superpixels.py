# -*- coding: utf-8 -*-
"""
Trumann
Mon Feb  3 08:53:36 2020

playing with superpixels

Note: origin='lower' in plots to compare to MAPS images,
#delete to compare to data in imageJ)
"""

# attempting to copy Math's result #
from skimage.segmentation import slic, mark_boundaries
from skimage.measure import regionprops
import sklearn.preprocessing
import numpy as np
import matplotlib.pyplot as plt


def standardize_map(map_of_sample):
    scaler = sklearn.preprocessing.StandardScaler()
    array_of_map = map_of_sample.reshape(-1,1)
    standarized_array = scaler.fit_transform(array_of_map)
    standarized_map = standarized_array.reshape(np.shape(map_of_sample))
    return standarized_map

img_raw = NBL3_2['XBIC_maps'][0][1,:,:-2]
img_stand = standardize_map(img_raw)
img = np.float64(img_stand)
edges = slic(img, n_segments=50, compactness=1, sigma=1)
# what to do once i can get to data in pixels...??? #

# access superpixel data
# =============================================================================
# for edge in np.unique(edges):
#    mask = np.zeros(img.shape, dtype='uint8') #make empty mask
#    mask[edges == edge] = True #make binary mask according to selected superpixel
#    superpixel = img[np.where(mask==1)] #get (1d) array of data within superpixel
#    
#    print()
# =============================================================================

plt.figure()
#ax0.imshow(img, cmap='inferno', origin='lower')
# for some reason the boundaries from SLIC are not changing color
# initiate RGB channel to act as boundary mask
bm = mark_boundaries(img, edges, color=(1,0,0)) #-> color is RGB
# make boolean mask where boundariy value == 1 above (e.g. 1,0,0 --> red)
bm_mask = bm[:,:,0] == 1
#everywhere where bm_mask is True, convert to nan
img_copy = img.copy()
img_copy[bm_mask] = np.nan
# plot image with boundary data "missing"
plt.imshow(img_copy, cmap='viridis') #bm[:,:,0]

import plot_defs as PLT
#PLT.plot_nice_superpixels_from_h5(NBL3_3, 0, img_copy, 'magma')

#%%
# failed fill superpixels with means values
regions = regionprops(edges, intensity_image=img)
img_copy = img.copy()
for r in regions:
    for i in range(r.coords.shape[0]):
        img_copy[r.coords[i][0]][r.coords[i][1]] = int(r.mean_intensity)
plt.figure()
plt.imshow(img_copy)