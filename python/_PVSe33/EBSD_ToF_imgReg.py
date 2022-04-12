# -*- coding: utf-8 -*-
"""

Trumann
Wed Apr  6 12:12:32 2022

this program takes the tiffs of ToF-SIMS and EBSD and tries to register them
    ToFSIMS_v0.py and EBSD_v0.py were run before this program to obtain the tiffs
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
#check
plt.imshow(EBSD_gray,cmap='Greys_r', alpha = 0.2)
plt.axis('off')

