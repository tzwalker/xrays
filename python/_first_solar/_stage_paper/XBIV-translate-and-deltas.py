"""
coding: utf-8

tzwalker
Thu Nov 18 20:36:03 2021

this file is needed so that the XBIC channel can be normalized to the US_IC
and plotted as an aligned map

basically, the US_IC channel also needs to be aligned

i will only do this for the 20C and 80C temperature steps

(1) run "main-FS3-ASCII.py"

the translation coordinates were taken from the SIFT algorithm

"""

from skimage.transform import SimilarityTransform, warp
import numpy as np

### start with map with largest offset (img2, scan330)
img2 = FS3.scan337
SHFT2 = SimilarityTransform(translation=(-32, -44))
# shift (translate) all imported channels
shifted_channels2 = []
for i, channel in enumerate(channels):
    IMG2_SHIFT = warp(img2[i,:,:-2], SHFT2)
    shifted_channels2.append(IMG2_SHIFT)
# store shifted channels
shifted_channels2 = np.array(shifted_channels2)

### make mask that defines area to crop
mask = IMG2_SHIFT!=0
mask = mask.astype(int)

### mask the map used as alignemnt reference
img0 = FS3.scan321
shifted_channels0 = []
for i, channel in enumerate(channels):
    # mask the translated maps
    IMG0_MSK = img0[i,:,:-2]*mask
    shifted_channels0.append(IMG0_MSK)
shifted_channels0 = np.array(shifted_channels0) 

#%%

### store aligned and masked images
aligned = [shifted_channels0,
           shifted_channels2]
### remove zeros according to indices of map with largest offset
aligned_crop = [arr[:,44:,32:] for arr in aligned]


#%%

# save aligned arrays for further processing
PATH_OUT = r'C:\Users\triton\Dropbox (ASU)\2_FS_operando\XBIV aligned image csvs\stage paper'
SCAN_STR = ['scan321','scan337']
CHANNELS = ['us_ic','XBIV']

for i,scan in enumerate(aligned_crop):
    for j,chan in enumerate(CHANNELS):
        FNAME = r'\FS3_{scn}_{chn}.csv'.format(scn=SCAN_STR[i], chn=CHANNELS[j])
        array = scan[j,:,:]
        np.savetxt(PATH_OUT+FNAME, array, delimiter=',')
        
