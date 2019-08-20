# calculatign Sobel gradient; identifying edges of images
    # works well for XBIC, not so well for Cu and Cd, which contain noise (see consolidated notes)
    # next step: apply gaussian filter to XRF, then find edges (or alter Sobel kernels, ,if possible)
    
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from skimage import filters
from scipy.ndimage import gaussian_filter

samp = NBL3_2
samp_maps = [samp['elXBIC'][0][0], samp['elXBIC'][0][1], samp['elXBIC'][0][2], samp['elXBIC'][0][3]] #0:Cu, 1:Cd, 2:Zn, 3:Mo
cu_map = samp_maps[0][:,:-2]
zn_map = samp_maps[2][:,:-2]

sig_filt = 1
thres = 75
# gaussian filter of original data
cu_gauss = gaussian_filter(cu_map, sigma=sig_filt)                 # maintains shape
zn_gauss = gaussian_filter(zn_map, sigma=sig_filt)

cu_gradient = filters.sobel(cu_gauss)                       # maintains shape
cu_gradient_no_edge = cu_gradient[np.nonzero(cu_gradient)] # returns raveled array
zn_gradient = filters.sobel(zn_gauss)
zn_gradient_no_edge = zn_gradient[np.nonzero(zn_gradient)]

cu_gradient_75quart_thres = np.percentile(cu_gradient_no_edge, thres)
zn_gradient_75quart_thres = np.percentile(zn_gradient_no_edge, thres)

cu_mask = np.where(cu_gradient > cu_gradient_75quart_thres, 1,0)
zn_mask = np.where(zn_gradient > zn_gradient_75quart_thres, 1,0)

# foro each pixel in the masks, if values match, record pixel coordinates for indexing into real data arrays, plot on scatter
     # --> matches pixels in the gradient maps that are above a certaiin percentile... make bulk stats of number of matches among the various areas scanned

#fig, (ax0, ax1, ax2) = plt.subplots(nrows=1,ncols=3)
#plt.tight_layout()
#sns.heatmap(origin_map, square=True, xticklabels=20, yticklabels=20, ax=ax0, cbar_kws={'shrink':0.5}).invert_yaxis()
#sns.heatmap(gauss_map, square=True, xticklabels=20, yticklabels=20, ax=ax1, cbar_kws={'shrink':0.5}).invert_yaxis()
#sns.heatmap(grad_matrix, square=True, xticklabels=20, yticklabels=20, ax=ax2, cbar_kws={'shrink':0.5}).invert_yaxis()
plt.figure()
sns.heatmap(cu_mask, square=True, xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}, cmap='BrBG').invert_yaxis()
sns.heatmap(zn_mask, square=True, xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}, cmap='PiYG').invert_yaxis()
#sns.regplot(cu_stand.ravel(), zn_stand.ravel(), scatter_kws={'s':5})
#sns.jointplot(origin_map.ravel(), origin_map1.ravel(), kind='hex')
#plt.figure()
#sns.regplot(no_edge_gmatrix, no_edge_gmatrix1, scatter_kws={'s':5})
#sns.jointplot(no_edge_gmatrix, no_edge_gmatrix1, kind='hex')


# =============================================================================
# fig, (ax0,ax1) = plt.subplots(nrows=1,ncols=2)
# plt.tight_layout()
# sns.heatmap(samp_maps[0],square=True, ax=ax0, xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()
# sns.heatmap(grad_matrix, square=True, ax=ax1,xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()
# sns.heatmap(grad_matrix[1], square=True, ax=ax2,xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()
# 
# for index, Map in enumerate(samp_maps):
#     fig, (ax0, ax1) = plt.subplots(nrows=1,ncols=2)
#     gradient_map = calc_grad_map(Map)
#     sns.heatmap(Map, square=True, ax=ax0, xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()
#     sns.heatmap(gradient_map, square=True, ax=ax1, xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()
# =============================================================================

# =============================================================================
# # gaussian filter of (shaped) standardized data
# cu_stand = cu_stand.reshape(np.shape(gauss_map))
# gauss_of_cu_stand = gaussian_filter(cu_stand, sigma=2)
# zn_stand = zn_stand.reshape(np.shape(gauss_map))
# gauss_of_zn_stand = gaussian_filter(zn_stand, sigma=2)
# =============================================================================
