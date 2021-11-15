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
translating shift XBIC images
scans [323,327,332,339,344]
trimming for delta maps
"""
# =============================================================================
# from skimage.transform import SimilarityTransform, warp
# import matplotlib.pyplot as plt
# import numpy as np
# 
# img0 = FS3.scan323[0,:,:-2]
# img1 = FS3.scan327[0,:,:-2]
# img2 = FS3.scan332[0,:,:-2]
# img3 = FS3.scan339[0,:,:-2]
# img4 = FS3.scan344[0,:,:-2]
# 
# # translate coordinates read from xml files exportde by ImageJ
#     # Plugins --> Registration --> Register Virtual Stack Slices
# SHFT1 = SimilarityTransform(translation=(-13, -11))
# SHFT2 = SimilarityTransform(translation=(-44, -19))
# SHFT3 = SimilarityTransform(translation=(-11, -8))
# SHFT4 = SimilarityTransform(translation=(-13, 24))
# 
# # apply translations
# IMG1_SHIFT = warp(img1, SHFT1)
# IMG2_SHIFT = warp(img2, SHFT2)
# IMG3_SHIFT = warp(img3, SHFT3)
# IMG4_SHIFT = warp(img4, SHFT4)
# sh_imgs = [img0,IMG1_SHIFT,IMG2_SHIFT,IMG3_SHIFT,IMG4_SHIFT]
# 
# # mask according to map with largest offset (img2 (scan330))
# mask = IMG2_SHIFT!=0
# mask = mask.astype(int)
# 
# # multiply values to keep by 1, and values to rid by 0
# IMG0_MSK = img0*mask
# IMG1_MSK = IMG1_SHIFT*mask
# IMG3_MSK = IMG3_SHIFT*mask
# IMG4_MSK = IMG4_SHIFT*mask
# aligned = [IMG0_MSK,IMG1_MSK,IMG2_SHIFT,IMG3_MSK,IMG4_MSK]
# 
# # remove zeros using indices of image with largest offset (img2)
# aligned_crop = [arr[45:,62:] for arr in aligned]
# 
# # save to folder using "export to imageJ.py"
# 
# # make delta maps
# DEL0 = aligned_crop[1]-aligned_crop[0]
# DEL1 = aligned_crop[2]-aligned_crop[1]
# DEL2 = aligned_crop[3]-aligned_crop[2]
# DEL3 = aligned_crop[4]-aligned_crop[3]
# deltas = [DEL0,DEL1,DEL2,DEL3]
# =============================================================================



from skimage.transform import SimilarityTransform, warp
import numpy as np

### start with map with largest offset
img2 = FS3.scan339
SHFT2 = SimilarityTransform(translation=(-11, -8))
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
img0 = FS3.scan323
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

img3 = FS3.scan339
SHFT3 = SimilarityTransform(translation=(-11, -8))
shifted_channels3 = []
for i, channel in enumerate(channels):
    IMG3_SHIFT = warp(img3[i,:,:-2], SHFT3)
    IMG3_MSK = IMG3_SHIFT*mask
    shifted_channels3.append(IMG3_MSK)
shifted_channels3 = np.array(shifted_channels3) 


### store aligned and masked images
aligned = [shifted_channels0,
           shifted_channels2]

### remove zeros according to indices of map with largest offsets
# in the XBIC images, the last 100C map is cut off both above and below, 
    # from row indices 19:176
aligned_crop = [arr[:,8:,11:] for arr in aligned]


# save aligned arrays for further processing
PATH_OUT = r'C:\Users\triton\Dropbox (ASU)\2_FS_operando\XBIC aligned image csvs\cts_per_s_XRF'
SCAN_STR = ['scan323','scan339']
CHANNELS = ['us_ic', 'Se', 'Cd', 'Te', 'Au']

for i,scan in enumerate(aligned_crop):
    for j,chan in enumerate(CHANNELS):
        FNAME = r'\FS3_{scn}_{chn}.csv'.format(scn=SCAN_STR[i], chn=CHANNELS[j])
        array = scan[j,:,:]
        np.savetxt(PATH_OUT+FNAME, array, delimiter=',')
        
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





