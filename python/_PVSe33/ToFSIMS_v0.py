# -*- coding: utf-8 -*-
"""

Trumann
Thu Mar 31 20:17:36 2022


this program opens ToF SIMS ASCIIs from Steve Harvey (NREL)

data were taken from shared Box folder; downloaded to

Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS

"""

'''this cell is for the 0hr Cl maps'''
import numpy as np
import tifffile

f = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\33.3.2_tomog_ (7) - Cl-.txt"

data = np.loadtxt(f)
indices = data[:,0:3].copy().astype('int')
values = data[:,3].copy()

res = np.zeros((49,512,512),float)

res[indices[:,2],indices[:,0],indices[:,1]] = values

res = res.astype('int')
# =============================================================================
# import matplotlib.pyplot as plt
# 
# slices = [0,10,20,30,40]
# for s in slices:
#     image = res[s,:,:]
#     plt.figure()
#     plt.imshow(image)
# =============================================================================

# save reconstructed data cube
PATH_OUT = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Cl_map.tif"
tifffile.imsave(PATH_OUT, res, bigtiff=True)

#%%
'''this cell is for the 500hr Cl maps'''
import numpy as np
import tifffile

f = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\33.4.3_tomog_ (7) - Cl-.txt"

data = np.loadtxt(f)
indices = data[:,0:3].copy().astype('int')
values = data[:,3].copy()

res = np.zeros((56,512,512),float)

res[indices[:,2],indices[:,0],indices[:,1]] = values

res = res.astype('int')
# =============================================================================
# import matplotlib.pyplot as plt
# 
# slices = [0,10,20,30,40]
# for s in slices:
#     image = res[s,:,:]
#     plt.figure()
#     plt.imshow(image)
# =============================================================================

# save reconstructed data cube
PATH_OUT = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\500hr_Cl_map.tif"
tifffile.imsave(PATH_OUT, res, bigtiff=True)

#%%
'''
this cell is for the 0hr Te maps
the raw data was placed on local directory
the tif images were placed in Dropbox

i want to see if the tiff file shows the fiducial marks as low values
instead of high values like the Cl maps

'''
import numpy as np
import tifffile

f = r"C:\Users\Trumann\Desktop\PVSe33_ToFSIMS\Te_ion_ascii\33.3.2_tomog_ (16) - ^125Te.txt"

data = np.loadtxt(f)
indices = data[:,0:3].copy().astype('int')
values = data[:,3].copy()

res = np.zeros((49,512,512),float)

res[indices[:,2],indices[:,0],indices[:,1]] = values

res = res.astype('int')
# =============================================================================
# import matplotlib.pyplot as plt
# 
# slices = [0,10,20,30,40]
# for s in slices:
#     image = res[s,:,:]
#     plt.figure()
#     plt.imshow(image)
# =============================================================================

# save reconstructed data cube
PATH_OUT = r"C:\Users\Trumann\Dropbox (ASU)\1_PVSe33 ex-situ\DATA\ToF_SIMS\0hr_Te_map.tif"
tifffile.imsave(PATH_OUT, res, bigtiff=True)