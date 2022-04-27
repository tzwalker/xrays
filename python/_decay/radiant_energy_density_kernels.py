# -*- coding: utf-8 -*-
"""

Trumann
Wed Apr 27 07:35:10 2022

this program is meant to simulate the dosage accumulation in a CdTe cell

the absorber is assumed ot be 3um or thicker, therefore the energy fraction
absorbed is assumed to be near 1.0 (following Stuckelberger, 2017, JMR)


"""

''' this cell calculates the cumulative dose sum for one row'''

# https://stackoverflow.com/questions/28949249/efficiently-generate-shifted-gaussian-kernel-in-python

import numpy as np
import matplotlib.pyplot as plt

# define center of kernel and its width
x0, y0, sigma = 5, 5, 1

# define spatial extent of kernel
gx_len = 11
gy_len = 11
x, y = np.arange(gx_len), np.arange(gy_len)

# calculate kernel
gx = np.exp(-(x-x0)**2/(2*sigma**2))
gy = np.exp(-(y-y0)**2/(2*sigma**2))
g = np.outer(gx, gy)

# create energy dose to kernel
example_radiant_distribution = g*radiant_energy_density #J/cm3

# define measurement area
# for computation purposes,
# the area must be large enough to contain the kernel
space = 21
area = np.zeros((space+gx_len, space+gy_len)) # map


dose_area  = area.copy()
l = np.arange(space)
doses = []
for pixel_idx in l:
    dose_area[0:11, pixel_idx:pixel_idx+11] = example_radiant_distribution
    dose_area_after = dose_area.copy()
    #plt.figure()
    #plt.imshow(dose_area)
    doses.append(dose_area_after)
doses_arr = np.array(doses)
does_sum = doses_arr.sum(axis=0)

plt.figure()
plt.imshow(does_sum)

#%%

''' this cell calculates the cumulative dose sum for a map'''

# https://stackoverflow.com/questions/28949249/efficiently-generate-shifted-gaussian-kernel-in-python

import numpy as np
import matplotlib.pyplot as plt

# define center of kernel and its width
x0, y0, sigma = 5, 5, 1

# define spatial extent of kernel
gx_len = 11
gy_len = 11
x, y = np.arange(gx_len), np.arange(gy_len)

# calculate kernel
gx = np.exp(-(x-x0)**2/(2*sigma**2))
gy = np.exp(-(y-y0)**2/(2*sigma**2))
g = np.outer(gx, gy)

energy = 12020807.330590038 #J/cm3
# create energy dose to kernel
example_radiant_distribution = g*energy #J/cm3

# define measurement area
# for computation purposes,
# the area must be large enough to contain the kernel
space = 21
area = np.zeros((space+gx_len, space+gy_len)) # map

dose_area  = area.copy()
l = np.arange(21)
m = np.arange(10)
doses_y = []
for pixel_idy in m:
    doses_x = []
    dose_area = area.copy()
    for pixel_idx in l:
        dose_area[pixel_idy:pixel_idy+11, pixel_idx:pixel_idx+11] = example_radiant_distribution
        dose_area_after = dose_area.copy()
        #plt.figure()
        #plt.imshow(dose_area)
        doses_x.append(dose_area_after)
    doses_arr = np.array(doses_x)
    does_sum = doses_arr.sum(axis=0)
    doses_y.append(does_sum)
doses_arr_y = np.array(doses_y)
does_sum_y = doses_arr_y.sum(axis=0)

plt.figure()
plt.imshow(does_sum_y)
# =============================================================================
# dose_area  = area.copy()
# l = np.arange(3)
#     dose_area  = area.copy()
#     for pixel_idx in m:
#         dose_area[pixel_idy:pixel_idy+11, pixel_idx:pixel_idx+11] = example_radiant_distribution
#         plt.figure()
#         plt.imshow(dose_area)
# =============================================================================