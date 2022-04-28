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
from matplotlib import colors
from matplotlib.patches import Rectangle

# define spatial extent of kernel (of interaction)
# maps show there is an effect over at least 10um, therefore the spatial extent
# should be at least this many pixels (for a 250nm step)
gx_len = 41 #10um
gy_len = 41 #10um
x, y = np.arange(gx_len), np.arange(gy_len)

# define center of kernel and its width
x0, y0 = int(gx_len/2), int(gy_len/2)

# define interaction spread
# change this so that at least half of the spatial extent is filled with color
# this parameter can be interpreted as the extent the beam doses the cell
# outside the pixel that is being illuminated 
sigma = 3

# calculate kernel
gx = np.exp(-(x-x0)**2/(2*sigma**2))
gy = np.exp(-(y-y0)**2/(2*sigma**2))
g = np.outer(gx, gy)
plt.figure()
plt.imshow(g)

energy = 12020807.330590038 #J/cm3
# create energy dose to kernel
example_radiant_distribution = g*energy #J/cm3

# define measurement area
# for computation purposes,
# the area must be large enough to contain the kernel !!!
# large map was 101 x 61; therefore double resolution since that was
# step size used to take smaller maps
# 
xdim = gx_len*2
ydim = gy_len*2
area = np.zeros((xdim, ydim)) # map

#dose_area  = area.copy()
# define size of smaller map
# small map was in 20 pixels of large map; therefore small map will be 40 pixels at this resolution
l = np.arange(gx_len)
m = np.arange(gy_len)
doses_y = []
for pixel_idy in m:
    doses_x = []
    dose_area = area.copy()
    for pixel_idx in l:
        dose_area[pixel_idy:pixel_idy+gx_len, pixel_idx:pixel_idx+gy_len] = example_radiant_distribution
        dose_area_after = dose_area.copy()
        #plt.figure()
        #plt.imshow(dose_area)
        doses_x.append(dose_area_after)
    doses_arr_x = np.array(doses_x)
    dose_sum_x = doses_arr_x.sum(axis=0)
    doses_y.append(dose_sum_x)
doses_arr_y = np.array(doses_y)
dose_sum_y = doses_arr_y.sum(axis=0)

fig, ax = plt.subplots()
im = ax.imshow(dose_sum_y,norm=colors.LogNorm(vmin=0.01,vmax=1e9))
ax.add_patch(Rectangle((20, 20), 40, 40, linestyle = 'dashed', facecolor="none", ec='k', lw=1))
fig.colorbar(im)

#  this is wrong... the box is drawn around the area where the gaussian kernel should start
    # but the guassian kernel is starting in the to pleft corner of the enitre area...
    # not the measurement area...

