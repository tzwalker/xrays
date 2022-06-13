# -*- coding: utf-8 -*-
"""

Trumann
Thu Jun  9 16:31:45 2022

run "ToFSIMS_v2" before this program

this program is meant to get the Cl count rate from the grain boundaries

"""

import numpy as np
import matplotlib.pyplot as plt

Cl = img.copy()
gb = out.copy()

val = Cl*gb
#plt.imshow(val,vmax=0.5)

valarr = val.copy().astype('float64')
valarr[valarr==0] = np.nan
valarr = valarr.ravel()

fig, ax1 = plt.subplots()
ax1.hist(valarr, color = "grey", alpha = 0.5, label='0hr',log=True) # 0hr
ax1.set_ylim(0.1,1e4)
ax1.legend()
ax1.set_xlabel("Cl Ion Count")
ax1.set_ylabel("Pixel Count")

#%%
'''this cell for use with _v2_imJreplica500hr'''
Cl1 = img.copy()
gb1 = out.copy()

val1 = Cl1*gb1
#plt.imshow(val1,vmax=0.5)

valarr1 = val1.copy().astype('float64')
valarr1[valarr1==0] = np.nan
valarr1 = valarr1.ravel()

hbins = 20
fig, (ax1,ax2) = plt.subplots(nrows=2,ncols=1,sharex=True)
ax1.hist(valarr, color = "grey", alpha = 0.5, bins=10, label='0hr', log=True) # 0hr
ax1.set_ylim(0.1,1e5)
ax1.legend()
ax1.set_ylabel("Pixel Count")

ax2.hist(valarr1, color = "red", alpha = 0.5, bins=10, label = '500hr', log=True) # 500hr
ax2.set_ylim(0.1,1e5)
ax2.legend()
ax2.set_xlabel("Cl Ion Count")
ax2.set_ylabel("Pixel Count")