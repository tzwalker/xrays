# -*- coding: utf-8 -*-
"""
kineticcross
Mon Aug 26 17:49:23 2019
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from scipy import stats
from put_nans_back_on import put_nans_back_on

cu_arr = NBL3_2['c_stand_arrs'][0][:,1]
xbic_arr =  NBL3_2['c_stand_arrs'][0][:,0]


slope, intercept, r_squared, p_value, std_err = stats.linregress(cu_arr, xbic_arr)


wanted_indices = np.where(xbic_arr > 2)
thres_cu_map = cu_arr[wanted_indices]
thres_xbic_map = xbic_arr[wanted_indices]

plt.figure()
#data = [thres_cu_map, thres_xbic_map]
#plt.boxplot(data)
plt.scatter(cu_arr, xbic_arr, s=4)


