'''
background subtract like in imageJ
then apply ug/cm2 threshold according to 1/e absorption
e.g. 
for Cu, the calculated absorption for the 75,15 geometry
yielded a threshold of 1.225527083 ug/cm2, see excel file:
"xrf absorption - thresholding.xlsx"; this calculation should be double
checked, the density of the element (8.96 g/cm3) is the
ratio between the calculated ug/cm2 and the depth of a (cubic) Cu voxel

however, when this threshold is applied to the normal map, almost everything
in the map is kept, that threshold is useless

i just want to see what the mask looks like after a background substraction has
happened; that's what i did in imageJ to get the pretty images...

background subtract
convert stnadardized background subtracted data back to ug/cm2
then apply threshold

'''

import numpy as np
from standardize_map import standardize_map
from background_subtraction import background_subtraction
from scipy.ndimage import gaussian_filter

# input images #
img = NBL33.scan264[1,:,:-2].copy()

# standardize data (to conveniently apply background substraction)
img_stand = standardize_map(img)

# apply gaussian filter (to account for interaction volume extending beyond
# the width of a pixel)
img_gaus = gaussian_filter(img_stand, sigma=1)

# subtract background (to account for secondary particle XRF)
img_sub = background_subtraction(img_gaus, 10)

# convert standardized data back to ug/cm2
MEAN = np.mean(img)
STD_DEV = np.std(img)
img_end = STD_DEV*img_sub + MEAN


# define ug/cm2 threshold (taken from excel file)
threshold = 1.225527083
# make boolean mask
mask = img_sub>2
# make binary mask
mask = mask.astype(int)

img_mask = img_end*mask




