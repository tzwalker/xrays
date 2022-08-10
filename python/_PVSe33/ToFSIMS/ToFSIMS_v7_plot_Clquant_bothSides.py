# -*- coding: utf-8 -*-
"""

Trumann
Tue Aug  9 18:47:45 2022

this program plots an integration from the Au side,
and integration from the TCO side
and the mask associated with the TCO-side integration

the intent is to compare the integrations from different sides
of CdTe layers that have different thicknesses

in this case the unaged cell has a thinner layer than the aged cell

only quantified Cl density maps are used

for TCO-side integration, the indices were identified and recorded in notes.pptx

"""
def match_EBSD_orientation(array):
    transformed = np.rot90(array, k=1)   # rotate image
    transformed = np.flipud(transformed)                # flip along horizontal axis
    return transformed
    
from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import LogNorm
from matplotlib.gridspec import GridSpec

file1 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Cl_maps_quantified.tif"
file2 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Cl_maps_quantified.tif"

cbar_txt_size = 11

# import ToF-SIMS images
imgs1 = io.imread(file1)
imgs2 = io.imread(file2)

# integrate near Au side, exclude index 0 since it has artifacts
img1 = imgs1[1:10,:,:].sum(axis=0)
img1 = match_EBSD_orientation(img1)
img2 = imgs2[1:10,:,:].sum(axis=0)
img2 = match_EBSD_orientation(img2)

# integrate near TCO side, taken from v6_Cl_at_gb
img3 = imgs1[39-18-9:39-18,:,:].sum(axis=0)
img4 = imgs2[44-15-8:44-15,:,:].sum(axis=0)

# get masks from TCO-side integration; run "v6_0hr" and "v6_500hr" to process masks
mask0 = masked_data0.copy()
mask500 = masked_data500.copy()

fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6)) = plt.subplots(figsize=((10,10)), nrows=3,ncols=2)

im1 = ax1.imshow(img1)
im2 = ax2.imshow(img2)
im3 = ax3.imshow(img3)
im4 = ax4.imshow(img4)
im5 = ax5.imshow(img3)
im6 = ax6.imshow(img4)

plt.tight_layout()