# -*- coding: utf-8 -*-
"""

Trumann
Wed Jun  8 15:27:48 2022

this program is meant to replicate the ImageJ procedure seen in
"Z\Trumann\Tutorial Videos\20220607_PVSe33_0hr_Cl_GBmask.mp4"

i don't need to rotate it since i will not use the images produced
in registration against the EBSD image (at least not yet)

20220608 this prgram is only meant for the 0hr images
    the FIB marks are manually masked and this mask position
    will be different for the 500hr images

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
TOF_slice = TOF[1:4,:,:].sum(axis=0)
#TOF_slice = TOF[0,:,:].astype('float64')


# alter image to match EBSD in EBSD_v1.py
img = np.rot90(TOF_slice, k=1)   # rotate image
img = np.flipud(img)                # flip along horizontal axis
#img = rotate_image(img, -3)         # rotate altered image

# crop image to about same dimension as EBSD
#img = img[75:425,100:450]
plt.imshow(img,vmax=2)
plt.axis("off")
#%%
# manually mask FIB marks
img2 = img.copy().astype('float64')\
# for cropped image
# =============================================================================
# img2[10:50,10:50] = np.nan      # top-left
# img2[10:50,300:340] = np.nan    # top-right
# img2[290:330,10:50] = np.nan    # bottom-left
# img2[290:330,300:340] = np.nan  # bottom-right
# =============================================================================

# for full image
img2[100:140,100:140] = np.nan      # top-left
img2[80:120,390:430] = np.nan    # top-right
img2[380:420,120:160] = np.nan    # bottom-left
img2[365:405,410:450] = np.nan  # bottom-right
plt.imshow(img2)

#%%
# threshold everything below 1 count
img3 = img2.copy()
img3[np.where(img3<2)] = 0
#img3[np.where(img3>2)] = 0

plt.imshow(img3)

#%%
# gaussian blur 5 times
img4 = img3.copy()
img4 = cv2.GaussianBlur(img4,(5,5),cv2.BORDER_DEFAULT)
img4 = cv2.GaussianBlur(img4,(5,5),cv2.BORDER_DEFAULT)
img4 = cv2.GaussianBlur(img4,(5,5),cv2.BORDER_DEFAULT)
img4 = cv2.GaussianBlur(img4,(5,5),cv2.BORDER_DEFAULT)
img4 = cv2.GaussianBlur(img4,(5,5),cv2.BORDER_DEFAULT)
plt.imshow(img4)

#%%
# create mask from blurred image
img_msk = img4.copy()

high = np.nanmax(img_msk)
low = np.nanmax(img_msk)/8
(thresh, img_msk) = cv2.threshold(img_msk, low, 255, cv2.THRESH_BINARY)

plt.imshow(img_msk)
#%%
# skeletonize
img5 = img_msk.copy().astype('uint8')

from skimage import morphology

out = morphology.medial_axis(img5)
plt.imshow(out,vmax=0.5)
plt.axis("off")
print(np.count_nonzero(out))

#%%
# overlay 
# =============================================================================
# over = out.copy()
# over = over.astype('int')
# over = np.ma.masked_where(over == 1, img2)
# 
# plt.imshow(img2)
# plt.imshow(over,alpha=0.5,cmap='inferno')
# =============================================================================

