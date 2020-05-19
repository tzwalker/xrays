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

scans = ['scan419', 'scan416']
img0 = getattr(NBL32, scans[0])[0,:,:-2]
img1 = getattr(NBL32, scans[1])[0,:,:-2]
# these values should be the negative of whatever is in the ImageJ xml file
xyshift = (19, 6)

X, Y = translate_and_crop(img0,img1,xyshift)
plt.figure()
plt.imshow(X)
plt.figure()
plt.imshow(Y)

'''to save aligned images'''
PATH_ALIGNED = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\DATA\Aligned XBIC_XBIV csvs'
OUT = PATH_ALIGNED + r'\NBL32_{s}_XBIC.csv'.format(s=scans[1])
np.savetxt(OUT, Y, delimiter=',')
#OUT = PATH_ALIGNED + r'\NBL32_{s}_XBIC.csv'.format(s=scans[1])
#np.savetxt(OUT, Y, delimiter=',')



#%%
'''import aligned images, save them as txt for imageJ'''
import pandas as pd
import numpy as np

PATH_ALIGNED = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\DATA\Aligned XBIC_XBIV csvs'
img_aligned = pd.read_csv(PATH_ALIGNED + r'\NBL32_scan416_XBIC.csv', header=None)
img_aligned1 = pd.read_csv(PATH_ALIGNED + r'\NBL32_scan419_XBIV.csv', header=None)
img_aligned2 = pd.read_csv(PATH_ALIGNED + r'\NBL32_scan422_XRF.csv', header=None)

a = np.array(img_aligned) # 95x80
b = np.array(img_aligned1) # 99x93
c = np.array(img_aligned2) #99x93

# to align b (or c) to a: b[:96,:81]
# all translations were done with reference to the XBIV image (e.g. a)
# this reference can be used to find further translations of future images

# =============================================================================
# PATH_IMG = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\DATA\for_imagej\NBL32'
# FNAME = r'\scan419_aligned.txt'
# PATH_OUT = PATH_IMG+FNAME
# np.savetxt(PATH_OUT, img_aligned)
# =============================================================================


#%%
'''
need to take approach similar to that of FS3 if i want to align more than
two maps at a time; which is the case for XBIC_XBIV_XRF registration

focusing on NBL31 as that electrical response may be more closely related
to the XRF response; collection in this sample is presumed to be 
around the ZnTe-CdTe interface, and our XRF probes around this interface with
some certainty
'''
from skimage.transform import SimilarityTransform, warp
import matplotlib.pyplot as plt
import numpy as np

img0 = NBL31.scan338[0,:,:-2]
img1 = NBL31.scan335[0,:,:-2]
img2 = NBL31.scan341[0,:,:-2]

# translate coordinates read from xml files exportde by ImageJ
    # Plugins --> Registration --> Register Virtual Stack Slices
SHFT1 = SimilarityTransform(translation=(12, 8))
SHFT2 = SimilarityTransform(translation=(2, 12))


# apply translations
IMG1_SHIFT = warp(img1, SHFT1)
IMG2_SHIFT = warp(img2, SHFT2)
IMG3_SHIFT = warp(img3, SHFT3)
IMG4_SHIFT = warp(img4, SHFT4)

# mask according to map with largest offset (img2 (scan330))
mask = IMG2_SHIFT!=0
mask = mask.astype(int)

# multiply values to keep by 1, and values to rid by 0
IMG0_MSK = img0*mask
IMG1_MSK = IMG1_SHIFT*mask
IMG3_MSK = IMG3_SHIFT*mask
IMG4_MSK = IMG4_SHIFT*mask
aligned = [IMG0_MSK,IMG1_MSK,IMG2_SHIFT,IMG3_MSK,IMG4_MSK]

# remove zeros using indices of image with largest offset (img2)
aligned_crop = [arr[45:,62:] for arr in aligned]

# save to folder using "export to imageJ.py"

# make delta maps
DEL0 = aligned_crop[1]-aligned_crop[0]
DEL1 = aligned_crop[2]-aligned_crop[1]
DEL2 = aligned_crop[3]-aligned_crop[2]
DEL3 = aligned_crop[4]-aligned_crop[3]
deltas = [DEL0,DEL1,DEL2,DEL3]