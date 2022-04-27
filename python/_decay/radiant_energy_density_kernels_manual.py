# -*- coding: utf-8 -*-
"""

Trumann
Wed Apr 27 09:55:02 2022


"""

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
area = np.zeros((21+gx_len, 21+gy_len)) # map


dose_area  = area.copy()
plt.figure()
plt.imshow(dose_area)

dose_area1  = area.copy()
dose_area2 = area.copy()
dose_area3 = area.copy()
dose_area4 = area.copy()
dose_area5 = area.copy()

# apply kernel to first pixel
dose_area1[0:11,0:11] = example_radiant_distribution
plt.figure()
plt.imshow(dose_area1)

# apply kernel to second pixel
dose_area2[0:11,1:12] = example_radiant_distribution
plt.figure()
plt.imshow(dose_area2)

# apply kernel to third pixel
dose_area3[0:11,2:13] = example_radiant_distribution
plt.figure()
plt.imshow(dose_area3)

# apply kernel to fourth pixel
dose_area4[0:11,3:14] = example_radiant_distribution
plt.figure()
plt.imshow(dose_area4)

# apply kernel to fifth pixel
dose_area5[0:11,4:15] = example_radiant_distribution
plt.figure()
plt.imshow(dose_area5)

# sum the dosages
dose_area = dose_area1 + dose_area2 + dose_area3 + dose_area4 + dose_area5
plt.figure()
plt.imshow(dose_area)

