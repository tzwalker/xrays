# -*- coding: utf-8 -*-
"""

Trumann
Tue Jun  7 09:03:06 2022

this is meant to analyze the EBSD images - i think it is less confusing 
to import/analyze EBSD data separately from the ToF-SIMS

i can alter the images in separate files, then combine the altered images in
a final file

"""

import cv2
from skimage import io
import matplotlib.pyplot as plt
import numpy as np

PATH_EBSD = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\EBSD\0hr_right_map.tif"

# import EBSD tiff
# (x,y,color_value)
EBSD = io.imread(PATH_EBSD)

# mask green (101) direction, it is confused with fiducials
green = EBSD[:,:,1]
msk = np.ma.masked_where(green==255,green,copy=True)

# convert EBSD image to grayscale
EBSD_gray = EBSD.copy()
#rgb_to_gray = lambda rgb : np.dot(rgb[... , :3] , [0.299 , 0.587, 0.114])
rgb_to_gray = lambda rgb : np.dot(rgb[... , :3] , [0.299 , 0, 0.114])
EBSD_gray = rgb_to_gray(EBSD_gray)

#check
plt.imshow(EBSD_gray,cmap='inferno')
plt.axis('off')

