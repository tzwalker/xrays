# -*- coding: utf-8 -*-
"""

Trumann
Wed Mar 16 13:15:19 2022

this program aligns the 80C XBIC map (scan339) to the 20C XBIC map (scan323)
2019_06_2IDD

the images are distorted along the y axis
so a full homography matrix was found

MStuckelberger suggested using ECC algorithm
to use this algorithm in python, OpenCV is needed

this program uses OpenCV, which is not a normal part of Anaconda
it is run in a separate Anaconda environnment

a separate Anaconda environment was setup to obtain the warp matrix
for images; the matrix is the output of the ECC algorithm

"""
import cv2
import numpy as np
import pandas as pd


# Read the data to be aligned
im1_path = r"C:\Users\Trumann\Dropbox (ASU)\0_stage design\DATA\combined_ASCII_2idd_0323.h5.csv" # 20C
im2_path = r"C:\Users\Trumann\Dropbox (ASU)\0_stage design\DATA\combined_ASCII_2idd_0339.h5.csv" # 80C

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

# Find size of image1
sz = im1.shape

# Define the motion model
#warp_mode = cv2.MOTION_TRANSLATION
warp_mode = cv2.MOTION_HOMOGRAPHY

# Define 2x3 or 3x3 matrices and initialize the matrix to identity
if warp_mode == cv2.MOTION_HOMOGRAPHY :
    warp_matrix = np.eye(3, 3, dtype=np.float32)
else :
    warp_matrix = np.eye(2, 3, dtype=np.float32)

# Specify the number of iterations.
number_of_iterations = 5000;

# Specify the threshold of the increment
# in the correlation coefficient between two iterations
termination_eps = 1e-10;

# Define termination criteria
criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)

# Run the ECC algorithm. The results are stored in warp_matrix.
#(cc, warp_matrix) = cv2.findTransformECC (im1_gray,im2_gray,warp_matrix, warp_mode, criteria)
(cc, warp_matrix) = cv2.findTransformECC (im1_F32,im2_F32,warp_matrix, warp_mode, criteria, None, 1)

if warp_mode == cv2.MOTION_HOMOGRAPHY :
# Use warpPerspective for Homography
    im2_aligned = cv2.warpPerspective (im2_F32, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
else :
# Use warpAffine for Translation, Euclidean and Affine
    im2_aligned = cv2.warpAffine(im2_F32, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);

