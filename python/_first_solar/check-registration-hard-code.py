"""
coding: utf-8

tzwalker
Thu Apr 30 17:29:36 2020
run main-FS3-ASCII.py before running this program
-if global variables arent referenced, go to Tools-Preferences-Run:
    General Settings-check 'run in console's namspace instead of empty one

translating shift XBIV images
scans 321,325,330,337,342
the change of coordinate in 'for_ImageJ_output_xml_delx_dely.csv'
is cumulative for each scan, e.g. 
scan 321 is reference for 325,
scan 325 is reference for 330, 
scan 330 is reference for 337, etc.
see inside of that csv for details
"""


from skimage.transform import SimilarityTransform, warp
import matplotlib.pyplot as plt
import numpy as np

img0 = FS3.scan321[0,:,:-2]
img1 = FS3.scan325[0,:,:-2]
img2 = FS3.scan330[0,:,:-2]
img3 = FS3.scan337[0,:,:-2]
img4 = FS3.scan342[0,:,:-2]

shft1 = SimilarityTransform(translation=(-25, -41))
shft2 = SimilarityTransform(translation=(-62, -45))
shft3 = SimilarityTransform(translation=(-32, -44))
shft4 = SimilarityTransform(translation=(-38, -39))

img1_shift = warp(img1, shft1)
img2_shift = warp(img2, shft2)
img3_shift = warp(img3, shft3)
img4_shift = warp(img4, shft4)

fig, (ax0,ax1,ax2,ax3,ax4) = plt.subplots(5,1)
ax0.imshow(img0); ax0.axis('off')
ax1.imshow(img1_shift, vmin=np.min(img1)); ax1.axis('off')
ax2.imshow(img2_shift, vmin=np.min(img2)); ax2.axis('off')
ax3.imshow(img3_shift, vmin=np.min(img3)); ax3.axis('off')
ax4.imshow(img4_shift, vmin=np.min(img4)); ax4.axis('off')