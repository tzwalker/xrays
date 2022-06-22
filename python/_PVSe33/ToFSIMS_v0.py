# -*- coding: utf-8 -*-
"""

Trumann
Thu Mar 31 20:17:36 2022


this program processes ToF SIMS ASCIIs from Steve Harvey (NREL)
into TIF images
    data size reduction from 300MB to 50MB

data were downloaded from shared Box folder t0
Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS

"""

'''this cell is for the 0hr CHLORINE maps'''
import numpy as np
import tifffile

f = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\33.3.2_tomog_ (7) - Cl-.txt"

data = np.loadtxt(f)
indices = data[:,0:3].copy().astype('int')
values = data[:,3].copy()

res = np.zeros((49,512,512),float)

res[indices[:,2],indices[:,0],indices[:,1]] = values

res = res.astype('int')

# save reconstructed data cube
PATH_OUT = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Cl_map.tif"
tifffile.imsave(PATH_OUT, res, bigtiff=True)

###############################################################################
'''this cell is for the 500hr CHLORINE maps''' 
import numpy as np
import tifffile

f = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\33.4.3_tomog_ (7) - Cl-.txt"

data = np.loadtxt(f)
indices = data[:,0:3].copy().astype('int')
values = data[:,3].copy()

res = np.zeros((56,512,512),float)

res[indices[:,2],indices[:,0],indices[:,1]] = values

res = res.astype('int')

# save reconstructed data cube
PATH_OUT = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Cl_map.tif"
tifffile.imsave(PATH_OUT, res, bigtiff=True)

#%%
'''
this cell is for the Te maps
these are needed for Cl quantification

also, wantde see if fiducial marks are low Te intensity

the raw data was placed on local directory
the tif images were placed in Dropbox
'''

'''this cell is for the 0hr TELLURIUM maps'''
import numpy as np
import tifffile

f = r"C:\Users\Trumann\Desktop\PVSe33_ToFSIMS\Te_ion_ascii\33.3.2_tomog_ (16) - ^125Te.txt"

data = np.loadtxt(f)
indices = data[:,0:3].copy().astype('int')
values = data[:,3].copy()

res = np.zeros((49,512,512),float)

res[indices[:,2],indices[:,0],indices[:,1]] = values

res = res.astype('int')

# save reconstructed data cube
PATH_OUT = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Te_maps.tif"
tifffile.imsave(PATH_OUT, res, bigtiff=True)

###############################################################################
'''this cell is for the 500hr TELLURIUM maps''' 
import numpy as np
import tifffile

f = r"C:\Users\Trumann\Desktop\PVSe33_ToFSIMS\Te_ion_ascii\33.4.3_tomog_ (16) - ^125Te.txt"

data = np.loadtxt(f)
indices = data[:,0:3].copy().astype('int')
values = data[:,3].copy()

res = np.zeros((56,512,512),float)

res[indices[:,2],indices[:,0],indices[:,1]] = values

res = res.astype('int')

# save reconstructed data cube
PATH_OUT = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Te_maps.tif"
tifffile.imsave(PATH_OUT, res, bigtiff=True)

#%%
'''
this cell is for the Se maps

want to corroborate cross-section Se XRF and dynamic Se SIMS
    there could be a Se redistribution

'''
import numpy as np
import tifffile

'''this cell is for the 0hr SELENIUM maps''' 
f = r"C:\Users\Trumann\Desktop\PVSe33_ToFSIMS\Se_ion_ascii\33.3.2_tomog_ (14) - Se-.txt"

data = np.loadtxt(f)
indices = data[:,0:3].copy().astype('int')
values = data[:,3].copy()

res = np.zeros((49,512,512),float)

res[indices[:,2],indices[:,0],indices[:,1]] = values

res = res.astype('int')

# save reconstructed data cube
PATH_OUT = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Se_maps.tif"
tifffile.imsave(PATH_OUT, res, bigtiff=True)

###############################################################################
'''this cell is for the 500hr SELENIUM maps''' 

f = r"C:\Users\Trumann\Desktop\PVSe33_ToFSIMS\Se_ion_ascii\33.4.3_tomog_ (14) - Se-.txt"

data = np.loadtxt(f)
indices = data[:,0:3].copy().astype('int')
values = data[:,3].copy()

res = np.zeros((56,512,512),float)

res[indices[:,2],indices[:,0],indices[:,1]] = values

res = res.astype('int')

# save reconstructed data cube
PATH_OUT = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Se_maps.tif"
tifffile.imsave(PATH_OUT, res, bigtiff=True)