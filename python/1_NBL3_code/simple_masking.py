# -*- coding: utf-8 -*-
"""
kineticcross
Mon Aug 26 17:49:23 2019
"""
from scipy.ndimage.filters import gaussian_filter
from skimage.filters import sobel
import numpy as np
import matplotlib.pyplot as plt

# cannot be used when kclustering is called on reduced arrays
def quick_label_check(original_map, model):
    clust_map = model.labels_.reshape(np.shape(original_map))
    plt.imshow(clust_map, origin='lower')
    return
### view difference between mask generated from clusters with filtered vs. non-filtered XRF channel
    # filtered (single, Cu) XRF channel; applied clustering algorithim 
    # refer to consolidated notes for some results: mostly no difference for good maps
# =============================================================================
# cu = NBL3_2['elXBIC'][2][0][:,:-2]
# model = NBL3_2['c_kmodels'][2]
# quick_label_check(cu, model)
# 
# cu_arr = cu_map.ravel()
# # check maps
# fig, axs = plt.subplots(1,2)
# axs[0].imshow(ele_map)
# # ravel filtered map
# filt_arr = filt_map.ravel()
# filt_arr = filt_arr.reshape(-1,1)
# # cluster filtered map
# model = KMeans(init='k-means++', n_clusters=3, n_init=10) 
# filt_clust = model.fit(filt_arr)
# # check clusters
# filt_clust_map = filt_clust.labels_.reshape(np.shape(ele_map))
# axs[1].imshow(filt_clust_map, cmap='Greys')
# plt.figure()
# sns.distplot(ele_arr, bins=50)
# =============================================================================


# get the maps
xbic = NBL3_2['XBIC_maps'][1][:,:-2] ; xbic_sob = sobel(xbic)
xbiv = NBL3_2['elXBIC'][1][2][:,:-2] ; xbiv_sob = sobel(xbiv)

#quick_label_check(xbic, NBL3_2['c_kmodels'][0])
# map check
fig, (ax0,ax1) = plt.subplots(1,2)
plt.tight_layout()
ax0.imshow(xbic, origin='lower')
ax1.imshow(xbiv, origin='lower')

plt.figure()
fig1, (ax1,ax2) = plt.subplots(1,2)
plt.tight_layout()
ax1.imshow(xbic_sob, origin='lower')
ax2.imshow(xbiv_sob, origin='lower')

# if necessary, filter map; sobel maps as well
xbic_filt = gaussian_filter(xbic, sigma=1) 
xbiv_filt = gaussian_filter(xbiv, sigma=1) 

# map check


# correlation check
plt.figure()
plt.scatter(xbic_sob,xbiv_sob, s=3)
plt.xlim([np.min(xbic_sob), np.max(xbic_sob)])
plt.ylim([np.min(xbiv_sob), np.max(xbiv_sob)])

# translate map --> manually...


# correlate