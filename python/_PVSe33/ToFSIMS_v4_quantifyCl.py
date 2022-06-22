# -*- coding: utf-8 -*-
"""

Trumann
Wed Jun 22 08:16:36 2022

this program brings together the Cl and Te map data to quantify Cl

the quantification advice is given in the presentation 
shared by Steve Harvey 20200304

"""

from skimage import io
import numpy as np
import tifffile
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# set path to tiff files
file_Cl_0hr = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Cl_maps.tif"
file_Te_0hr = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Te_maps.tif"

# import ToF-SIMS images
Cl0 = io.imread(file_Cl_0hr)
Te0 = io.imread(file_Te_0hr)

# construct (empty) quantified array 
res = np.zeros((49,512,512),float)

# quantify each depth slice and fill quantified array
for depth in range(Cl0.shape[0]):
    # get depth slice in each map
    Cl = Cl0[depth,:,:].astype('float32')
    Te = Te0[depth,:,:].astype('float32')
    
    # set Te zeros to nan (can't say what Cl quantities are in those pixels)
    Te[np.where(Te==0)] = np.nan
    
    # divide Cl intensity by Te intensity pixel-by-pixel
    ratio = Cl/Te
    
    # scale ratio by quantification factor
    quant = ratio*3.8097e19
    
    # fill quantified array with quantified Cl
    res[depth,:,:] = quant


# construct integration
integration = res.copy()

# convert nan back to zeroes
integration[np.isnan(integration)] = 0

# integrate along depth
section = integration[1:10,:,:].sum(axis=0)

# save reconstructed data cube
#PATH_OUT = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Cl_maps_quantified.tif"
#tifffile.imsave(PATH_OUT, integration, bigtiff=True)

# =============================================================================
# # alter image to match orientation of other plots
# img = np.rot90(section, k=1)   # rotate image
# img = np.flipud(img)                # flip along horizontal axis
# 
# fig, ax = plt.subplots(figsize=(10,10))
# im = ax.imshow(img,interpolation='none',vmin=1e18,vmax=8.5e19)#,norm=LogNorm(vmin=1e18, vmax=1e21))
# cax1 = fig.add_axes([ax.get_position().x1+0.025,ax.get_position().y0,0.025,ax.get_position().height])
# 
# ax.axis('off')
# 
# fmt = mticker.ScalarFormatter(useMathText=True)
# fmt.set_powerlimits((0, 0))
# 
# 
# cbar = fig.colorbar(im,cax=cax1,format=fmt)
# cbar.ax.set_ylabel('Cl (atom/cm$^3$)', rotation=90, va="bottom", size=18, labelpad=50)
# cbar.ax.tick_params(labelsize=18)
# #cbar.yaxis.(labelsize=18)
# cbar.ax.yaxis.set_offset_position('left')
# cbar.ax.yaxis.offsetText.set(size=18)
# =============================================================================

#%%
'''this cell is for the 500hr maps'''
# set path to tiff files
file_Cl_0hr = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Cl_maps.tif"
file_Te_0hr = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Te_maps.tif"

# import ToF-SIMS images
Cl0 = io.imread(file_Cl_0hr)
Te0 = io.imread(file_Te_0hr)

# construct (empty) quantified array 
res = np.zeros((56,512,512),float)

# quantify each depth slice and fill quantified array
for depth in range(Cl0.shape[0]):
    # get depth slice in each map
    Cl = Cl0[depth,:,:].astype('float32')
    Te = Te0[depth,:,:].astype('float32')
    
    # set Te zeros to nan (can't say what Cl quantities are in those pixels)
    Te[np.where(Te==0)] = np.nan
    
    # divide Cl intensity by Te intensity pixel-by-pixel
    ratio = Cl/Te
    
    # scale ratio by quantification factor
    quant = ratio*3.8097e19
    
    # fill quantified array with quantified Cl
    res[depth,:,:] = quant


# construct integration
integration = res.copy()

# convert nan back to zeroes
integration[np.isnan(integration)] = 0

# integrate along depth
section = integration[1:8,:,:].sum(axis=0)

# save reconstructed data cube
#PATH_OUT = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Cl_maps_quantified.tif"
#tifffile.imsave(PATH_OUT, integration, bigtiff=True)

# alter image to match orientation of other plots
img = np.rot90(section, k=1)   # rotate image
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