# calculatign Sobel gradient; identifying edges of images
    # works well for XBIC, not so well for Cu and Cd, which contain noise (see consolidated notes)
    # next step: apply gaussian filter to XRF, then find edges (or alter Sobel kernels, ,if possible)
    
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import colorConverter 
from skimage import filters
from scipy.ndimage import gaussian_filter

samp = NBL3_2
samp_maps = [samp['elXBIC'][0][0], samp['elXBIC'][0][1], samp['elXBIC'][0][2], samp['elXBIC'][0][3]] #0:Cu, 1:Cd, 2:Zn, 3:Mo
cu_map = samp_maps[0][:,:-2]
zn_map = samp_maps[2][:,:-2]

sig_filt = 1

# gaussian filter of original data
cu_gauss = gaussian_filter(cu_map, sigma=sig_filt)                 # maintains shape
zn_gauss = gaussian_filter(zn_map, sigma=sig_filt)
# gradients of gaussian filtered image
cu_gradient = filters.sobel(cu_gauss)                       # maintains shape
zn_gradient = filters.sobel(zn_gauss)
# gradients without trimmed 'zero 'edges; prepping to find percentiles
cu_gradient_no_edge = cu_gradient[np.nonzero(cu_gradient)] # returns raveled array
zn_gradient_no_edge = zn_gradient[np.nonzero(zn_gradient)]
# pix by pix product
product = cu_gradient * zn_gradient
# geometric mean of gradients
gmean = np.sqrt(product)

# generate the colors for your colormap
color1 = colorConverter.to_rgba('c')
color2 = colorConverter.to_rgba('c')
# make the colormaps
cmap1 = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap',['k','tab:orange'])
cmap2 = matplotlib.colors.LinearSegmentedColormap.from_list('my_cmap2',[color1,color2])
#cmap1._init() # create lut array with rgba values
cmap2._init() # create the _lut array, with rgba values
# create your alpha array and fill the colormap with them
# here it is progressive, but you can create whathever you want
#alphas1 = np.linspace(0, 0.9, cmap1.N+3)
alphas2 = np.linspace(0, 1.0, cmap2.N+3)
#cmap1._lut[:,1] = alphas1
cmap2._lut[:,-1] = alphas2
fig, axs = plt.subplots(1,3)
plt.tight_layout()
axs[0].imshow(cu_gradient, cmap='Oranges_r', origin='lower')
axs[1].imshow(zn_gradient, cmap='Blues_r', origin='lower')
axs[2].imshow(cu_gradient, cmap='Oranges_r', origin='lower')
axs[2].imshow(zn_gradient, cmap=cmap2, origin='lower')

plt.figure()
plt.scatter(cu_gradient_no_edge,zn_gradient_no_edge, s=3, color='#6B8E23')
plt.plot(np.unique(cu_gradient_no_edge), np.poly1d(np.polyfit(cu_gradient_no_edge, zn_gradient_no_edge, 1))(np.unique(cu_gradient_no_edge)), color='#20B2AA')
#fig, (ax0, ax1, ax2) = plt.subplots(nrows=1,ncols=3)
#plt.tight_layout()
#ax0.imshow(cu_gradient, origin='lower', cmap='Greys_r')
#ax1.imshow(zn_gradient, origin='lower', cmap='Greys_r')
#ax2.imshow(cu_map, origin='lower', cmap='magma')

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




# =============================================================================
# # threshold percentile of gradient map
# cu_gradient_75quart_thres = np.percentile(cu_gradient_no_edge, percentile)
# zn_gradient_75quart_thres = np.percentile(zn_gradient_no_edge, percentile)
# # find pixels in gradient map within a given percentile
# cu_mask = np.where(cu_gradient >= cu_gradient_75quart_thres, 1,0) # retains shape
# zn_mask = np.where(zn_gradient >= zn_gradient_75quart_thres, 1,0)
# # find where gradient maps mismatch --> quantifies the error in saying g.bs are where the gradients lie??
# a_mismatched_map = np.where(cu_mask == zn_mask, 1, 0)
# # parameter to minimize mismatch
# mismatch = a_mismatched_map.sum()
# print(percentile, mismatch, round(mismatch/init_mismatch, 3))
# 
# fig, (ax0, ax1, ax2) = plt.subplots(nrows=1,ncols=3)
# plt.tight_layout()
# ax0.imshow(cu_mask, origin='lower', cmap='Greys_r')
# ax1.imshow(zn_mask, origin='lower', cmap='Greys_r')
# ax2.imshow(a_mismatched_map, origin='lower', cmap='Greys_r')
# #if mismatch < init_mismatch:
#     #best_percentile = percentile
# # for each pixel in the masks, if values match, record pixel coordinates for indexing into real data arrays, plot on scatter
#      # --> matches pixels in the gradient maps that are above a certaiin percentile... make bulk stats of number of matches among the various areas scanned
# =============================================================================
