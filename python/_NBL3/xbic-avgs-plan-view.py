"""
coding: utf-8

tzwalker
Sun Apr 19 18:21:43 2020

this is to import xbic max of NBL3 plan view data into Origin
want to make boxplots that show NBL31 xbic > NBL33 xbic
"""


import numpy as np
xbicscans = TS58A.maps[0:3] + TS58A.maps[6:10]

xbic_maxs = [np.max(array[0,:,:-2]) for array in xbicscans]
xbic_avgs = [np.mean(array[0,:,:-2]) for array in xbicscans]

maxes = np.array(xbic_maxs)
avgs = np.array(xbic_avgs)

merge = np.concatenate((maxes.reshape(-1,1),avgs.reshape(-1,1)), axis=1)

a = np.array([378,379,380,385,386,387,388])

#%%
# plotting for Eric
import matplotlib.pyplot as plt

fig, ax = plt.subplots(2,2)
plt.tight_layout(w_pad=-10)
ax[0,0].imshow(NBL33.scan264[0,:,:], cmap='magma')
ax[0,0].set_axis_off()
ax[0,1].imshow(NBL33.scan264[1,:,:], cmap='Reds_r')
ax[0,1].set_axis_off()
ax[1,0].imshow(NBL33.scan264[4,:,:], cmap='Greys_r')
ax[1,0].set_axis_off()
ax[1,1].imshow(NBL33.scan264[3,:,:], cmap='Greens_r')
ax[1,1].set_axis_off()