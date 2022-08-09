# -*- coding: utf-8 -*-
"""

Trumann
Wed Jun 22 09:50:39 2022

this prgram helps plot the quantified Cl vs the coutn Cl
"""

'''this cell is for count Cl'''

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from skimage import io

PATH_TOF = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Cl_maps.tif"

# import ToF-SIMS image
TOF = io.imread(PATH_TOF)

TOF_slice = TOF[1:4,:,:].sum(axis=0)
#TOF_slice = TOF[0,:,:].astype('float64')


# alter image to match EBSD in EBSD_v1.py
img = np.rot90(TOF_slice, k=1)   # rotate image
img = np.flipud(img)                # flip along horizontal axis

fig, ax = plt.subplots(figsize=(10,10))
im = ax.imshow(img,interpolation='none',vmin=0,vmax=3)#,norm=LogNorm(vmin=1e18, vmax=1e21))
cax1 = fig.add_axes([ax.get_position().x1+0.025,ax.get_position().y0,0.025,ax.get_position().height])

ax.axis('off')

fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))


cbar = fig.colorbar(im,cax=cax1)
cbar.ax.set_ylabel('Cl (cts/s)', rotation=90, va="bottom", size=18, labelpad=50)
cbar.ax.tick_params(labelsize=18)
#cbar.yaxis.(labelsize=18)
#cbar.ax.yaxis.set_offset_position('left')
#cbar.ax.yaxis.offsetText.set(size=18)

#%%
'''this cell is for quantified Cl'''

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from skimage import io

# set path to tiff files
file_Cl_0hr = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Cl_maps_quantified.tif"

# import ToF-SIMS image
Cl = io.imread(file_Cl_0hr)

# integrate along depth
section1 = Cl[1:10,:,:].sum(axis=0)
img = np.rot90(section1, k=1)   # rotate image
img = np.flipud(img)                # flip along horizontal axis


fig, ax = plt.subplots(figsize=(10,10))
im = ax.imshow(img,interpolation='none',vmin=1e18,vmax=8.5e19)#,norm=LogNorm(vmin=1e18, vmax=1e21))
cax1 = fig.add_axes([ax.get_position().x1+0.025,ax.get_position().y0,0.025,ax.get_position().height])

ax.axis('off')

fmt = mticker.ScalarFormatter(useMathText=True)
fmt.set_powerlimits((0, 0))

cbar = fig.colorbar(im,cax=cax1,format=fmt)
cbar.ax.set_ylabel('Cl (atom/cm$^3$)', rotation=90, va="bottom", size=18, labelpad=50)
cbar.ax.tick_params(labelsize=18)
#cbar.yaxis.(labelsize=18)
cbar.ax.yaxis.set_offset_position('left')
cbar.ax.yaxis.offsetText.set(size=18)