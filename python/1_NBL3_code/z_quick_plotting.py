# calculatign Sobel gradient; identifying edges of images
    # works well for XBIC, not so well for Cu and Cd, which contain noise (see consolidated notes)
    # next step: apply gaussian filter to XRF, then find edges (or alter Sobel kernels, ,if possible)
    
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from skimage import filters


def calc_grad_map(channel_map):
    img_grad = filters.sobel(channel_map)
    return img_grad

samp_maps = [NBL3_2['XBIC_maps'][0], NBL3_2['elXBIC_corr'][0][0], NBL3_2['elXBIC_corr'][0][1]]

#grad_matrix= filters.sobel(samp_maps[0])
#print(np.shape(samp_maps[0]))
#fig, (ax0,ax1) = plt.subplots(nrows=1,ncols=2)
#plt.tight_layout()
#sns.heatmap(samp_maps[0],square=True, ax=ax0, xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()
#sns.heatmap(grad_matrix, square=True, ax=ax1,xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()
#sns.heatmap(grad_matrix[1], square=True, ax=ax2,xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()


for index, Map in enumerate(samp_maps):
    fig, (ax0, ax1) = plt.subplots(nrows=1,ncols=2)
    gradient_map = calc_grad_map(Map)
    sns.heatmap(Map, square=True, ax=ax0, xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()
    sns.heatmap(gradient_map, square=True, ax=ax1, xticklabels=20,yticklabels=20,cbar_kws={'shrink':0.5}).invert_yaxis()
