# -*- coding: utf-8 -*-
"""

Trumann
Tue Mar 22 10:38:07 2022

run first cell in "opencv_ECC_register.py" before this program

this program plots the registration results for the stage paper

i want to add a figure that shows the XBIC registration lineouts to the
main manuscript

and the lineouts of the XRF channels in the supporting information

"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

# Normalize XBIC to upstream_ion chamber
xbic = np.array(imgs1[1])
us_ic = np.array(imgs1[0])
xbic20 = xbic[:,:-2] / us_ic[:,:-2]

xbic = np.array(imgs2[1])
us_ic = np.array(imgs2[0])
xbic80 = xbic[:,:-2] / us_ic[:,:-2]

# Convert 80C map to float32
im2_F32 = xbic80.astype("float32")

# Apply warp matrix to 80C map
im2_aligned = cv2.warpPerspective (im2_F32, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)

# Crop aligned area
xbic20_crop = xbic20[30:190,20:]
xbic80_crop = im2_aligned[30:190,20:]

# Get lines in 20C
lineout_20x = xbic20_crop[58,:]
lineout_20y = xbic20_crop[:,180]

x = np.array(list(range(0,len(lineout_20x))))
y = np.array(list(range(0,len(lineout_20y))))

#%%
# =============================================================================
# fig, (ax1,ax2) = plt.subplots(2)
# # Plot 20C map
# ax1.imshow(xbic20_crop)
# ax1.axhline(y=58,linestyle='--', linewidth=1, color='w')
# ax1.axvline(x=180,linestyle='--', linewidth=1, color='w')
# 
# # Plot aligned 80C map
# ax2.imshow(xbic80_crop)
# ax2.axhline(y=58,linestyle='--', linewidth=1, color='w')
# ax2.axvline(x=180,linestyle='--', linewidth=1, color='w')
# 
# =============================================================================
# From C:\Users\Trumann\xrays\python\_NBL3\XBIC-XBIV-scatter-hex-fit.py
# setup histograms in margins #

fig = plt.figure(constrained_layout=True)

grid = GridSpec(3, 3, figure=fig)
main_ax = fig.add_subplot(grid[1:,:2])
hline = fig.add_subplot(grid[0, :-1], xticklabels=[], xticks=[])
vline = fig.add_subplot(grid[1:, -1], yticklabels=[], yticks=[])

# plot 
main_ax.imshow(xbic20_crop, cmap='inferno')
main_ax.axhline(y=58, linestyle='--', linewidth=1)
main_ax.axvline(x=180, linestyle='--', linewidth=1)

hline.plot(x,lineout_20x, color='gray')
hline.set_xlim([0,279])
vline.plot(lineout_20y,y, color='gray')
