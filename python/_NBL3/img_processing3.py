'''
used this in conjunction with "plot_scalebar.py"
to get masks on top of original data maps
with a scalebar

input variable 'masked' into plot_master.py
'''

import numpy as np
import matplotlib.pyplot as plt

# define sample and scan; NAME and NUM for navigation to mask #
SAMP = NBL31; SAMP_NAME = 'NBL31'
SCAN_IDX = 6; SCAN_NUM = str(SAMP.scans[SCAN_IDX])

# retireve mask made in ImageJ #
SYS_PATH = r'Z:\Trumann\XRF images\py_exports_interface'
# change mask: "bound_0in_1out_mask" | "cores_0in_mask"
MASK_PATH = r'\{sam}\scan{scn}\bound_core\bound_0in_1out_mask.txt'.format(sam=SAMP_NAME, 
               scn=SCAN_NUM)
FULL_PATH = SYS_PATH + MASK_PATH
mask = np.loadtxt(FULL_PATH)

img = NBL31.maps[SCAN_IDX][3,:,:-2]
masked = np.ma.masked_where(mask == 255, img)
plt.imshow(masked)

#%%
'''
there was code here that was to get the average of the pixels within the masks
drawn by hand; see img_processing2.py for quick averages and totals
'''

'''
this was to see what the histograms of the Cu maps looked like
because it wasn't clear if they were normally distributed... in which case
the whole standardization procedure sort of fails...
'''
Cu_NBL31 = [MAP[1,:,:-2] for MAP in NBL31.maps[6:10]]
Cu_NBL32 = [MAP[1,:,:-2] for MAP in NBL32.maps[6:10]]
Cu_NBL33 = [MAP[1,:,:-2] for MAP in NBL33.maps[6:10]]
Cu_TS58A = [MAP[1,:,:-2] for MAP in TS58A.maps[6:10]]


import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter
# =============================================================================
# colors = ['red', 'blue', 'green', 'grey']
# for idx, Cu_map in enumerate(Cu_NBL32):
#     array = Cu_map.ravel()
#     plt.hist(array, color = colors[idx], alpha=0.25, bins=36)
#     #plt.xlim([0,10])
# =============================================================================

# =============================================================================
# copy = [array.copy() for array in Cu_NBL32]
# img_gaus = [gaussian_filter(img, sigma=1) for img in copy]
# for array in copy:
#     # ZnTe|CdTe interface threshold
#     array[array>0.832832] = np.nan
#     array[array<0.306381771] = np.nan
# 
#     plt.figure()
#     plt.imshow(array)
# =============================================================================

copy = [array.copy() for array in Cu_NBL33]
img_gaus = [gaussian_filter(img, sigma=1) for img in copy]
for array in copy:
    # ZnTe|CdTe interface threshold
    array[array>3.331328] = np.nan
    array[array<1.225527083] = np.nan

    plt.figure()
    plt.imshow(array)

#%%
"""
experimenting with Otsu thresholding XBIC maps to make quantitative
comparisons between shunted areas in plan-view XBIC maps

look in "superpixels_quick.py" for additional codes:
    -use superpixel segmentation boundaries as mask
    -access the inside averages of each superpixel
"""
import matplotlib.pyplot as plt
import numpy as np
from standardize_map import standardize_map
from skimage.segmentation import slic,mark_boundaries
from skimage import color

def mark_superpixels(img, edges):
    # initiate RGB image; color=(i,j,k) corresponds to bm[:,:,(i,j,k)] 
    bm = mark_boundaries(img, edges, color=(1,0,0)) #-> color is RGB
    # make boolean mask where color channel==1 above (e.g. 1,0,0 --> red)
    bm_mask = bm[:,:,0] == 1
    # make a copy of the image (to preserve original data)
    img_copy = img.copy()
    # in copy image, where bm_mask is True, convert to nan
    img_copy[bm_mask] = np.nan #--> could make function to convert to a color
    return img_copy

# use filtered, fast scan
img = NBL31.scan341[0,:,:-2]
#img = NBL33.scan264[0,:,:-2]
img_stand = standardize_map(img)
# prepare for SLIC segmentation; float32 to float64
img_cln = img_stand.astype('float64')
# simple linear iterative clustering (SLIC) segmentation
labels = slic(img_cln, n_segments=75, compactness=1,sigma=1)
plt.imshow(mark_superpixels(img_cln, labels))

# replacing with average #
# non-zero labels for regionprops,color
labels = labels + 1  
# replace each segment with its average
sup_pix_avgs = color.label2rgb(labels, img_cln, kind='avg')
plt.imshow(sup_pix_avgs)

x = sup_pix_avgs.ravel()
plt.figure()
plt.hist(x,bins=50)

# these superpixel images are not returning bimodal distributions...
# tried an XBIC image from both NBL33 and NBL31
# going to try to see what manual threholding might accomplish
    # the number of pixels in the 10th percentil is probably much lower
    # in NBL33 and TS58A than NBL31 and NBL32


#%%
"""
this was used to test normalizztion procedure as outlined by
Michael in his perovskite paper
    sum along the row of an image, then divide the pixels of a row
    by the sum of the row
it was also used to experiment with different manual thresholds
"""
# use unfiltered, slow scan; these scans best resolve pinhole features
import matplotlib.pyplot as plt
import numpy as np

#img_lo = NBL31.scan341[0,:,:-2]
img = NBL33.scan264[0,:,:-2]
#im_stlo = standardize_map(img_lo)
img_stand = standardize_map(img)

# apply ro-sum normalization, as outlined by Michael in perovskite paper
arr_norm = np.sum(img,axis=1)
norm = img / arr_norm[:,None]

# if i will count pixels, percentile cannot be used
    # 10th percentile implies 1000 pixels, 20th 2000 pixels, etc.

threshold = np.percentile(norm, q=15) # what else could this threshold be...?
y_new = np.ma.masked_where(norm<threshold, norm)
plt.imshow(y_new)

pts_blw_thrs = np.count_nonzero(y_new.mask)


