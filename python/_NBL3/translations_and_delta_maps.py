"""
coding: utf-8

tzwalker
Wed May 13 15:00:27 2020

translating shift in XBIC and XBIV images taken for NBL3 set

enter xy_shift from ImageJ xml file output 
Plugins --> Registration --> Register Virtual Stack Slices:
    the shift in x and y are found on the first line w/ "iict_transform data" 
    these steps are required for SimilarityTransform to properly translate
        -round to nearest integer
        -take the negative of each value
this operation is undone later to properly crop the aligned images
the boolean checks were made according to 
this mapping of the tuple sign to the shift in the numpy array
the x and y coordinate need to reverse their sign and order to
obtain a proper shift in the numpy array:
(+x, +y) --> [:-y , :-x] 
(+x, -y) --> [+y: , :-x]
(-x, +y) --> [:-y , +x:] # tested
(-x, -y) --> [+y: , +x:] # tested

this file was used in conjunction with "XBIC-XBIV-sctter-hex-fit.py"
in that file the linear regressions of the aligned images were found

"""

from skimage.transform import SimilarityTransform, warp

def translate_and_crop(img0, img1, xyshift):
    '''img0 is the reference, img2 will be translated'''
    shift = SimilarityTransform(translation=xyshift)
    # apply shift
    shiftd_img = warp(img1, shift)
    # mask according to offset
    mask = shiftd_img!=0
    mask = mask.astype(int)
    # apply mask to reference img0
    masked_img = img0*mask
    # set up cropping
    x = xyshift[0]
    y = xyshift[1]
    # get boolean tuple pair
    x_bool = x >= 0
    y_bool = y >= 0
    xy_bool = (x_bool, y_bool)
    # check and assign proper cropping indices
    if xy_bool == (True,True): 
        img0_cln = masked_img[:-y , :-x]
        img1_cln = shiftd_img[:-y , :-x]
    elif xy_bool == (True,False): 
        img0_cln = masked_img[-y: , :-x]        
        img1_cln = shiftd_img[-y: , :-x]
        
    elif xy_bool == (False,True): 
        img0_cln = masked_img[:-y , -x:]
        img1_cln = shiftd_img[:-y , -x:]
    elif xy_bool == (False,False): 
        img0_cln = masked_img[-y: , -x:]
        img1_cln = shiftd_img[-y: , -x:]
    return img0_cln, img1_cln

import numpy as np

PATH_ALIGNED = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\DATA\Aligned XBIC_XBIV csvs'

scans = ['scan384', 'scan380']
img0 = getattr(TS58A, scans[0])[0,:,:-2]
img1 = getattr(TS58A, scans[1])[0,:,:-2]
# these values should be the negative of whatever is in the ImageJ xml file
xyshift = (22, 14)

X, Y = translate_and_crop(img0,img1,xyshift)
plt.figure()
plt.imshow(X)
plt.figure()
plt.imshow(Y)

OUT = PATH_ALIGNED + r'\TS58A_{s}_XBIV.csv'.format(s=scans[0])
np.savetxt(OUT, X, delimiter=',')

OUT = PATH_ALIGNED + r'\TS58A_{s}_XBIC.csv'.format(s=scans[1])
np.savetxt(OUT, Y, delimiter=',')
#%%
# save shifted images #

samples = [NBL31.maps,NBL31.maps,NBL31.maps,
           NBL32.maps,NBL32.maps,NBL32.maps,
           NBL33.maps,NBL33.maps,NBL33.maps,
           TS58A.maps,TS58A.maps,TS58A.maps]

scans = [(338,335), (339,336), (340,337),
         (419,422), (420,423), (421,424),
         (261,258), (262,259), (263,260),
         (382,378), (383,379), (384,380)]

shifts = [(12,8), (12,9), (13,10),
          (6,-2), (-14,-9), (-11,-7),
          (8,-6), (10,-2), (10,-1),
          (18,12),(22,13),(22,14)]

#%%
# check if saved text files were aligned
# this only seems to work up to the end of NBL31.maps
# not sure why, but after this the translate function just stops working...
# may have to do it manually...
import pandas as pd

xbiv = pd.read_csv(PATH_ALIGNED + r'\TS58A_scan382_XBIV.csv', header=None)
xbic = pd.read_csv(PATH_ALIGNED + r'\TS58A_scan378_XBIC.csv', header=None)
plt.figure()
plt.imshow(xbiv)
plt.figure()
plt.imshow(xbic)
