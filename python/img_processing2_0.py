'''
import mask made in imagek
standardize data
process image
extract data from mask
simple linear regression
generate scatter plot and slopes for a set of two variables
manually enter slope output form this program to Origin

partially emulate ImageJ processing prodcedures (for NBL3 CdTe)

the intention of this program is to quantify the Cu decoration
at the grain boundaries
we can readily observe some correlation by eye in the processed images,
but when correlations are done using unprocessed data, the patterns
may not be nearly as strong as the processed images suggest

therefore, it only makes sense to process the data in the same way as was done
in ImageJ, then perform the correlation with these processed data
the hypothesis here is the observed correlations will increase

'''

import numpy as np
from standardize_map import standardize_map
import matplotlib.pyplot as plt
#from sklearn.linear_model import LinearRegression
#from sklearn.metrics import mean_squared_error

# imitate image process in ImageJ #
# =============================================================================
# from background_subtraction import rollball_bkgnd_subtraction
# from scipy.ndimage import gaussian_filter
# def emulate_ImgJ(img, ball_radius, gauss_filt_sigma):
#     '''returns image with: 
#         background subtract, gauss filt, background subtract'''
#     # standardize map
#     img1 = standardize_map(img)
#     # background-subtracted, standardized data
#     img2 = rollball_bkgnd_subtraction(img1, ball_radius)
#     # apply gaussian filter
#     img3 = gaussian_filter(img2, sigma=gauss_filt_sigma)
#     # background subtract image with gaussian filter
#     img_fin = rollball_bkgnd_subtraction(img3, ball_radius)
#     return img_fin
# =============================================================================

def check_mask(map_from_a_scan, mask__of_scan):
    plt.imshow(map_from_a_scan)
    plt.imshow(mask__of_scan, cmap='Greys')
    return

# define sample and scan; NAME and NUM for navigation to mask #
SAMP = NBL33; SAMP_NAME = 'NBL33'
SCAN_IDX = 6; SCAN_NUM = str(SAMP.scans[SCAN_IDX])

# retireve mask made in ImageJ #
SYS_PATH = r'Z:\Trumann\XRF images\py_exports_interface'
# change mask: "bound_0in_1out_mask" | "cores_0in_mask"
MASK_PATH = r'\{sam}\scan{scn}\bound_core\cores_0in_mask.txt'.format(sam=SAMP_NAME, 
               scn=SCAN_NUM)
FULL_PATH = SYS_PATH + MASK_PATH
mask = np.loadtxt(FULL_PATH)

# input images #
X = SAMP.maps[SCAN_IDX][1,:,:-2]
Y = SAMP.maps[SCAN_IDX][2,:,:-2]

# standardized maps if X and Y are fitted data#
X1 = standardize_map(X)
Y1 = standardize_map(Y)

# apply ImageJ processing; returns standardized image data #
#X1 = emulate_ImgJ(X, 10, 1)
#Y1 = emulate_ImgJ(Y, 25, 1)

# check the mask on map of data in X #
#mask_plot = np.ma.masked_where(mask == 0, mask) 
#check_mask(Y1, mask_plot)

# get data in mask pixels
Xmask=X1[np.where(mask!=0)]
Ymask=Y1[np.where(mask!=0)]

# prep for fitting #
x=Xmask.ravel().reshape(-1,1)
y=Ymask.ravel().reshape(-1,1)

#MODELR = LinearRegression()
#FITTING = MODELR.fit(x, y)
#ypred = FITTING.predict(x)

#output fit slope
#print(FITTING.coef_[0][0], FITTING.intercept_[0])
#output slope error
#print(np.sqrt(mean_squared_error(x,y)))

#convert average of data within mask (standardized) to concentration
A = np.mean(Y)
B = np.std(Y)
C = np.mean(Ymask)
data_in_mask_avg_in_ug = C*B + A
print(data_in_mask_avg_in_ug)
#%%
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
