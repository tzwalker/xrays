# -*- coding: utf-8 -*-
"""

Trumann
Thu Mar 24 10:49:12 2022

this program tests how well the 20C and 80C XBIV images align when they 
were separately registered to the 20C XBIC map

this does not work unless you're warping the cropped images

note on displaying the data: if the XRF maps use rigin='lower', then the
XBIC maps should use origin='lower'
both are pivoted by using the x pixel no and y pixel no
so their origins should be the same
    i chose origin='lower' since it displays the y-axis ticklabels properly
    
"""

import cv2
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# Read the data to be aligned
im1_path = r"C:\Users\Trumann\Dropbox (ASU)\0_stage design\DATA\combined_ASCII_2idd_0321.h5.csv" # 20C - XBIV
im2_path = r"C:\Users\Trumann\Dropbox (ASU)\0_stage design\DATA\combined_ASCII_2idd_0337.h5.csv" # 80C - XBIC

im1_data = pd.read_csv(im1_path)
im2_data = pd.read_csv(im2_path)

# Read images of interest
columns = ["US_IC", "us_ic", "Se", "Cd_L", "Te_L", "Au_L"]

i = 'y pixel no'
j = 'x pixel no'
imgs1 = [im1_data.pivot(index=i, columns=j, values=c) for c in columns]
imgs2 = [im2_data.pivot(index=i, columns=j, values=c) for c in columns]

# Read one image, index here selects from 'columns'
im1 = np.array(imgs1[1])
im2 = np.array(imgs2[1])

# Remove NaN columns
im1 = im1[:,:-2]
im2 = im2[:,:-2]

# Convert images to float32
im1_F32 = im1.astype("float32")
im2_F32 = im2.astype("float32")

# =============================================================================
# # Normalize XBIC to upstream_ion chamber
# xbic = np.array(imgs1[1])
# us_ic = np.array(imgs1[0])
# xbic20 = xbic[:,:-2] / us_ic[:,:-2]
# 
# xbic = np.array(imgs2[1])
# us_ic = np.array(imgs2[0])
# xbic80 = xbic[:,:-2] / us_ic[:,:-2]
# 
# # Convert 80C map to float32
# im2_F32 = xbic80.astype("float32")
# =============================================================================

# Apply warp matrix to 20C map
warp_20C = np.array([
    [1.016300320625305176e+00,6.653011776506900787e-03,-1.107764601707458496e+00],
    [-2.814425388351082802e-03,1.126218318939208984e+00,-7.171729564666748047e+00],
    [1.367810796182311606e-06,1.688669726718217134e-04,1.000000000000000000e+00]])

sz = im1.shape

im1_aligned = cv2.warpPerspective (im1_F32, warp_20C, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)

# Apply warp matrix to 80C map
warp_80C = np.array([
    [1.020379304885864258e+00,6.930129230022430420e-02,-1.122546577453613281e+01],
    [2.278784057125449181e-03,1.115842461585998535e+00,-8.717557907104492188e+00],
    [3.789008405874483287e-05,1.488693524152040482e-04,1.000000000000000000e+00]])

sz = im2.shape

im2_aligned = cv2.warpPerspective (im2_F32, H, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
im2_msk = np.ma.masked_where(im2_aligned==0,im2_aligned)
plt.figure()
plt.imshow(im1_aligned)
plt.figure()
plt.imshow(im2_msk)

# Crop aligned area
#xbic20_crop = xbic20[30:190,20:]
#xbic80_crop = im2_aligned[30:190,20:]