# -*- coding: utf-8 -*-
"""

Trumann
Fri Mar 25 09:11:20 2022

this program aligns the 20C,40,C,60C,80C,100C XBIV maps with the 20C XBIC map
to get the average of the XBIV channel as a function of temperature

only translations are used to preserve the count rates in their original
positions
    preserving the count rates is more crucial when comparing XBIC and XBIV
    i'm not sure if a full hompgrahy transform alters the count rate
    (i.e. image imensity)
    therefore, i will only translate the images
    
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

scans = [323,321,325,330,337,342]

columns = ["US_IC", "us_ic", "Se", "Cd_L", "Te_L", "Au_L"]
i = 'y pixel no'
j = 'x pixel no'

# Import data
electrical = []
us_ic = []
for scan in scans:
    scn = str(scan)
    im_path = r"C:\Users\Trumann\Dropbox (ASU)\0_stage design\DATA\combined_ASCII_2idd_0{s}.h5.csv".format(s=scn)
    im_data = pd.read_csv(im_path)
    imgs = [im_data.pivot(index=i, columns=j, values=c) for c in columns]
    elect = np.array(imgs[1]).astype("float32")
    electrical.append(elect)
    ion_cham = np.array(imgs[0]).astype("float32")
    us_ic.append(ion_cham)

# check images
for img in electrical:
    plt.figure()
    plt.imshow(img[:,:-2])

# normalize electrical channel to upstream ion chamber
norm = [e[:,:-2] / u[:,:-2] for e,u in zip(electrical, us_ic)]
# check images
for img in norm:
    plt.figure()
    plt.imshow(img)
#%%
# set this to 1 if you want to work with normalized data, else you will have mV
norm_key = 0

if norm_key == 1:
    xbic20 = norm[0]
    xbiv20 = norm[1]
    xbiv40 = norm[2]
    xbiv60 = norm[3]
    xbiv80 = norm[4]
    xbiv100 = norm[5]
else:
    xbic20 = electrical[0][:,:-2]
    xbiv20 = electrical[1][:,:-2]
    xbiv40 = electrical[2][:,:-2]
    xbiv60 = electrical[3][:,:-2]
    xbiv80 = electrical[4][:,:-2]
    xbiv100 = electrical[5][:,:-2]
    scaler = 1 / (2E5*10000) # these are the scaler settings from
    # C:\Users\Trumann\Dropbox (ASU)\2_FS_operando\FS_plan_electrical.csv

# Translate XBIV 20C to match XBIC 20C - manual - the added integers are the
    # translations found after running the ECC registration
    # they were taken from the [0,3] and [1,3] positions of the warp matrix

# Translate XBIV 20C to match XBIC 20C - manual
x = -15
y = -22-4
# Translate matrix
M = np.float32([
	[1, 0, x],
	[0, 1, y]
])

im1shft = cv2.warpAffine(xbiv20, M, (xbiv20.shape[1], xbiv20.shape[0]))
im1msk = np.ma.masked_where(im1shft==0,im1shft)

plt.figure()
plt.imshow(xbic20)
plt.figure()
plt.imshow(im1msk)

# Translate XBIV 40C to match XBIC 20C - manual
x = 7+3
y = 10+5
# Translate matrix
M = np.float32([
	[1, 0, x],
	[0, 1, y]
])

im2shft = cv2.warpAffine(xbiv40, M, (xbiv40.shape[1], xbiv40.shape[0]))
im2msk = np.ma.masked_where(im2shft==0,im2shft)

plt.figure()
plt.imshow(xbic20)
plt.figure()
plt.imshow(im2msk)

# Translate XBIV 60C to match XBIC 20C - manual
x = 45+1
y = 25-7
# Translate matrix
M = np.float32([
	[1, 0, x],
	[0, 1, y]
])

im3shft = cv2.warpAffine(xbiv60, M, (xbiv60.shape[1], xbiv60.shape[0]))
im3msk = np.ma.masked_where(im3shft==0,im3shft)

plt.figure()
plt.imshow(xbic20)
plt.figure()
plt.imshow(im3msk)


# Translate XBIV 80C to match XBIC 20C - manual
x = 11+5
y = 20
# Translate matrix
M = np.float32([
	[1, 0, x],
	[0, 1, y]
])

im4shft = cv2.warpAffine(xbiv80, M, (xbiv80.shape[1], xbiv80.shape[0]))
im4msk = np.ma.masked_where(im4shft==0,im4shft)

plt.figure()
plt.imshow(xbic20)
plt.figure()
plt.imshow(im4msk)

# Translate XBIV 100C to match XBIC 20C - manual
x = 22-1
y = 10+3
# Translate matrix
M = np.float32([
	[1, 0, x],
	[0, 1, y]
])

im5shft = cv2.warpAffine(xbiv100, M, (xbiv100.shape[1], xbiv100.shape[0]))
im5msk = np.ma.masked_where(im5shft==0,im5shft)

plt.figure()
plt.imshow(xbic20)
plt.figure()
plt.imshow(im5msk)
#%%
# crop area from the largest translation margins
# only crop original reference image and translated images

# most positive x value goes here img[:,x:]
# most negative x value goes here img[:,:x]
# most positive y value goes here img[y:,:]
# most negative y value goes here img[:y,:]
plt.figure()
plt.imshow(xbic20[20:-26,46:-15])
plt.figure()
plt.imshow(im1shft[20:-26,46:-15])
plt.figure()
plt.imshow(im2shft[20:-26,46:-15])
plt.figure()
plt.imshow(im3shft[20:-26,46:-15])
plt.figure()
plt.imshow(im4shft[20:-26,46:-15])
plt.figure()
plt.imshow(im5shft[20:-26,46:-15])
#%%
# save histogram data
#xbic20_crop = norm[0][20:-26,46:-15]
xbiv20_crop = im1shft[20:-26,46:-15]
xbiv40_crop = im2shft[20:-26,46:-15]
xbiv60_crop = im3shft[20:-26,46:-15]
xbiv80_crop = im4shft[20:-26,46:-15]
xbiv100_crop = im5shft[20:-26,46:-15]

images = [xbiv20_crop,xbiv40_crop,xbiv60_crop,xbiv80_crop,xbiv100_crop]
converted = [arr * scaler * 1000 for arr in images] # convert to mV
histograms = [arr.ravel() for arr in converted]
histograms_arr = np.array(histograms).T

OUT_PATH = r'C:\Users\Trumann\Dropbox (ASU)\0_stage design\DATA'
FNAME = r'\histogram_data_from_refined_ECC_translations_XBIV20to100C.txt'
fname = OUT_PATH+FNAME
np.savetxt(fname, histograms_arr)
#%%
# Automatic translation - with manual translation as guesses
# Find size of image1 - cropped xbic 20C image
sz = xbic20_crop.shape

# input cropped manual translated image
im2 = xbiv100_crop
# Define the motion model
warp_mode = cv2.MOTION_TRANSLATION

# Define 2x3 or 3x3 matrices and initialize the matrix to identity
warp_matrix = np.eye(2, 3, dtype=np.float32)

# Specify the number of iterations.
number_of_iterations = 10000;

# Specify the threshold of the increment
# in the correlation coefficient between two iterations
termination_eps = 1e-10;

# Define termination criteria
criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)
# Find tranlastion

(cc, warp_matrix) = cv2.findTransformECC (xbic20_crop, im2, warp_matrix, warp_mode, criteria, None,3)

aligned = cv2.warpAffine(im2, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);
alignedMSK = np.ma.masked_where(aligned < im2.min(),aligned)

plt.figure()
plt.imshow(xbic20_crop)
plt.figure()
plt.imshow(im2)
plt.figure()
plt.imshow(alignedMSK)