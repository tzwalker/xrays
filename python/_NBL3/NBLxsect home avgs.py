"""
this program is meant to extract the peak of the integrated
XBIC (or XRF) signals through the depth of the CdTe device
to be used on the data from M. Stuckelberger Spring, 2018 ESRF
cross-section maps of NBL3 sample set
"""
#r'C:\Users\Trumann\Desktop\NBL3_data\cross_sections_MS\csvs'
PATH = r'C:\Users\triton\Desktop\NBL3_data\cross_section_MS' 
#r'C:\Users\Trumann\xrays\python\NBL3xsect'
DEFS = r'C:\Users\triton\xrays\python\_NBL3' 

import sys
sys.path.append(DEFS)
from definitions_NBLxSect import import_xSect_csvs, get_scan_metadata
import numpy as np

def integrate_maps(imp_rot_dfs):
    integrated_arrays_of_each_channel = []
    x = imp_rot_dfs[0].columns.values
    x = x.reshape(-1,1)
    for df in imp_rot_dfs:
        y_integrate = df.sum(axis=0)        #df
        y_integrate = y_integrate.to_numpy()
        y_integrate = y_integrate.reshape(-1,1)
        integrated_arrays_of_each_channel.append(y_integrate)
    integrated_arrays_of_each_channel.insert(0, x)
    arrays = np.concatenate(integrated_arrays_of_each_channel, axis=1)
    return arrays

SAMPLE = ['NBL31','NBL31','NBL31','NBL31', 
          'NBL33','NBL33','NBL33','NBL33',
          'NBL33','NBL33','NBL33','NBL33',
          'TS58A','TS58A','TS58A','TS58A']
SCAN = [1,6,7,8, 
        1,2,12,13,
        14,15,17,20, 
        2,3,4,5]
ROTATION = [0,0,0,0,
            15,15,15,15,
            15,15,15,15,
            0,0,0,0]

CHANNELS = ['XBIC_lockin', 'Cu_K', 'Cd_L3']

profiles = []; maxes = [] ; avgs = []
for sample,scan,rot in zip(SAMPLE,SCAN,ROTATION):
    META_DATA = get_scan_metadata(PATH, sample, scan)
    MAPS = import_xSect_csvs(PATH, sample, scan, CHANNELS, META_DATA, rot)
    ARRAYS = integrate_maps(MAPS)
    profiles.append(ARRAYS)
    XBIC_MAX = np.max(ARRAYS[:,1])
    maxes.append(XBIC_MAX)
    XBIC_AVG = np.mean(ARRAYS[:,1])
    avgs.append(XBIC_AVG)
maxes_arr = np.array(maxes)
avgs_arr = np.array(avgs)


