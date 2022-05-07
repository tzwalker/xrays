# -*- coding: utf-8 -*-
"""

Trumann
Wed Apr  6 12:12:32 2022

this program takes the tiffs of ToF-SIMS and EBSD and tries to register them
    ToFSIMS_v0.py and EBSD_v0.py were run before this program to obtain the tiffs
    
note the ToF SIMS TIF files will have a different orientation that the EBSD tif files

to get the image orientations to match, i think i need to do these operations:
the ToF-SIMS image will need a 90deg rotation counter-clockwise, then a mirror along the vertical axis operation
the EBSD image will need a  mirror along the horizontal axis
    this was based on playing around with the images in powerpoint
    "C:\Users\Trumann\Dropbox (ASU)\Internal Reports\Q18_202204\figures_TW\SUM_0hr_Cl_maps_slice2-5.png" saved from ImageJ
    "C:\Users\Trumann\Dropbox (ASU)\4_collab updates\ASU_NREL\PVSe33 - Se alloyed exsitu stress\20220304 ToF-SIMS PVSe33 - SHarvey Summary.pptx" see flipped EBSD
"""

import cv2
from skimage import io
import matplotlib.pyplot as plt
import numpy as np

PATH_TOF = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Cl_maps.tif"
PATH_EBSD = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\EBSD\0hr_right_map.tif"

TOF = io.imread(PATH_TOF)
EBSD = io.imread(PATH_EBSD)

# take average from top 3 depth slices, excluding first slice
TOF_slice = TOF[1:4,:,:].mean(axis=0)


# convert EBSD image to grayscale
EBSD_gray = EBSD.copy()
rgb_to_gray = lambda rgb : np.dot(rgb[... , :3] , [0.299 , 0.587, 0.114])
EBSD_gray = rgb_to_gray(EBSD_gray)
#%%
#check
plt.imshow(TOF_slice)
#plt.figure()
#check
plt.imshow(EBSD_gray,cmap='Greys_r', alpha = 0.5)
plt.axis('off')

plt.figure()
#check
plt.imshow(EBSD, alpha = 0.9)
plt.axis('off')
