'''
simplifying mask analysis

just import the mask
extract data in boundaries and cores
save those data as csv

to find number of data points in each mask,
check length of arrays in data
'''

import numpy as np

SAMPLE = 'NBL32'
SCAN = 'scan422'
REGION = 'cores_0in_mask' #'bound_0in_1out_mask'

PATH_SYS = r'Z:\Trumann\XRF images\py_exports_interface\{S}\{s}\bound_core'.format(S=SAMPLE, s=SCAN)
PATH_MASK = r'\{R}.txt'.format(R=REGION)
PATH_IN = PATH_SYS + PATH_MASK
mask = np.loadtxt(PATH_IN)

mask = mask!=0
mask = mask.astype('int')

maps = NBL32.scan422[:,:,:-2]

data = []
for ax in maps:
    ax_masked = ax*mask
    arr = ax_masked[ax_masked!=0]
    data.append(arr)
    
data = np.array(data)
data = data.T

PATH_SYS1 = r'C:\Users\triton\Dropbox (ASU)\1_NBL3\DATA\Core Boundary csvs'
PATH_DATA = r'\{S}_{s}_{R}.csv'.format(S=SAMPLE, s=SCAN, R=REGION)
PATH_OUT = PATH_SYS1 + PATH_DATA
np.savetxt(PATH_OUT, data, delimiter=',')

plt.figure()
plt.imshow(maps[3,:,:])
plt.figure()
plt.imshow(mask)
