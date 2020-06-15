'''
used this in conjunction with "plot_scalebar.py"
to get masks on top of original data maps
with a scalebar

input variable 'masked' into plot_scalebar.py
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
