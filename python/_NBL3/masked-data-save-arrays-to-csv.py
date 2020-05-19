'''
saving data from then hand drawn masks

just import the mask
extract data in boundaries and cores
save those data as csv

check length of arrays in 'data'
check mask against plot of Te channel
'''

import numpy as np
import matplotlib.pyplot as plt


SAMPLES = [NBL31, NBL32,NBL33,TS58A]
SAMPLE_NAMES = ['NBL31', 'NBL32','NBL33','TS58A']
SCAN = ['scan341','scan422','scan264','scan386']
REGION = ['cores_0in_mask', 'bound_0in_1out_mask']

for samp_obj, samp_name, scan in zip(SAMPLES, SAMPLE_NAMES, SCAN):
    maps = getattr(samp_obj,scan)[:,:,:-2]
    
    for reg in REGION:
        PATH_SYS = r'Z:\Trumann\XRF images\py_exports_interface\{S}\{s}\bound_core'.format(S=samp_name, s=scan)
        PATH_MASK = r'\{R}.txt'.format(R=reg)
        PATH_IN = PATH_SYS + PATH_MASK

        mask = np.loadtxt(PATH_IN)
        mask = mask!=0
        mask = mask.astype('int')

        data = []
        for ax,radius in zip(maps,RADII):
            ax_masked = ax[np.where(mask>0)]
            data.append(ax_masked)
            #print(np.size(ax_masked))
        data = np.array(data)
        data = data.T
        
        PATH_SYS1 = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\DATA\Core Boundary csvs'
        PATH_DATA = r'\{S}_{s}_{R}.csv'.format(S=samp_name, s=scan, R=reg)
        PATH_OUT = PATH_SYS1 + PATH_DATA
        np.savetxt(PATH_OUT, data, delimiter=',')
    plt.figure()
    plt.imshow(maps[3,:,:])
    plt.figure()
    plt.imshow(mask)

#%%

'''
see if the masked data will have more significant difference
in Cu concentration between cores and boundaries
if it is background subtracted

since background subtraction of small XBIV and XBIC values
requires standardization, these arrays will be saved in arbitrary units
'''
from background_subtraction import background_subtraction
from standardize_map import standardize_map

RADII = [20,15,30,30,15]

for samp_obj, samp_name, scan in zip(SAMPLES, SAMPLE_NAMES, SCAN):
    maps = getattr(samp_obj,scan)[:,:,:-2]
    
    for reg in REGION:
        PATH_SYS = r'Z:\Trumann\XRF images\py_exports_interface\{S}\{s}\bound_core'.format(S=samp_name, s=scan)
        PATH_MASK = r'\{R}.txt'.format(R=reg)
        PATH_IN = PATH_SYS + PATH_MASK

        mask = np.loadtxt(PATH_IN)
        mask = mask!=0
        mask = mask.astype('int')

        data = []
        for ax,radius in zip(maps,RADII):
            ax1 = standardize_map(ax)               # new line
            ax1 = background_subtraction(ax1,radius) # new line
            ax_masked = ax1[np.where(mask>0)]       # new line
            data.append(ax_masked)
            print(np.size(ax_masked))
        data = np.array(data)
        data = data.T
        
        PATH_SYS1 = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\DATA\Core Boundary csvs'
        PATH_DATA = r'\bksub_{S}_{s}_{R}.csv'.format(S=samp_name, s=scan, R=reg)
        PATH_OUT = PATH_SYS1 + PATH_DATA
        np.savetxt(PATH_OUT, data, delimiter=',')