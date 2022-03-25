# -*- coding: utf-8 -*-
"""

Trumann
Fri Mar 25 07:04:52 2022

this program aligns the 20C XBIV map, 80C XBIC map, and 80C XBIV map
to get the histograms used in the stage paper

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

scans = [323,339,321,337]

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
# Translate XBIC 80C to match XBIC 20C - manual
x = 6
y = 5
# Translate matrix
M = np.float32([
	[1, 0, x],
	[0, 1, y]
])

im2shft = cv2.warpAffine(norm[1], M, (norm[1].shape[1], norm[1].shape[0]))
im2msk = np.ma.masked_where(im2shft==0,im2shft)

plt.figure()
plt.imshow(norm[0])
plt.figure()
plt.imshow(im2msk)


# Translate XBIV 20C to match XBIC 20C - manual
x = -15
y = -22
# Translate matrix
M = np.float32([
	[1, 0, x],
	[0, 1, y]
])

im3shft = cv2.warpAffine(norm[2], M, (norm[2].shape[1], norm[2].shape[0]))
im3msk = np.ma.masked_where(im3shft==0,im3shft)

#plt.figure()
#plt.imshow(norm[0])
plt.figure()
plt.imshow(im3msk)


# Translate XBIV 80C to match XBIC 20C - manual
x = 11
y = 20
# Translate matrix
M = np.float32([
	[1, 0, x],
	[0, 1, y]
])

im4shft = cv2.warpAffine(norm[3], M, (norm[3].shape[1], norm[3].shape[0]))
im4msk = np.ma.masked_where(im4shft==0,im4shft)

#plt.figure()
#plt.imshow(norm[0])
plt.figure()
plt.imshow(im4msk)
#%%
# crop area from the largest translation margins

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
plt.imshow(norm[0][20:179,11:284])
plt.figure()
plt.imshow(im2shft[20:179,11:284])
plt.figure()
plt.imshow(im3shft[20:179,11:284])
plt.figure()
plt.imshow(im4shft[20:179,11:284])