# -*- coding: utf-8 -*-
"""
kineticcross
Sun Feb  9 19:47:25 2020

these functions import electrical and XRF data from two types of files:
    csv file containing the lockin settings of each scan
    h5 file containing the XRF data of each scan
each sample object has data related to that sample
"""

from class_Sample import Sample
            
data_path = '/home/kineticcross/Desktop/data'
# create sample objects
NBL32 = Sample(); NBL33 = Sample(); TS58A = Sample()

# define stack and scans of each sample
NBL32.stack = {'Mo':   [10.2, 500E-7], 
                 'ZnTe': [6.34, 375E-7], 
                 'Cu':   [8.96, 2.5E-7], 
                 'CdTe': [5.85, 10.85E-4], 
                 'CdS':  [4.82, 80E-7], 
                 'SnO2': [100E-7]}
NBL32.scans =  [422,423,424,550,538,575, 419,420,421,551]

NBL33.stack = {'Mo':   [10.2, 500E-7], 
                 'ZnTe': [6.34, 375E-7], 
                 'Cu':   [8.96, 10E-7], 
                 'CdTe': [5.85, 10.85E-4], 
                 'CdS':  [4.82, 80E-7], 
                 'SnO2': [100E-7]}
NBL33.scans =  [261,262,263,472, 264,265,266, 475,491]

TS58A.stack = {'Mo':   [10.2, 500E-7], 
                 'ZnTe': [6.34, 375E-7], 
                 'Cu':   [8.96, 2.5E-7], 
                 'CdTe': [5.85, 10.85E-4], 
                 'CdS':  [4.82, 80E-7], 
                 'SnO2': [100E-7]}
TS58A.scans =  [385,386,387, 439,427,408, 382,383,384, 440]

# import h5 data for each sample
NBL32.import_scan_data(data_path)
NBL33.import_scan_data(data_path)
TS58A.import_scan_data(data_path)
# "sample.h5data" now exists: holds h5 files

# calc factor (cts-->ampere) for XBIC channel in each h5
NBL32.get_lockin(data_path+'/a_class_electrical.csv')
NBL33.get_lockin(data_path+'/a_class_electrical.csv')
TS58A.get_lockin(data_path+'/a_class_electrical.csv')
# "sample.lockin" now exists: holds scaler factors

# import maps:
# arg1: electrical scaler channel
# arg2: element maps to extract
# arg3: scaler channel to normalize elemental signal
# arg4: use 'fit' on fitted h5s, or 'roi' for unfitted h5s
elements = ['Cu', 'Cd_L', 'Te_L']
NBL32.import_maps('ds_ic', elements, 'us_ic', 'fit')
NBL33.import_maps('ds_ic', elements, 'us_ic', 'fit')
TS58A.import_maps('ds_ic', elements, 'us_ic', 'fit')
# "sample.maps" now exists: holds electrical and XRF for each scan
# each scan is accessed by index, e.g. "NBL32.maps[2]" --> scan 424
# to access a specific map of a given scan:
#   "NBL32.maps[2][0,:,:]" --> electrical map for scan 424
#   "NBL32.maps[2][1,:,:]" --> Cu map for scan 424

# apply iio correction to XRF at different beamtimes

# clean up plotting functions... and 