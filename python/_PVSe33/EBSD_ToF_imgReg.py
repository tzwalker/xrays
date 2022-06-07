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
    "Dropbox (ASU)\Internal Reports\Q18_202204\figures_TW\SUM_0hr_Cl_maps_slice2-5.png" saved from ImageJ
    "Dropbox (ASU)\4_collab updates\ASU_NREL\PVSe33 - Se alloyed exsitu stress\20220304 ToF-SIMS PVSe33 - SHarvey Summary.pptx" see flipped EBSD

20220607 swent to stackoverflow
tof == 'left_img'
ebsd == 'right_img'
"""

import cv2
from skimage import io
import matplotlib.pyplot as plt
import numpy as np

im_left = img.copy()
im_right = EBSD_gray.copy()

sz = im_left.shape

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
(cc, warp_matrix) = cv2.findTransformECC (im_right,im_left,warp_matrix, warp_mode, criteria, None, 1)

if warp_mode == cv2.MOTION_HOMOGRAPHY :
# Use warpPerspective for Homography
    im2_aligned = cv2.warpPerspective (im_left, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
else :
# Use warpAffine for Translation, Euclidean and Affine
    im2_aligned = cv2.warpAffine(im_left, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);
