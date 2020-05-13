"""
coding: utf-8

tzwalker
Wed May 13 15:00:27 2020

translating shift in XBIC and XBIV images taken for NBL3 set

enter xy_shift from ImageJ xml file output
translate coordinates read from xml files exported by ImageJ
    Plugins --> Registration --> Register Virtual Stack Slices
    the shift in x and y are found on the first line w/ "iict_transform data" 
    round to nearest integer
    take the negative of each value

"""

from skimage.transform import SimilarityTransform, warp
import matplotlib.pyplot as plt
import numpy as np

def translate_and_crop(img0, img1, xy_tuple):
    '''img0 is the reference, img2 will be translated'''
    shift = SimilarityTransform(translation=xy_move_tuple)
    # apply shift
    shifted_image = warp(img1, shift)
    # mask according to offset
    mask = shifted_image=0
    mask = mask.astype(int)
    # apply mask to reference img0
    masked_img = img0*mask
    # crop the two images according to shift
    if xy_tuple[0] < 0:
        x_shift = -xy_tuple[0]
    
    if xy_tuple[1] < 0:
        y_shift = -xy_tuple[1]
    
    img0_cln = img0[x_shift:,x_shift:]
    return img0_cln, img1_cln

img0 = NBL33.scan263[0,:,:-2]
img1 = NBL33.scan266[0,:,:-2]


xy_shift = (-9, 1)

# multiply values to keep by 1, and values to rid by 0

aligned=[IMG0_MSK, IMG1_SHIFT]

# remove zeros using indices of image with largest offset
# this is tricky, need to pay attention to how the array
# is indexed and what the transform does to the array
aligned_crop = [arr[:-1,9:] for arr in aligned]

X = aligned_crop[1] # xbic
Y = aligned_crop[0] # xbiv


# tuple sign mapped to numpy array shift; incorporate this into definition above
(+x, +y) --> [:-y , :-x]

(-x, -y) --> [+y: , +x:]

(-x, +y) --> [:-y , +x:]

(+x, -y) --> [+y: , :-x]











