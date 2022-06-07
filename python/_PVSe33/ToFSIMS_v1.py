# -*- coding: utf-8 -*-
"""

Trumann
Tue Jun  7 08:54:08 2022

this program is meant to analyze ToF-SIMS images

start with importing, integrating, and rotating

"""

import cv2
from skimage import io,transform
import matplotlib.pyplot as plt
import numpy as np

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

PATH_TOF = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Cl_maps.tif"

# import ToF-SIMS image
TOF = io.imread(PATH_TOF)

# take average from top 3 depth slices, excluding first slice
# averaging give float array
# summing give integer array
# a float array is needed for image transforms
# the integer array can be 
TOF_slice = TOF[1:4,:,:].mean(axis=0)
#TOF_slice = TOF[0,:,:].astype('float64')


# alter image to match EBSD in EBSD_v1.py
img = rotate_image(TOF_slice, 90)   # rotate image
img = np.flipud(img)                # flip along horizontal axis
img = rotate_image(img, -3)         # rotate altered image

# crop image to about same dimension as EBSD
img = img[75:425,100:450]

# check 
fig, ax = plt.subplots()
ax.imshow(img, vmax=0.5)
ax.axis("off")
ax.set_aspect(0.9)






