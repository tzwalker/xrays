# -*- coding: utf-8 -*-
"""
Trumann
Mon Feb  3 08:53:36 2020

first background subtract image
then apply superpixels

Note: origin='lower' in plots to compare to MAPS images,
#delete to compare to data in imageJ
"""
# mimic ImageJ rolling-ball background substraction #

import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as scim
from skimage.morphology import ball
import sklearn.preprocessing as sklp
from skimage.segmentation import slic, mark_boundaries
from skimage.measure import regionprops

aMAP = NBL3_3['XBIC_maps'][0][3,:,:-2]
scaler = sklp.StandardScaler()

def rollball_bkgnd_subtraction(array, ball_radius):
    # maintain map dimensions
    map_dimensions = np.shape(array)
    # standardization requires one column
    array = array.reshape(-1,1) 
    # standardize
    array = scaler.fit_transform(array) 
    # shape standardized data back into map
    array = array.reshape(map_dimensions) 
    # Create 3D ball structure
    s = ball(ball_radius) 
    # Take only the upper half of the ball
    h = int((s.shape[1] + 1) / 2)
    # Flat the 3D ball to a weighted 2D disc
    s = s[:h, :, :].sum(axis=0)
    # Rescale weights into 0-1
    s = (1 * (s - s.min())) / (s.max()- s.min()) 
    # Use "white tophat" transform 
    nobkgnd_array = scim.white_tophat(array, structure=s)
    return nobkgnd_array

# this image is of standardized data
aMAPbk=rollball_bkgnd_subtraction(aMAP, 25)

# simple linear iterative clustering (SLIC) #
aMAPbk = np.float64(aMAPbk)
edges = slic(aMAPbk, n_segments=50, compactness=1, sigma=1)

def plot_superpixels(img, edges):
    # initiate RGB image; color=(i,j,k) corresponds to bm[:,:,(i,j,k)] 
    bm = mark_boundaries(img, edges, color=(1,0,0)) #-> color is RGB
    # make boolean mask where color channel==1 above (e.g. 1,0,0 --> red)
    bm_mask = bm[:,:,0] == 1
    # make a copy of the image (to preserve original data)
    img_copy = img.copy()
    # in copy image, where bm_mask is True, convert to nan
    img_copy[bm_mask] = np.nan #--> could make function to convert to a color
    # plot image with boundary data "missing"
    plt.imshow(img_copy, cmap='viridis')
    return

plot_superpixels(aMAPbk, edges)

# what to do once i can get to data in pixels...??? #
#%%
# access superpixel data
for edge in np.unique(edges):
   mask = np.zeros(img.shape, dtype='uint8') #make empty mask
   mask[edges == edge] = True #make binary mask according to selected superpixel
   superpixel = img[np.where(mask==1)] #get (1d) array of data within superpixel
   
   print()

#import plot_defs as PLT
#PLT.plot_nice_superpixels_from_h5(NBL3_3, 0, img_copy, 'magma')