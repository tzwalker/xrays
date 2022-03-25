# -*- coding: utf-8 -*-
"""

Trumann
Thu Mar 24 08:23:25 2022

this program aligns 
the 20C XBIV map (scan321) to the 20C XBIC map (scan323) and
the 80C XBIV map (scan337) to the 20C XBIC map (scan323)
2019_06_2IDD 


the images are distorted along the y axis
so a full homography matrix was found

the 20C XBIC map was used as the reference image for all registrations
this should produce warp matrices that give the same area

MStuckelberger suggested using ECC algorithm
to use this algorithm in python, OpenCV is needed

this program uses OpenCV, which is not a normal part of Anaconda
it is run in a separate Anaconda environnment

a separate Anaconda environment was setup to obtain the warp matrix
for images; the matrix is the output of the ECC algorithm

"""
"""IMPORT DATA"""
import cv2
import numpy as np
import pandas as pd

# Read the data to be aligned
# ASCIIs were copied from this path
#'Z:\Trumann\Fitted_Sychrotron_Data\2019_06_2IDD_FS3_operando\ASCIIS_TW_BL'
im1_path = r"C:\Users\Trumann\Dropbox (ASU)\0_stage design\DATA\combined_ASCII_2idd_0323.h5.csv" # 20C - XBIC
im2_path = r"C:\Users\Trumann\Dropbox (ASU)\0_stage design\DATA\combined_ASCII_2idd_0321.h5.csv" # 20C - XBIV

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
#%%
"""MANUAL TRANSLATION TO MAKE GOOD INITIAL GUESS FOR ECC ALGORITHM"""
import matplotlib.pyplot as plt

#plt.figure()
#plt.imshow(im1_F32)
#plt.figure()
#plt.imshow(im2_F32)
#plt.figure()
#plt.imshow(im2_F32)

x = -15
y = -22
# Translate matrix
M = np.float32([
	[1, 0, x],
	[0, 1, y]
])

im2_shifted = cv2.warpAffine(im2_F32, M, (im2_F32.shape[1], im2_F32.shape[0]))
im2_shft_msk = np.ma.masked_where(im2_shifted==0,im2_shifted)

#plt.figure()
#plt.imshow(im2_shft_msk)

# CROP IMAGES SO ZEROS IN TRANSLATED IMAGE TO NOT MESS WITH ALIGNMENT
if x and y < 0:
    im1_F32_crop = im1_F32[:y,:x]
    im2_shfted_crop = im2_shifted[:y,:x]
if x and y > 0:
    im1_F32_crop = im1_F32[y:,x:]
    im2_shfted_crop = im2_shifted[y:,x:]
if x < 0 and y > 0:
    im1_F32_crop = im1_F32[y:,:x]
    im2_shfted_crop = im2_shifted[y:,:x]
if x > 0 and y < 0:
    im1_F32_crop = im1_F32[:y,x:]
    im2_shfted_crop = im2_shifted[:y,x:]

plt.figure()
plt.imshow(im1_F32_crop)
plt.figure()
plt.imshow(im2_shfted_crop)
#%%
"""REGISTRATION"""
# Find size of image1
sz = im1.shape

# Define the motion model
#warp_mode = cv2.MOTION_TRANSLATION
#warp_mode = cv2.MOTION_AFFINE
warp_mode = cv2.MOTION_HOMOGRAPHY

# Define 2x3 or 3x3 matrices and initialize the matrix to identity
if warp_mode == cv2.MOTION_HOMOGRAPHY :
    warp_matrix = np.eye(3, 3, dtype=np.float32)
else :
    warp_matrix = np.eye(2, 3, dtype=np.float32)

# Specify the number of iterations.
number_of_iterations = 10000;

# Specify the threshold of the increment
# in the correlation coefficient between two iterations
termination_eps = 1e-10;

# Define termination criteria
criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)

# Run the ECC algorithm. The results are stored in warp_matrix.
# If manual alignment was done to get good initial guess, then input cropped maps
(cc, warp_matrix) = cv2.findTransformECC (im1_F32_crop,im2_shfted_crop,warp_matrix, warp_mode, criteria, None,3)

if warp_mode == cv2.MOTION_HOMOGRAPHY :
# Use warpPerspective for Homography
    im2_aligned = cv2.warpPerspective (im2_shfted_crop, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
else :
# Use warpAffine for Translation, Euclidean and Affine
    im2_aligned = cv2.warpAffine(im2_shfted_crop, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);

#%%
"""CHECK REGISTRATION RESULT"""
# this line gives the cropped images, aligned, with same dimension as Fig 4 and Fig 5
plt.figure(); plt.imshow(im1_F32_crop[30:190,20:]); plt.figure(); plt.imshow(im2_aligned[30:190,20:])

# this line gives the cropped images, aligned, with different dimension than Fig 4 and Fig 5
plt.figure();plt.imshow(im1_F32_crop[10:170,1:275]);plt.figure();plt.imshow(im2_aligned[10:170,1:275])

