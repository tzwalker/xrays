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
from background_subtraction import rollball_bkgnd_subtraction
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# imitate image process in ImageJ #
def emulate_ImgJ(img, ball_radius, gauss_filt_sigma):
    '''returns image with: 
        background subtract, gauss filt, background subtract'''
    # standardize map
    img1 = standardize_map(img)
    # background-subtracted, standardized data
    img2 = rollball_bkgnd_subtraction(img1, ball_radius)
    # apply gaussian filter
    img3 = gaussian_filter(img2, sigma=gauss_filt_sigma)
    # background subtract image with gaussian filter
    img_fin = rollball_bkgnd_subtraction(img3, ball_radius)
    return img_fin


def check_mask(map_from_a_scan, mask__of_scan):
    plt.imshow(map_from_a_scan)
    plt.imshow(mask__of_scan, cmap='Greys')
    return
# slowly grab averages of masked data #
# extract linear fit values (from standardized data)
# define sample and scan; NAME and NUM for navigation to mask #
SAMP = NBL31; SAMP_NAME = 'NBL31'
SCAN_IDX = 6; SCAN_NUM = str(SAMP.scans[SCAN_IDX])

# retireve mask made in ImageJ #
SYS_PATH = r'Z:\Trumann\XRF images\py_exports_interface'
# change mask: "bound_0in_1out_mask" | "cores_0in_mask"
MASK_PATH = r'\{sam}\scan{scn}\bound_0in_1out_mask.txt'.format(sam=SAMP_NAME, 
               scn=SCAN_NUM)
FULL_PATH = SYS_PATH + MASK_PATH
mask = np.loadtxt(FULL_PATH)

# input images #
X = SAMP.maps[SCAN_IDX][1,:,:-2]
Y = SAMP.maps[SCAN_IDX][1,:,:-2]

# standardized maps if X and Y are fitted data#
X1 = standardize_map(X)
Y1 = standardize_map(Y)

# apply ImageJ processing; returns standardized image data #
#X1 = emulate_ImgJ(X, 10, 1)
#Y1 = emulate_ImgJ(Y, 25, 1)

# check the mask on map of data in X #
mask_plot = np.ma.masked_where(mask == 0, mask) 
check_mask(Y, mask_plot)


Xmask=X1[np.where(mask!=0)]
Ymask=Y1[np.where(mask!=0)]

# prep for fitting #
x=Xmask.ravel().reshape(-1,1)
y=Ymask.ravel().reshape(-1,1)

MODELR = LinearRegression()
FITTING = MODELR.fit(x, y)
ypred = FITTING.predict(x)

#output fit slope
print(FITTING.coef_[0][0], FITTING.intercept_[0])
#output slope error
print(np.sqrt(mean_squared_error(x,y)))


A = np.mean(Y)
B = np.std(Y)
C = np.mean(Ymask)
data_in_mask_avg_in_ug = C*B + A
print(data_in_mask_avg_in_ug)
#%%
import numpy as np
# quickly grab AVERAGE of masked data #
SYS_PATH = r'Z:\Trumann\XRF images\py_exports_interface'
SAMPS = [NBL31, NBL32, NBL33, TS58A]
NAMES = ['NBL31', 'NBL32', 'NBL33', 'TS58A']
SCAN_IDXS = [6,6,6,7]
REGIONS = ['cores_0in_mask', 'bound_0in_1out_mask']
CHANNELS= [1,2,3]

# each item is a sample:
    # each subitem is a region: core 1st, boundary 2nd
    # each subsubitem is ug/cm2 of an element;
    # subsubitem order follows list 'elements'
all_list = []
for samp,name,scan_idx in zip(SAMPS,NAMES,SCAN_IDXS):
    SAMP_LIST = []
    SCAN_NUM = str(samp.scans[scan_idx])
    for region in REGIONS:
        REGION_LIST = []
    # load mask
        MASK_PATH = r'\{sam}\scan{scn}\bound_core\{REG}.txt'.format(sam=name, 
                   scn=SCAN_NUM, REG=region)
        FULL_PATH = SYS_PATH + MASK_PATH
        mask = np.loadtxt(FULL_PATH)
        for chan in CHANNELS:
        # grab data from a given channel
            X = samp.maps[scan_idx][chan,:,:-2]
        #standardize data 
        #(not necessary as its just undone in a few lines)
        #kept here to be consistent; may change later
            #X1 = standardize_map(X)
        # get data in mask pixels
            Xmask=X[np.where(mask!=0)]
        #convert average of (standardized) data within mask to ug/cm2
            #UG_DATA_MEAN = np.mean(X)
            #UG_DATA_STD = np.std(X)
            #STAND_MASKDATA_MEAN = np.mean(Xmask)
            #UG_MASKDATA_MEAN = STAND_MASKDATA_MEAN*UG_DATA_STD + UG_DATA_MEAN
            #UG_MASKDATA_MEAN = np.mean(Xmask)
            UG_MASKDATA_STD = np.std(Xmask)
        #construct averages found in region
            REGION_LIST.append(UG_MASKDATA_STD)
        SAMP_LIST.append(REGION_LIST)
    all_list.append(SAMP_LIST)

# convert extracted averages to array 
all_arr = [np.array(item) for item in all_list]
# make 3d array out of listed 2d arrays
all_arr_3d = np.array(all_arr)
# reshape 3d array to be consistent with origin format
dim1 = all_arr_3d.shape[0]*all_arr_3d.shape[1]
dim2 = all_arr_3d.shape[2]
all_arr_ravel = all_arr_3d.reshape(dim1, dim2)

#%%
# quickly grab TOTALS of masked data #

SAMPS = [NBL31, NBL32, NBL33, TS58A]
NAMES = ['NBL31', 'NBL32', 'NBL33', 'TS58A']
SCAN_IDXS = [6,6,6,7]
REGIONS = ['cores_0in_mask', 'bound_0in_1out_mask']
CHANNELS= [1,2,3]
SYS_PATH = r'Z:\Trumann\XRF images\py_exports_interface'

# each item is a sample:
    # each subitem is a region: core 1st, boundary 2nd
    # each subsubitem is ug/cm2 of an element;
    # subsubitem order follows list 'elements'
all_list = []
for samp,name,scan_idx in zip(SAMPS,NAMES,SCAN_IDXS):
    SAMP_LIST = []
    SCAN_NUM = str(samp.scans[scan_idx])
    for region in REGIONS:
        REGION_LIST = []
    # load mask
        MASK_PATH = r'\{sam}\scan{scn}\{REG}.txt'.format(sam=name, 
                   scn=SCAN_NUM, REG=region)
        FULL_PATH = SYS_PATH + MASK_PATH
        mask = np.loadtxt(FULL_PATH)
        for chan in CHANNELS:
        # grab data from a given channel
            X = samp.maps[scan_idx][chan,:,:-2]
        # get data in mask pixels
            Xmask=X[np.where(mask!=0)]
        #find total ug/cm2 in masked region
            UG_MASKDATA_TOT = np.sum(Xmask)
        #construct averages found in region
            REGION_LIST.append(UG_MASKDATA_TOT)
        SAMP_LIST.append(REGION_LIST)
    all_list.append(SAMP_LIST)

# convert extracted averages to array 
all_arr = [np.array(item) for item in all_list]
# make 3d array out of listed 2d arrays
all_arr_3d = np.array(all_arr)
# reshape 3d array to be consistent with origin format
dim1 = all_arr_3d.shape[0]*all_arr_3d.shape[1]
dim2 = all_arr_3d.shape[2]
all_arr_ravel = all_arr_3d.reshape(dim1, dim2)
