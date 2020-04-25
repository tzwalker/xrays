"""
coding: utf-8

tzwalker
Sun Apr 19 18:21:43 2020

this is to import stats of plan view xbic maps into Origin
"""

import numpy as np
xbic_maps = [scan[0,:,:-2] for scan in FS3.maps]

#xbic_maxs = [np.max(array[0,:,:-2]) for array in xbicscans]
xbic_avgs = [np.mean(array) for array in xbic_maps]

#maxes = np.array(xbic_maxs)
avgs = np.array(xbic_avgs)

p = [25,50,75] # percentiles
xbic_percentiles = [np.percentile(array, p) for array in xbic_maps]
percentiles = np.array(xbic_percentiles)
#merge = np.concatenate((maxes.reshape(-1,1),avgs.reshape(-1,1)), axis=1)

import numpy as np
import matplotlib.pyplot as plt


xbic_maps = [scan[0,:,:-2] for scan in FS3.maps]

for array in xbic_maps:
    plt.figure()
    plt.imshow(array,vmin=5.6E-8,vmax=9E-8)

