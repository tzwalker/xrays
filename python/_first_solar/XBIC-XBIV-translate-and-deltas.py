"""
coding: utf-8

tzwalker
Sun Apr 19 18:21:43 2020

load data from main-FS3-ASCII.py
this is file is meant for various tasks that are part of processing
the XBIV/C vs Temp data of the FS3 2019_06_2IDD
see docstring of each sub-script for purpose

20200707: these alignments were never saved as separate csvs...
they were only used to plot for the DoE meeting
    -GOAL: make aligned csvs of XBIC, XBIV, and XRF
    to correlate composition performance changes
    
cannot directly use the code from the NBL3 translations because
these are four scans of the same area, not two scans of the same area
    i need to translate both XBIC and XRF relative to the first XBIV map...
"""

"""
translating shift XBIV images
scans 321,325,330,337,342
trimming for delta maps
"""
from skimage.transform import SimilarityTransform, warp
import matplotlib.pyplot as plt
import numpy as np

img0 = FS3.scan321[0,:,:-2]
img1 = FS3.scan325[0,:,:-2]
img2 = FS3.scan330[0,:,:-2]
img3 = FS3.scan337[0,:,:-2]
img4 = FS3.scan342[0,:,:-2]

# translate coordinates read from xml files exportde by ImageJ
    # Plugins --> Registration --> Register Virtual Stack Slices
SHFT1 = SimilarityTransform(translation=(-25, -41))
SHFT2 = SimilarityTransform(translation=(-62, -45))
SHFT3 = SimilarityTransform(translation=(-32, -44))
SHFT4 = SimilarityTransform(translation=(-38, -39))

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


#%%
from skimage.transform import SimilarityTransform, warp
import matplotlib.pyplot as plt
import numpy as np

### start with map with largest offset (img2, scan330)
img2 = FS3.scan330
SHFT2 = SimilarityTransform(translation=(-62, -45))
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

### workflow for translating and masking images with other offsets:
    #import image array
    #translate image arrays
    #mask image arrays
    #store image arrays
img1 = FS3.scan325
SHFT1 = SimilarityTransform(translation=(-25, -41))
shifted_channels1 = []
for i, channel in enumerate(channels):
    IMG1_SHIFT = warp(img1[i,:,:-2], SHFT1)
    # mask the translated maps
    IMG1_MSK = IMG1_SHIFT*mask
    shifted_channels1.append(IMG1_MSK)
shifted_channels1 = np.array(shifted_channels1)   

img3 = FS3.scan337
SHFT3 = SimilarityTransform(translation=(-32, -44))
shifted_channels3 = []
for i, channel in enumerate(channels):
    IMG3_SHIFT = warp(img3[i,:,:-2], SHFT3)
    IMG3_MSK = IMG3_SHIFT*mask
    shifted_channels3.append(IMG3_MSK)
shifted_channels3 = np.array(shifted_channels3) 

img4 = FS3.scan342
SHFT4 = SimilarityTransform(translation=(-38, -39))
# shift (translate) all imported channels
shifted_channels4 = []
for i, channel in enumerate(channels):
    IMG4_SHIFT = warp(img4[i,:,:-2], SHFT4)
    # mask the translated maps
    IMG4_MSK = IMG4_SHIFT*mask
    shifted_channels4.append(IMG4_MSK)
shifted_channels4 = np.array(shifted_channels4) 

### store aligned and masked images
aligned = [shifted_channels0,shifted_channels1,
           shifted_channels2,shifted_channels3,
           shifted_channels4]
### remove zeros according to indices of map with largest offset
aligned_crop = [arr[:,45:,62:] for arr in aligned]

### check alignment of images
# =============================================================================
# for scan in aligned_crop:
#     plt.figure()
#     plt.imshow(scan[1,:,:]) # change this number to check
# #plt.imshow(aligned_crop[0][2,:,:])
# #plt.imshow(aligned_crop[1][2,:,:])
# =============================================================================

PATH_OUT = r'C:\Users\triton\Dropbox (ASU)\1_FS_operando\XBIC_XBIV aligned image csvs'
SCAN_STR = ['scan321','scan']

# =============================================================================
# """
# parsing,reading,andextracting SIFT translation from ImageJ
# decided it was better just to do it by hand (only 5 images);
# opened each xml, entered the delx and dely into
# 'for_ImageJ_output_xml_delx_dely.csv'
# """
# import xml.etree.ElementTree as ET
# XML_PATH = r'C:\Users\triton\FS3_2019_06_operando\for_imageJ\output'
# XML_FILE = r'\scan325_XBIV.xml'
# XML = XML_PATH + XML_FILE
# 
# doc = ET.parse(XML)
# root = doc.getroot()
# 
# # get xy translation from XML file exported
# # using ImageJ plugin Register Virtual Stack Slices
# print(root[0].attrib['data']) 
# =============================================================================
    

# =============================================================================
# """export plan-view maps as arrays for histograms in OriginLab"""
# # note: voltage is primarily affected by temperature, not current
#     # for DoE report, want to plot voltage histogram of same area from 25-100C
# import numpy as np
# 
# eh_maps = [scan[0,:,:-2] for scan in FS3.maps]
# eh_arr = [array.ravel() for array in eh_maps]
# arrs = np.array(eh_arr).T
# fname = r"\XBIVvTemp_scans321_325_330_337_342_hist.csv"
# path = r'C:\Users\triton\FS3_2019_06_operando'
# out = path + fname
# np.savetxt(out, arrs, delimiter=",")
# =============================================================================

# =============================================================================
# """checking normal stats of xbic maps"""
# #xbic_maxs = [np.max(array[0,:,:-2]) for array in xbicscans]
# xbic_avgs = [np.mean(array) for array in xbic_maps]
# #maxes = np.array(xbic_maxs)
# avgs = np.array(xbic_avgs)
# p = [25,50,75] # percentiles
# xbic_percentiles = [np.percentile(array, p) for array in xbic_maps]
# percentiles = np.array(xbic_percentiles)
# #merge = np.concatenate((maxes.reshape(-1,1),avgs.reshape(-1,1)), axis=1)
# # see ppt notes for maxes and mins of XBIC for same area from 25-100C
# =============================================================================





