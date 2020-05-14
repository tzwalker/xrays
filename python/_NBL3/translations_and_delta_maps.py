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
"""

from skimage.transform import SimilarityTransform, warp
import matplotlib.pyplot as plt
import numpy as np

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

img0 = NBL33.scan263[0,:,:-2]
img1 = NBL33.scan266[0,:,:-2]
xyshift = (-9, 1)

X, Y = translate_and_crop(img0,img1,xyshift)














