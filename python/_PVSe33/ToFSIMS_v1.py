# -*- coding: utf-8 -*-
"""

Trumann
Tue Jun  7 08:54:08 2022

this program is meant to analyze ToF-SIMS images 

"""

'''
this cell will match area the ToF SIMS area to the EBSD area
    imports, integrated, and rotates

sort of preparation for registration

'''
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

#%%
'''
this cell plots 1D profile of Se

want to check Se againt cross-section Se XRF and dynmiac Se SIMS

integrate the Se channel through CdSeTe depth

'''
from skimage import io
import numpy as np
import matplotlib.pyplot as plt

file1 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Se_maps.tif"
file2 = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Se_maps.tif"

# import ToF-SIMS images
img1 = io.imread(file1)
img2 = io.imread(file2)

# average of each slice
#p = TOF.mean(axis=(1,2))
#p1 = TOF1.mean(axis=(1,2))

# total in each slice
t1 = img1.sum(axis=(1,2))
t2 = img2[7:,:,:].sum(axis=(1,2)) # integrate over same # of slices as 0hr

# error in each slice
s1 = img1.std(axis=(1,2))
s2 = img2[7:,:,:].std(axis=(1,2)) # integrate over same # of slices as 0hr
#%%
d1 = np.arange(0,5.39,0.11) # um
d2 = np.arange(0,6.615,0.135) # um

fig, ax = plt.subplots()
ax.plot(d1,t1, label='0hr')
ax.plot(d2-0.81,t2, label='500hr')
plt.legend()

# =============================================================================
# # depth calibration
# d = np.arange(0,5.39,0.11) # um
# d1 = np.arange(0,7.56,0.135) # um
# 
# fig, ax = plt.subplots()
# ax.plot(d, p, label='0hr')
# ax.plot(d1, p1, label='500hr')
# plt.legend()
# =============================================================================
